import tkinter as tk
from tkinter import messagebox
import random

# --- Basic Classes for Context and Protocol ---
class Context:
    def __init__(self, emotional_tone, user_intent, environment_state):
        self.emotional_tone = emotional_tone
        self.user_intent = user_intent
        self.environment_state = environment_state

    def __str__(self):
        return f"[Tone: {self.emotional_tone}, Intent: {self.user_intent}, Env: {self.environment_state}]"

class Protocol:
    def __init__(self, name, trigger_condition, response_behavior):
        self.name = name
        self.trigger_condition = trigger_condition
        self.response_behavior = response_behavior
        self.reward_score = 0
        self.evolution_threshold = 3  # After this score, the protocol evolves
    
    def try_activate(self, context, user_feedback=None):
        if self.trigger_condition(context):
            response = self.response_behavior(context)
            if user_feedback is not None:
                self.update_reward(user_feedback)
            return response
        return None

    def update_reward(self, user_feedback):
        # Simple reward logic: positive feedback increases the reward, negative decreases it
        if user_feedback == "positive":
            self.reward_score += 1
        elif user_feedback == "negative":
            self.reward_score -= 1
        
        # Evolve protocol if the reward score exceeds the threshold
        if self.reward_score >= self.evolution_threshold:
            self.evolve_protocol()

    def evolve_protocol(self):
        # Simulated evolution: change the response or trigger condition
        self.reward_score = 0  # Reset reward score after evolution
        self.response_behavior = self.mutate_response(self.response_behavior)
        print(f"Protocol '{self.name}' has evolved!")

    def mutate_response(self, old_response):
        # Simulate "mutation" of the response behavior
        def new_response(ctx):
            base = old_response(ctx)
            if random.random() < 0.5:
                base["message"] = base["message"].replace("Let’s", "We could")
            base["emotion"] = random.choice(["soothing", "warm", "neutral"])
            return base
        return new_response


# --- Define Protocols ---
def happy_create_trigger(ctx):
    return ctx.emotional_tone == "happy" and ctx.user_intent == "create"

def relaxed_explore_trigger(ctx):
    return ctx.emotional_tone == "relaxed" and ctx.user_intent == "explore"

def frustrated_collaborate_trigger(ctx):
    return ctx.emotional_tone == "frustrated" and ctx.user_intent == "collaborate"

def anxious_relax_trigger(ctx):
    return ctx.emotional_tone == "anxious" and ctx.user_intent == "relax"

def confident_learn_trigger(ctx):
    return ctx.emotional_tone == "confident" and ctx.user_intent == "learn"

def curious_escape_trigger(ctx):
    return ctx.emotional_tone == "curious" and ctx.user_intent == "escape"

# --- Response Behaviors ---
def response_happy_creation(ctx):
    return {"message": "Great energy! Let’s create something amazing!", "emotion": "warm"}

def response_relaxed_exploration(ctx):
    return {"message": "Take it easy. The world is your canvas. Explore freely.", "emotion": "soothing"}

def response_frustrated_collaboration(ctx):
    return {"message": "Let’s step back and recalibrate. Teamwork will get us there.", "emotion": "neutral"}

def response_anxious_relaxation(ctx):
    return {"message": "Breathe deeply. Slow down. Relax and find your peace.", "emotion": "soothing"}

def response_confident_learning(ctx):
    return {"message": "You’ve got this! Knowledge is at your fingertips.", "emotion": "warm"}

def response_curious_escape(ctx):
    return {"message": "Curiosity drives adventure. Let’s find a new world to discover.", "emotion": "warm"}

# --- GUI Main Class ---
class AEONApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ÆON: The Conscious Context Engine")
        self.root.geometry("500x500")
        
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

        # Feedback Buttons
        self.feedback_label = tk.Label(root, text="Was this response helpful?", font=("Helvetica", 10))
        self.feedback_label.pack(pady=10)
        
        self.positive_feedback_button = tk.Button(root, text="Yes", command=lambda: self.submit_feedback("positive"))
        self.positive_feedback_button.pack(side="left", padx=10)
        
        self.negative_feedback_button = tk.Button(root, text="No", command=lambda: self.submit_feedback("negative"))
        self.negative_feedback_button.pack(side="left", padx=10)

        # Response Display
        self.response_label = tk.Label(root, text="Response will appear here.", font=("Helvetica", 12), wraplength=350)
        self.response_label.pack(pady=20)

        # Protocol for response
        self.protocols = [
            Protocol(name="HappyCreate", trigger_condition=happy_create_trigger, response_behavior=response_happy_creation),
            Protocol(name="RelaxedExplore", trigger_condition=relaxed_explore_trigger, response_behavior=response_relaxed_exploration),
            Protocol(name="FrustratedCollaborate", trigger_condition=frustrated_collaborate_trigger, response_behavior=response_frustrated_collaboration),
            Protocol(name="AnxiousRelax", trigger_condition=anxious_relax_trigger, response_behavior=response_anxious_relaxation),
            Protocol(name="ConfidentLearn", trigger_condition=confident_learn_trigger, response_behavior=response_confident_learning),
            Protocol(name="CuriousEscape", trigger_condition=curious_escape_trigger, response_behavior=response_curious_escape),
        ]

    def generate_response(self):
        # Get user input
        emotional_tone = self.emotional_tone_entry.get().lower()
        user_intent = self.user_intent_entry.get().lower()

        # Create a context with some environmental state
        context = Context(emotional_tone, user_intent, environment_state="neutral")

        # Process context and respond
        triggered = False
        for protocol in self.protocols:
            result = protocol.try_activate(context)
            if result:
                self.update_response(result["message"], result["emotion"])
                triggered = True
                break
        
        if not triggered:
            self.update_response("No immediate adaptation found. Learning...", "neutral")

    def submit_feedback(self, feedback):
        # Provide feedback to protocol
        for protocol in self.protocols:
            result = protocol.try_activate(
                Context(self.emotional_tone_entry.get().lower(), self.user_intent_entry.get().lower(), "neutral"),
                user_feedback=feedback
            )
        self.feedback_label.config(text=f"Feedback received: {feedback}")

    def update_response(self, message, emotion):
        # Update the response label with the generated message
        color_map = {
            "soothing": "#A4C6E1",  # light blue
            "warm": "#FFD700",      # warm yellow
            "neutral": "#D3D3D3",    # light gray
        }
        self.response_label.config(text=message, bg=color_map.get(emotion, "#D3D3D3"))

# --- Start the GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AEONApp(root)
    root.mainloop

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
            self.train_initial_model()

    def train_initial_model(self):
        # Initial training data (Features: [emotional_tone, user_intent])
        # Labels correspond to response types.
        # Each entry is a tuple (tone, intent) -> response
        features = [
            [0, 0],  # happy_create
            [4, 2],  # relaxed_explore
            [2, 4],  # frustrated_collaborate
            [6, 3],  # anxious_relax
            [3, 1],  # confident_learn
            [5, 5],  # curious_escape
        ]
        labels = [0, 1, 2, 3, 4, 5]  # Corresponding to response_map indices
        
        self.train_model(features, labels)
        self.save_model()
        print("Model trained and saved as ai_model.pkl.")

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

# --- Start the GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AEONApp(root)
    root.mainloop()
