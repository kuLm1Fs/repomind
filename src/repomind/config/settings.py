from openai import OpenAI
import dotenv, os

dotenv.load_dotenv()

class Settings:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

    OPENAI_MODEL = os.getenv("OPENAI_MODEL")

    TOP_K = int(os.getenv("TOP_K", 5))

    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 80))

    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 10))

    MAX_RETRY = int(os.getenv("MAX_RETRY", 1))


settings = Settings()