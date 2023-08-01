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
    top_champs_by_cost, top_champs_by_distance = synergy_builder.main(
        config, champion_names
    )

    cost_expander = st.expander("Top Champions by Cost", expanded=False)
    with cost_expander:
        selected_champ_cost = display_images(
            top_champs_by_cost, CHAMPION_IMAGE_FOLDER, "cost"
        )

    distance_expander = st.expander("Top Champions by Distance", expanded=False)
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
st.title("TFT Embedded Helper")

champion_names_input = st.text_input("Enter the champion|s name separated by comma:")

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
    TFT Embedded Helper is a recommendation system for the game Teamfight Tactics (TFT), 
    built to suggest the best champions and items for a given player's champion or champions. 
    This is a fun project to explore how well semantic-based search performs when comparing 
    embeddings between champions and items. 
    """,
)
st.write("---")
st.markdown(
    """
    <p align="center">View the source on 
    <a href="https://github.com/neo-con/tft-embedded-helper.git" target="_blank">
    <img src="data:image/png;base64,{0}" alt="GitHub" width="32"></a></p>
    """.format(github_logo_b64),
    unsafe_allow_html=True,
)