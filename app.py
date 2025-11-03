from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import random

app = Flask(__name__)

# 1️⃣ Load trained AI model and clustered dataset
scaler = joblib.load("scaler.joblib")
kmeans = joblib.load("kmeans_model.joblib")
df = pd.read_csv("Indian_Food_Clustered.csv")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # 2️⃣ Get user input
    age = int(request.form['age'])
    gender = request.form['gender']
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    activity = request.form['activity']
    goal = request.form['goal']
    preference = request.form['preference']

    # 3️⃣ BMI calculation
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        bmi_status = "Underweight"
    elif 18.5 <= bmi < 25:
        bmi_status = "Normal weight"
    elif 25 <= bmi < 30:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    # 4️⃣ Calorie calculation (Mifflin–St Jeor)
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_factor = {'low': 1.2, 'medium': 1.55, 'high': 1.725}
    calories = bmr * activity_factor.get(activity, 1.2)

    # Adjust based on goal
    if goal == 'weight_loss':
        calories -= 300
        ai_goal = 'Weight Loss'
    elif goal == 'muscle_gain':
        calories += 300
        ai_goal = 'Muscle Gain'
    else:
        ai_goal = 'Maintain'

    # 5️⃣ Filter AI recommendations
    recommendations = df[df['Goal_Label'] == ai_goal]
    if preference.lower() == 'veg':
        recommendations = recommendations[~recommendations['Dish Name'].str.contains('chicken|fish|egg|mutton|meat|prawn', case=False)]
    elif preference.lower() == 'non-veg':
        recommendations = recommendations[recommendations['Dish Name'].str.contains('chicken|fish|egg|mutton|meat|prawn', case=False)]

    selected_meals = recommendations.sample(n=3, replace=False) if not recommendations.empty else pd.DataFrame()
    meals = selected_meals[['Dish Name', 'Calories (kcal)', 'Protein (g)', 'Carbohydrates (g)', 'Fats (g)']].to_dict(orient='records')

    return render_template(
        'result.html',
        calories=int(calories),
        preference=preference,
        goal=ai_goal,
        bmi=round(bmi, 1),
        bmi_status=bmi_status,
        meals=meals
    )

# 6️⃣ AJAX route for "Show More Options"
@app.route('/more_meals', methods=['POST'])
def more_meals():
    goal = request.form['goal']
    preference = request.form['preference']

    recommendations = df[df['Goal_Label'] == goal]
    if preference.lower() == 'veg':
        recommendations = recommendations[~recommendations['Dish Name'].str.contains('chicken|fish|egg|mutton|meat|prawn', case=False)]
    elif preference.lower() == 'non-veg':
        recommendations = recommendations[recommendations['Dish Name'].str.contains('chicken|fish|egg|mutton|meat|prawn', case=False)]

    more_meals = recommendations.sample(n=3, replace=False)[['Dish Name', 'Calories (kcal)', 'Protein (g)', 'Carbohydrates (g)', 'Fats (g)']].to_dict(orient='records')

    return jsonify(more_meals)

if __name__ == '__main__':
    app.run(debug=True)
