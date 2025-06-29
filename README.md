<p align="center">
    <img alt="img" src="img/img.png" width=400 />
    <h1 align="center">Automating LinkedIn Post</h1>
    <h3 align="center">crewAI automates my LinkedIn Posts </h3>
</p>

---

> Looking for a more detailed explanation of this repository? You might be interested in the [YouTube video](https://www.youtube.com/watch?v=oIb5JqZ5ylA&ab_channel=TheNeuralMaze)! 😁 


## Description 

This repository contains a crewAI application for reframing LinkedIn posts.
The crew uses several specialized agents:

1️⃣ **Influencer Scraper** – pulls a couple of posts from a chosen influencer profile to learn the desired writing style.

2️⃣ **Target Scraper** – grabs the latest post from a target profile so it can be rewritten.

3️⃣ **Doppelganger Agent** – rewrites the target's post using the style inferred from the influencer posts.

4️⃣ **Web Researcher Agent** – finds a relevant article to reference in the final post.

5️⃣ **Lead Researcher Agent** – searches LinkedIn and the web for potential clients interested in Terraform services.

6️⃣ **Outreach Writer Agent** – crafts a short LinkedIn message to engage those leads.

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

The script prints whether the latest post is **PERSONAL** or **EDUCATIONAL** before outputting the rewritten version. It also generates a list of potential leads and an outreach message you can send them.

Make sure to set the following environment variables (you can use a `.env` file):

- `LINKEDIN_EMAIL` / `LINKEDIN_PASSWORD` – credentials for logging into LinkedIn.
- `OPENAI_API_KEY` – API key used by the language model.
- `SERPER_API_KEY` – API key for searching the web to fetch relevant articles.
- `MISTRAL_API_KEY` – optional API key for the Mistral language model.

```shell
python3 main.py
```
