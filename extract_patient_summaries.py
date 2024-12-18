import spacy
import subprocess
import re
import pandas as pd
import datetime
from concurrent.futures import ThreadPoolExecutor
from transformers import pipeline


# Function to install spaCy model
def install_model(model_name):
    subprocess.run(["python", "-m", "spacy", "download", model_name], check=True)


# Load the spaCy model
model_name = "de_core_news_lg"
nlp = spacy.load(model_name)

# Load summarization model from Hugging Face
summarizer = pipeline("summarization")


def preprocess_text(section):
    """
    Preprocess the input text: lowercasing, removing numbers and punctuation.
    """
    cleaned_text = section.lower()
    cleaned_text = re.sub(r'\b\d+\b', '', cleaned_text)  # Remove numbers
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # Remove punctuation
    return cleaned_text


def extract_summary(text, max_length=100, min_length=30):
    """
    Extract a short summary from the input text using the Hugging Face summarizer.
    """
    if len(text.strip()) == 0:
        return ""
    try:
        # Ensure the text length is within model's acceptable range
        text = text[:512]  # Truncate the text if too long for BART model
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except IndexError as e:
        # Handle the index error if the issue is with the input text length
        print(f"IndexError: {str(e)} - likely input text was too long.")
        return "IndexError in Summarization"
    except Exception as e:
        # General exception handling
        print(f"Unexpected error during summarization: {str(e)}")
        return "Error in Summarization"


def extract_report_data(report):
    """
    Extract relevant information from a single report.
    """
    try:
        chiffre = report.iloc[0].lstrip("['").rstrip("']")
    except Exception:
        chiffre = "Unknown"

    # Extract summaries using the summarizer for each section
    summary_section_1 = extract_summary(report.iloc[1] if pd.notna(report.iloc[1]) else "")
    summary_section_2 = extract_summary(report.iloc[2] if pd.notna(report.iloc[2]) else "")
    summary_section_3 = extract_summary(report.iloc[3] if pd.notna(report.iloc[3]) else "")
    summary_section_5 = extract_summary(report.iloc[5] if pd.notna(report.iloc[5]) else "")

    # Extract diagnose
    diagnose_text = report.iloc[6] if pd.notna(report.iloc[6]) else ""
    diagnose = re.findall(r'F\d+\.?\d+?', diagnose_text)
    diagnose = ", ".join(diagnose)

    # Calculate age
    try:
        year_part = int(chiffre[5:7])
        year_of_birth = 1900 + year_part if year_part > 30 else 2000 + year_part
        age = datetime.datetime.now().year - year_of_birth
    except ValueError:
        age = "Unknown"

    # Determine gender
    if "Die Pat" in report.iloc[1] or "Die Pat" in report.iloc[3]:
        gender = "f"
    elif "Der Pat" in report.iloc[1] or "Der Pat" in report.iloc[3]:
        gender = "m"
    else:
        gender = "d"

    return [
        chiffre,
        summary_section_1,
        summary_section_2,
        summary_section_3,
        summary_section_5,
        diagnose,
        age,
        gender
    ]


def main():
    # Load the report data
    reports_df = pd.read_csv('processed_reports.csv', sep=';')
    reports_df = reports_df.fillna('')  # Replace NaN with empty strings to avoid issues

    # Collect summaries from all reports using parallel processing
    all_summaries = []
    with ThreadPoolExecutor() as executor:
        all_summaries = list(executor.map(extract_report_data, [report for _, report in reports_df.iterrows()]))

    # Create a DataFrame to hold the results
    summaries_df = pd.DataFrame(all_summaries, columns=[
        'Chiffre',
        'Summary Section 1',
        'Summary Section 2',
        'Summary Section 3',
        'Summary Section 5',
        'Diagnose',
        'age',
        'gender'
    ])

    # Write the DataFrame to a new CSV file
    summaries_df.to_csv('summaries_output.csv', sep=';', index=False)


if __name__ == "__main__":
    main()