import streamlit as st
from openai import OpenAI
from PIL import Image
import json
import os
from dotenv import load_dotenv
from prompt import DEFAULT_PROMPT
from query_openai_vision_functions import query_openai_vision

load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Visual AI Calorie Tracker")
st.write("Upload a food photo to get an instant nutritional estimate.")

uploaded_file = st.file_uploader(
    "Drag & drop or browse a food image",
    type=["jpg", "jpeg", "png", "webp", "bmp"],
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_container_width=True)

    with st.spinner("Analyzing..."):
        raw = query_openai_vision(openai_client, image, DEFAULT_PROMPT)

    try:
        data = json.loads(raw)
        st.subheader(data.get("food_name", "Food"))
        st.caption(f"Serving: {data.get('serving_description', '—')}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Calories", f"{data.get('calories', '—')} kcal")
        col2.metric("Fat", f"{data.get('fat_grams', '—')} g")
        col3.metric("Protein", f"{data.get('protein_grams', '—')} g")

        confidence = data.get("confidence_level", "—")
        color = {"High": "green", "Medium": "orange", "Low": "red"}.get(confidence, "gray")
        st.markdown(f"**Confidence:** :{color}[{confidence}]")
    except json.JSONDecodeError:
        st.error("Could not parse the model response.")
        st.code(raw)
