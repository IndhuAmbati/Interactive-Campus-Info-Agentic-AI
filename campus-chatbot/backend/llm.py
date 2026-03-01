import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.0"))

prompt_template = """
You are a helpful campus information assistant for a university. Use the provided context to answer the user's question concisely.

Context:
{context}

Question: {question}

Instructions:
- Answer in 2-4 sentences
- Be friendly and helpful
- If the answer isn't in the context, say you don't have that information
- Cite relevant context if appropriate

Answer:
"""

PROCEDURE_PROMPT = """
You are a campus procedure guide. Explain the step-by-step process for:
{query}

Available procedures:
{procedures}

Provide clear, numbered steps and mention required documents.
"""

EVENT_PROMPT = """
You are an event coordinator assistant. Provide information about:
{query}

Upcoming events:
{events}

Include dates, times, venues, and registration details if available.
"""

CONTACT_PROMPT = """
You are a campus directory assistant. Find contact information for:
{query}

Available contacts:
{contacts}

Provide name, designation, email, phone, and office location.
"""


def answer_procedure(query, procedures):
    # Specialized procedure answering
    pass


prompt = PromptTemplate.from_template(prompt_template)


def answer_from_context(context: str, question: str) -> str:
    """Return a Groq-generated answer when GROQ_API_KEY is set, otherwise a safe fallback."""
    if not GROQ_API_KEY:
        if not context.strip():
            return "I'm sorry, I don't have any information about that yet. Please contact the admin to add more campus information."
        return f"I found this information, but I'm in demo mode (no API key). Here's what I know:\n\n{context[:500]}..."

    try:
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=GROQ_MODEL,
            temperature=GROQ_TEMPERATURE,
        )
        chain = prompt | llm | StrOutputParser()
        resp = chain.invoke({"context": context, "question": question})
        return resp.strip()
    except Exception as e:
        print(f"Groq error: {e}")
        return f"I encountered an error processing your request. Using context instead:\n\n{context[:500]}..."
