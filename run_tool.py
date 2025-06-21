import os
from tools import scrape_linkedin_posts_fn

profile = os.environ.get("TARGET_PROFILE_NAME") or os.environ.get("INFLUENCER_PROFILE_NAME")
print(scrape_linkedin_posts_fn(profile))
