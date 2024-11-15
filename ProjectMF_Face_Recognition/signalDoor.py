from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app, resources={r"/signal": {"origins": "http://127.0.0.1:5500"}})

@app.route('/signal', methods=['POST'])
def handle_signal():
    data = request.form
    signal_value = data.get('signal')
    if signal_value == '0':
        # Perform any necessary database updates or other operations here
        return jsonify({'success': True, 'message': 'Signal received and processed successfully'})
    else:
        return jsonify({'success': False, 'message': 'Invalid signal value'})

if __name__ == '__main__':
    app.run(debug=True)