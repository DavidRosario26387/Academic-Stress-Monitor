import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class Chain:
    llm = None  # class-level placeholder

    def __init__(self):
        if Chain.llm is None:
            Chain.llm = ChatGroq(
                temperature=0,
                groq_api_key=os.getenv("GROQ_API_KEY"),
                model_name="openai/gpt-oss-120b")
        self.llm = Chain.llm

    def infer(self, user_message, category, rag_data):

        STRESS_REASONS = ["Academic pressure", "Financial problems", "Relationship conflicts", "Health issues", "Lack of sleep",
                  "Time management", "Social pressure", "Traumatic events"]

        prompt_message = PromptTemplate.from_template("""
        You are a friendly psychological advisor helping students cope with stress.
        Answer **directly**, without asking questions, using the provided RAG data if it is useful.

        The user just said: "{user_message}"
        Their stress level is: "{stress_category}" (low / medium / high).

        Write a **friendly, crisp, message** for the user, you can use the following RAG data if it is useful:
        {rag_data}

        Select **strictly one reason** from this list that best explains the stress:
        {reasons}

        Respond strictly in **JSON format** with exactly two keys: "message" and "reason".
        Do not include any preamble, explanation, or extra text.

        Example:
        {{
            "message": "Your drafted advice here",
            "reason": "The selected reason"
        }}
        """
        )

        chain_message = prompt_message | self.llm
        try:
            res = chain_message.invoke({"user_message": str(user_message), "stress_category": str(category),"rag_data":str(rag_data),"reasons":str(STRESS_REASONS)})
            return res.content.strip()
        except Exception as e:
            print(f"LLM invocation error: {e}")
            return "Sorry, I couldn't generate a response at the moment."