import re
import pandas as pd
import streamlit as st
from streamlit_float import *
from Topsis import Topsis
import os

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
        st.session_state.preVal_w = [0] * 6
        st.session_state.preVal_i = [0] * 6

    if 'val_w' and 'val_i' not in st.session_state:
        st.session_state.val_w = [0] * 6
        st.session_state.val_i = [0] * 6

    weight = [0] * 6
    impact = [0] * 6
    st.markdown("<h1 style='text-align: center; color: black;'>Sistem Pendukung Keputusan <span style='color: #ab2b7e;'> Pemilihan Laptop</span> Menggunakan Metode <span style='color: #2f359e;'> TOPSIS</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: black;'>oleh <b>Aliya Rahmania</b> (210005), <b>Adinda Salsabila</b> (210017), <b>Sarah Khairunnisa Prihantoro</b> (210063), dan <b>Zakia Noorardini</b> (210065) sebagai Project UAS Mata Kuliah Decision Support System</p>", unsafe_allow_html=True)

    attributes = ["Prosesor 💽", "Layar 💻", "Memori Internal 🖥️", "Penyimpanan 💾", "Berat ⚖️", "Baterai 🔋"]
    descriptions = [
        "Menyediakan instruksi dan daya pemrosesan yang diperlukan oleh komputer untuk menjalankan tugasnya.",
        "Ukuran dan kualitas layar.",
        "Ukuran memori internal (RAM).",
        "Kapasitas penyimpanan total.",
        "Berat laptop.",
        "Jumlah sel baterai.",
    ]

    st.sidebar.markdown(f"<h4 style='color: #ab2b7e; font-weight: bold;'>{attributes[0]}</h4>", unsafe_allow_html=True)
    weight[0] = st.sidebar.slider(descriptions[0], min_value=1.3, max_value=3.1, step=0.1, key='0')
    st.sidebar.markdown(f"<h4 style='color: #ab2b7e; font-weight: bold;'>{attributes[1]}</h4>", unsafe_allow_html=True)
    weight[1] = st.sidebar.slider(descriptions[1], min_value=12.5, max_value= 17.3, step=0.1, key='1')
    st.sidebar.markdown(f"<h4 style='color: #ab2b7e; font-weight: bold;'>{attributes[2]}</h4>", unsafe_allow_html=True)
    weight[2] = st.sidebar.slider(descriptions[2], min_value=4, max_value=32, step=4, key='2')
    st.sidebar.markdown(f"<h4 style='color: #ab2b7e; font-weight: bold;'>{attributes[3]}</h4>", unsafe_allow_html=True)
    weight[3] = st.sidebar.slider(descriptions[3], min_value=128, max_value= 2256, step=4, key='3')
    st.sidebar.markdown(f"<h4 style='color: #ab2b7e; font-weight: bold;'>{attributes[4]}</h4>", unsafe_allow_html=True)
    weight[4] = st.sidebar.slider(descriptions[4], min_value=1.2,max_value= 4.42, step=0.01,key='4')
    st.sidebar.markdown(f"<h4 style='color: #ab2b7e; font-weight: bold;'>{attributes[5]}</h4>", unsafe_allow_html=True)
    weight[5] = st.sidebar.slider(descriptions[5], min_value=3, max_value=6, step=1, key='5')

    for i in range(len(attributes)):
        impact[i] = 1 if weight[i] >= 0 else 0
        weight[i] = abs(weight[i])
        st.session_state.preVal_w[i] = weight[i]
        st.session_state.preVal_i[i] = impact[i]
    st.sidebar.markdown("***")

    float_init()
    float_container = st.sidebar.container()
    with float_container:
        if weight != [0] * 6:
            button = float_container.button("Search", on_click=click_button, disabled=False, use_container_width=True)
        else:
            error = float_container.error("Please change at least one preference!")
            button = float_container.button("Search", on_click=click_button, disabled=True, use_container_width=True)

    float_container.float("bottom: 0; background-color: #f0f2f6; padding: 0px 0px 20px")

    if st.session_state.clicked == True:
        data = pd.read_csv('data/Laptop.csv')
        topsis = Topsis(data, st.session_state.preVal_w, st.session_state.preVal_i)

        for i in range(0, 6):
            st.session_state.val_w[i] = st.session_state.preVal_w[i]
            st.session_state.val_i[i] = st.session_state.preVal_i[i]

        st.session_state.clicked = False
        st.session_state.searched = True

    if st.session_state.searched == False:
        st.markdown("<h4 style='text-align: center; color: black;'>⬅️ Anda belum mencari laptop, beralihlah ke sidebar!</h4>", unsafe_allow_html=True)
    else:
        if data is not None:
            data = pd.read_csv('data/Laptop.csv')
            topsis = Topsis(data, st.session_state.val_w, st.session_state.val_i)
            topsis.run()
            name = topsis.getName()
            rec = topsis.getEmbed()
            percent = topsis.getPercentage()

            for namalap, percentage, i in zip(name, percent, rec):
                iframe_code = f'<iframe style="border-radius:12px; background-color: transparent;" src="{i}?utm_source=generator" width="100%" height="160" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
                st.write(f'Laptop Recommendation: {namalap}')
                st.write(f'Persentase Rekomendasi: {percentage * 100:.3f}')
                st.markdown(iframe_code, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
