from crewai import Crew
from dotenv import load_dotenv

from agents import (
    influencer_scraper_agent,
    target_scraper_agent,
    web_researcher_agent,
    doppelganger_agent,
    lead_research_agent,
    outreach_agent,
)
from tasks import (
    scrape_influencer_posts_task,
    scrape_target_post_task,
    research_article_task,
    reframe_post_task,
    search_prospects_task,
    compose_outreach_task,
)

load_dotenv()


crew = Crew(
    agents=[
        influencer_scraper_agent,
        target_scraper_agent,
        web_researcher_agent,
        doppelganger_agent,
        lead_research_agent,
        outreach_agent,
    ],
    tasks=[
        scrape_influencer_posts_task,
        scrape_target_post_task,
        research_article_task,
        reframe_post_task,
        search_prospects_task,
        compose_outreach_task,
    ]
)

result = crew.kickoff()


print("Here is the result: ")
print(result)
