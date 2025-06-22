import os
from textwrap import dedent

from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI

from tools import scrape_influencer_posts_tool, scrape_target_posts_tool

load_dotenv()


openai_llm = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model="gpt-3.5-turbo-0125")
mistral_llm = ChatMistralAI(api_key=os.environ.get("MISTRAL_API_KEY"), model="mistral-large-latest")

scrape_website_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()

influencer_scraper_agent = Agent(
    role="Influencer Post Scraper",
    goal="Scrape posts from the influencer profile to understand the writing style",
    tools=[scrape_influencer_posts_tool],
    backstory=dedent(
        """
        You are an experienced programmer who excels at web scraping.
        """
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm
)

target_scraper_agent = Agent(
    role="Target Post Scraper",
    goal="Scrape the latest posts from the target profile",
    tools=[scrape_target_posts_tool],
    backstory=dedent(
        """
        You efficiently gather the most recent LinkedIn posts from a profile.
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
         "Avoid emojis, hype, or exclamation marks, and keep the total length under 120 words. "
         "Remove personal references and rewrite them as neutral educational points. "
         "Conclude with a brief reference to the researched article.",
         
    backstory=dedent(
        """
        You are an expert in replicating an influencer's voice while presenting content in a concise, actionable format.
        Your posts start with a compelling hook and deliver value in plain language.
        Avoid corporate jargon and clichés. Aim for a professional, straightforward tone.
        Strip out personal anecdotes or references so the final post reads as universally useful advice.
        """
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm
)


lead_research_agent = Agent(
    role="Lead Researcher",
    goal="Identify potential clients on LinkedIn and compile a short list of prospects",
    tools=[search_tool, scrape_website_tool],
    backstory=dedent(
        """
        You excel at finding LinkedIn profiles and company pages related to Terraform, DevOps,
        or cloud infrastructure services. Summarize the top results succinctly so they can be
        contacted later.
        """
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
)


outreach_agent = Agent(
    role="Outreach Writer",
    goal="Craft concise LinkedIn outreach messages referencing a helpful article",
    tools=[],
    backstory=dedent(
        """
        You write short, professional outreach messages offering Terraform development services.
        Each message should mention how the referenced article is relevant and invite the prospect
        to discuss their infrastructure goals. Keep the tone friendly and under 80 words.
        """
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
)
