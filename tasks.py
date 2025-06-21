from crewai import Task
from textwrap import dedent
from agents import (
    influencer_scraper_agent,
    target_scraper_agent,
    web_researcher_agent,
    doppelganger_agent,
)

scrape_influencer_posts_task = Task(
    description=dedent(
        "Scrape the influencer's LinkedIn profile to get writing style examples."),
    expected_output=dedent("A list of posts from the influencer profile"),
    agent=influencer_scraper_agent,
)

scrape_target_post_task = Task(
    description=dedent(
        "Scrape the target LinkedIn profile to obtain its latest post."),
    expected_output=dedent("The latest post from the target profile"),
    agent=target_scraper_agent,
)

research_article_task = Task(
    description=dedent(
        "Search the web for an article that complements the topic of the target's latest post."),
    expected_output=dedent("A URL or citation of a relevant article"),
    agent=web_researcher_agent,
)

research_article_task.context = [scrape_target_post_task]

reframe_post_task = Task(
    description=dedent(
        "Check whether the latest post is personal or educational and rewrite it in the influencer's style. "
        "If personal, remove the personal references so it reads as an educational insight. "
        "Finish by pointing readers to the researched article for further reading."),
    expected_output=dedent(
        "A reframed LinkedIn post in the influencer's style that cites the article and contains no personal references."),
    agent=doppelganger_agent,
)

reframe_post_task.context = [scrape_influencer_posts_task, scrape_target_post_task, research_article_task]
