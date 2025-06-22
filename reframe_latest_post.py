import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from tools import search_linkedin_posts_with_urls_fn

load_dotenv()

# Keywords we want to search for
KEYWORDS = ["terraform", "devops", "aws", "azure"]
QUERY = " ".join(KEYWORDS)

posts = search_linkedin_posts_with_urls_fn(QUERY)

llm = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model="gpt-3.5-turbo-0125")

outreach_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You craft short LinkedIn outreach messages about Terraform and cloud services. "
        "Post:\n{post}\n",
    ),
for entry in posts:
    outreach = outreach_chain.invoke({"post": post_text}).content


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

