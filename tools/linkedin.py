import os
import time

from crewai.tools import tool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from urllib.parse import quote_plus
from tools.utils import get_linkedin_posts, get_linkedin_posts_with_urls


class LinkedinToolException(Exception):
    def __init__(self):
        super().__init__("You need to set the LINKEDIN_EMAIL and LINKEDIN_PASSWORD env variables")


def scrape_linkedin_posts_fn(profile_name: str) -> list[str]:
    """Scrape the latest posts from a LinkedIn profile.

    Args:
        profile_name: The LinkedIn handle of the profile to scrape.

    Returns:
        A list of post contents.
    """
    linkedin_username = os.environ.get("LINKEDIN_EMAIL")
    linkedin_password = os.environ.get("LINKEDIN_PASSWORD")

    if not (linkedin_username and linkedin_password):
        raise LinkedinToolException()

    browser = webdriver.Chrome()
    browser.get("https://www.linkedin.com/login")

    username_input = browser.find_element("id", "username")
    password_input = browser.find_element("id", "password")
    username_input.send_keys(linkedin_username)
    password_input.send_keys(linkedin_password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(20)

    browser.get(f"https://www.linkedin.com/in/{profile_name}/recent-activity/all/")

    for _ in range(2):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    posts = get_linkedin_posts(browser.page_source)
    browser.quit()

    # We'll just return 2 of the latest posts, since it should be enough for the LLM to get the overall style
    return posts[:2]


def scrape_linkedin_posts_with_urls_fn(profile_name: str) -> list[dict]:
    """Scrape posts and their URLs from a LinkedIn profile."""
    linkedin_username = os.environ.get("LINKEDIN_EMAIL")
    linkedin_password = os.environ.get("LINKEDIN_PASSWORD")

    if not (linkedin_username and linkedin_password):
        raise LinkedinToolException()

    browser = webdriver.Chrome()
    browser.get("https://www.linkedin.com/login")

    username_input = browser.find_element("id", "username")
    password_input = browser.find_element("id", "password")
    username_input.send_keys(linkedin_username)
    password_input.send_keys(linkedin_password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(20)

    browser.get(f"https://www.linkedin.com/in/{profile_name}/recent-activity/all/")

    for _ in range(2):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    posts = get_linkedin_posts_with_urls(browser.page_source)
    browser.quit()

    return posts[:2]


def search_linkedin_posts_with_urls_fn(query: str, max_posts: int = 5) -> list[dict]:
    """Search LinkedIn for posts matching the query and return them with URLs."""
    linkedin_username = os.environ.get("LINKEDIN_EMAIL")
    linkedin_password = os.environ.get("LINKEDIN_PASSWORD")

    if not (linkedin_username and linkedin_password):
        raise LinkedinToolException()

    browser = webdriver.Chrome()
    browser.get("https://www.linkedin.com/login")

    username_input = browser.find_element("id", "username")
    password_input = browser.find_element("id", "password")
    username_input.send_keys(linkedin_username)
    password_input.send_keys(linkedin_password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(20)

    encoded_query = quote_plus(query)
    search_url = f"https://www.linkedin.com/search/results/content/?keywords={encoded_query}"
    browser.get(search_url)

    for _ in range(2):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    posts = get_linkedin_posts_with_urls(browser.page_source)
    browser.quit()

    return posts[:max_posts]


@tool("ScrapeInfluencerPosts")
def scrape_influencer_posts_tool() -> list[str]:
    """Scrape posts from the influencer profile defined in ``INFLUENCER_PROFILE_NAME``."""
    profile = os.environ.get("INFLUENCER_PROFILE_NAME")
    return scrape_linkedin_posts_fn(profile)


@tool("ScrapeTargetPosts")
def scrape_target_posts_tool() -> list[str]:
    """Scrape posts from the target profile defined in ``TARGET_PROFILE_NAME``."""
    profile = os.environ.get("TARGET_PROFILE_NAME")
    return scrape_linkedin_posts_fn(profile)
