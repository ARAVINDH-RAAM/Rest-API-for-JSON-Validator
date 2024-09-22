from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_cors import CORS
import logging
import re

app = Flask(__name__)
CORS(app)  

logging.basicConfig(level=logging.INFO)
@app.route('/')
def welcome():
    return render_template(index.html)
    
@app.route('/process', methods=['POST'])
def process_json():
    try:
        data = request.get_json()
        logging.info(f"Received data: {data}")

        data_list = data.get('data', [])
        
        text = ''.join(data_list)

        selected_filters = data.get('filters', [])

        alphabets = [char for char in text if char.isalpha()]
        
        numbers = re.findall(r'\d+', text)
        numbers = [str(num) for num in numbers] 

        highest_alphabet = max(alphabets) if alphabets else None

        response = {}

        if "alphabets" in selected_filters:
            response["alphabets"] = alphabets
        
        if "numbers" in selected_filters:
            response["numbers"] = numbers
        
        if "highest-alphabet" in selected_filters:
            response["highest-alphabet"] = highest_alphabet

        logging.info(f"Response to send: {response}")

        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
