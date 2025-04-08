import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Identity Survey", page_icon=":bar_chart:")

# --- CUSTOM CSS FOR A MATRIX-STYLE LOOK ---
# This helps reduce default padding/margins around each radio and question.
st.markdown("""
<style>
/* Remove extra spacing between blocks */
[data-testid="stBlock"] { margin: 0; padding: 0; }

/* Make radio buttons appear more “matrix-like” */
div[role="radiogroup"] {
    display: flex !important;
    gap: 20px !important;
    margin-top: -8px !important;
    margin-bottom: -8px !important;
}
</style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS SETUP ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google_sheets"]  # Make sure you have your credentials in Streamlit secrets
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("Survey Responses").sheet1  # ← Update with your actual sheet name if different

# --- DEMOGRAPHICS ---
st.title("Identity Survey")

st.markdown("### Demographics")
name = st.text_input("Your Name (Optional)")
age = st.number_input("Age", min_value=10, max_value=100, value=25)
country = st.text_input("Country of Residence", value="USA")

st.markdown("---")

# --- 7-POINT LIKERT SCALE ---
# Show numeric values (1–7), but we’ll add short text for clarity.
scale_options = [
    "1 (Strongly Disagree)",
    "2",
    "3",
    "4 (Neither)",
    "5",
    "6",
    "7 (Strongly Agree)"
]

# We’ll map each selected string to a numeric value:
scale_map = {
    "1 (Strongly Disagree)": 1,
    "2": 2,
    "3": 3,
    "4 (Neither)": 4,
    "5": 5,
    "6": 6,
    "7 (Strongly Agree)": 7
}

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

# We'll store the results in a dict
responses = {}

# Use a form so that everything is submitted at once
with st.form("survey_form"):
    st.markdown("### Please rate how much you agree or disagree with each statement:")
    
    # We'll present each question as a "row":
    for question in survey_questions:
        # Create one row with 2 columns:
        #   col[0] = question text
        #   col[1] = horizontal radio
        row = st.columns([3, 5])  # adjust proportions as needed
        
        with row[0]:
            st.write(question)
        
        with row[1]:
            choice_label = st.radio(
                label="",              # Hide label; we already printed question
                options=scale_options, # 7 options
                key=question,          # unique key
                horizontal=True        # show side-by-side
            )
            numeric_value = scale_map[choice_label]
            responses[question] = numeric_value
    
    # Submit button
    submitted = st.form_submit_button("Submit")

# --- HANDLE FORM SUBMISSION ---
if submitted:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build row data for Google Sheets:
    # [timestamp, name, age, country, Q1_value, Q2_value, ...]
    row_data = [timestamp, name, age, country]
    
    for q in survey_questions:
        row_data.append(responses[q])
    
    # Append new row in the sheet
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
