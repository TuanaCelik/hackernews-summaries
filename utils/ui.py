import streamlit as st
from PIL import Image

def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def set_initial_state():
    set_state_if_absent("top_k", "How many of the top posts would you like a summary for?")
    set_state_if_absent("result", None)
    set_state_if_absent("haystack_started", False)

def reset_results(*args):
    st.session_state.result = None
    st.session_state.top_k = None

def set_openai_api_key(api_key: str):
    st.session_state["HF_TGI_TOKEN"] = api_key

def sidebar():
    with st.sidebar:
        # image = Image.open('logo/haystack-logo-colored.png')
        st.markdown("Thanks for coming to this 🤗 Space.\n\n"
        "This is a project for fun, and is not a final product."
        " There's a lot that can be improved to make this app better.\n\n"
        "**Take results with a grain of** 🧂\n\n"
        "For more on how this was built, instructions to run locally and to contribute: [visit GitHub](https://github.com/TuanaCelik/hackernews-summaries#readme)")

        st.markdown(
            "## How to use\n"
            "1. Enter your Hugging Face Token below\n"
            "2. Select the number of summaries you want\n"
            "3. Enjoy 🤗\n"
        )

        api_key_input = st.text_input(
            "Hugging Face Token",
            type="password",
            placeholder="Paste your Hugging Face TGI Token",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",
            value=st.session_state.get("HF_TGI_TOKEN", ""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)

        st.markdown("---")
        st.markdown(
            "## How this works\n"
            "This app was built with [Haystack 2.0-Beta](https://haystack.deepset.ai) using the"
            " [`HuggingFaceTGIGenerator`](https://docs.haystack.deepset.ai/v2.0/docs/hugginfacetgigenerator and [`PromptBuilder`](https://docs.haystack.deepset.ai/v2.0/docs/promptbuilder).\n\n"
            " The source code is also on [GitHub](https://github.com/TuanaCelik/hackernews-summaries)"
            " with instructions to run locally.\n"
            "You can see how the `PromptBuilder` was set up [here](https://github.com/TuanaCelik/hackernews-summaries/blob/main/utils/haystack.py)")
        st.markdown("---")
        st.markdown("Made by [tuanacelik](https://twitter.com/tuanacelik)")