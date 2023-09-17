import pandas as pd
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data/processed')
WITH_INDEX = False


def sanitize_traning_questions():
    trainingQuestionsDataFiles = [
        open(os.path.join(BASE_DIR, 'data/raw/hr/context.csv')),
        open(os.path.join(BASE_DIR, 'data/raw/about_bot/context.csv')),
        open(os.path.join(BASE_DIR, 'data/raw/project_setup/context.csv')),
        open(os.path.join(BASE_DIR, 'data/raw/greetings/context.csv')),
        open(os.path.join(BASE_DIR, 'data/raw/it_support/context.csv')),
    ]
    training_data = pd.concat(pd.read_csv(file_name, on_bad_lines='skip', skipinitialspace=True).dropna() for file_name in trainingQuestionsDataFiles)
    training_data.to_csv(os.path.join(PROCESSED_DATA_DIR, 'training_questions.csv'), index=WITH_INDEX)


def sanitize_answer():
    trainingQuestionsDataFiles = [
        open(os.path.join(BASE_DIR, 'data/raw/hr/answer.csv')),
        open(os.path.join(BASE_DIR, 'data/raw/about_bot/answer.csv')),
        open(os.path.join(BASE_DIR, 'data/raw/project_setup/answer.csv')),
        open(os.path.join(BASE_DIR, 'data/raw/it_support/answer.csv')),

    ]
    training_data = pd.concat(pd.read_csv(file_name, on_bad_lines='skip', skipinitialspace=True).dropna() for file_name in trainingQuestionsDataFiles)
    training_data.to_csv(os.path.join(PROCESSED_DATA_DIR, 'answer.csv'), index=WITH_INDEX)


def sanitize_labels():
    trainingQuestionsDataFiles = [
        open(os.path.join(BASE_DIR, 'data/raw/hr_label.csv')),
        open(os.path.join(BASE_DIR, 'data/raw/it_support_label.csv')),
        open(os.path.join(BASE_DIR, 'data/raw/project_setup_support_label.csv'))
    ]
    training_data = pd.concat(pd.read_csv(file_name, on_bad_lines='skip', skipinitialspace=True).dropna() for file_name in trainingQuestionsDataFiles)
    training_data.to_csv(os.path.join(PROCESSED_DATA_DIR, 'labels.csv'), index=WITH_INDEX)



#  greetings data sanitize
def sanitize_greetings_lable_data():
    df = pd.read_csv('data/raw/greetings/lable.csv', on_bad_lines='skip').dropna()
    df.to_csv(os.path.join(PROCESSED_DATA_DIR, 'greetings_lable.csv'), index=WITH_INDEX)

def sanitize_greetings_answer_data():
    df = pd.read_json('data/raw/greetings/greetings_answer.json')
    df.to_json(os.path.join(PROCESSED_DATA_DIR, 'greetings_answer.json'))



# run process action
sanitize_traning_questions()
sanitize_answer()

sanitize_greetings_answer_data()
sanitize_greetings_lable_data()

# sanitize_labels

print('process done!')