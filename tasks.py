from crewai import Task
from textwrap import dedent
from agents import linkedin_scraper_agent, web_researcher_agent, doppelganger_agent


scrape_linkedin_task = Task(
    description=dedent(
        "Scrape a LinkedIn profile to get some relevant posts"),
    expected_output=dedent("A list of LinkedIn posts obtained from a LinkedIn profile"),
    agent=linkedin_scraper_agent,
)

web_research_task = Task(
    description=dedent(
        "Get valuable and high quality web information about some current event or topic that is relevant to DevOps, Cloud, AI, or Software Engineering"),
    expected_output=dedent("Your task is to gather high quality information about some current event or topic that is relevant to DevOps, Cloud, AI, or Software Engineering"),
    agent=web_researcher_agent,
)

create_linkedin_post_task = Task(
    description=dedent(
        "Create a concise LinkedIn post about some current event or topic that is relevant to DevOps, Cloud, AI, or Software Engineering. "
        "Use short sentences and simple vocabulary. Avoid emojis, hype, and exclamation marks. "
        "Start with a strong hook, provide clear practical insight, and keep the post under 120 words. "
        "Follow the writing-style expressed in the scraped LinkedIn posts."
    ),
    expected_output=dedent(
        "A high-quality LinkedIn post under 120 words that grabs attention in the first line, provides practical value, "
        "and mirrors the tone of the scraped posts without using emojis, hype, complex wording, or clichés."
    ),
    agent=doppelganger_agent,
)

create_linkedin_post_task.context = [scrape_linkedin_task, web_research_task]
