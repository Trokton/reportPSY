import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd
import datetime


reports_df = pd.read_csv('processed_reports.csv', sep=';')


def find_top_keywords(section):
    keywords = []
    german_stopwords = set(stopwords.words('german'))

    custom_stopwords = {'evtl', 'zb', 'sei', 'seien','pat', 'ca', 'seit', 'könne', 'j', 'mehr', 'beim', 'o'}
    german_stopwords.update(custom_stopwords)

    # Text preprocessing
    cleaned_text = section.lower()
    cleaned_text = re.sub(r'\b\d+\b', '', cleaned_text)  # remove numbers
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # remove punctuation

    # Tokenization
    words = word_tokenize(cleaned_text, language='german')

    # Remove stopwords
    filtered_words = [word for word in words if word not in german_stopwords]

    # Find the most common words
    word_freq = Counter(filtered_words)
    most_common_keywords = word_freq.most_common(20)

    # Save the keywords in the dictionary
    for word, freq in most_common_keywords:
        keywords.append(word)

    return keywords

# Collect keywords
all_keywords = []

for report in reports_df.iterrows():
    chiffre = report[1].iloc[0].lstrip("['").rstrip("']")
    keywords_section_1 = find_top_keywords(report[1].iloc[1])
    keywords_section_2 = find_top_keywords(report[1].iloc[2])
    keywords_section_3 = find_top_keywords(report[1].iloc[3])
    keywords_section_5 = find_top_keywords(report[1].iloc[5])
    diagnose = report[1].iloc[6]
    diagnose = re.findall(r'F\d+\.?\d+?', diagnose)
    diagnose = ", ".join(diagnose)
    age = (datetime.datetime.now().year - 1900 - int(chiffre[5:7]))
    gender = ''

    if "Die Pat" in report[1].iloc[1] or "Die Pat" in report[1].iloc[3]:
        gender = "f"
    elif "Der Pat" in report[1].iloc[1] or "Der Pat" in report[1].iloc[3]:
        gender = "m"
    else:
        gender = "d"
    all_keywords.append([
        chiffre,
        ", ".join(keywords_section_1),
        ", ".join(keywords_section_2),
        ", ".join(keywords_section_3),
        ", ".join(keywords_section_5),
        diagnose,
        age,
        gender
    ])

# Create a DataFrame to hold the results
keywords_df = pd.DataFrame(all_keywords, columns=[
    'Chiffre',
    'Keywords Section 1',
    'Keywords Section 2',
    'Keywords Section 3',
    'Keywords Section 5',
    'Diagnose',
    'age',
    'gender'
])

# Write the DataFrame to a new CSV file
keywords_df.to_csv('keywords_output.csv', sep=';', index=False)
