import streamlit as st
from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import HuggingFaceTGIGenerator
from .hackernews_fetcher import HackernewsFetcher

def start_haystack(hf_token):
    prompt_template = """
You will be provided one or more top HakcerNews posts, followed by their URL.
For the posts you have, provide a short summary followed by the URL that the post can be found at.

Posts:
{% for article in articles %}
  Post content: {{article.content}}
  Post URL: {{article.meta['url']}}
{% endfor %}
Summaries:
"""

    prompt_builder = PromptBuilder(template=prompt_template)
    llm = HuggingFaceTGIGenerator("mistralai/Mixtral-8x7B-Instruct-v0.1", token=hf_token)
    fetcher = HackernewsFetcher()

    pipe = Pipeline()
    pipe.add_component("hackernews_fetcher", fetcher)
    pipe.add_component("prompt_builder", prompt_builder)
    pipe.add_component("llm", llm)

    pipe.connect("hackernews_fetcher.articles", "prompt_builder.articles")
    pipe.connect("prompt_builder.prompt", "llm.prompt")
    return pipe


@st.cache_data(show_spinner=True)
def query(top_k, _pipeline):
    try:
        replies = _pipeline.run(data={"hackernews_fetcher": {"top_k": top_k}, 
                                      "llm": {"generation_kwargs": {"max_new_tokens": 600}}
                                      })
        
        result = replies['llm']['replies']
    except Exception as e:
        result = ["Sorry, there seems to be an issue here 😔"]
    return result