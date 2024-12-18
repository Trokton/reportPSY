""" Code to find similar reports to a given client
    - ICD10 diagnose reference
    - Report keywords reference
    - Report age reference
    - Report gender reference
    - Report diagnose reference
    Michael Roehrig
    11/2024
    """
import copy

import pandas as pd
import datetime
import re

import prepare_icd10


class MatchReport:
    def __init__(self, id, age, gender, keywords, diagnose):
        self.id = id
        self.keywords = keywords
        self.age = age
        self.gender = gender
        self.diagnose = diagnose


    def icd10_match(self, diagnose):
        icd10_definitions = []
        for code in diagnose:
            if code:
                icd10_definitions.append(prepare_icd10.icd10_data[code])
        return icd10_definitions

    def report_match(self):
        reports_keywords_df = pd.read_csv('keywords_output.csv', sep=';')
        match_set_diagnose_1 = set()
        match_set_diagnose_2 = set()
        match_set_age= set()
        match_set_gender = set()
        match_set_keywords_1 = set()
        match_set_keywords_2 = set()
        match_set_keywords_3 = set()
        match_set_keywords_5 = set()
        best_match_set = set()
        current_match_set = set()

        for report in reports_keywords_df.iterrows():
            diagnose_report = re.findall(r'F\d+\.?\d+?', report[1].iloc[5])
            if self.diagnose[0] in diagnose_report[0]:
                match_set_diagnose_1.add(report[0])
            try:
                if self.diagnose[1] in diagnose_report[1]:
                    match_set_diagnose_2.add(report[0])
            except IndexError:
                pass
            chiffre = re.search(r'[A-Z]\d{6}', report[1].iloc[0]).group(0)
            if abs(int(self.age) - int(chiffre[5:7])) > 10:
                continue
            else:
                match_set_age.add(report[0])
            if self.gender in report[1].iloc[7]:
                match_set_gender.add(report[0])
        keyword_matches = {}
        counter = 1
        for keyword in self.keywords:
            keyword = keyword.lower().strip()

            matching_section_1 = set(reports_keywords_df[reports_keywords_df['Keywords Section 1'].str.contains(keyword)].index)
            matching_section_2 = set(reports_keywords_df[reports_keywords_df['Keywords Section 2'].str.contains(keyword)].index)
            matching_section_3 = set(reports_keywords_df[reports_keywords_df['Keywords Section 3'].str.contains(keyword)].index)
            matching_section_5 = set(reports_keywords_df[reports_keywords_df['Keywords Section 5'].str.contains(keyword)].index)


            keyword_matches[f'{counter}set_1'] = matching_section_1
            keyword_matches[f'{counter}set_2'] = matching_section_2
            keyword_matches[f'{counter}set_3'] = matching_section_3
            keyword_matches[f'{counter}set_5'] = matching_section_5

            counter += 1

        for keyword in range(1, counter):
                match_set_keywords_1 = match_set_keywords_1.union(keyword_matches[f'{keyword}set_1'])
                match_set_keywords_2 = match_set_keywords_2.union(keyword_matches[f'{keyword}set_2'])
                match_set_keywords_3 = match_set_keywords_3.union(keyword_matches[f'{keyword}set_3'])
                match_set_keywords_5 = match_set_keywords_5.union(keyword_matches[f'{keyword}set_5'])

        priority_list = [match_set_age, match_set_keywords_1, match_set_diagnose_2,
                         match_set_keywords_2, match_set_keywords_3, match_set_keywords_5,
                         match_set_gender]
        best_match_set = best_match_set.union(match_set_diagnose_1)
        current_match_set = current_match_set.union(best_match_set)

        for match_set in priority_list:
            if len(best_match_set) > 3:
                best_match_set = best_match_set.intersection(match_set)
                if len(best_match_set) > 3:
                    current_match_set = current_match_set.intersection(match_set)
                elif len(best_match_set) < 3:
                    best_match_set = best_match_set.union(current_match_set)
                else:
                    break
        return best_match_set

    def match_filter(self, best_match_set):
        report_summaries_df = pd.read_csv('summaries_output.csv', sep=';')
        filter_set_keywords_1 = set()
        filter_set_keywords_2 = set()
        filter_set_keywords_3 = set()
        filter_set_keywords_5 = set()
        filter_matches ={}
        low_score_matches = set()
        average_score_matches = set()
        counter = 1

        for keyword in self.keywords:
            filter_section_1 = set(report_summaries_df[report_summaries_df
                ['Summary Section 1'].str.contains(keyword,case=False)].index)
            filter_section_2 = set(report_summaries_df[report_summaries_df
                ['Summary Section 2'].str.contains(keyword, case=False)].index)
            filter_section_3 = set(report_summaries_df[report_summaries_df
                ['Summary Section 3'].str.contains(keyword, case=False)].index)
            filter_section_5 = set(report_summaries_df[report_summaries_df
                ['Summary Section 5'].str.contains(keyword, case=False)].index)

            filter_matches[f'{counter}set_1'] = filter_section_1
            filter_matches[f'{counter}set_2'] = filter_section_2
            filter_matches[f'{counter}set_3'] = filter_section_3
            filter_matches[f'{counter}set_5'] = filter_section_5

            counter += 1
            matches_ranked = {}
            for index in best_match_set:
                matches_ranked[index] = 0

            for keyword in range(1, counter):

                filter_set_keywords_1 = filter_set_keywords_1.union(filter_matches[f'{keyword}set_1'])
                filter_set_keywords_2 = filter_set_keywords_2.union(filter_matches[f'{keyword}set_2'])
                filter_set_keywords_3 = filter_set_keywords_3.union(filter_matches[f'{keyword}set_3'])
                filter_set_keywords_5 = filter_set_keywords_5.union(filter_matches[f'{keyword}set_5'])

            for index in best_match_set:
                if index in filter_set_keywords_1:
                    matches_ranked[index] += 1
                if index in filter_set_keywords_2:
                    matches_ranked[index] += 1
                if index in filter_set_keywords_3:
                    matches_ranked[index] += 1
                if index in filter_set_keywords_5:
                    matches_ranked[index] += 1

        for index in matches_ranked.keys():
            if matches_ranked[index] < 1:
                try:
                    best_match_set.remove(index)
                except KeyError:
                    pass
            if matches_ranked[index] < 2:
                low_score_matches = copy.deepcopy(best_match_set)
                try:
                    best_match_set.remove(index)
                except KeyError:
                    pass
            if matches_ranked[index] < 3:
                average_score_matches = copy.deepcopy(best_match_set)
                try:
                    best_match_set.remove(index)
                except KeyError:
                    pass
            if len(best_match_set) >= 3:
                return best_match_set
            else:
                weaker_matches = list[average_score_matches] + list[low_score_matches]
                return  weaker_matches


