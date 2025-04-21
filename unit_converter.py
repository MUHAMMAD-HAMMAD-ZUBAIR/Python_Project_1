# Advanced Unit Converter using Streamlit

import streamlit as st
import requests
from streamlit_lottie import st_lottie
from fpdf import FPDF

# 🚀 Page setup: Set the page configuration for Streamlit app
st.set_page_config(page_title="Smart Unit Converter", page_icon="🧮", layout="centered")

# ✅ Initialize session state for history if it doesn't already exist
if "history" not in st.session_state:
    st.session_state.history = []

# 🌐 Function to load Lottie animation from a URL
def load_lottie_url(url: str):
    # Send a GET request to the Lottie URL
    response = requests.get(url)
    if response.status_code != 200:
        return None  # Return None if the request fails
    return response.json()  # Return the JSON response of the Lottie animation

# Load the Lottie animation for the unit converter
lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_1pxqjqps.json")

# Display the Lottie animation if available
if lottie_animation:
    st_lottie(lottie_animation, height=250, key="unit-convert")
else:
    st.warning("⚠️ Animation could not be loaded. Please check the URL.")

# 🧮 App Header: Display the main header and subheader of the app
st.markdown("<h1 style='text-align: center;'>🔁 Smart Unit Converter</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>✨ Convert Length, Weight, Time, Temperature, Speed & More — Fast and Fun! ✨</p>", unsafe_allow_html=True)
st.divider()  # Divider line to separate sections

# 📂 Category Selection: Dropdown to choose the conversion category
category = st.selectbox("📦 Choose a category:", [
    "📏 Length", "⚖️ Weight", "⏰ Time", "💡 Energy", "💰 Currency", 
    "🌡️ Temperature", "🏃 Speed", "🧴 Volume"
])

# Conversion units for each category
units = {
    "📏 Length": ["Kilometers ➡️ Miles", "Miles ➡️ Kilometers"],
    "⚖️ Weight": ["Kilograms ➡️ Pounds", "Pounds ➡️ Kilograms"],
    "⏰ Time": [
        "Seconds ➡️ Minutes", "Minutes ➡️ Seconds",
        "Minutes ➡️ Hours", "Hours ➡️ Minutes",
        "Hours ➡️ Days", "Days ➡️ Hours"
    ],
    "💡 Energy": ["Joules ➡️ Kilojoules", "Kilojoules ➡️ Joules"],
    "💰 Currency": ["USD ➡️ EUR", "EUR ➡️ USD"],
    "🌡️ Temperature": ["Celsius ➡️ Fahrenheit", "Fahrenheit ➡️ Celsius"],
    "🏃 Speed": ["Kilometers per hour ➡️ Miles per hour", "Miles per hour ➡️ Kilometers per hour"],
    "🧴 Volume": ["Liters ➡️ Gallons", "Gallons ➡️ Liters"]
}

# Unit selection: Dropdown to choose the unit for conversion based on the selected category
unit = st.selectbox("🔄 Select conversion:", units[category])

# Input value: User input for the value to be converted
value = st.number_input("🔢 Enter value:", min_value=0.0, step=0.1)

# 🔧 Conversion logic: Function to handle conversion based on category, unit, and value
def convert(category, unit, value):
    if category == "📏 Length":
        return value * 0.621371 if "Kilometers" in unit else value / 0.621371
    elif category == "⚖️ Weight":
        return value * 2.20462 if "Kilograms" in unit else value / 2.20462
    elif category == "⏰ Time":
        conversions = {
            "Seconds ➡️ Minutes": value / 60,
            "Minutes ➡️ Seconds": value * 60,
            "Minutes ➡️ Hours": value / 60,
            "Hours ➡️ Minutes": value * 60,
            "Hours ➡️ Days": value / 24,
            "Days ➡️ Hours": value * 24
        }
        return conversions.get(unit, None)
    elif category == "💡 Energy":
        return value * 1000 if "Joules" in unit else value / 1000
    elif category == "💰 Currency":
        conversion_rates = {"USD ➡️ EUR": 0.85, "EUR ➡️ USD": 1.18}
        return value * conversion_rates.get(unit, 1)
    elif category == "🌡️ Temperature":
        if unit == "Celsius ➡️ Fahrenheit":
            return (value * 9/5) + 32
        elif unit == "Fahrenheit ➡️ Celsius":
            return (value - 32) * 5/9
    elif category == "🏃 Speed":
        if unit == "Kilometers per hour ➡️ Miles per hour":
            return value * 0.621371
        elif unit == "Miles per hour ➡️ Kilometers per hour":
            return value / 0.621371
    elif category == "🧴 Volume":
        if unit == "Liters ➡️ Gallons":
            return value * 0.264172
        elif unit == "Gallons ➡️ Liters":
            return value / 0.264172
    return None

# 📥 Convert Button: Trigger the conversion process when the button is clicked
if st.button("🎉 Convert Now"):
    if value <= 0:
        st.warning("⚠️ Please enter a value greater than 0.")  # Warn if input value is not valid
    else:
        result = convert(category, unit, value)  # Perform the conversion
        if result is not None:
            st.balloons()  # Trigger balloons animation for success
            st.success(f"🎯 {value} converted using {unit} is: **{result:.2f}** ✅")  # Display conversion result
            st.session_state.history.append(f"{category} - {unit}: {value} ➡️ {result:.2f}")  # Save to history

            # Function to remove emojis from the text (used for PDF export)
            def remove_emojis(text):
                return text.encode('ascii', 'ignore').decode('ascii')

            # PDF generation for conversion history
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt="Unit Conversion Result", ln=True, align='C')
            pdf.ln(10)

            history_records = st.session_state.history[-5:]  # Get the last 5 conversion history records
            for record in history_records:
                clean_record = remove_emojis(record)  # Clean text of emojis
                pdf.cell(200, 10, txt=f"History: {clean_record}", ln=True)

            pdf_output_path = "conversion_result.pdf"  # Save the PDF file
            pdf.output(pdf_output_path)

            # Provide the PDF file for download
            with open(pdf_output_path, "rb") as f:
                st.download_button(
                    label="📥 Download Result as PDF",  # Button to download PDF
                    data=f,
                    file_name="conversion_result.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("❌ Conversion failed. Please check your input.")  # Error if conversion fails

# 📚 Conversion History: Display the last 5 conversions made
st.subheader("📜 Conversion History")
for record in st.session_state.history[-5:]:
    st.markdown(f"- {record}")

# 🗑️ Clear History: Button to clear the conversion history
if st.button("🗑️ Clear History"):
    st.session_state.history.clear()  # Clear session history
    st.success("🧹 History cleared!")  # Display success message

# 👣 Footer: Add a footer with creator details and technology used
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 16px;'>"
    "Made with ❤️ by <b>MUHAMMAD HAMMAD ZUBAIR</b> 👨‍💻<br>"
    "Powered by <span style='color: #FF4B4B;'>Python</span> 🐍 & <span style='color: #4F8BF9;'>Streamlit</span> 🚀"
    "</div>",
    unsafe_allow_html=True
)


# #Basic Unit Converter using Streamlit
# import streamlit as st
# # Title and intro (commented out, can be enabled)
# st.title("🌍 Welcome to Unit Converter App")
# st.markdown("### This app converts units of length, weight, and time instantly.")
# st.write("Welcome! select a category to convert units.")

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
