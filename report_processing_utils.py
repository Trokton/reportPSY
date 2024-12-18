import re
from report_filter import report_dict_list as dic


def process_reports(reports: list):
    for report in reports:
        kognitionen = ''
        emotionen = ''
        physiologie = ''
        funktion = ''
        s_variabel = ''
        r_variabel = ''
        k_variabel = ''
        if '5' in report:
            section = report['5']
            words = section.split(' ')

            while words:
                word = words.pop(0)
                if word == "Emotionen:":
                    emotionen = word + ' '
                    break
                kognitionen += word + ' '

            while words:
                word = words.pop(0)
                if word == "Physiologie:":
                    physiologie = word + ' '
                    break
                emotionen += word + ' '

            while words:
                word = words.pop(0)
                if word == "Funktion:":
                    funktion = word + ' '
                    break
                physiologie += word + ' '

            while words:
                word = words.pop(0)
                if re.search(r'^S:.?|\sS\s', word):
                    s_variabel += word + ' '
                    break
                funktion += word + ' '

            while words:
                word = words.pop(0)
                if re.search(r'^R:.?|\sR\s', word):
                    r_variabel += word + ' '
                    break
                s_variabel += word + ' '

            while words:
                word = words.pop(0)
                if re.search(r'^K/C:.?|\sK/C\s', word):
                    k_variabel += word + ' '
                    k_variabel += ' '.join(words) + ' '
                    break
                r_variabel += word + ' '

        results = [kognitionen.strip(), emotionen.strip(), physiologie.strip(),
                   funktion.strip(), s_variabel.strip(), r_variabel.strip(),
                   k_variabel.strip()]
        yield results


def sorkc_csv(result: list) -> dict:
    sorkc_dict = {}

    # Assuming the first four elements are 'key: value' format
    for entry in result[:4]:
        key, value = entry.split(':', maxsplit=1)
        sorkc_dict[key] = value.strip()

    # Assuming 'S:' and 'R:' entries follow a specific pattern that needs custom parsing
    for entry in result[4:6]:
        key = entry[0]  # Assuming the pattern is consistent
        value = entry[2:].strip()
        sorkc_dict[key] = value

    try:
        key, value = result[6].split(':', maxsplit=1)
        sorkc_dict[key] = value.strip()
    except ValueError:
        pass  # handle cases where split doesn't find a ':' character

    return sorkc_dict


# Running the processing steps
for result in process_reports(dic):
    data_dict = sorkc_csv(result)
    # You can proceed to use data_dict as needed