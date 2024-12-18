import csv
import re

from report_filter import report_dict_list as dic


def process_reports(dic: list):
    for report in dic:
        kognitionen = ''
        emotionen = ''
        motorik = ''
        physiologie = ''
        funktion = ''
        s_variabel = ''
        r_variabel = ''
        k_variabel = ''
        Sbsp = ''
        Rbsp = ''
        KCbsp = ''


        if '5' in report:
            section = report['5']
            if "Emotionen:" in section:
                words = section.split(' ')

                while words:
                    word = words.pop(0)
                    if word == "Emotionen:":
                        emotionen = word + ' '
                        break
                    kognitionen += word + ' '

                while words:
                    word = words.pop(0)
                    if word == "Motorik":
                        motorik = word + ' '
                        break
                    emotionen += word + ' '

                while words:
                    word = words.pop(0)
                    if word == "Physiologie:":
                        physiologie = word + ' '
                        break
                    motorik += word + ' '

                while words:
                    word = words.pop(0)
                    if word == "Funktion:":
                        funktion = word + ' '
                        break
                    physiologie += word + ' '

                while words:
                    word = words.pop(0)
                    if re.search(r'S:.?|\sS\s', word):
                        s_variabel += word + ' '
                        break
                    funktion += word + ' '

                while words:
                    word =words.pop(0)
                    if re.search(r'\bz\.b\.|\bz\.B\.', word, re.IGNORECASE):
                        Sbsp = word + ' '
                        break
                    s_variabel += word + ' '

                while words:
                    word = words.pop(0)
                    if re.search(r'\bR:.?|\sR\s', word):
                        r_variabel += word + ' '
                        break
                    Sbsp += word + ' '

                while words:
                    word = words.pop(0)
                    if re.search(r'\bz\.b\.|\bz\.B\.', word, re.IGNORECASE):
                        Rbsp = word + ' '
                        break
                    r_variabel += word + ' '

                while words:
                    word = words.pop(0)
                    if re.search(r'K/C:.?|\sK/C\s', word):
                        k_variabel += word + ' '
                        break
                    Rbsp += word + ' '

                while words:
                    word = words.pop(0)
                    if re.search(r'\bz\.b\.', word, re.IGNORECASE):
                        KCbsp = word + ' '
                        break
                    k_variabel += word + ' '

                while words:
                    for word in words:
                        word = words.pop(0)
                        KCbsp += word + ' '
        chiffre = report['0']
        diagnose = report['6']
        results = [chiffre ,diagnose, kognitionen, emotionen, motorik, physiologie, funktion, s_variabel, Sbsp, r_variabel, Rbsp, k_variabel, KCbsp]
        yield results


def sorkc_csv(result: list) -> dict:
    sorkc_dict = {}
    keys = ['Chiffre', 'Diagnose', 'Kognitionen', 'Emotionen', 'Motorik', 'Physiologie', 'Funktion', 'S', 'Sbsp', 'R', 'Rbsp', 'K/C' , 'KCbsp']

    for idx, each_result in enumerate(result[:13]):
        default_key = keys[idx]

        value = each_result.split(':', maxsplit=1)
        key = default_key
        sorkc_dict[key] = value[-1].strip()


    for expected_key in keys:
        if expected_key not in sorkc_dict:
            sorkc_dict[expected_key] = 'NaN'

    return sorkc_dict


with open('sorkc_2.csv', 'a') as f:
    csv_writer = csv.DictWriter(f, delimiter=',',
                                fieldnames=[ 'Chiffre', 'Diagnose', 'Kognitionen', 'Emotionen', 'Motorik',
                                             'Physiologie', 'Funktion', 'S','Sbsp', 'R', 'Rbsp', 'K/C', 'KCbsp'])
    csv_writer.writeheader()

    for result in process_reports(dic):
        data_dict = sorkc_csv(result)
        csv_writer.writerow(data_dict)

