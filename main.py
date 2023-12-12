import re
import pandas as pd
import streamlit as st
from streamlit_float import *
from Topsis import Topsis
import os

def display_recommendation(iframe_code, percentage):
    st.markdown(f"This laptop matches your preferences by **{percentage * 100:.3f}%**")
    st.progress(percentage)
    st.markdown(iframe_code, unsafe_allow_html=True)

def main():
    dataset_filename = os.path.abspath("data/Laptop.csv")
    data = None  # Initialize data outside the if conditions

    if 'searched' not in st.session_state:
        st.session_state.searched = False

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    def click_button():
        st.session_state.clicked = True

    if 'preVal_w' and 'preVal_i' not in st.session_state:
        st.session_state.preVal_w = [0] * 7
        st.session_state.preVal_i = [0] * 7

    if 'val_w' and 'val_i' not in st.session_state:
        st.session_state.val_w = [0] * 7
        st.session_state.val_i = [0] * 7

    weight = [0] * 7
    impact = [0] * 7
    st.markdown("<h1 style='text-align: center; color: black;'>Rekomendasi <span style='color: #e69ded;'>Laptop</span> Menggunakan Metode TOPSIS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: black;'>oleh <b>Aliya Rahmania</b> (210005), <b>Adinda Salsabila</b> (210017), <b>Sarah Khairunnisa Prihantoro</b> (210063), <b>Zakia Noorardini</b> (210065) sebagai Project UAS Mata Kuliah Decision Support System</p>", unsafe_allow_html=True)

    attributes = ["Processor", "Screen", "InternalMemory", "TotalStorage", "Weight", "BatteryCells", "PointingDevice"]
    descriptions = [
        "Provides the instructions and processing power the computer needs to do its work.",
        "Screen size and quality.",
        "Internal memory (RAM) size.",
        "Total storage capacity.",
        "Weight of the laptop.",
        "Numbers of battery cells.",
        "Type of pointing device (e.g., touchpad)."
    ]

    for i in range(len(attributes)):
        st.sidebar.markdown(f"<h4 style='color: #1DB954; font-weight: bold;'>{attributes[i]}</h4>", unsafe_allow_html=True)
        weight[i] = st.sidebar.slider(descriptions[i], -10, 10, 0)
        impact[i] = 1 if weight[i] >= 0 else 0
        weight[i] = abs(weight[i])
        st.session_state.preVal_w[i] = weight[i]
        st.session_state.preVal_i[i] = impact[i]
    st.sidebar.markdown("***")

    float_init()
    float_container = st.sidebar.container()
    with float_container:
        if weight != [0] * 7:
            button = float_container.button("Search", on_click=click_button, disabled=False, use_container_width=True)
        else:
            error = float_container.error("Please change at least one preference!")
            button = float_container.button("Search", on_click=click_button, disabled=True, use_container_width=True)

    float_container.float("bottom: 0; background-color: #f0f2f6; padding: 0px 0px 20px")

    if st.session_state.clicked == True:
        data = pd.read_csv(dataset_filename)
        topsis = Topsis(data, st.session_state.preVal_w, st.session_state.preVal_i)

        for i in range(0, 7):
            st.session_state.val_w[i] = st.session_state.preVal_w[i]
            st.session_state.val_i[i] = st.session_state.preVal_i[i]

        st.session_state.clicked = False
        st.session_state.searched = True

    if st.session_state.searched == False:
        st.markdown("<h4 style='text-align: center; color: black;'>↖️ You haven't searched for a laptop yet, head to the sidebar!</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: black;'>How about a recommendation for you 👇</h4>", unsafe_allow_html=True)
        # Assuming you want to display a sample recommendation when not searched
        if data is not None:
            sample_columns = ["Processor", "Screen", "InternalMemory", "TotalStorage", "Weight", "BatteryCells", "PointingDevice"]
            sample = data[sample_columns].iloc[[0]]
            st.write("Sample Recommendation:")
            st.write(sample)  # Display sample laptop details
    else:
        if data is not None:
            data = pd.read_csv(dataset_filename)
            topsis = Topsis(data, st.session_state.val_w, st.session_state.val_i)
            topsis.run()
            rec = topsis.getEmbed()
            percent = topsis.getPercentage()

            for i, percentage in zip(rec, percent):
                iframe_code = f'<iframe style="border-radius:12px; background-color: transparent;" src="{i}?utm_source=generator" width="100%" height="160" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
                st.markdown(iframe_code, unsafe_allow_html=True)
                st.write(f'Recommendation Percentage: {percentage}')

if __name__ == '__main__':
    main()
