import streamlit as st
import numpy as np
import joblib
import os
from PIL import Image
import base64

st.set_page_config(page_title="Crop Recommender", layout="wide")

# Function to set video background
def set_video_background(video_file):
    video_bytes = open(video_file, 'rb').read()
    video_base64 = base64.b64encode(video_bytes).decode('utf-8')
    video_html = f"""
        <style>
        .stApp {{
            position: relative;
            height: 100vh;
            overflow: hidden;
        }}
        #video-background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
        }}
        </style>
        <video autoplay muted loop id="video-background">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
    """
    st.markdown(video_html, unsafe_allow_html=True)

# Function to set background image on main page
def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(to bottom right, #6ec03f, #913FC0);
            background-attachment: fixed;
        }}
        
        </style>
        """,
        unsafe_allow_html=True
    )

# Session to store farmer name
if "farmer_name" not in st.session_state:
    st.session_state["farmer_name"] = ""

# Language selector
# Custom style for selectbox
st.markdown("""
    <style>
    .language-label {
        font-size: 28px;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 10px;
        display: block;
    }
    div[data-baseweb="select"] > div {
        font-size: 24px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Custom label manually
st.markdown('<label class="language-label">🌐 Select Language / भाषा चुनें</label>', unsafe_allow_html=True)

# Then hide the default label using label_visibility
language = st.selectbox("", ["English", "हिन्दी 🇮🇳"], label_visibility="collapsed")


# Set text based on selected language
if language == "English":
    welcome_text = "🌾 Welcome to Smart Agriculture Platform"
    name_prompt = "Please enter your name to continue"
    farmer_label = "👨‍🌾 Farmer Name"
    login_button = "Login"
    enter_details = "Enter the details below to get the best crop recommendation for your field."
    recommend_button = "Recommend Crop"
    recommended_crop_label = "🌾 Recommended Crop"
    image_not_found = "Image for the recommended crop not found."
    footer_text = "Developed with ❤️ for Smart Agriculture."
    labels = {
        "nitrogen": "🌱Nitrogen (N) level",
        "phosphorus": "🌾Phosphorus (P) level",
        "potassium": "🍃Potassium (K) level",
        "temperature": "🌡️Temperature (°C)",
        "humidity": "💧Humidity (%)",
        "ph": "⚖️Soil pH",
        "rainfall": "🌧️Rainfall (mm)"
    }
else:
    welcome_text = "🌾 स्मार्ट कृषि प्लेटफ़ॉर्म में आपका स्वागत है"
    name_prompt = "कृपया जारी रखने के लिए अपना नाम दर्ज करें"
    farmer_label = "👨‍🌾 किसान का नाम"
    login_button = "लॉग इन करें"
    enter_details = "अपने खेत के लिए सर्वोत्तम फसल सिफारिश प्राप्त करने के लिए नीचे विवरण भरें।"
    recommend_button = "फसल सिफारिश करें"
    recommended_crop_label = "🌾 सिफारिश की गई फसल"
    image_not_found = "अनुशंसित फसल की छवि नहीं मिली।"
    footer_text = "स्मार्ट कृषि के लिए ❤️ के साथ विकसित किया गया।"
    labels = {
        "nitrogen": "नाइट्रोजन (N) स्तर",
        "phosphorus": "फॉस्फोरस (P) स्तर",
        "potassium": "पोटेशियम (K) स्तर",
        "temperature": "तापमान (°C)",
        "humidity": "नमी (%)",
        "ph": "मिट्टी का pH",
        "rainfall": "वर्षा (मिमी)"
    }

# Login page
if st.session_state["farmer_name"] == "":
    set_video_background("login_bg.mp4")  # Ensure the video file exists in this folder

    st.markdown(f"<h1 style='text-align: center; font-size: 40px; color: white;'>{welcome_text}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; font-size: 28px; color: white;'>{name_prompt}</h3>", unsafe_allow_html=True)

    st.markdown(f"<label style='font-size:26px; color: white;'>{farmer_label}</label>", unsafe_allow_html=True)
    name = st.text_input("", "", label_visibility="collapsed")

    if st.button(login_button):
        if name.strip():
            st.session_state["farmer_name"] = name.strip()
            st.experimental_rerun()
        else:
            st.warning("Please enter your name.")

# Main app after login
else:
    set_background("background.jpg")  # Optional: background image for main app

    st.sidebar.success(f"Welcome, {st.session_state['farmer_name']} 👋")

    model = joblib.load("crop_recommendation_model.pkl")
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Add a logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state["farmer_name"] = ""  # Clear session state
        st.experimental_rerun()  # Redirect to login page

    st.markdown(
        f"""
        <div style='background-color: rgba(0, 0, 0, 0.7); padding: 8px; border-radius: 12px;'>
            <h1 style='color: #2e7d32; text-align: center; font-size: 48px;'>🌱 Crop Recommendation System</h1>
            <p style='color: #FFFFFF; text-align: center; font-size: 26px; font-weight: 500;'>
                {enter_details}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<label style='font-size:24px;color:black;font-weight: bold;'>{labels['nitrogen']}</label>", unsafe_allow_html=True)
        nitrogen = st.number_input("", min_value=0.0, max_value=100.0, step=0.1, label_visibility="collapsed", key="nitrogen")

        st.markdown(f"<label style='font-size:24px;color:black;font-weight: bold;'>{labels['phosphorus']}</label>", unsafe_allow_html=True)
        phosphorus = st.number_input("", min_value=0.0, max_value=100.0, step=0.1, label_visibility="collapsed", key="phosphorus")

        st.markdown(f"<label style='font-size:24px;color:black;font-weight: bold;'>{labels['potassium']}</label>", unsafe_allow_html=True)
        potassium = st.number_input("", min_value=0.0, max_value=100.0, step=0.1, label_visibility="collapsed", key="potassium")

    with col2:
        st.markdown(f"<label style='font-size:24px;color:black;font-weight: bold;'>{labels['temperature']}</label>", unsafe_allow_html=True)
        temperature = st.number_input("", min_value=-10.0, max_value=50.0, step=0.1, label_visibility="collapsed", key="temperature")

        st.markdown(f"<label style='font-size:24px;color:black;font-weight: bold;'>{labels['humidity']}</label>", unsafe_allow_html=True)
        humidity = st.number_input("", min_value=0.0, max_value=500.0, step=0.1, label_visibility="collapsed", key="humidity")

        st.markdown(f"<label style='font-size:24px;color:black;font-weight: bold;'>{labels['ph']}</label>", unsafe_allow_html=True)
        ph = st.number_input("", min_value=0.0, max_value=20.0, step=0.1, label_visibility="collapsed", key="ph")

        st.markdown(f"<label style='font-size:24px;color:black;font-weight: bold;'>{labels['rainfall']}</label>", unsafe_allow_html=True)
        rainfall = st.number_input("", min_value=0.0, max_value=2000.0, step=0.1, label_visibility="collapsed", key="rainfall")
    st.markdown("""
    <style>
    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }
    .stButton button {
        background-color: #2e7d32;
        color: white;
        border: none;
        padding: 14px 32px;
        font-size: 22px;
        border-radius: 10px;
        box-shadow: 0 0 10px #2e7d32, 0 0 20px #2e7d32;
        transition: 0.3s ease-in-out;
    }
    .stButton button:hover {
        background-color: #4caf50;
        box-shadow: 0 0 15px #4caf50, 0 0 30px #4caf50;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Center the button
    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    recommend = st.button(recommend_button)
    st.markdown('</div>', unsafe_allow_html=True)

    if recommend:
     if all([nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]):
        user_input = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        predicted_crop = model.predict(user_input)[0]
        st.markdown(f"""
    <div style='text-align: center; margin-top: 30px;'>
        <h2 style='color: #2e7d32; font-size: 36px; font-weight: bold;'>
            {recommended_crop_label}: <span style='color: #000; font-size: 38px;'>{predicted_crop.capitalize()}</span>
        </h2>
    </div>
""", unsafe_allow_html=True)

        # Display crop image if available
        image_path = os.path.join("crop_images", f"{predicted_crop}.jpg")
        if os.path.exists(image_path):
            image = Image.open(image_path)
            st.markdown(f"""
        <div style='text-align: center; margin-top: 20px;'>
            <img src='data:image/jpeg;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}' width='300'/>
            <p style='font-size: 20px; color: #333; font-weight: bold;'>{predicted_crop.capitalize()} Field</p>
        </div>
    """, unsafe_allow_html=True)
        else:
            st.warning(image_not_found)
    else:
        st.warning("Please fill in all the input fields before proceeding.")


    st.markdown("---")
    st.markdown(f"<p style='font-size:20px;'>{footer_text}</p>", unsafe_allow_html=True)
