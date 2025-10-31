from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    age = int(request.form['age'])
    gender = request.form['gender']
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    activity = request.form['activity']
    goal = request.form['goal']
    preference = request.form['preference']

    # --- Calorie Calculation (Mifflin-St Jeor Equation) ---
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_factor = {'low': 1.2, 'medium': 1.55, 'high': 1.725}
    calories = bmr * activity_factor.get(activity, 1.2)

    # --- Adjust Based on Goal ---
    if goal == 'weight_loss':
        calories -= 300
    elif goal == 'muscle_gain':
        calories += 300

    # --- BMI Calculation ---
    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 1)

    if bmi < 18.5:
        bmi_cat = "Underweight"
    elif 18.5 <= bmi < 25:
        bmi_cat = "Normal (Healthy)"
    elif 25 <= bmi < 30:
        bmi_cat = "Overweight"
    else:
        bmi_cat = "Obese"

    # --- Meal Recommendations ---
    if preference.lower() == 'veg':
        meals = ['Oats with fruits', 'Paneer salad', 'Vegetable stir-fry with rice']

    elif preference.lower() == 'non-veg':
        meals = ['Boiled eggs and toast', 'Grilled chicken salad', 'Fish curry with rice']

    elif preference.lower() == 'vegan':
        meals = ['Smoothie bowl', 'Chickpea salad', 'Tofu stir-fry with quinoa']

    elif 'mixed' in preference.lower():
        # Smart planned mix — veg & non-veg alternately
        mixed_meals = [
            ['Breakfast: Vegetable Oats with Milk 🥣', 'Lunch: Grilled Chicken with Brown Rice 🍗', 'Dinner: Paneer Tikka with Salad 🧀'],
            ['Breakfast: Boiled Eggs & Toast 🍳', 'Lunch: Dal Rice & Veggies 🥦', 'Dinner: Fish Curry with Roti 🐟'],
            ['Breakfast: Fruit Smoothie 🥤', 'Lunch: Chicken Salad 🐔', 'Dinner: Veg Pulao with Raita 🥗']
        ]
        meals = random.choice(mixed_meals)

    else:
        meals = ['Mixed fruit bowl', 'Dal and rice', 'Nut butter sandwich']

    # --- Render Result Page ---
    return render_template(
        'result.html',
        calories=int(calories),
        preference=preference,
        meals=meals,
        bmi=bmi,
        bmi_cat=bmi_cat
    )

if __name__ == '__main__':
    app.run(debug=True)
