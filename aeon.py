import tkinter as tk
from tkinter import messagebox
import random
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pickle

# --- Define the Context ---
class Context:
    def __init__(self, emotional_tone, user_intent, environment_state):
        self.emotional_tone = emotional_tone
        self.user_intent = user_intent
        self.environment_state = environment_state

    def __str__(self):
        return f"[Tone: {self.emotional_tone}, Intent: {self.user_intent}, Env: {self.environment_state}]"

# --- AI Model for Decision Making ---
class AIDecisionModel:
    def __init__(self):
        self.model = DecisionTreeClassifier()
        self.features = []
        self.labels = []
        self.label_map = {
            "happy_create": 0,
            "relaxed_explore": 1,
            "frustrated_collaborate": 2,
            "anxious_relax": 3,
            "confident_learn": 4,
            "curious_escape": 5,
        }
        self.response_map = {
            0: "Great energy! Let’s create something amazing!",
            1: "Take it easy. The world is your canvas. Explore freely.",
            2: "Let’s step back and recalibrate. Teamwork will get us there.",
            3: "Breathe deeply. Slow down. Relax and find your peace.",
            4: "You’ve got this! Knowledge is at your fingertips.",
            5: "Curiosity drives adventure. Let’s find a new world to discover.",
        }

    def train_model(self, features, labels):
        # Train the AI model
        self.model.fit(features, labels)

    def predict_response(self, context):
        # Convert context to features (numerical encoding)
        feature_vector = self.encode_features(context)
        prediction = self.model.predict([feature_vector])
        return self.response_map.get(prediction[0], "No response found.")

    def encode_features(self, context):
        # Convert the emotional tone and intent to numeric values
        tone_map = {"happy": 0, "sad": 1, "frustrated": 2, "confident": 3, "relaxed": 4, "curious": 5, "anxious": 6}
        intent_map = {"create": 0, "learn": 1, "explore": 2, "relax": 3, "collaborate": 4, "escape": 5}
        
        tone_value = tone_map.get(context.emotional_tone, 0)
        intent_value = intent_map.get(context.user_intent, 0)
        
        return [tone_value, intent_value]

    def save_model(self):
        # Save the trained model for future use
        with open('ai_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self):
        # Load the model from file
        try:
            with open('ai_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
        except FileNotFoundError:
            print("Model not found. Training from scratch.")
            self.model = DecisionTreeClassifier()

# --- GUI Main Class ---
class AEONApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ÆON: The Conscious Context Engine")
        self.root.geometry("500x500")
        
        # Load or create the AI model
        self.ai_model = AIDecisionModel()
        self.ai_model.load_model()

        # GUI Elements
        self.label = tk.Label(root, text="Welcome to ÆON. Enter your emotional state and intent.", font=("Helvetica", 12))
        self.label.pack(pady=20)

        # Emotional Tone Input
        self.emotional_tone_label = tk.Label(root, text="Enter Emotional Tone (e.g. happy, sad, frustrated, etc.):")
        self.emotional_tone_label.pack()
        self.emotional_tone_entry = tk.Entry(root)
        self.emotional_tone_entry.pack()

        # User Intent Input
        self.user_intent_label = tk.Label(root, text="Enter User Intent (e.g. create, learn, relax, etc.):")
        self.user_intent_label.pack()
        self.user_intent_entry = tk.Entry(root)
        self.user_intent_entry.pack()

        # Generate Response Button
        self.response_button = tk.Button(root, text="Generate Response", command=self.generate_response)
        self.response_button.pack(pady=10)

        # Response Display
        self.response_label = tk.Label(root, text="Response will appear here.", font=("Helvetica", 12), wraplength=350)
        self.response_label.pack(pady=20)

    def generate_response(self):
        # Get user input
        emotional_tone = self.emotional_tone_entry.get().lower()
        user_intent = self.user_intent_entry.get().lower()

        # Create context and make prediction using AI model
        context = Context(emotional_tone, user_intent, environment_state="neutral")
        response = self.ai_model.predict_response(context)
        
        # Display the response
        self.update_response(response)

    def update_response(self, message):
        # Update the response label with the generated message
        self.response_label.config(text=message)

    def train_model(self, features, labels):
        # Train the AI model with new data
        self.ai_model.train_model(features, labels)
        self.ai_model.save_model()

# --- Start the GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AEONApp(root)
    root.mainloop()
