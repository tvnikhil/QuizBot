OPEN_ENDED_SYS_INSTR = '''You are very good at answering user questions based on the provided context and you only output the answer in json'''

OPEN_ENDED_QUESTION_PROMPT = """
Answer the question based only on the following context:

{context}

---

Answer the following question based on the above context: {question}"""