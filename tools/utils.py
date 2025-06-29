from bs4 import BeautifulSoup


def parse_html_content(page_source: str):
    """
    Parses the HTML from the LinkedIn's profile and returns a collection of LinkedIn posts. We don't need
    all of them, just a few, since we can get the "writing-style" very easily.

    Args:
        page_source: The HTML content

    Returns:
        A list of div containers representing a collection of LinkedIn posts
    """
    linkedin_soup = BeautifulSoup(page_source.encode("utf-8"), "lxml")

    containers = linkedin_soup.find_all("div", {"class": "feed-shared-update-v2"})
    containers = [container for container in containers if 'activity' in container.get('data-urn', '')]
    return containers


def get_post_content(container, selector, attributes):
    """
    Gets the content of a LinkedIn post container
    Args:
        container: The div container
        selector: The selector
        attributes: Attributes to be fetched

    Returns:
        The post content
    """
    try:
        element = container.find(selector, attributes)
        if element:
            return element.text.strip()
    except Exception as e:
        print(e)
    return ""


def get_linkedin_posts(page_source: str):
    containers = parse_html_content(page_source)
    posts = []

    for container in containers:
        post_content = get_post_content(container, "div", {"class": "update-components-text"})
        posts.append(post_content)

    return posts


def get_linkedin_posts_with_urls(page_source: str):
    """Return LinkedIn posts along with their URLs."""
    containers = parse_html_content(page_source)
    posts = []

    for container in containers:
        post_content = get_post_content(container, "div", {"class": "update-components-text"})
        urn = container.get("data-urn", "")
        url = f"https://www.linkedin.com/feed/update/{urn}/" if urn else ""
        posts.append({"post": post_content, "url": url})

    return posts


def is_personal_post(post: str) -> bool:
    """Return ``True`` if the text appears to reference personal life events."""
    if not post:
        return False

    personal_keywords = [
        " i ",
        " my ",
        " me ",
        " myself",
        " we ",
        " our ",
        " family",
        " birthday",
        " wedding",
        "anniversary",
        "friend",
        "mom",
        "dad",
        "baby",
    ]
    lower = f" {post.lower()} "
    return any(word in lower for word in personal_keywords)


def classify_post(post: str) -> str:
    """Classify a LinkedIn post as ``PERSONAL`` or ``EDUCATIONAL``."""
    return "PERSONAL" if is_personal_post(post) else "EDUCATIONAL"
