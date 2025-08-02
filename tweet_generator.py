from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

class SimpleTweetGenerator:
    def __init__(self):
        self.positive_templates = [
            "{company} is making waves in {industry}! 🚀 {message}",
            "Big news from {company} today in {industry}: {message}"
        ]
        self.negative_templates = [
            "Rough patch for {company} in {industry} sector. {message} 😟",
            "{company} is facing criticism in the {industry} space. {message}"
        ]
        self.neutral_templates = [
            "{company} shares updates on {industry}. {message}",
            "Steady progress from {company} in {industry}. {message}"
        ]

    def generate_smart_tweet(self, company, industry, word_count, sentiment_target, has_media, message):
        if sentiment_target > 0.5:
            templates = self.positive_templates
        elif sentiment_target < -0.5:
            templates = self.negative_templates
        else:
            templates = self.neutral_templates

        base_tweet = random.choice(templates).format(company=company, industry=industry, message=message)
        tweet = " ".join(base_tweet.split())

        if has_media:
            tweet += " 📸"

        return tweet[:280]

# Instantiate your class
tweet_generator = SimpleTweetGenerator()

@app.route('/generate_smart_tweet', methods=['POST'])
def generate_tweet():
    try:
        data = request.get_json()
        company = data.get("company")
        industry = data.get("industry")
        word_count = int(data.get("word_count", 20))
        sentiment_target = float(data.get("sentiment_target", 0))
        has_media = data.get("has_media", False)
        message = data.get("message", "")

        tweet = tweet_generator.generate_smart_tweet(
            company, industry, word_count, sentiment_target, has_media, message
        )

        return jsonify({"tweet": tweet})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


le_company = joblib.load('company_encoder.pkl')



model = joblib.load('like_predictor.pkl')


@app.route('/predict_likes', methods=['POST'])

def predict():
    data = request.get_json()
    features = np.array([
        data['word_count'],
        data['char_count'],
        data['has_media'],
        data['hour'],
        data['sentiment'],
        data['company_encoded'],
        
        data['day_of_week'],
    ]).reshape(1, -1)

    prediction_log = model.predict(features)[0]
    prediction = round(np.expm1(prediction_log))
    return jsonify({'predicted_likes': int(prediction)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

