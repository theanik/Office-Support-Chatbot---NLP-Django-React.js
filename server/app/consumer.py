import json
import os
import pandas as pd
from pathlib import Path
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from .models.utils.tokenizer import text_tokenizer
from .models.learnner import add_missed_question
from .models.text_similarity_metrics import get_prob_label
import numpy as np
import pandas as pd
import random


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None
        # load data
        traning_data = pd.read_csv(os.path.join(settings.PROCESSED_DATA_DIR, 'training_questions.csv'))
        self.answer_data = pd.read_csv(os.path.join(settings.PROCESSED_DATA_DIR, 'answer.csv'))
        self.answer_dict = dict(zip(self.answer_data["label"], self.answer_data["answer"]))
        self.config_data = pd.read_csv(os.path.join(settings.PROCESSED_DATA_DIR, 'config_data/config.csv'))

        greeting_label_data = pd.read_csv(os.path.join(settings.PROCESSED_DATA_DIR, 'greetings_lable.csv'))
        self.greeting_labels = greeting_label_data['label'].values.tolist()

        greeting_answer_data = pd.read_json(os.path.join(settings.PROCESSED_DATA_DIR, 'greetings_answer.json'))
        greeting_answers = {}
        for _, row in greeting_answer_data.iterrows():
            greeting_answers[row['label']] = row['answer']
        self.greeting_answers_dict = greeting_answers

        self.model = tf.keras.models.load_model(os.path.join(settings.BASE_DIR, 'app/models/port_chat_model.h5'))
        self.vectorizer = TfidfVectorizer(tokenizer=text_tokenizer)
        self.vectorizer.fit_transform(tuple(traning_data['question']))

        self.label_encoder = LabelEncoder()
        self.label_encoder.fit_transform(traning_data["label"])



    def connect(self):
        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = f"chat_{room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_info',
            'message': random.choice(self.greeting_answers_dict["welcome_message"])
        }))

    def receive(self, text_data=None, bytes_data=None):
        request_data = json.loads(text_data)
        message = request_data["message"]
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "chat_message", "message": message}
        )

    def chat_message(self, event):
        question = event["message"]
        quetion_vectorized = self.vectorizer.transform([question])

        predicted_label = self.model.predict(quetion_vectorized.toarray())
        predicted_label_index = np.argmax(predicted_label)
        predicted_label_name = self.label_encoder.classes_[predicted_label_index]

        print('Predicted label', predicted_label_name)
        print('Predicted label', predicted_label)
        threshold = 0.90
        binary_predictions = (predicted_label >= threshold).astype(int)
        reply_text = ''
        print('Predicted sum', binary_predictions.sum())
        not_understand = False
        if binary_predictions.sum():
            if predicted_label_name in self.greeting_answers_dict:
                reply_text = random.choice(self.greeting_answers_dict[predicted_label_name])
            else:
                reply_text = self.answer_dict[predicted_label_name]
        else:
            prob = get_prob_label(question)
            not_understand = True
            if prob['porb'] >= threshold:
                predicted_label_name = prob['label']
                reply_text = random.choice(self.greeting_answers_dict[predicted_label_name])
            else:
                
                add_missed_question(question)
                reply_text = random.choice(self.greeting_answers_dict["not_understand_reply"])

        for _, row in self.config_data.iterrows():
            reply_text = reply_text.replace(str(row['key']), str(row['value']))

        # Send message to WebSocket
        print(predicted_label_name)
        self.send(text_data=json.dumps({
            "message": reply_text,
            "label": predicted_label_name,
            "qcontext": question,
            "type": "system_message" if not_understand else "reply"
        }))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    
    # def simi_static_reply(text):


