import json
import numpy as np
import faiss
import pickle
import openai
from dotenv import load_dotenv
import os

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

# Load Environment Variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ITEM_DATA_PKL = os.getenv("ITEM_DATA_PKL")
ITEM_DATA_JSON = os.getenv("ITEM_DATA_JSON")
I_EMBEDDINGS_PATH = os.getenv("I_EMBEDDINGS_PATH")
EMBEDDING_MODEL = "text-embedding-3-small"

if not all([OPENAI_API_KEY, ITEM_DATA_PKL, ITEM_DATA_JSON, I_EMBEDDINGS_PATH]):
    raise EnvironmentError("Some required environment variables are missing.")

openai.api_key = OPENAI_API_KEY


def load_data(file_name):
    """
    Load JSON data from a file.
    """
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data


def preprocess_data(items):
    """
    Preprocess the item data and extract the embeddings.
    """
    docs = {}
    embeddings = {}
    for item_name, spells_dict in items.items():
        for spell_name, spell_content in spells_dict.items():
            # Ensure spell_content is a string
            spell_content = str(spell_content)
            docs[spell_name] = spell_content
            embeddings[item_name] = extract_embeddings(spell_content)
    return docs, embeddings


# using tenacity to throttle openai calls
@retry(
    stop=stop_after_attempt(10),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type(
        (
            openai.error.ServiceUnavailableError,
            openai.error.APIConnectionError,
            openai.error.RateLimitError,
            openai.error.Timeout,
            openai.error.APIError,
        )
    ),
)
def extract_embeddings(desc):
    """
    Extract embeddings from the description using the OpenAI API.
    """
    desc = (
        desc.replace("\n", " ")
        .replace("  ", " ")
        .strip()
        .replace("+", "")
        .replace("%", "")
    )
    response = openai.Embedding.create(model=EMBEDDING_MODEL, input=[desc])
    embedding = np.array(response["data"][0]["embedding"])
    return embedding


def build_faiss_index(embeddings):
    """
    Build a Faiss index from the embeddings.
    """
    # Note: OpenAI dimensions are always 1536 (as of 07.2023)
    dimension = embeddings[list(embeddings.keys())[0]].shape[0]

    # Initialize the index
    index = faiss.IndexFlatIP(dimension)

    # Add vectors to the index
    for i, (title, embedding) in enumerate(embeddings.items()):
        index.add(np.array([embedding]))

    return index


def save_faiss_index(index, file_name):
    """
    Save a Faiss index to a file.
    """
    faiss.write_index(index, file_name)


def save_data(data, file_name):
    """
    Save data to a file using pickle.
    """
    with open(file_name, "wb") as f:
        pickle.dump(data, f)


def main():
    """
    Main execution function.
    """
    tft_item_data = load_data(ITEM_DATA_JSON)
    docs, embeddings = preprocess_data(tft_item_data)
    index = build_faiss_index(embeddings)
    save_faiss_index(index, I_EMBEDDINGS_PATH)
    save_data({"docs": docs, "embeddings": embeddings}, ITEM_DATA_PKL)


if __name__ == "__main__":
    main()
