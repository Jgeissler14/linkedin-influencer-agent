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
        "Create a LinkedIn post about some current event or topic that is relevant to DevOps, Cloud, AI, or Software Engineering following the writing-style "
        "expressed in the scraped LinkedIn posts."
    ),
    expected_output=dedent("A high-quality and engaging LinkedIn post about some current event or topic that is relevant to DevOps, Cloud, AI, or Software Engineering."
                           " The LinkedIn post must follow"
                           " the same writing-style as the one expressed in the scraped LinkedIn posts"),
    agent=doppelganger_agent,
)

create_linkedin_post_task.context = [scrape_linkedin_task, web_research_task]
