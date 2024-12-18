import glob
import os
import re
import csv

REPORTS_PATH = os.path.expanduser(r'reports')


class ReportProcessor:
    def __init__(self, path):
        self.path = path
        self.dict_list = []

    def find_files(self):
        """ Find text files in the specified directory. """
        for file in glob.glob(os.path.join(self.path, '*.txt')):
            yield file

    def create_reports_dict_list(self):
        """ Create a list of dictionaries from the report files. """
        for file in self.find_files():
            try:
                with open(file, "r", encoding="utf-8") as checking_file:
                    report_dict = self._make_report_dict(checking_file)  # give opened file to the function
                    yield report_dict  # -> _make_report_dict to create dictionary from file
            except IOError as e:
                print(f"Error opening/reading file: {file}.\nError: {e}")

    def _make_report_dict(self, checking_report):
        """ Create a dictionary from a report file. """
        report_dict = {}
        for line in checking_report:
            line = line.strip()

            # Replace multiple spaces with a single space
            line = re.sub(r'\s{2,}', ' ', line)
            line = re.sub(r'(mit|Mit) freundlichen Grü(ß|ss)en', '', line)
            line = re.sub(r'Dipl.Psych. C.*.* Dr.Andreas .*', '', line)
            line = re.sub(r'B.* Röh...', '', line)
            line = re.sub(r'1. Angaben zur spontan berichteten und erfragten Symptomatik:?', '', line)
            line = re.sub(r'2. Lebensgeschichtliche Entwicklung und Krankheitsanamnese:?', '', line)
            line = re.sub(r'3. Psychischer Befund zum Zeitpunkt der Antrag.?stellung:?', '', line)
            line = re.sub(r'4. Somatischer Befund:?', '', line)
            line = re.sub(r'5. Verhaltensanalyse:?', '', line)
            line = re.sub(r'6. Diagnose zum Zeitpunkt der Antrag.?stellung:?', '', line)
            line = re.sub(r'7. Therapieziele und Prognose:?', '', line)
            line = re.sub(r'8. Behandlungsplan:?', '', line)
            line = re.sub(r'\t', '', line)
            line = re.sub(r'\n', '', line)

            if line.startswith('6') and "ICD" in line:
                line = line[0:2] + ", ".join(re.findall(r'F\s?\d+\.?\d?', line))
                line = re.sub(r'\s?(F)\s+(\d+\.?\d+)', r'\1\2', line)

            if "Chiffre" in line:
                line = line[0:2] + "".join(re.findall(r'\b[A-Z].?\d{6}', line))
                line = re.sub(r'(\b[A-Z]).?(\d{6})', r'\1\2', line)

            if "Bochum"  in line:
                line = ''

            key_value = line.split(":", 1)  # split ':' (file has heading index for each paragraph)

            if len(key_value) < 2:  # if list has not 2 or more entries
                continue  # skip those lines
            else:
                key, value = key_value  # assigning list elements as key (line[0]) and values
                if value == ' ':
                    continue
                elif key == '9':
                    continue
                else:
                    value = value.strip()
                    report_dict.setdefault(key, []).append(value)  # dictionary: set key and append all values as a list

        return report_dict  # returns dictionary to create_reports_dict_list


    def process_reports(self):
        """ Perform all processing steps. """
        self.dict_list = list(self.create_reports_dict_list())
        if not self.dict_list:
            print("No files found.")

report_processor = ReportProcessor(REPORTS_PATH)
report_processor.process_reports()


for report in report_processor.dict_list:
    with open('processed_reports.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=report.keys())
        writer.writerow(report)