from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import random

app = Flask(__name__)

# ---------------- LOAD MODEL & DATA ----------------
scaler = joblib.load("scaler.joblib")
kmeans = joblib.load("kmeans_model.joblib")
df = pd.read_csv("Indian_Food_Clustered.csv")


# ---------------- HOME PAGE ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- LOGIN PAGE (UI Only) ----------------
@app.route('/login')
def login_page():
    return render_template("login.html")


# ---------------- RECOMMENDATION ENGINE ----------------
@app.route('/recommend', methods=['POST'])
def recommend():
    age = int(request.form['age'])
    gender = request.form['gender']
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    activity = request.form['activity']
    goal = request.form['goal']
    preference = request.form['preference']

    # BMI
    bmi = round(weight / ((height / 100) ** 2), 2)

    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 24.9:
        bmi_status = "Normal"
    elif bmi < 29.9:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    # Calories (Mifflin-St Jeor)
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

    # Filter by goal
    recommendations = df[df['Goal_Label'] == ai_goal]

    # Filter by preference
    if preference.lower() == 'veg':
        recommendations = recommendations[
            ~recommendations['Dish Name'].str.contains('chicken|egg|fish|meat|mutton|prawn', case=False)
        ]
    elif preference.lower() == 'non-veg':
        recommendations = recommendations[
            recommendations['Dish Name'].str.contains('chicken|egg|fish|meat|mutton|prawn', case=False)
        ]

    # Select 3 meals
    selected = recommendations.sample(n=3, replace=False)
    meals = selected[['Dish Name', 'Calories (kcal)', 'Protein (g)',
                      'Carbohydrates (g)', 'Fats (g)']].to_dict(orient='records')

    return render_template(
        'result.html',
        calories=int(calories),
        bmi=bmi,
        bmi_status=bmi_status,
        preference=preference,
        goal=ai_goal,
        meals=meals
    )


# ---------------- SHOW MORE MEALS ----------------
@app.route('/more_meals', methods=['POST'])
def more_meals():
    goal = request.form['goal']
    preference = request.form['preference']

    recommendations = df[df['Goal_Label'] == goal]

    if preference.lower() == 'veg':
        recommendations = recommendations[
            ~recommendations['Dish Name'].str.contains('chicken|egg|fish|meat|mutton|prawn', case=False)
        ]
    elif preference.lower() == 'non-veg':
        recommendations = recommendations[
            recommendations['Dish Name'].str.contains('chicken|egg|fish|meat|mutton|prawn', case=False)
        ]

    # Pick 3 new meals
    more_meals = recommendations.sample(n=3, replace=False)
    more_meals = more_meals[['Dish Name', 'Calories (kcal)', 'Protein (g)',
                             'Carbohydrates (g)', 'Fats (g)']].to_dict(orient='records')

    return jsonify(more_meals)


# ---------------- OTHER STATIC PAGES ----------------
@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/tips')
def tips():
    return render_template("tips.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/explore', methods=["GET", "POST"])
def explore():
    foods = None
    if request.method == "POST":
        goal = request.form["goal"]
        foods = df[df["Goal_Label"] == goal]["Dish Name"].tolist()
    return render_template("explore.html", foods=foods)


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)
