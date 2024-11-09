import fitz  # PyMuPDF

# Replace with the path to your PDF file
pdf_path = "/Users/thanikella_nikhil/Projects-Courses/NS/data/NS_Merged_compressed.pdf"
text_output_path = "/Users/thanikella_nikhil/Projects-Courses/NS/data/out.txt"

# Open the PDF file
with fitz.open(pdf_path) as pdf:
    # Prepare to store all text from all pages
    all_text = ""
    
    # Iterate over each page
    for page_num in range(pdf.page_count):
        page = pdf[page_num]
        
        # Extract text from the page
        text = page.get_text()
        
        # Append page text to the main text content
        all_text += f"Page {page_num + 1}:\n{text}\n\n"
    
    # Write the extracted text to a text file
    with open(text_output_path, "w", encoding="utf-8") as f:
        f.write(all_text)

print("PDF text extraction complete. Saved to:", text_output_path)
