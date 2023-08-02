import streamlit as st
import base64
import os
import builders.item_builder as item_builder
import builders.synergy_builder as synergy_builder


CHAMPION_IMAGE_FOLDER = "assets/images/champions"
ITEM_IMAGE_FOLDER = "assets/images/items"

# Load configs
config = item_builder.load_config()
config_items = item_builder.load_config_items()

# Setting the browser title
st.set_page_config(
    page_title="TFT Embedded Synergy Builder",
    page_icon=None,
    layout="centered",
)


def get_image_b64_string(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


# Get the logo base64 strings
logo_path = "assets/images/logo/Teamfight_Tactics.png"
github_logo_path = "assets/images/logo/github-mark-white.png"
logo_b64 = get_image_b64_string(logo_path)
github_logo_b64 = get_image_b64_string(github_logo_path)


def get_html_template():
    with open("template/template.html") as f:
        return f.read()


html_template = get_html_template()


def display_images(data_names, folder, category=None):
    selected = None
    for i in range(0, len(data_names), 5):
        row_data = data_names[i : i + 5]
        columns = st.columns(len(row_data))
        for data, column in zip(row_data, columns):
            try:
                with open(os.path.join(folder, f"{data}.png"), "rb") as f:
                    img_data = base64.b64encode(f.read()).decode()
            except FileNotFoundError:
                st.error(f"Image not found for {data}")
                continue
            html = html_template.format(img_data=img_data, item=data)
            column.markdown(html, unsafe_allow_html=True)
            if category and column.button("Get Items", key=data + category):
                selected = data
    return selected


def display_champion_synergies(champion_names):
    config = synergy_builder.load_config()
    result = synergy_builder.main(config, champion_names)

    if result is None:
        st.write(
            "No champion synergies found. Please make sure you've entered the correct champion name(s), separated by commas with a space after each comma."
        )
        st.write(
            """Example:

            Teemo, Jarvan IV"""
        )
        return None, None

    top_champs_by_cost, top_champs_by_distance = result

    cost_expander = st.expander("Top Champions by Cost", expanded=False)
    with cost_expander:
        selected_champ_cost = display_images(
            top_champs_by_cost, CHAMPION_IMAGE_FOLDER, "cost"
        )

    distance_expander = st.expander("Top Champions by Distance (FINAL)", expanded=False)
    with distance_expander:
        selected_champ_distance = display_images(
            top_champs_by_distance, CHAMPION_IMAGE_FOLDER, "distance"
        )

    return selected_champ_cost, selected_champ_distance


def display_item_images_for_champ(champion_name):
    top_items = item_builder.main(config, config_items, [champion_name])

    if top_items:
        item_expander = st.expander(f"Top items for {champion_name}", expanded=True)
        with item_expander:
            display_images(top_items, ITEM_IMAGE_FOLDER)


# Display logo
st.markdown(
    f'<div style="text-align: center"><img src="data:image/png;base64,{logo_b64}" alt="TFT logo" width="300"></div>',
    unsafe_allow_html=True,
)


# Main UI
st.title("TFT Embedded Synergy Builder")

champion_names_input = st.text_input(
    "Enter the champion name(s) separated by comma (e.g. Ahri) or (Yasuo, Jinx):"
)

if champion_names_input:
    champion_names = champion_names_input.split(", ")
    selected_champ_cost, selected_champ_distance = display_champion_synergies(
        champion_names
    )

    if selected_champ_cost:
        display_item_images_for_champ(selected_champ_cost)
    if selected_champ_distance:
        display_item_images_for_champ(selected_champ_distance)

# Footer
st.write("---")
st.markdown("#### About")
st.markdown(
    """
    <p align="left">TFT Embedded Synergy Builder is a recommendation system for the game Teamfight Tactics (TFT). 
    It utilizes semantic-based search and embeddings to provide players with personalized 
    suggestions for the best champions and items based on their selected champion or champions. 
    This project aims to explore the effectiveness of semantic search in the context of champion 
    and item recommendations in TFT.</p>
    <p align="center"> Expect fun, not perfection!</p>""",
    unsafe_allow_html=True,
)
st.write("---")
st.markdown(
    """
    <p align="center">View the source on 
    <a href="https://github.com/neo-con/tft-embedded-synergy-builder.git" target="_blank">
    <img src="data:image/png;base64,{0}" alt="GitHub" width="32"></a></p>
    """.format(
        github_logo_b64
    ),
    unsafe_allow_html=True,
)
