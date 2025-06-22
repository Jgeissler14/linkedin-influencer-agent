import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import json
from tools import (
    scrape_linkedin_posts_fn,
    scrape_linkedin_posts_with_urls_fn,
    classify_post,
)

load_dotenv()

influencer_profile = os.environ.get("INFLUENCER_PROFILE_NAME")
target_profile = os.environ.get("TARGET_PROFILE_NAME")

if not influencer_profile or not target_profile:
    raise SystemExit("INFLUENCER_PROFILE_NAME and TARGET_PROFILE_NAME must be set")

influencer_posts = scrape_linkedin_posts_fn(influencer_profile)
target_posts = scrape_linkedin_posts_with_urls_fn(target_profile)

style_examples = "\n\n".join(influencer_posts)

llm = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model="gpt-3.5-turbo-0125")

reframe_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You rewrite LinkedIn posts while mimicking a specific writing style. "
        "If the original text is personal, remove those references and turn it into a neutral, educational post.",
    ),
    (
        "user",
        "Rewrite the following post in the given style.\n\nPost:\n{post}\n\nStyle examples:\n{style}\n",
    ),
])
reframe_chain = reframe_prompt | llm

outreach_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You craft short LinkedIn outreach messages about Terraform and cloud services. "
        "Reference the person's post and invite them to chat. Keep it under 200 characters",
    ),
    (
        "user",
        "Post:\n{post}\n\nReframed version:\n{reframed}\n",
    ),
])
outreach_chain = outreach_prompt | llm

outputs = []

for entry in target_posts:
    post_text = entry.get("post", "")
    url = entry.get("url", "")
    post_type = classify_post(post_text)
    print(f"Post type: {post_type}")
    reframed = reframe_chain.invoke({"post": post_text, "style": style_examples}).content
    outreach = outreach_chain.invoke({"post": post_text, "reframed": reframed}).content
    outputs.append({"post": post_text, "url": url, "response": outreach})

with open("output.json", "w") as f:
    json.dump(outputs, f, indent=2)

print(json.dumps(outputs, indent=2))

