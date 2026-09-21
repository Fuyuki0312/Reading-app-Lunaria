from app.config import Config

from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os

config = Config()


env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path) # Get OpenAI API

client = OpenAI()


def get_client():

    return client
