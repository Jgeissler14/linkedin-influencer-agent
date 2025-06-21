import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from tools import scrape_linkedin_posts_fn

load_dotenv()

influencer_profile = os.environ.get("INFLUENCER_PROFILE_NAME")
target_profile = os.environ.get("TARGET_PROFILE_NAME")

if not influencer_profile or not target_profile:
    raise SystemExit("INFLUENCER_PROFILE_NAME and TARGET_PROFILE_NAME must be set")

influencer_posts = scrape_linkedin_posts_fn(influencer_profile)
target_posts = scrape_linkedin_posts_fn(target_profile)

latest_post = target_posts[0] if target_posts else ""
style_examples = "\n\n".join(influencer_posts)

llm = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model="gpt-3.5-turbo-0125")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You rewrite LinkedIn posts while mimicking a specific writing style."),
    (
        "user",
        "Rewrite the following post in the style demonstrated below.\n\nPost:\n{post}\n\nStyle examples:\n{style}\n",
    ),
])
chain = prompt | llm

result = chain.invoke({"post": latest_post, "style": style_examples})

print(result.content)

