import tensorflow as tf
from pathlib import Path
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from models.utils.tokenizer import text_tokenizer
import numpy as np
import pandas as pd
import random
from models.learnner import add_missed_question


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data/processed')


traning_data = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'training_questions.csv'))
answer_data = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'answer.csv'))
answers = dict(zip(answer_data["label"], answer_data["answer"]))

#load label data
greeting_label = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'greetings_lable.csv'))
greeting_labels = greeting_label['label'].values.tolist()

greeting_answer = pd.read_json(os.path.join(PROCESSED_DATA_DIR, 'greetings_answer.json'))
greeting_answers = {}
for index, row in greeting_answer.iterrows():
    greeting_answers[row['label']] = row['answer']

model = tf.keras.models.load_model(os.path.join(BASE_DIR, 'app/models/port_chat_model.h5'))


vectorizer = TfidfVectorizer(tokenizer=text_tokenizer)
tfidf_vectorizer = vectorizer.fit_transform(tuple(traning_data['question']))

label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(traning_data["label"])


while True:
    quetion = input("-> ")

    if quetion == "quit" or quetion == "exit":
        print("Have a good day!")
        break

    quetion_vectorized = vectorizer.transform([quetion])

    predicted_label = model.predict(quetion_vectorized.toarray())
    predicted_label_index = np.argmax(predicted_label)
    predicted_label_name = label_encoder.classes_[predicted_label_index]

    threshold = 0.75
    binary_predictions = (predicted_label >= threshold).astype(int)
    
    if binary_predictions.sum():
        if predicted_label_name in greeting_labels:
            print(random.choice(greeting_answers[predicted_label_name]))
        else:
            print(answers[predicted_label_name])
    else:
        add_missed_question(quetion)
        print("Sorry I can't understnand")