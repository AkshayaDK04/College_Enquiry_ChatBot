import json
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense
from tensorflow.keras.models import Model

class Chatbot:
    def __init__(self):
        # Load conversation data from JSON file
        with open('intents.json', 'r') as file:
            self.data = json.load(file)

        # Preprocess data
        self.words, self.labels, docs_x, docs_y = self.preprocess_data()

        # Tokenizer for words and patterns
        self.tokenizer = Tokenizer(num_words=len(self.words), oov_token='<OOV>')
        self.tokenizer.fit_on_texts(docs_x)
        
        sequences = self.tokenizer.texts_to_sequences(docs_x)
        self.max_len = max([len(seq) for seq in sequences])
        self.padded_sequences = pad_sequences(sequences, maxlen=self.max_len)

        # Convert labels to one-hot encoded labels
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(self.labels)
        self.labels_matrix = self.label_encoder.transform(docs_y)
        self.labels_matrix = np.eye(len(self.labels))[self.labels_matrix]

        self.num_classes = len(self.labels)

        # Define neural network model
        input_layer = Input(shape=(self.max_len,))
        embedding_layer = Embedding(input_dim=len(self.words), output_dim=128)(input_layer)
        lstm_layer = LSTM(128)(embedding_layer)
        dense_layer = Dense(64, activation='relu')(lstm_layer)
        output_layer = Dense(self.num_classes, activation='softmax')(dense_layer)

        self.model = Model(input_layer, output_layer)

        # Compile and train neural network model
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model.fit(self.padded_sequences, self.labels_matrix, epochs=100, batch_size=8, validation_split=0.2)

        # Save the trained weights to a file
        self.model.save_weights('chatbot_weights1.weights.h5')

    def preprocess_data(self):
        words = []
        labels = []
        docs_x = []
        docs_y = []

        for intent in self.data['intents']:
            for pattern in intent['patterns']:
                # Clean and tokenize each pattern
                word_list = self.clean_text(pattern)
                words.extend(word_list)
                docs_x.append(word_list)
                docs_y.append(intent['tag'])

            if intent['tag'] not in labels:
                labels.append(intent['tag'])

        # Convert words to lowercase and remove duplicates
        words = sorted(list(set(words)))

        return words, labels, docs_x, docs_y

    def clean_text(self, text):
        # Remove punctuation and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text.lower())
        return text.split()

    def load(self):
        self.model.load_weights('chatbot_weights1.weights.h5')

    def predict_intent(self, text):
        cleaned_text = self.clean_text(text)
        sequence = self.tokenizer.texts_to_sequences([cleaned_text])
        matrix = pad_sequences(sequence, maxlen=self.max_len)
        predicted_intent_matrix = self.model.predict(matrix)[0]
        top_n = 3
        top_indices = predicted_intent_matrix.argsort()[-top_n:][::-1]
        print("Top predicted intents with confidence:")
        for index in top_indices:
            intent_label = self.label_encoder.inverse_transform([index])[0]
            confidence = predicted_intent_matrix[index]
            print(f"Intent: {intent_label}, Confidence: {confidence}")
    
        predicted_intent_index = np.argmax(predicted_intent_matrix)
        predicted_intent_label = self.label_encoder.inverse_transform([predicted_intent_index])[0]
    
        confidence = predicted_intent_matrix[predicted_intent_index]
    
    # Threshold handling
        if confidence < 0.5:
            return None
    
        return predicted_intent_label


    def start_chatbot(self, user_input):
        predicted_intent = self.predict_intent(user_input)
        response = self.get_response(predicted_intent, self.data)
        return response

    def get_response(self, predicted_intent, data):
        for intent in data['intents']:
            if intent['tag'] == predicted_intent:
                return np.random.choice(intent['responses'])
        return "Sorry, I am unaware of ur query. If u can plz rephrase it!"

# Example usage:
# chatbot = Chatbot()
# response = chatbot.start_chatbot("What are the courses provided?")
# print(response)
