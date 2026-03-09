from flask import Flask, render_template, request
from model import get_recommendations

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cuisine = request.form.get('cuisine', '').strip()
        if not cuisine:
            return render_template('index.html', error="Please enter a cuisine.")
        recs = get_recommendations(cuisine)
        if recs is None:
            return render_template('index.html', error=f"Sorry, '{cuisine}' is not available in our dataset.")
        return render_template('results.html', recs=recs.to_dict('records'), cuisine=cuisine)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)