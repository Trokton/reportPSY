import csv
import glob
import os
import json

import reliner

REPORTS_PATH = os.path.expanduser(r'resources')

class ReportProcessor:
    def __init__(self, path: str):
        self.path = path
        self.dict_list = []

    def find_files(self):
        """ Find text files in the specified directory. """
        return glob.glob(os.path.join(self.path, '*.txt'))

    def line_generator(self, file: str):
        with open(file, "r", encoding="utf-8") as checking_file:
            for line in checking_file:
                gender =''
                line = line.strip()
                if "Die Pat." in line:
                   gender = 'f'
                elif "Der Pat." in line:
                    gender = 'm'
                else:
                    gender = 'd'
                match line:
                    case _ if line.startswith('0'):
                        line = reliner.line_0(line)
                    case _ if line.startswith('1'):
                        line = reliner.line_1(line)
                    case _ if line.startswith('2'):
                        line = reliner.line_2(line)
                    case _ if line.startswith('3'):
                        line = reliner.line_3(line)
                    case _ if line.startswith('4'):
                        line = reliner.line_4(line)
                    case _ if line.startswith('5'):
                        line = reliner.line_5(line)
                    case _ if line.startswith('6'):
                        line = reliner.line_6(line)
                    case _ if line.startswith('7'):
                        line = reliner.line_7(line)
                    case _ if line.startswith('8'):
                        line = reliner.line_8(line)
                    case _ if line.startswith('9'):
                        line = reliner.line_9(line)
                    case _:
                        continue
                line = reliner.gender(line, gender)
                if line:
                    yield line

    def report_maker(self, report_lines:list)->dict:
        report_dict = {}
        for line in report_lines:
            if ':' in line:
                key, line = line.split(':', maxsplit=1)
                if key in report_dict:
                    report_dict[key] += ', ' + line
                else:
                    report_dict[key] = line
        report_dict = {key: report_dict[key] for key in sorted(report_dict)}
        return report_dict


    def csv_maker(self, report_dict:dict):
        with open('reports.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=report_dict.keys())
            writer.writerow(report_dict)

    def pretty_print_dict(self, d: dict):
        print(json.dumps(d, indent=4, ensure_ascii=False))

def initialize_data():
    global report_dict_list

report_dict_list = []
finder = ReportProcessor(REPORTS_PATH)
for file in finder.find_files():
    report_lines = []
    for line in finder.line_generator(file):
        report_lines.append(line)

    report_dict = finder.report_maker(report_lines)
    report_dict_list.append(report_dict)


initialize_data()





