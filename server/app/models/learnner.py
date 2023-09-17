import datetime
import pandas as pd
import os
import csv

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
def add_missed_question(text):
    file_name = os.path.join(BASE_DIR, 'data/raw/unknown/' + get_current_date_string() + '.csv')
    if not os.path.exists(file_name):
        create_csv_file(file_name)
    append_row_to_csv(file_name, text, '')

def create_csv_file(filename):
  df = pd.DataFrame(columns=['question', 'label'])
  df.to_csv(filename, index=False)

def append_row_to_csv(filename, question, label):
  df = pd.read_csv(open(filename))
  df.loc[len(df)] = [question, label]
  df.to_csv(filename, index=False)

def get_current_date_string():
    x = datetime.datetime.now()
    return x.strftime("%d-%m-%y")