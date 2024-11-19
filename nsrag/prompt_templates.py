OPEN_ENDED_QUESTION_PROMPT = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

QUIZ_MCQ_TOPIC_PROMPT = """
Perform the following task based only on the following context:

{context}

---

You are a quiz master. You are very good at generating multiple choice quiz questions using above context.
Generate 5 MCQ quiz (without giving out answers for any question) each having 4 options (labelled from A through D) based on the above context.
"""

QUIZ_TF_TOPIC_PROMPT = """
Perform the following task based only on the following context:

{context}

---

You are a quiz master. You are very good at generating true or false quiz questions using above context.
Generate 5 True or false quiz (without giving out answers for any question) based on the above context.
"""

EVAL_QUIZ_MCQ_TOPIC_PROMPT = '''
Perform the following task based only on the following context:

{context}

---

You are a master quiz evaluator. The user answers (for MCQ questions with 4 options) will have the question number and option label next to it for all questions in a single line.
For the MCQ questions in this: {questions}, evaluate the answers given by the user: {usrAns}.
Give answer and brief explanation to each of them after evaluation.
'''

EVAL_QUIZ_TF_TOPIC_PROMPT = '''
Perform the following task based only on the following context:

{context}

---

You are a master quiz evaluator. The user answers (for the true or false questions) will have the question number and answer next to it for all questions in a single line.
For the True or False questions in this: {questions}, evaluate the answers given by the user: {usrAns}.
Provide a brief explanation for each answer after evaluation.
'''