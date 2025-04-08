import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# --------------------------
# PAGE CONFIGURATION
# --------------------------
st.set_page_config(page_title="Survey: Big Five Personality Items", page_icon=":bar_chart:")
st.title("Survey: Big Five Personality Items")

# --------------------------
# SET UP GOOGLE SHEETS ACCESS
# --------------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google_sheets"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
# Replace "Survey Responses" with your actual Google Sheet name.
sheet = client.open("Survey Responses").sheet1

# --------------------------
# DEFINE HEADER AND CHECK ITS PRESENCE
# --------------------------
# Create header list: static demographics info plus items from the personality scale.
personality_questions = [
    ("Extraversion", "I am the life of the party."),
    ("Extraversion", "I feel comfortable around people."),
    ("Agreeableness", "I am interested in other people's problems."),
    ("Agreeableness", "I sympathize with others' feelings."),
    ("Conscientiousness", "I am always prepared."),
    ("Conscientiousness", "I pay attention to details."),
    ("Neuroticism", "I get stressed out easily."),
    ("Neuroticism", "I worry about things."),
    ("Openness", "I have a vivid imagination."),
    ("Openness", "I have a rich vocabulary.")
]

header = (
    ["Timestamp", "Age", "Gender", "Country", "Education", "Employment", "Income", "Ethnicity"] +
    [f"{domain}: {question}" for domain, question in personality_questions]
)

# Check if the first row exists and if not, insert our header
first_row = sheet.row_values(1)
if not first_row or first_row[0] != "Timestamp":
    sheet.insert_row(header, index=1)

# --------------------------
# ENHANCED DEMOGRAPHICS SECTION
# --------------------------
st.markdown("### Demographics")
age = st.number_input("Age", min_value=10, max_value=100, value=25)
gender = st.radio(
    "Gender",
    options=["Male", "Female", "Other", "Prefer not to say"],
    index=0
)
country = st.text_input("Country of Residence", value="USA")
education = st.selectbox(
    "Highest Education Level",
    options=["High School", "Associate Degree", "Bachelor's Degree", "Master's Degree", "Doctorate", "Other"]
)
employment = st.selectbox(
    "Employment Status",
    options=["Employed Full-Time", "Employed Part-Time", "Self-Employed", "Student", "Unemployed", "Retired", "Other"]
)
income = st.selectbox(
    "Annual Income Range",
    options=["< $25,000", "$25,000 - $50,000", "$50,000 - $100,000", ">$100,000"]
)
ethnicity = st.selectbox(
    "Ethnicity",
    options=["Hispanic or Latino", "Not Hispanic or Latino", "Prefer not to say", "Other"]
)

st.markdown("---")

# --------------------------
# BIG FIVE PERSONALITY ITEMS
# --------------------------
st.markdown("### Please indicate your level of agreement for each statement:")

dropdown_options = [
    "1 (Strongly disagree)",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7 (Strongly agree)"
]

with st.form("survey_form"):
    responses = {}
    for domain, question in personality_questions:
        key_label = f"{domain}: {question}"
        responses[key_label] = st.selectbox(key_label, dropdown_options, key=question)
    
    submitted = st.form_submit_button("Submit Survey")

# --------------------------
# HANDLE FORM SUBMISSION AND DISPLAY RADAR DIAGRAM
# --------------------------
if submitted:
    # Current timestamp for record keeping
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build a row of data; make sure your sheet columns match this order.
    row_data = [timestamp, age, gender, country, education, employment, income, ethnicity]
    
    # Dictionaries to collect scores per domain
    domain_scores = {
        "Extraversion": [],
        "Agreeableness": [],
        "Conscientiousness": [],
        "Neuroticism": [],
        "Openness": []
    }
    
    # Convert dropdown selections to numbers and aggregate scores per domain
    for domain, question in personality_questions:
        key_label = f"{domain}: {question}"
        numeric_value = int(responses[key_label].split()[0])
        row_data.append(numeric_value)
        domain_scores[domain].append(numeric_value)
    
    # Append the new row to the Google Sheet
    sheet.append_row(row_data)
    
    st.success("Thank you! Your responses have been recorded.")
    st.balloons()
    
    # Compute average scores for each Big Five domain
    domains = ["Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism", "Openness"]
    averages = [sum(domain_scores[d]) / len(domain_scores[d]) for d in domains]
    
    # Prepare data for radar chart
    angles = np.linspace(0, 2 * np.pi, len(domains), endpoint=False).tolist()
    # Close the loop on the radar chart
    stats = averages + [averages[0]]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, stats, marker='o', linewidth=2)
    ax.fill(angles, stats, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), domains)
    ax.set_title("Your Big Five Personality Profile", y=1.08)
    ax.set_ylim(1, 7)  # Likert scale minimum and maximum
    
    st.pyplot(fig)

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
