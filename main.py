import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Identity Survey", page_icon=":bar_chart:")

# --- GOOGLE SHEETS SETUP ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google_sheets"]  # Make sure you have your credentials in Streamlit secrets
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Replace "Survey Responses" with your actual Google Sheet name.
sheet = client.open("Survey Responses").sheet1

# --- DEMOGRAPHIC QUESTIONS ---
st.title("Identity Survey")

st.markdown("### Demographics")
name = st.text_input("Your Name (Optional)")
age = st.number_input("Age", min_value=10, max_value=100, value=25)
country = st.text_input("Country of Residence", value="USA")

st.markdown("---")

# --- 7-POINT LIKERT OPTIONS ---
# We'll store the label → numeric mapping in a dict:
likert_map = {
    "Strongly Disagree": 1,
    "Somewhat Disagree": 2,
    "Slightly Disagree": 3,
    "Neither agree nor disagree": 4,
    "Slightly Agree": 5,
    "Somewhat Agree": 6,
    "Strongly Agree": 7
}

# We'll use the keys (text labels) for the radio display.
likert_options = list(likert_map.keys())

# --- SURVEY QUESTIONS ---
st.markdown("### Please rate how much you agree or disagree with each statement:")

survey_questions = [
    "I love the United States.",
    "Being an American is an important part of my identity.",
    "It is important to me to contribute to the United States.",
    "It is important to me to view myself as an American.",
    "I am strongly committed to the United States.",
    "It is important to me that everyone will see me as an American.",
    "It is important for me to serve my country.",
    "When I talk about Americans I usually use 'we' rather than 'they'."
]

responses = {}

# Create a form so all answers submit at once.
with st.form("survey_form"):
    for question in survey_questions:
        # Display each question with horizontal radio buttons
        user_choice = st.radio(
            question,
            options=likert_options,
            horizontal=True,
            key=question  # unique key
        )
        # Convert from label to numeric
        numeric_value = likert_map[user_choice]
        responses[question] = numeric_value

    submitted = st.form_submit_button("Submit")

# --- HANDLE FORM SUBMISSION ---
if submitted:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare row: [timestamp, name, age, country, q1_value, q2_value, ...]
    row_data = [timestamp, name, age, country]
    for q in survey_questions:
        row_data.append(responses[q])

    # Append to Google Sheet
    sheet.append_row(row_data)

    st.success("Thank you! Your responses have been recorded.")
    st.balloons()

# --- FOOTER ---
st.markdown("---")
st.markdown("### **Gabriele Di Cicco, PhD in Social Psychology**")
st.markdown("""
[GitHub](https://github.com/gdc0000) | 
[ORCID](https://orcid.org/0000-0002-1439-5790) | 
[LinkedIn](https://www.linkedin.com/in/gabriele-di-cicco-124067b0/)
""")
