import csv

from config.settings import DEFAULT_DATA_ROOT

# function to import questionaires and questionaire_answers
def import_questionaire_answers ():
    with open(
        DEFAULT_DATA_ROOT + '/sample_questionaires.csv',
        mode='r', 
        newline='', 
        encoding='utf-8'
    ) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
    for row in csv_reader:
        # Each 'row' is a dictionary
        print(row['question'])
        print(row['ans_sort_order'])



