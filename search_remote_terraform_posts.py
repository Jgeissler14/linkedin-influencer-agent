import os
import re
import requests
from langchain_openai import ChatOpenAI


def serper_search(query: str):
    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY env variable not set")
    resp = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
        json={"q": query},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("organic", [])


def extract_user_link(link: str) -> str:
    match = re.search(r"https://www.linkedin.com/in/[A-Za-z0-9_-]+", link)
    return match.group(0) if match else link


def generate_pitch(llm, post_text: str) -> str:
    prompt = (
        "You found the following LinkedIn post mentioning a remote Terraform job. "
        "Write a short professional outreach message expressing interest in the position "
        "and highlighting cloud infrastructure expertise.\n\n"
        f"Post: {post_text}"
    )
    response = llm.invoke(prompt)
    return response.content.strip()


def main():
    results = serper_search('terraform "remote" "hiring" site:linkedin.com')
    llm = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model="gpt-3.5-turbo-0125")
    for res in results:
        snippet = res.get("snippet", "")
        link = res.get("link", "")
        if "remote" not in snippet.lower():
            continue
        user_link = extract_user_link(link)
        pitch = generate_pitch(llm, snippet)
        print(f"Link: {user_link}\nPost: {snippet}\nPitch: {pitch}\n")


if __name__ == "__main__":
    main()
