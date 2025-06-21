from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

llm = init_chat_model("meta-llama/llama-4-scout-17b-16e-instruct", model_provider="groq")