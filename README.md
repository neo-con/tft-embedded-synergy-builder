# tft-embedded-synergy-builder


## Description
TFT Embedded Synergy Builder is a recommendation system for the game Teamfight Tactics (TFT). It utilizes semantic-based search and embeddings to provide players with personalized suggestions for the best champions and items based on their selected champion or champions. The system manages multiple champion embeddings by calculating the average embedding of the selected champions. This average embedding is then used to find similar champions based on their embeddings. This project aims to explore the effectiveness of semantic search in the context of champion and item recommendations in TFT.

## Interactive Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tft-embedded.streamlit.app/)

## Setup and Installation
To set up the project, follow these steps:

1. Ensure that pipenv is installed on your system. If not, you can install it using `pip install pipenv`.
2. Clone the repository from GitHub using the following command: `git clone https://github.com/neo-con/tft-embedded-synergy-builder.git`
3. Navigate to the cloned repository's directory. If you cloned the repository into your current directory, you can do this with: `cd tft-embedded-synergy-builder`
4. Run `pipenv install` to install all dependencies listed in the `Pipfile`. 
5. After the installation completes, activate the Pipenv shell: `pipenv shell`
6. You can now run the application using `streamlit run app.py`.

## Usage
Input your chosen champion into the text box provided. The system will then generate a team composition based on the champion's embeddings match. An example of the application in use can be found at the live Streamlit app [here](https://tft-embedded.streamlit.app).

## Project Structure
Below is a brief overview of the key files and folders:

- `app.py` - This is the main application file where the Streamlit app is defined.
- `assets/` - This directory contains all the static files used in the project, including images for champions and items.
- `builders/` - This directory contains the builder files (`item_builder.py` and `synergy_builder.py`) used for item and synergy recommendations.
- `data/` - This directory contains all the data files used in the project.
- `embeddings/` - This directory contains the embeddings for champions and items.
- `scripts/` - This directory contains the scripts used to generate embeddings and scrape data.
- `template/` - This directory contains the HTML template used in the Streamlit app.

## Acknowledgments
Special thanks to the Facebook team for their work on [FAISS](https://github.com/facebookresearch/faiss), and OpenAI for their [Embedding API](https://platform.openai.com/docs/guides/embeddings).

## Known Issues:
Layout on mobile device sucks. This is due to Streamlit's lack of responsiveness controls. Hoping to switch frameworks in the future, perhaps Django or Flask, or even React.

## License
This project is licensed under the terms of the MIT License. You are free to use, modify, and distribute the code, provided that proper credit is given.

**Note:** This project is not affiliated with or endorsed by the creators of Teamfight Tactics or Riot Games. All game images, names, and other details are property of their respective owners.
