import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --------------------------
# PAGE CONFIGURATION
# --------------------------
st.set_page_config(page_title="Survey: Big Five", page_icon=":bar_chart:")

st.title("Survey: Big Five Personality Items")

# --------------------------
# SET UP GOOGLE SHEETS ACCESS
# --------------------------
# Define the scope for using the Google Sheets and Drive APIs
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from Streamlit secrets (stored securely in .streamlit/secrets.toml on Streamlit Cloud)
creds_dict = st.secrets["google_sheets"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
# Replace "Survey Responses" with your actual Google Sheet name.
sheet = client.open("Survey Responses").sheet1

# --------------------------
# DEMOGRAPHICS SECTION
# --------------------------
st.markdown("### Demographics")
age = st.number_input("Age", min_value=10, max_value=100, value=25)
country = st.text_input("Country of Residence", value="USA")

st.markdown("---")

# --------------------------
# SURVEY QUESTIONS (Big Five Items)
# --------------------------
st.markdown("### Please indicate your level of agreement for each statement:")

# Define the survey questions (each statement will be one row)
survey_questions = [
    "I love the United States.",
    "Being an American is an important part of my identity.",
    "It is important to me to contribute to the United States.",
    "It is important to me to view myself as an American.",
    "I am strongly committed to the United States.",
    "It is important to me that everyone sees me as an American.",
    "It is important for me to serve my country.",
    "When I talk about Americans I usually use 'we' rather than 'they'."
]

# Define the dropdown options:
# Options 1 and 7 include labels; the middle numbers are displayed as numbers only.
dropdown_options = [
    "1 (Strongly disagree)",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7 (Strongly agree)"
]

# Initialize a dictionary to store each response
responses = {}

# Build a form so all responses are submitted at once
with st.form("survey_form"):
    for question in survey_questions:
        # For each question, show the statement and a dropdown (selectbox).
        # The key ensures Streamlit can keep track of each element uniquely.
        responses[question] = st.selectbox(question, dropdown_options, key=question)
    
    submitted = st.form_submit_button("Submit Survey")

# --------------------------
# HANDLE FORM SUBMISSION
# --------------------------
if submitted:
    # Get the current timestamp (for record keeping)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build a row to send to Google Sheets:
    # Here we store: timestamp, demographics, then each survey response as a numeric value.
    row_data = [timestamp, age, country]
    
    # Convert the selected dropdown options to numeric values:
    for question in survey_questions:
        # We assume that the number is the first character in the string.
        # For example: "1 (Strongly disagree)" → 1, "7 (Strongly agree)" → 7.
        numeric_value = int(responses[question].split()[0])
        row_data.append(numeric_value)
    
    # Append the new row to the Google Sheet.
    sheet.append_row(row_data)
    
    st.success("Thank you! Your responses have been recorded.")
    st.balloons()

# --------------------------
# FOOTER WITH PROFESSIONAL REFERENCES
# --------------------------
st.markdown("---")
st.markdown("### **Gabriele Di Cicco, PhD in Social Psychology**")
st.markdown("""
[GitHub](https://github.com/gdc0000) | 
[ORCID](https://orcid.org/0000-0002-1439-5790) | 
[LinkedIn](https://www.linkedin.com/in/gabriele-di-cicco-124067b0/)
""")
