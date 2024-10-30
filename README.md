# TFT Embedded Synergy Builder

![License](https://img.shields.io/badge/License-MIT-blue.svg)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tft-embedded-synergy-builder.streamlit.app/)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Interactive Demo](#interactive-demo)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Acknowledgments](#acknowledgments)
- [Known Issues](#known-issues)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Description

**TFT Embedded Synergy Builder** is a recommendation system designed for [Teamfight Tactics (TFT)](https://support.leagueoflegends.com/). Leveraging semantic-based search and embeddings, it offers personalized suggestions for optimal champions and items based on your selected champions. By computing the average embedding of chosen champions, the system identifies synergistic champions to enhance your team composition.

This project investigates the effectiveness of semantic search techniques in generating champion and item recommendations, aiming to assist players in strategizing and optimizing their gameplay.

## Features

- **Personalized Recommendations:** Tailored suggestions for champions and items based on your selections.
- **Semantic Search:** Utilizes embeddings to understand champion relationships and synergies.
- **Interactive Interface:** User-friendly interface built with Streamlit for seamless interaction.
- **Real-time Suggestions:** Instantaneous recommendations as you select your champions.

## Interactive Demo

Experience the application firsthand! Click the badge below to launch the live demo.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tft-embedded-synergy-builder.streamlit.app/)

## Setup and Installation

Follow these steps to set up the project locally:

### Prerequisites

- **Python 3.8 or higher**
- **Pipenv**: Python dependency manager.

#### Install Pipenv

If you don't have Pipenv installed, install it using pip:

```bash
pip install pipenv
```

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/neo-con/tft-embedded-synergy-builder.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd tft-embedded-synergy-builder
   ```

3. **Install Dependencies**

   Use Pipenv to install project dependencies:

   ```bash
   pipenv install
   ```

4. **Activate the Pipenv Shell**

   ```bash
   pipenv shell
   ```

5. **Run the Application**

   Launch the Streamlit app:

   ```bash
   streamlit run app.py
   ```

   The application should now be accessible at `http://localhost:8501`.

## Usage

1. **Select Your Champion(s):**

   Enter your chosen champion(s) into the input text box. You can input multiple champions separated by commas.

2. **Receive Recommendations:**

   The system will generate a recommended team composition based on the embeddings and synergies of your selected champions.

3. **Explore Suggested Items:**

   Along with champion recommendations, optimal items for your team will be suggested to enhance performance.


## Acknowledgments

- **[FAISS by Facebook Research](https://github.com/facebookresearch/faiss):** For providing efficient similarity search and clustering of dense vectors.
- **[OpenAI Embedding API](https://platform.openai.com/docs/guides/embeddings):** For powering the semantic search capabilities.

## Known Issues

- **Mobile Responsiveness:** The layout on mobile devices is suboptimal due to limited responsiveness controls in Streamlit. Plans to migrate to more flexible frameworks like Django, Flask, or React are underway to address this limitation.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add your feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

Please ensure your contributions adhere to the project's coding standards and include relevant tests.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code, provided that proper credit is given.

## Disclaimer

**Note:** This project is not affiliated with or endorsed by the creators of Teamfight Tactics or Riot Games. All game images, names, and other details are property of their respective owners.
