<p align="center">
    <img alt="img" src="img/img.png" width=400 />
    <h1 align="center">Automating LinkedIn Post</h1>
    <h3 align="center">crewAI automates my LinkedIn Posts </h3>
</p>

---

> Looking for a more detailed explanation of this repository? You might be interested in the [YouTube video](https://www.youtube.com/watch?v=oIb5JqZ5ylA&ab_channel=TheNeuralMaze)! 😁 


## Description 

This repository contains a crewAI application for reframing LinkedIn posts.
The crew now scrapes two different profiles:

1️⃣ **Influencer Scraper** – pulls a couple of posts from the influencer profile (set with `INFLUENCER_PROFILE_NAME`) to learn the desired writing style.

2️⃣ **Target Scraper** – grabs the latest post from the target profile (set with `TARGET_PROFILE_NAME`).

3️⃣ **Doppelganger Agent** – rewrites the target's post using the style inferred from the influencer posts.

4️⃣ **Web Researcher Agent** – finds a relevant article to reference in the final post.

The doppelganger also checks if the target post is personal or educational and strips any personal references.
The web researcher provides an article that is cited at the end of the rewritten post.

All these agents rely on Selenium tools that require several env variables. Check the `.env.example` file for details.


<p align="center">
    <img alt="img" src="img/architecture.png" width=400 />
</p>


## Usage

First of all, install the necessary dependencies.

```shell
pip install -r requirements.txt
```

After all the dependencies are installed, run `main.py` to scrape the profiles and produce the reframed post.

The script prints whether the latest post is **PERSONAL** or **EDUCATIONAL** before outputting the rewritten version.

Make sure to set the following environment variables (you can use a `.env` file):

- `LINKEDIN_EMAIL` / `LINKEDIN_PASSWORD` – credentials for logging into LinkedIn.
- `INFLUENCER_PROFILE_NAME` – profile handle whose style you want to mimic.
- `TARGET_PROFILE_NAME` – profile handle whose latest post you want to rewrite.
- `OPENAI_API_KEY` – API key used by the language model.
- `SERPER_API_KEY` – API key for searching the web to fetch relevant articles.

```shell
python3 main.py
```
