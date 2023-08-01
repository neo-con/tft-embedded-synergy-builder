#item_builder.py
import os
import json
import pickle
import numpy as np
import faiss
from dotenv import load_dotenv


def load_config():
    load_dotenv()
    return {
        "champ_data_pkl": os.getenv("CHAMP_DATA_PKL"),
        "champ_data_json": os.getenv("CHAMP_DATA_JSON"),
        "embeddings": os.getenv("EMBEDDINGS_PATH"),
    }


def load_config_items():
    load_dotenv()
    return {
        "item_data_pkl": os.getenv("ITEM_DATA_PKL"),
        "item_data_json": os.getenv("ITEM_DATA_JSON"),
        "i_embeddings": os.getenv("I_EMBEDDINGS_PATH"),
    }


def load_pickle_data(file_name):
    """
    Loads data from a pickle file

    Parameters:
    file_name (str): The path to the pickle file

    Returns:
    dict: The loaded data
    """
    try:
        with open(file_name, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def load_json_data(file_name):
    """
    Loads data from a json file

    Parameters:
    file_name (str): The path to the json file

    Returns:
    dict: The loaded data
    """
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def search(
    query_embedding,
    index_path,
    embeddings,
    top_k=15,
):
    """
    Search for the top_k nearest neighbors to the query_embedding

    Parameters:
    query_embedding (np.array): The embedding of the query
    index_path (str): The path to the faiss index
    embeddings (dict): The embeddings dictionary
    top_k (int, optional): The number of nearest neighbors to return. Defaults to 10.

    Returns:
    list: The names of the top_k nearest neighbors in the embeddings
    """
    index = faiss.read_index(index_path)

    # faiss requires the query to be a 2D array
    query = np.array([query_embedding])
    _, nearest_indices = index.search(query, top_k)
    nearest_items = [list(embeddings.keys())[i] for i in nearest_indices[0]]

    return nearest_items[:top_k]


def main(config, config_items, champion_names, top_k_items=15):
    champ_data_pkl = load_pickle_data(config["champ_data_pkl"])
    queries = [
        champ_data_pkl["embeddings"][champion_name] for champion_name in champion_names
    ]
    avg_query = np.mean(queries, axis=0)

    item_data_pkl = load_pickle_data(config_items["item_data_pkl"])
    original_item_data = load_json_data(config_items["item_data_json"])

    top_items = search(
        avg_query,
        config_items["i_embeddings"],
        item_data_pkl["embeddings"],
        top_k_items,
    )

    return top_items
    #print(f"\nTop Items: {top_items}\n")


if __name__ == "__main__":
    champion_names = input(
        "Please enter the champion names separated by comma: "
    ).split(", ")

    config = load_config()
    config_items = load_config_items()
    main(config, config_items, champion_names)
