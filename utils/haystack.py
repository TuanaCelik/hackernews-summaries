import streamlit as st
from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import HuggingFaceTGIGenerator, OpenAIGenerator
from .hackernews_fetcher import HackernewsFetcher

st.cache_resource
def start_haystack(key, model):
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
    if model == "Mistral":
        llm = HuggingFaceTGIGenerator("mistralai/Mistral-7B-Instruct-v0.2", token=key)
    elif model == "GPT-4":
        llm = OpenAIGenerator(api_key=key, model="gpt-4")
    fetcher = HackernewsFetcher()

    pipe = Pipeline()
    pipe.add_component("hackernews_fetcher", fetcher)
    pipe.add_component("prompt_builder", prompt_builder)
    pipe.add_component("llm", llm)

    pipe.connect("hackernews_fetcher.articles", "prompt_builder.articles")
    pipe.connect("prompt_builder.prompt", "llm.prompt")
    return pipe


def query(top_k, _pipeline):
    try:
        run_args = {"hackernews_fetcher": {"top_k": top_k}}
        
        if st.session_state.get("model") == "Mistral":
            run_args = {"hackernews_fetcher": {"top_k": top_k}, 
                        "llm": {"generation_kwargs": {"max_new_tokens": 600}}
                        }

        replies = _pipeline.run(data=run_args)
        
        result = replies['llm']['replies']
    except Exception as e:
        result = ["Sorry, there seems to be an issue here 😔"]
    return result