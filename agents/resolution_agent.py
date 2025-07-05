import pandas as pd
from fuzzywuzzy import fuzz
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import streamlit as st

class ResolutionAgent:
    def __init__(self, faq_df):
        self.faq_df = faq_df
        self.llm = ChatOpenAI(openai_api_key=st.secrets["openai"]["api_key"], temperature=0.2)
        self.role = "Query Resolution Agent"
        self.goal = "Find the best FAQ match or provide AI-based answers."
        self.backstory = (
            "Tools: Fuzzy matching on FAQs + LLM fallback.\n"
            "Guardrails: Only use LLM if FAQ match score is below 80.\n"
            "Memory: Remembers previous FAQ searches during the session."
        )

    def query_faq_and_llm(self, query: str) -> str:
        """FAQ search + LLM fallback."""
        best_score, best_answer = 0, None
        for _, row in self.faq_df.iterrows():
            score = fuzz.partial_ratio(query.lower(), row["Question"].lower())
            if score > best_score:
                best_score = score
                best_answer = row["Answer"]

        faq_response = best_answer if best_score >= 80 else None

        template = PromptTemplate.from_template(
            "You are a helpful customer support assistant. Answer clearly:\n\n{question}"
        )
        llm_response = self.llm.invoke(template.format(question=query)).content

        if faq_response:
            return f"✅ FAQ Answer: {faq_response}\n\n🤖 AI Insight: {llm_response}"
        else:
            return llm_response
