import matplotlib.pyplot as plt
import numpy as np

class AnalyticsDashboard:
    @staticmethod
    def generate_lifestyle_chart(water, sleep, workout_mins, screen_hours):
        categories = ['Water (L)', 'Sleep (hrs)', 'Workout (mins/10)', 'Screen (hrs)']
        user_vals = [water, sleep, workout_mins / 10.0, screen_hours]
        target_vals = [3.0, 8.0, 3.0, 3.0]
        
        x = np.arange(len(categories))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(x - width/2, user_vals, width, label='Your Stats', color='#4CAF50')
        ax.bar(x + width/2, target_vals, width, label='Ideal Target', color='#2196F3')
        
        ax.set_ylabel('Scores / Units')
        ax.set_title('Daily Lifestyle vs Target')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=15)
        ax.legend()
        plt.tight_layout()
        
        return fig
