from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Setup logging
logging.basicConfig(level=logging.INFO)

@app.route('/process', methods=['POST'])
def process_json():
    try:
        # Retrieve JSON data from the request
        data = request.get_json()
        logging.info(f"Received data: {data}")

        # Extract the list of data from the "data" key
        data_list = data.get('data', [])
        
        # Join the list to form a string to apply the same logic
        text = ''.join(data_list)

        # Get selected filters from the request data
        selected_filters = data.get('filters', [])

        # Initialize response data
        alphabets = [char for char in text if char.isalpha()]
        
        # Extract and concatenate consecutive numbers
        numbers = re.findall(r'\d+', text)
        numbers = [str(num) for num in numbers]  # Ensure all numbers are strings

        # Find the highest alphabet
        highest_alphabet = max(alphabets) if alphabets else None

        # Create the response based on selected filters
        response = {}

        if "alphabets" in selected_filters:
            response["alphabets"] = alphabets
        
        if "numbers" in selected_filters:
            response["numbers"] = numbers
        
        if "highest-alphabet" in selected_filters:
            response["highest-alphabet"] = highest_alphabet

        logging.info(f"Response to send: {response}")

        # Return the filtered response as JSON
        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
