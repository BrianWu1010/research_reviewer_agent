import os
from dotenv import load_dotenv
from openai import OpenAI
import ast
from itertools import combinations

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def QueryToKeywords(user_query):
    prompt = f"""
You are a research planning agent.

Your job is to break down the following research question into 3–6 search keywords.

Respond in a Python list of strings. Be concise and focused.

Query:
\"\"\"{user_query}\"\"\"
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    output = response.choices[0].message.content
    return ast.literal_eval(output)


def SearchKeywords(keywords,user_query):
    """
    Use ChatGPT to form keywords for paper searching in retriever agent.
    """

    prompt = f"""
You are a helpful AI research assistant.

You will be given a list of technical keyword groups. 
Your task is to rewrite them into clear, cobination of keywords connected by "AND" that could be used to retrieve academic papers, 
Make sure the combination of keywords capture the idea of the question: {user_query}.

Input (a list of phrases):
{keywords}

Respond with a Python list of 3 search phrases.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    output = response.choices[0].message.content
    return ast.literal_eval(output)

def FormNewSearchKeyWords(keywords,user_query):
    refined = SearchKeywords(keywords,user_query)
    return refined

def run_planner(user_query):
    keywords = QueryToKeywords(user_query)
    search_phrases = FormNewSearchKeyWords(keywords,user_query)
    return search_phrases