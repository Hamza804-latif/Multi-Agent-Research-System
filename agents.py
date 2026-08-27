from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url 
from dotenv import load_dotenv

load_dotenv()

#model setup 
llm = ChatGroq(    
    model="qwen/qwen3.6-27b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    reasoning_effort="none"
    # other params...
    )


#1st agent 
def build_search_agent():
    return create_agent(
        model = llm,
        tools= [web_search],
        system_prompt="""
        You are a web research agent.

        Use the web_search tool to find relevant and reliable sources.

        IMPORTANT:
        Preserve every URL returned by the web_search tool.
        Do not omit or summarize away the URLs.

        Return each result in this format:

        Title: ...
        URL: ...
        Snippet: ...
        """
    )

#2nd agent 

def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url],
        system_prompt="""
        You are a research reading agent.

        Your job is to read a URL provided in the search results.

        IMPORTANT:
        - Identify the most relevant URL from the provided search results.
        - You MUST call the scrape_url tool with the selected URL.
        - Do not simply describe the URL or say that you need a URL.
        - After scraping, analyze and return the useful information extracted from the page.
        """
    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()
