import re

import PyPDF2


class ICD10():
    """ class of diagnosis with ICD 10 code, definition"""

    def __init__(self, icd10_key, icd10_value, chapter, title):
        self.icd10_key = icd10_key
        self.icd10_value = icd10_value
        self.chapter = chapter
        self.title = title

    def get_icd10_data(self):

        icd10_data = {}

        file_path = ('icd10gm2025syst_referenz_20240913.pdf')

        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            page_list = []
            for page in reader.pages[160:210]:
                text = page.extract_text()
                page_list.append(text.splitlines())
        line_list = [item for sublist in page_list for item in sublist]

        for item in line_list:
            item = item.strip()
            item = re.sub(r'\d{3}ICD-10-GM Version 2025', '', item)
            if (
                    re.match(r'^\(?\s*F\d{2}', item)
                    and not item.endswith(').')
                    and not re.match(r'\(F\d{2}\..\)', item)):

                if re.match(r'\(F\d{2}-F\d{2}\)(?!\.)', item):
                    title = icd10_data[code][-1]
                    icd10_data[code].pop()
                    code = item.split(' ', 1)[0]
                    icd10_data[code] = [title, ]
                else:
                    code = item.split(' ', 1)[0]
                    try:
                        title = item.split(' ', 1)[1]
                    except:
                        title = ''

                    icd10_data[code] = [title, ]
            else:
                if not re.match(r'^\d{3}', item):
                    icd10_data[code].append(item)

        # manual correction

        icd10_data['(F90-F98)'] = "Verhaltens- und emotionale Störungen mit Beginn in der Kindheit und Jugend"
        icd10_data['F89'].pop()

        for key, value in icd10_data.items():
            value = '\n'.join(value)
            icd10_data[key] = value

        return icd10_data

    def get_and_process_icd10_data(self):
        icd10_data = self.get_icd10_data()

        chapters = {}
        for key, value in icd10_data.items():
            if re.match(r'F\d{2}.-', key):
                title = (value[:])
                chapter = key
                chapters[chapter] = title

        diagnoses = {k: v for k, v in icd10_data.items() if k not in chapters or chapters[k] != v}
        icd10_catalog = {}
        for key, value in diagnoses.items():
            for c_key, c_value in chapters.items():
                if len(key) == len(c_key) == 6 and key[:5] == c_key[:5]:
                    chapter = c_key
                    title = c_value
                    diagnoses[key] = ICD10(key, value, chapter, title)
                elif len(key) == len(c_key) == 5 and key[0:4] == c_key[0:4]:
                    chapter = c_key
                    title = c_value
                    diagnoses[key] = ICD10(key, value, chapter, title)
                elif len(key) == len(c_key) == 4 and key[0:3] == c_key[0:3]:
                    chapter = ''
                    title = ''
                    diagnoses[key] = ICD10(key, value, chapter, title)

            icd10_catalog[key] = ICD10(key, value, chapter, title)

        return icd10_catalog

    def __str__(self):
        return f"{self.chapter} {self.title} {self.icd10_key} {self.icd10_value}"

    # Main execution

def initialize_data():
    global icd10_data

# Create an instance of Diagnose
diagnose_instance = ICD10(None, None, None, None)
icd10_data = diagnose_instance.get_and_process_icd10_data()

initialize_data()
if __name__ == "__main__":
    print(icd10_data)