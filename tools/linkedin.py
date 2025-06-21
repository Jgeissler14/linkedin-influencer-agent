import os
import time

from crewai.tools import tool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from tools.utils import get_linkedin_posts


class LinkedinToolException(Exception):
    def __init__(self):
        super().__init__("You need to set the LINKEDIN_EMAIL and LINKEDIN_PASSWORD env variables")


def scrape_linkedin_posts_fn() -> str:
    """
    A tool that can be used to scrape LinkedIn posts
    """
    linkedin_username = os.environ.get("LINKEDIN_EMAIL")
    linkedin_password = os.environ.get("LINKEDIN_PASSWORD")
    linkedin_profile_name = os.environ.get("LINKEDIN_PROFILE_NAME")

    if not (linkedin_username and linkedin_password):
        raise LinkedinToolException()

    browser = webdriver.Chrome()
    browser.get("https://www.linkedin.com/login")

    username_input = browser.find_element("id", "username")
    password_input = browser.find_element("id", "password")
    username_input.send_keys(linkedin_username)
    password_input.send_keys(linkedin_password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)

    browser.get(f"https://www.linkedin.com/in/{linkedin_profile_name}/recent-activity/all/")

    for _ in range(2):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    posts = get_linkedin_posts(browser.page_source)
    browser.quit()

    # We'll just return 2 of the latest posts, since it should be enough for the LLM to get the overall style
    return str(posts[:2])


@tool("ScrapeLinkedinPosts")
def scrape_linkedin_posts_tool() -> str:
    """
    A tool that can be used to scrape LinkedIn posts
    """
    return scrape_linkedin_posts_fn()


def scrape_linkedin_group_posts_fn() -> str:
    """Scrape latest posts from the groups provided in ``LINKEDIN_GROUP_URLS``."""
    linkedin_username = os.environ.get("LINKEDIN_EMAIL")
    linkedin_password = os.environ.get("LINKEDIN_PASSWORD")
    group_urls = os.environ.get("LINKEDIN_GROUP_URLS")

    if not (linkedin_username and linkedin_password):
        raise LinkedinToolException()

    if not group_urls:
        raise Exception("You need to set the LINKEDIN_GROUP_URLS env variable")

    browser = webdriver.Chrome()
    browser.get("https://www.linkedin.com/login")

    username_input = browser.find_element("id", "username")
    password_input = browser.find_element("id", "password")
    username_input.send_keys(linkedin_username)
    password_input.send_keys(linkedin_password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)

    posts_by_group = {}
    for url in [url.strip() for url in group_urls.split(",") if url.strip()]:
        browser.get(url)
        for _ in range(2):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        posts = get_linkedin_posts(browser.page_source)
        posts_by_group[url] = posts[:2]

    browser.quit()
    return str(posts_by_group)


@tool("ScrapeLinkedinGroupPosts")
def scrape_linkedin_group_posts_tool() -> str:
    """A tool that scrapes LinkedIn groups for recent posts."""
    return scrape_linkedin_group_posts_fn()
