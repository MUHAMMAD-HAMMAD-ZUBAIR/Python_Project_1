 # Advanced Unit Converter using Streamlit

import streamlit as st
import requests
from streamlit_lottie import st_lottie

# Page setup
st.set_page_config(page_title="Smart Unit Converter", page_icon="🧮", layout="centered")

# Function to load Lottie animation from URL
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load working animation
lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_1pxqjqps.json")

# Display Lottie animation
if lottie_animation:
    st_lottie(lottie_animation, height=250, key="unit-convert")
else:
    st.warning("⚠️ Animation could not be loaded. Please check the URL.")

# App Header
st.markdown("<h1 style='text-align: center;'>🔁 Smart Unit Converter</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>✨ Convert Length, Weight & Time — Fast and Fun! ✨</p>", unsafe_allow_html=True)
st.divider()

# Category Selection
category = st.selectbox("📂 Choose a category to convert:", ["📏 Length", "⚖️ Weight", "⏰ Time"])

units = {
    "📏 Length": ["Kilometers ➡️ Miles", "Miles ➡️ Kilometers"],
    "⚖️ Weight": ["Kilograms ➡️ Pounds", "Pounds ➡️ Kilograms"],
    "⏰ Time": [
        "Seconds ➡️ Minutes", "Minutes ➡️ Seconds",
        "Minutes ➡️ Hours", "Hours ➡️ Minutes",
        "Hours ➡️ Days", "Days ➡️ Hours"
    ]
}

unit = st.selectbox("🔄 Select unit conversion:", units[category])
value = st.number_input("🔢 Enter the value to convert:", min_value=0.0, step=0.1)

# Conversion Function
def convert(category, unit, value):
    if category == "📏 Length":
        return value * 0.621371 if "Kilometers" in unit else value / 0.621371
    elif category == "⚖️ Weight":
        return value * 2.20462 if "Kilograms" in unit else value / 2.20462
    elif category == "⏰ Time":
        time_map = {
            "Seconds ➡️ Minutes": value / 60,
            "Minutes ➡️ Seconds": value * 60,
            "Minutes ➡️ Hours": value / 60,
            "Hours ➡️ Minutes": value * 60,
            "Hours ➡️ Days": value / 24,
            "Days ➡️ Hours": value * 24
        }
        return time_map.get(unit, None)
    return None

# Button to trigger conversion
if st.button("🎉 Convert Now"):
    if value <= 0:
        st.warning("⚠️ Please enter a value greater than 0.")
    else:
        result = convert(category, unit, value)
        if result is not None:
            st.balloons()
            st.success(f"🎯 {value} converted using {unit} is: **{result:.2f}** ✅")
            st.session_state.history.append(f"{category} - {unit}: {value} ➡️ {result:.2f}")
        else:
            st.error("❌ Conversion failed. Please check your input.")

# Conversion History Section
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("🔄 Conversion History")

# Display last 5 conversions
for record in st.session_state.history[-5:]:
    st.markdown(f"- {record}")

# Button to clear history
if st.button("🗑️ Clear History"):
    st.session_state.history.clear()
    st.success("History cleared!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 16px;'>"
    "Made with ❤️ by <b>MUHAMMAD HAMMAD ZUBAIR</b> 👨‍💻<br>"
    "Powered by <span style='color: #FF4B4B;'>Python</span> 🐍 & <span style='color: #4F8BF9;'>Streamlit</span> 🚀"
    "</div>",
    unsafe_allow_html=True
)

# Basic Unit Converter using Streamlit
# import streamlit as st
# # Title and intro (commented out, can be enabled)
# # st.title("🌍 Welcome to Unit Converter App")
# # st.markdown("### This app converts units of length, weight, and time instantly.")
# # st.write("Welcome! select a category to convert units.")

# # User selects category (Length, Weight, Time)
# category = st.selectbox("Select a category", ["Length", "Weight", "Time"])

# # Function to handle conversion logic
# def convert_units(category, value, unit):
#     # Length conversions
#     if category == "Length":
#         if unit == "kilometer to miles":
#             return value * 0.621371
#         elif unit == "miles to kilometer":
#             return value / 0.621371
#     # Weight conversions
#     elif category == "Weight":
#         if unit == "kilogram to pounds":
#             return value * 2.20462
#         elif unit == "pounds to kilogram":
#             return value / 2.20462
#     # Time conversions
#     elif category == "Time":
#         if unit == "seconds to minutes":
#             return value / 60
#         elif unit == "minutes to seconds":
#             return value * 60
#         elif unit == "minutes to hours":
#             return value / 60
#         elif unit == "hours to minutes":
#             return value * 60
#         elif unit == "hours to days":
#             return value / 24
#         elif unit == "days to hours":
#             return value * 24

# # Unit selection based on category
# if category == "Length":
#     unit = st.selectbox("Select a unit", ["miles to kilometer","kilometer to miles" ])
# elif category == "Weight":
#     unit = st.selectbox("Select a unit", ["kilogram to pounds", "pounds to kilogram"])
# elif category == "Time":
#     unit = st.selectbox("Select a unit", ["seconds to minutes", "minutes to seconds", "minutes to hours", "hours to minutes", "hours to days", "days to hours"])

# # User inputs the value to convert
# value = st.number_input("Enter the value to convert")

# # Convert button triggers the conversion
# if st.button("Convert"):
#     result = convert_units(category, value, unit)  # Call conversion function
#     st.success(f"The converted value is: {result:.2f}")  # Display result
