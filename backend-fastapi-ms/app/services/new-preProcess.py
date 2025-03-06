import os
import time
from pdf2image import convert_from_path
from google import genai
from google.genai import types
from pydantic import BaseModel
import PIL.Image
from secretKeys import *

class Res(BaseModel):
    mdText: str

# Paths
data_path = "/Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/backend-fastapi-ms/data/data1"
final_img_path = "/Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/backend-fastapi-ms/data/data1img"
final_md_path = "/Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/backend-fastapi-ms/data/data1md"

# List of API keys to rotate through
current_api_key_index = 0

def get_client():
    """Returns a genai Client using the current API key."""
    global current_api_key_index
    return genai.Client(api_key=api_keys[current_api_key_index])

def rotate_api_key():
    """Rotates to the next API key."""
    global current_api_key_index
    current_api_key_index = (current_api_key_index + 1) % len(api_keys)
    print(f"Rotated API key. Now using key index: {current_api_key_index}")

def convert_pdf_to_images(pdf_path, output_dir, prefix):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    images = convert_from_path(pdf_path)
    
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f"{prefix}_page_{i+1}.jpg")
        image.save(image_path, "JPEG")

def convert_all_pdfs_to_images():
    for filename in os.listdir(data_path):
        if filename.lower().endswith(".pdf"):
            pdf_file = os.path.join(data_path, filename)
            pdf_name, _ = os.path.splitext(filename)
            convert_pdf_to_images(pdf_file, final_img_path, pdf_name)
            print(f"{filename} done")

generate_content_config = types.GenerateContentConfig(
    temperature=0.3,
    max_output_tokens=8192,
    response_mime_type="application/json",
    response_schema=Res,
)

prompt = """
You are an expert at extracting and converting content from page images into clean, human-readable Markdown. Your tasks are as follows:

1. **Text Extraction:**  
   - Extract all visible text and tables from the provided page image.
   - Preserve the layout and formatting (such as columns) to reflect how a human reader would interpret the content.
   - Ignore non-essential elements like footnotes, page numbers, headers, or footers.

2. **Image Summarization:**  
   - For any embedded images or diagrams within the page (for example, an encryption diagram featuring Alice and Bob), provide a concise summary that explains the key elements and purpose of the image.
   - The summary should capture the essential meaning without reproducing the image itself.

3. **Output Formatting:**
   - Everything should be in markdown only. Your whole response should be clean, correct markdown.
   - Return all the extracted content as Markdown.
   - Ensure the output is clean, without unnecessary whitespace, extraneous formatting, or symbols.
   - Do not include any additional explanations beyond the content conversion.

Now, analyze the provided page image, extract its content following these guidelines, and output the result in Markdown format.
"""

def convert_all_images_to_md(img_dir, md_dir, base_sleep=2):
    for filename in os.listdir(img_dir):
        if filename.lower().endswith(".jpg"):
            output_md_path = os.path.join(md_dir, f"{os.path.splitext(filename)[0]}.md")
            # Skip processing if the Markdown file already exists
            if os.path.exists(output_md_path):
                print(f"Skipping {filename} as it has already been processed.")
                continue

            image_path = os.path.join(img_dir, filename)
            print(f"Processing: {filename}")
            image = PIL.Image.open(image_path)
            success = False
            attempts = 0
            # Keep retrying until success
            while not success:
                try:
                    client = get_client()
                    response = client.models.generate_content(
                        # gemini-2.0-pro-exp-02-05
                        model="gemini-2.0-pro-exp-02-05",
                        contents=[prompt, image],
                        config=generate_content_config,
                    )
                    with open(output_md_path, "w") as file:
                        # Remove any extraneous symbols (e.g., tildes)
                        md_text = response.parsed.mdText.replace("~", "")
                        file.write(md_text)
                    print(f"Markdown saved to: {output_md_path}")
                    success = True
                except Exception as e:
                    attempts += 1
                    error_message = str(e)
                    print(f"Error processing {filename} on attempt {attempts}: {error_message}")
                    # If a 429 error is detected (rate limit exceeded)
                    if "429" in error_message:
                        print("Received 429 error - Rate limit exceeded.")
                        # If we've rotated through all API keys, sleep for 70 seconds
                        if attempts % len(api_keys) == 0:
                            print("All API keys have been exhausted due to rate limits. Sleeping for 70 seconds before retrying...")
                            time.sleep(70)
                        else:
                            rotate_api_key()
                            sleep_time = base_sleep * attempts  # Exponential backoff
                            # print(f"Sleeping for {sleep_time} seconds before retrying with next API key...")
                            # time.sleep(sleep_time)
                    else:
                        # For other errors, rotate the API key and use exponential backoff
                        rotate_api_key()
                        time.sleep(5)
                        # sleep_time = base_sleep * attempts
                        # print(f"Sleeping for {sleep_time} seconds before retrying...")
                        # time.sleep(sleep_time)

# Uncomment if you want to convert PDFs to images first
# convert_all_pdfs_to_images()

convert_all_images_to_md(final_img_path, final_md_path)
