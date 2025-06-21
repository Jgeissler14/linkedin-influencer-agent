from crewai import Task
from textwrap import dedent
from agents import influencer_scraper_agent, target_scraper_agent, doppelganger_agent

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

reframe_post_task = Task(
    description=dedent(
        "Check whether the latest post is personal or educational and rewrite it in the influencer's style. "
        "If personal, remove the personal references so it reads as an educational insight."),
    expected_output=dedent(
        "A reframed LinkedIn post in the influencer's style with no personal references."),
    agent=doppelganger_agent,
)

reframe_post_task.context = [scrape_influencer_posts_task, scrape_target_post_task]
