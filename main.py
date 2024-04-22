from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
import re

app = Flask(__name__)
CORS(app, resources={r"/chatbot": {"origins": "http://localhost:3300"}})

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hello! I am your career guidance bot. How can I assist you today?', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('I can help you explore career options, provide advice on job search, offer educational guidance, and more.', ['help', 'assistance', 'guide', 'support'], single_response=True)
    response('I can provide information about different career paths, required qualifications, and job prospects.', ['career', 'job', 'occupation'], required_words=['career'])
    response('Education is crucial for career success. Consider pursuing further education or certifications in your field of interest.', ['education', 'study', 'learn'], required_words=['education'])
    response('Networking is key to finding job opportunities. Attend industry events, join professional groups, and connect with professionals on LinkedIn.', ['networking', 'connect', 'linkedin'], required_words=['networking'])

    # Responses for education after 10th
    response('After completing 10th, you have several options such as pursuing 12th standard in a chosen stream (Science, Commerce, Arts), opting for a diploma course, or enrolling in vocational training programs.', ['10th', 'after 10th', 'options after 10th'], required_words=['10th'])
    # Responses for education after 12th
    response('After completing 12th, you can pursue higher education in various fields such as engineering, medicine, arts, commerce, science, management, law, etc. You can also consider diploma courses, vocational training, or skill development programs.', ['12th', 'after 12th', 'options after 12th'], required_words=['12th'])
    # Responses for education after engineering
    response('After completing engineering, you have several options such as pursuing higher studies (Masters, PhD), obtaining certifications in specialized fields, applying for jobs in your field of engineering, or exploring entrepreneurship opportunities.', ['engineering', 'after engineering', 'options after engineering'], required_words=['engineering'])

    # Responses for common phrases
    response('Okay.', ['okay', 'alright'], single_response=True)
    response('You\'re welcome!', ['thank', 'thanks', 'thankyou', 'thanks a lot'], single_response=True)

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return "I'm sorry, I didn't quite understand that. Can you please rephrase?" if highest_prob_list[best_match] < 1 else best_match

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Parse JSON data from the request
    data = request.get_json()

    # Get the user's message from the JSON data
    user_message = data.get('message')

    # Get the bot's response
    bot_response = get_response(user_message)

    # Return the bot's response as JSON
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
