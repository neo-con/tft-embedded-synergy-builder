# tft-embedded-helper


## Description
TFT Embedded Helper is a recommendation system for the game Teamfight Tactics (TFT), built to suggest the best champions and items for a given player's champion or champions. This is a fun project to explore how well semantic-based search performs when comparing embeddings between champions and items.

## Setup and Installation
To set up the project, follow these steps:

1. Ensure that pipenv is installed on your system. If not, you can install it using `pip install pipenv`.
2. Clone the repository from GitHub using the following command: `git clone https://github.com/neo-con/tft-embedded-helper.git`
3. Navigate to the cloned repository's directory. If you cloned the repository into your current directory, you can do this with: `cd tft-embedded-helper`
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

## License
This project is licensed under the terms of the MIT License. You are free to use, modify, and distribute the code, provided that proper credit is given.

**Note:** This project is not affiliated with or endorsed by the creators of Teamfight Tactics or Riot Games. All game images, names, and other details are property of their respective owners.