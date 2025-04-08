import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Set up the Streamlit page
st.set_page_config(page_title="Survey: Demographics & Big Five", page_icon=":bar_chart:")
st.title("Survey: Demographics & Big Five Personality Traits")
st.markdown("Please fill in the survey below. Your responses will be securely recorded.")

# --- CONNECT TO GOOGLE SHEETS ---
# Define the scope for Google Sheets and Google Drive API access
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from st.secrets (make sure you add your service account JSON in Streamlit secrets)
creds_dict = st.secrets["google_sheets"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open your Google Sheet by name; update the sheet name if necessary
sheet = client.open("Survey Responses").sheet1

# --- DEFINE SURVEY QUESTIONS ---
# Likert scale options for Big Five items
likert_scale = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]

# Define sample Big Five items (10 items, 2 per trait as an example)
big5_questions = {
    "q1": "I am the life of the party.",                      # Extraversion
    "q2": "I feel little concern for others.",                # Agreeableness (reversed)
    "q3": "I am always prepared.",                            # Conscientiousness
    "q4": "I get stressed out easily.",                       # Neuroticism
    "q5": "I have a rich vocabulary.",                        # Openness
    "q6": "I enjoy social gatherings.",                       # Extraversion
    "q7": "I make plans and stick to them.",                  # Conscientiousness
    "q8": "I am not interested in abstract ideas.",           # Openness (reversed)
    "q9": "I sympathize with others' feelings.",              # Agreeableness
    "q10": "I rarely feel anxious or depressed."             # Neuroticism (reversed)
}

# --- BUILD THE SURVEY FORM ---
with st.form("survey_form"):
    st.header("Basic Demographics")
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
    education = st.selectbox("Highest Education Level", 
                             ["High School", "Bachelor's Degree", "Master's Degree", "PhD/Doctorate", "Other"])
    country = st.text_input("Country", value="USA")
    
    st.header("Big Five Personality Traits")
    st.markdown("Please indicate how much you agree or disagree with each statement:")
    
    # Create a dictionary to hold responses for each Big Five item
    responses = {}
    for key, question in big5_questions.items():
        responses[key] = st.radio(question, likert_scale, key=key)
    
    # Submit button
    submitted = st.form_submit_button("Submit Survey")

# --- HANDLE FORM SUBMISSION ---
if submitted:
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare the data row: timestamp, demographics, then Big Five responses sorted by key
    row = [timestamp, age, gender, education, country]
    for key in sorted(big5_questions.keys()):
        row.append(responses[key])
    
    # Append the new row to the Google Sheet
    sheet.append_row(row)
    
    st.success("Thank you! Your survey responses have been recorded.")
