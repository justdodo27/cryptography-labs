import streamlit as st
import os
import cv2 as cv
from vc import create_parts
import shamir
import random as rn
import dh
from primes import PRIMES
import rsa_

st.set_page_config(layout="wide")
tab1, tab2, tab3, tab4 = st.tabs(['VC', 'Shamir', 'Diffie-Hellman', 'RSA'])

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
        res0, res2 = shamir.shamir_e(s, n, t, p)
        "## Współczynniki"
        for line in res0:
            st.write(line)
        "## Udziały"
        for line in res2:
            st.write(line)

    with scol2:
        "# Shamir Decryptor"
        keys = []
        while len(keys) < t:
            key = rn.choice(res2)
            if key not in keys:
                keys.append(key)
        res22 = shamir.shamir_d(keys)
        
        "## Udziały"
        for line in keys:
            st.write(line)
        "## Odszyfrowane"
        st.write(res22)

with tab3: 
    st.header("Diffie Hellman")
    N = st.number_input("N - liczba pierwsza", value=5387)
    g = st.number_input("g - pierwiastek pierwotny", value=2144)

    steps, graph = dh.diffie_hellman(N, g)

    col1, col2 = st.columns(2)

    with col1:
        for line in steps:
            st.write(line)

    with col2:
        st.graphviz_chart(graph)


with tab4:
    st.header("RSA")
    "### Prime numbers"
    
    p= st.number_input("p", value=rn.choice(PRIMES))
    q = st.number_input("q", value=rn.choice(PRIMES))

    pub_key, priv_key = rsa_.generate_keys(p, q)

    f"#### Public key: {pub_key}"
    f"#### Private key: {priv_key}"

    msg = st.text_input("Message", value="Lorem ipsum dolor sitt amet, consectetur koniec...", max_chars=50)

    encrypted_msg = rsa_.encrypt_message(pub_key, msg)

    decrypted_msg = rsa_.decrypt_message(priv_key, encrypted_msg)

    f"#### Decrypted message: {decrypted_msg}"

    if msg == decrypted_msg:
        "#### Message after decryption is the same as original one"

