# neural net model v.
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy


def model(tfidf_vectorizer, encoded_labels, label_encoder, epochs_num):
    adam_optimizer = Adam(learning_rate=0.001)
    loss_entropy = SparseCategoricalCrossentropy(from_logits=True)

    model = Sequential([
            Dense(512, activation='relu', input_dim=tfidf_vectorizer.shape[1]),
            Dropout(0.5),
            Dense(128, activation='relu'),
            Dropout(0.3),
            Dense(len(label_encoder.classes_), activation='softmax')
        ])

    model.compile(loss=loss_entropy, optimizer=adam_optimizer, metrics=[SparseCategoricalAccuracy()])

    model.fit(tfidf_vectorizer.toarray(), encoded_labels, epochs=epochs_num, batch_size=32)
    return model