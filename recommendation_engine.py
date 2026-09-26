import pandas as pd
import os

class RecommendationEngine:
    def __init__(self, food_path, exercise_path, clothing_path):
        self.food_path = food_path
        self.exercise_path = exercise_path
        self.clothing_path = clothing_path

    def calculate_bmi(self, weight_kg, height_cm):
        height_m = height_cm / 100.0
        if height_m <= 0:
            return 0, "Invalid Height"
        bmi = round(weight_kg / (height_m ** 2), 1)
        
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal Weight"
        elif 25.0 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obesity"
            
        return bmi, category

    def generate_recommendations(self, user_data):
        recs = []
        
        water = user_data.get('water_intake_l', 2.0)
        if water < 2.5:
            recs.append("💧 Water Intake: Aim for at least 2.5 - 3 Liters daily to stay hydrated.")
        else:
            recs.append("💧 Water Intake: Excellent hydration habits!")
            
        sleep = user_data.get('sleep_hours', 7.0)
        if sleep < 7.0:
            recs.append("😴 Sleep: Try to get 7-8 hours of sleep for proper recovery.")
        else:
            recs.append("😴 Sleep: Great sleep schedule!")
            
        screen = user_data.get('screen_hours', 4.0)
        if screen > 5.0:
            recs.append("👁️ Screen Time: Take regular 20-20-20 eye breaks to reduce strain.")
            
        return recs
