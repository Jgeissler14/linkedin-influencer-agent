import os
from textwrap import dedent

from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI

from tools import (
    scrape_linkedin_posts_tool,
    scrape_linkedin_group_posts_tool,
)

load_dotenv()


openai_llm = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model="gpt-3.5-turbo-0125")
mistral_llm = ChatMistralAI(api_key=os.environ.get("MISTRAL_API_KEY"), model="mistral-large-latest")

scrape_website_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()

linkedin_scraper_agent = Agent(
    role="LinkedIn Post Scraper",
    goal="Your goal is to scrape a LinkedIn profile to get a list of posts from the given profile",
    tools=[scrape_linkedin_posts_tool],
    backstory=dedent(
        """
        You are an experienced programmer who excels at web scraping. 
        """
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm
)

web_researcher_agent = Agent(
    role="Web Researcher",
    goal="Your goal is to search for relevant content about some current event or topic that is relevant to DevOps, Cloud, AI, or Software Engineering",
    tools=[scrape_website_tool, search_tool],
    backstory=dedent(
        """
        You are proficient at searching for specific topics in the web, selecting those that provide
        more value and information.
        """
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm
)

doppelganger_agent = Agent(
    role="LinkedIn Post Creator",
    goal="You will craft short LinkedIn posts about current DevOps, Cloud, AI, or Software Engineering topics. "
         "Mirror the tone of the scraped influencer posts while keeping language simple and direct. "
         "Avoid emojis, hype, or exclamation marks, and keep the total length under 120 words.",
         
    backstory=dedent(
        """
        You are an expert in replicating an influencer's voice while presenting content in a concise, actionable format.
        Your posts start with a compelling hook and deliver value in plain language.
        Avoid corporate jargon and clichés. Aim for a professional, straightforward tone.
        """
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm
)


group_scraper_agent = Agent(
    role="LinkedIn Group Scraper",
    goal="Scrape the latest posts from the LinkedIn groups provided",
    tools=[scrape_linkedin_group_posts_tool],
    backstory=dedent(
        """
        You are skilled at navigating LinkedIn groups and collecting recent posts
        for analysis.
        """
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
)

group_reply_agent = Agent(
    role="LinkedIn Group Reply Creator",
    goal="Write concise replies to posts in LinkedIn groups.",
    tools=[],
    backstory=dedent(
        """
        You craft short professional replies that encourage discussion while
        keeping a friendly tone.
        """
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
)
