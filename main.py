import streamlit as st
import os
import cv2 as cv
from vc import create_parts
import shamir
import random as rn

st.set_page_config(layout="wide")
tab1, tab2, tab3, tab4 = st.tabs(['VC', 'Shamir', 'wip', 'wip'])

with tab1:
    st.header("Visual Cryptography")
    images = os.listdir('images')
    image = st.selectbox('Images', images, 0)
    image_data = cv.imread('images/'+image, cv.IMREAD_GRAYSCALE)
    st.write("#### Image size: ", image_data.shape)
    st.image(image_data)

    part_1, part_2 = create_parts(image_data)

    col1, col2 = st.columns(2)
    with col1:
        "### Part 1"
        st.image(part_1)
    
    with col2:
        "### Part 2"
        st.image(part_2)

    merged_parts = part_1 == part_2

    "### Merged Image"
    st.image(merged_parts * 255)

with tab2:
    st.header("Shamir Method")
    p = st.number_input("p - liczba pierwsza", value=8017)
    n = st.slider(label="n - całkowita liczba udziałów", min_value=0, max_value=100, step=1, value=7)
    t = st.slider("t - wymagana minimalna liczba udziałów potrzebna do odtworzenia", min_value=0, max_value=n, step=1, value=3)
    s = st.number_input("s - sekret", value=7)
    res2 = ""
    k = st.text(f"Keys: {res2}")

    scol1, scol2 = st.columns(2)

    with scol1:
        "# Shamir Encryptor"
        res0, res1, res2 = shamir.shamir_e(s, n, t, p)
        "## Współczynniki"
        for line in res0:
            st.write(line)
        "## Obliczenie udziałów"
        for line in res1:
            st.write(line)
        "## Udziały"
        for line in res2.split(";"):
            st.write(line)

    with scol2:
        "# Shamir Decryptor"
        keys = []
        while len(keys) < t:
            key = rn.choice(res2.split(";"))
            if key not in keys:
                keys.append(key)
        res20, res21, res22 = shamir.shamir_d(res2, p)
        
        "## Udziały"
        for line in keys:
            st.write(line)
        "## Wyniki"
        for line in res21:
            st.write(line)
        "## Odszyfrowane"
        st.write(res22)