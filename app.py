from flask import Flask, render_template, request

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

    # Calorie calculation using Mifflin-St Jeor Equation
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_factor = {'low': 1.2, 'medium': 1.55, 'high': 1.725}
    calories = bmr * activity_factor.get(activity, 1.2)

    # Adjust based on goal
    if goal == 'weight_loss':
        calories -= 300
    elif goal == 'muscle_gain':
        calories += 300

    # Sample meal recommendations
    if preference.lower() == 'veg':
        meals = ['Oats with fruits', 'Paneer salad', 'Vegetable stir-fry with rice']
    elif preference.lower() == 'non-veg':
        meals = ['Boiled eggs and toast', 'Grilled chicken salad', 'Fish curry with rice']
    elif preference.lower() == 'vegan':
        meals = ['Smoothie bowl', 'Chickpea salad', 'Tofu stir-fry with quinoa']
    else:
        meals = ['Mixed fruit bowl', 'Dal and rice', 'Nut butter sandwich']

    return render_template('result.html', calories=int(calories), preference=preference, meals=meals)

if __name__ == '__main__':
    app.run(debug=True)