---
title: Hacker News Summaries
emoji: 🧡
colorFrom: yellow
colorTo: green
sdk: streamlit
sdk_version: 1.25.0
app_file: app.py
pinned: true
---

# Hacker News Summaries

### Try it out on [🤗 Spaces](https://huggingface.co/spaces/deepset/hackernews-summaries)

##### A simple app to get summaries of some of the latest top hackernews posts

This is a demo just for fun 🥳
This repo contains a streamlit application that given a number between 1 - 5 gives you summaries of that many of the latest top Hacker News posts.
It uses a [custom Haytack component](https://docs.haystack.deepset.ai/v2.0/docs/custom-component?utm_campaign=developer-relations)
It's been built with [Haystack](https://haystack.deepset.ai) using the [`HuggingFaceTGIGenerartor`](https://docs.haystack.deepset.ai/v2.0/docs/huggingfacetgigenerator?utm_campaign=developer-relations) and by creating a [`PromptBuilder`](https://docs.haystack.deepset.ai/v2.0/docs/promptbuilder?utm_campaign=developer-relations)


If you try to run it yourself and find ways to make this app better, please feel free to create an issue/PR 🙌

## Installation and Running
1. Install requirements:
`pip install -r requirements.txt`
2. Run the streamlit app:
`streamlit run app.py`

This will start up the app on `localhost:8501` where you will dind a simple search bar

#### The Haystack Community is on [Discord](https://discord.com/invite/VBpFzsgRVF)
