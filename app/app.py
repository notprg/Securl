import streamlit as st
import joblib
import pandas as pd
import base64
from url_utilities.url import *

image_urls = [
    "images/logo.png",
    "images/green_logo.png",
    "images/red_logo.png"
]

with open("models_stats/Naive Bayes/cr_nb.txt", "r") as file:
    cr_nb = file.read()

with open("models_stats/Random Forest/cr_rf.txt", "r") as file:
    cr_rf = file.read()

with open("models_stats/Stochastic Gradient Descent/cr_sgd.txt", "r") as file:
    cr_sgd = file.read()

stats = {'Random Forest': {'Classification Report': cr_rf},
         'Naive-Bayes': {'Classification Report':  cr_nb},
         'Stochastic Gradient Descent': {'Classification Report':  cr_sgd}}

current_image_index = 0


@st.cache_data
def load(scaler_path, model_path):
    sc = joblib.load(scaler_path)
    model = joblib.load(model_path)
    return sc, model


def get_features(url):
    row = []
    char = ['@', '?', '-', '=', '.', '#', '%', '+', '$', '!', '*', ',', '//']
    row.append(len(url))
    for c in char:
        row.append(url.count(c))
    row.append(abnormal_url(url))
    row.append(http_secure(url))
    row.append(digit_count(url))
    row.append(letter_count(url))
    row.append(shortening_service(url))
    row.append(ip_address(url))
    return row


def change_image(index):
    global current_image_index
    current_image_index = index
    image_container.image(image_urls[current_image_index])


def inference(row, scaler, model, feat_cols):
    df = pd.DataFrame([row], columns=feat_cols)
    X = scaler.transform(df)
    features = pd.DataFrame(X)
    prediction = model.predict(features)
    if prediction == 0:
        change_image(1)
        return "This is a benign URL ✅"
    elif prediction == 1:
        change_image(2)
        return "This is a defacement URL ❌"
    elif prediction == 2:
        change_image(2)
        return "This is a phishing URL 🎣"
    elif prediction == 3:
        change_image(2)
        return "This is a malware URL 🦠"


st.set_page_config(
    page_title="Malicious URL Detection",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 2500px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)
image_container = st.empty()
image_container.image(image_urls[current_image_index])
st.markdown("""
## Welcome to Malicious URL Detection

This app is designed to detect malicious URLs. Enter a URL in the text field and press the "Detect URL" button to get the result.
""")
st.markdown("""
    <style>
        body {
            zoom: 2.5;
        }
    </style>
""", unsafe_allow_html=True)
url = st.text_input("Insert URL")
st.sidebar.link_button("Explore the dataset", "https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset/",
                       use_container_width=True)
with st.sidebar.expander("Advanced technologies"):
    st.write(
        "Our malicious URL detection system is built upon a sophisticated artificial intelligence model meticulously trained on an extensive dataset comprising over 600,000 samples. Leveraging state-of-the-art machine learning techniques, our model achieves an impressive accuracy rate exceeding 90%. This high level of accuracy ensures robust identification and classification of potentially harmful URLs, providing an advanced layer of security for users navigating the online landscape. Our commitment to utilizing cutting-edge technologies underscores our dedication to delivering a reliable and effective solution for preemptively identifying and mitigating cyber threats.")
with st.sidebar.expander("Advanced options"):
    m = st.selectbox(
        'Select the model',
        ('Random Forest', 'Stochastic Gradient Descent', 'Naive-Bayes'))


lines = stats[m]['Classification Report'].split("\n")
formatted_string = "```\n"
formatted_string += "Classification Report\n\n\n"
for line in lines:
    if line.startswith('precision') or line.startswith('accuracy'):
        formatted_string += f"# {line}\n"
    else:
        formatted_string += f"  {line}\n"
formatted_string += "\n"
formatted_string += "```"

with st.sidebar.expander("Statistics"):
    # st.write("Classification Report")
    st.markdown(formatted_string, unsafe_allow_html=True)

with st.sidebar.expander("About Us"):
    prg, rl = st.columns(2)
    with prg:
        st.write("<span style='font-size: 20px;'><b>Rocco Pizzulo</b></span>", unsafe_allow_html=True)
        st.image("images/prg.jpg")
        st.write("<span style='font-size: 13px;'><b>Computer Engineer</b></span>", unsafe_allow_html=True)
        # st.image("images/linkedin.png", width=90)
        st.markdown(
            """<a href="https://www.linkedin.com/in/rocco-gerardo-pizzulo-718659241/">
            <img src="data:image/png;base64,{}" width="100">
            </a>""".format(
                base64.b64encode(open("images/linkedin.png", "rb").read()).decode()
            ),
            unsafe_allow_html=True,
        )
        st.markdown("")

    with rl:
        st.write("<span style='font-size: 20px;'><b>Luigi Russo</b></span>", unsafe_allow_html=True)
        st.image("images/prg.jpg")
        st.write("<span style='font-size: 13px;'><b>Computer Engineer</b></span>", unsafe_allow_html=True)
        # st.image("images/linkedin.png", width=90)
        st.markdown(
            """<a href="https://www.linkedin.com/in/luiigirusso/">
            <img src="data:image/png;base64,{}" width="100">
            </a>""".format(
                base64.b64encode(open("images/linkedin.png", "rb").read()).decode()
            ),
            unsafe_allow_html=True,
        )
        st.markdown("")


if not url:
    detect_button = st.button("Detect URL", disabled=True)
else:
    detect_button = st.button("Detect URL", disabled=False)

if detect_button:
    with st.spinner("Detecting..."):
        feat_cols = ['url_len', '@', '?', '-', '=', '.', '#', '%', '+', '$', '!', '*', ',', '//', 'abnormal_url', 'https', 'digits', 'letters', 'shortening_service', 'ip_address']
        if m == 'Random Forest':
            model_path = 'models/rf.joblib'
        elif m == 'Stochastic Gradient Descent':
            model_path = 'models/sgd.joblib'
        elif m == 'Naive-Bayes':
            model_path = 'models/nb.joblib'
        sc, model = load('models/scaler.joblib', model_path)
        r = get_features(url)
        result = inference(r, sc, model, feat_cols)
        st.markdown(f"### {result}")
