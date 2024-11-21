import random
import spacy
import json

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Load the intents JSON file
with open('intents.json') as file:
    intents = json.load(file)["intents"]

def nlp_match_intent(query):
    query_doc = nlp(query.lower())
    best_match = None
    best_score = 0.0

    # Iterate through all intents and patterns
    for intent in intents:
        for pattern in intent["patterns"]:
            pattern_doc = nlp(pattern.lower())
            similarity = query_doc.similarity(pattern_doc)
            
            # Find the highest similarity score
            if similarity > best_score:
                best_score = similarity
                best_match = intent
    
    # Set a similarity threshold to ensure only good matches are returned
    if best_score > 0.5:  # You can adjust this threshold based on your needs
        return random.choice(best_match["responses"])
    
    # If no good match is found, return None
    return None
