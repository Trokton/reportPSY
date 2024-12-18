import re



def clean(line):
    line = re.sub(r'\t', '', line)
    line = re.sub(r'\n', '', line)
    line = re.sub(r'\s{2,}', ' ', line)
    if line[3:] == '':
        return None
    else:
        return line.strip()

def line_0(line):
    line = line[0:2] + "".join(re.findall(r'\b[A-Z].?\d{6}', line))
    line = re.sub(r'(\b[A-Z]).?(\d{6})', r'\1\2', line)
    return clean(line)

def line_1(line):
    line = re.sub(r'1. Angaben zur spontan berichteten und erfragten Symptomatik:?', '', line)
    return clean(line)

def line_2(line):
    line = re.sub(r'2. Lebensgeschichtliche Entwicklung und Krankheitsanamnese:?', '', line)
    return clean(line)

def line_3(line):
    line = re.sub(r'3. Psychischer Befund zum Zeitpunkt der Antrag.?stellung:?', '', line)
    return clean(line)

def line_4(line):
    line = re.sub(r'4. Somatischer Befund:?', '', line)
    return clean(line)

def line_5(line):
    line = re.sub(r'5. Verhaltensanalyse:?', '', line)
    line = re.sub (r'Physionolgie\s', 'Physiologie:', line )
    return clean(line)

def line_6(line):
    line = re.sub(r'6. Diagnose zum Zeitpunkt der Antrag.?stellung:?', '', line)
    line = line[0:2] + " ".join(re.findall(r'F\s?\d+\.?\d?', line))
    line = re.sub(r'\s?\d?(F)\s+(\d+\.?\d+)', r' \1\2', line)
    return clean(line)

def line_7(line):
    line = re.sub(r'7. Therapieziele und Prognose:?', '', line)
    return clean(line)

def line_8(line):
    line = re.sub(r'8. Behandlungsplan:?', '', line)
    line = re.sub(r'(mit|Mit) freundlichen Grü(ß|ss)en', '', line)
    line = re.sub(r'Dipl.Psych. C.*.* Dr.Andreas .*', '', line)
    line = re.sub(r'B.* Röh...', '', line)

    return clean(line)

def line_9(line):
    return clean(line)

def gender(line, gender):
    if gender == 'f':
        line = re.sub(r'ie Pat.', 'ie Patientin', line)
        line = re.sub(r'der Pat.', 'der Patientin', line)
    if gender == 'm':
        line = re.sub(r'er Pat.', 'er Patient', line)
        line = re.sub('den Pat.', 'den Patienten', line)
        line = re.sub('dem Pat.', 'dem Patienten', line)
        line = re.sub('des Pat.', 'des Patienten', line)
    else:
        line = line
    return line
def __str__(line):
    print(line)
    return line