# Create an instance using manual_input_client
# manual_input_client
id = input("Chiffre des Klienten: ")
if id == '': id = "R030176"

gender = input("Geschlecht des Klienten: ")
if gender == '': gender = "f"

diagnose_1 = input("Diagnose des Klienten: ")
diagnose_2 = input("2. Diagnose des Klienten: ")
diagnose = [d for d in [diagnose_1, diagnose_2] if d]
if not diagnose:
    diagnose = ['F32.1']

cues_input = input("Spezielle Hinweise :")
if cues_input == '': cues_input = "leben, weine, kraft, traurig"

keywords = cues_input.strip().split(',')
age = datetime.datetime.now().year - int(id[5:7]) - 1900

new_client = MatchReport(id, age, gender, keywords, diagnose)


# Call icd10_match on the instance
icd10_match = new_client.icd10_match(diagnose)
icd10_match = str(icd10_match)
match_final_result = list(new_client.match_filter(best_match_set=new_client.report_match()))

import google.generativeai as genai
import os



examples = ""
for i in match_final_result:
    df = pd.read_csv('processed_reports.csv', sep=';')
    file_to_write = (df.loc[i]).to_string()
    examples.join(file_to_write)

# Fetch the API key from an environment variable
def ai_response(self):

    api_key = os.environ.get("AI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (f"Schreibe einen Bericht für den Patienten: {id} mit der Diagnose: {diagnose},"
              f" der Patient ist {age} Jahre alt. Schreibe den Bericht in der Struktur nachfolgender Berichte"
              f"yu den Punkten: 1. Spontan berichtete Symptomatik, 2. Lebensgeschichtliche Entwicklung und "
              f"Krankheitsgenese, 3. Psychischer Befund, 5. Verhaltensanalzse nach SORCK, 6.Diagnose, 7. Therapieziel"
              f" 8. Behandlungsplan.  Formuliere mit fiktionalen Angaben einen schlüssigen Bericht. Siehe folgende"
              f"Beispiele und Diagnosekriterien: ")

    response = model.generate_content([prompt, icd10_match, examples])
    print(response)

