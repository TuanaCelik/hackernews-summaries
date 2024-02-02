import os
from dotenv import load_dotenv

load_dotenv()
TWITTER_BEARER = os.getenv('HF_TGI_TOKEN')