#synergy_builder.py
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
    champion_data,
    champion_names,
    top_k=15,
    sort_by_cost=False,
):
    """
    Search for the top_k nearest neighbors to the query_embedding

    Parameters:
    query_embedding (np.array): The embedding of the query
    index_path (str): The path to the faiss index
    embeddings (dict): The embeddings dictionary
    champion_data (dict): The original champion data with 'cost' property
    top_k (int, optional): The number of nearest neighbors to return. Defaults to 10.
    sort_by_cost (bool, optional): If True, sort champions by cost. Defaults to False.

    Returns:
    list: The names of the top_k nearest neighbors in the embeddings, optionally sorted by cost
    """
    index = faiss.read_index(index_path)

    # faiss requires the query to be a 2D array
    query = np.array([query_embedding])
    _, nearest_indices = index.search(query, top_k + len(champion_names))
    nearest_champs = [list(embeddings.keys())[i] for i in nearest_indices[0]]

    if sort_by_cost:
        nearest_champs = sorted(
            nearest_champs, key=lambda champ: champion_data[champ]["cost"]
        )

    return nearest_champs[:top_k]


def main(config, champion_names, top_k_champs=15):
    champ_data_pkl = load_pickle_data(config["champ_data_pkl"])
    original_champ_data = load_json_data(config["champ_data_json"])
    
    try:
        queries = [
            champ_data_pkl["embeddings"][champion_name] for champion_name in champion_names
        ]
    except KeyError:
        print("Make sure you enter a champ from the recent set.")
        return None

    avg_query = np.mean(queries, axis=0)

    top_champs_by_cost = search(
        avg_query,
        config["embeddings"],
        champ_data_pkl["embeddings"],
        original_champ_data,
        champion_names,
        top_k_champs,
        sort_by_cost=True,
    )

    top_champs_by_distance = search(
        avg_query,
        config["embeddings"],
        champ_data_pkl["embeddings"],
        original_champ_data,
        champion_names,
        top_k=10,
    )

    return top_champs_by_cost, top_champs_by_distance


if __name__ == "__main__":
    champion_names = input(
        "Please enter the champion names separated by comma: "
    ).split(", ")

    config = load_config()
    main(config, champion_names)
