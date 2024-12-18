import csv
import re

path = 'reports.csv'

def csv_reader(path):
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:

            row[0] = re.sub(r'([A-Z])\s?(\d{6})', r'\1\2', row[0])
            row[0] = row[0][0:1] + "".join(re.findall(r'\b[A-Z]\s?\d{6}', row[0]))

            row[1] = re.sub(r'1. Angaben zur spontan berichteten und erfragten Symptomatik:?', '', row[1]).strip()
            row[2] = re.sub(r'2. Lebensgeschichtliche Entwicklung und Krankheitsanamnese:?', '', row[2]).strip()
            row[3] = re.sub(r'3. Psychischer Befund zum Zeitpunkt der Antrag.?stellung:?', '', row[3]).strip()
            row[4] = re.sub(r'4. Somatischer Befund:?', '', row[4]).strip()
            row[5] = re.sub(r'5. Verhaltensanalyse:?', '', row[5]).strip()
            row[6] = re.sub(r'6. Diagnose zum Zeitpunkt der Antrag.?stellung:?', '', row[6]).strip()
            row[7] = re.sub(r'7. Therapieziele und Prognose:?', '', row[7]).strip()
            row[8] = re.sub(r'8. Behandlungsplan:?', '', row[8]).strip()
            print(row[0], row[8])
            report_dict = {}
            for i in range(len(row)):
                report_dict[i] = row[i]


csv_reader(path)