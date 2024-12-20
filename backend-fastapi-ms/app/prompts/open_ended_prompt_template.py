OPEN_ENDED_SYS_INSTR = '''You are an expert assistant designed to provide accurate answers to user questions based strictly on the provided context. Always output the answer in JSON format.'''
OPEN_ENDED_QUESTION_PROMPT = """
Answer the following question using only the given context.

Context:
{context}

---

Question:
{question}
"""
