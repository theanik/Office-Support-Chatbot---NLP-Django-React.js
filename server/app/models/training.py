from nn_model import model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os
from pathlib import Path
from utils.tokenizer import text_tokenizer
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data/processed')

traning_data = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'training_questions.csv'))

vectorizer = TfidfVectorizer(tokenizer=text_tokenizer)
tfidf_vectorizer = vectorizer.fit_transform(tuple(traning_data['question']))


label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(traning_data["label"])

model = model(tfidf_vectorizer, encoded_labels, label_encoder, 1000)

model.save(os.path.join(BASE_DIR, 'app/models/port_chat_model.h5'))

