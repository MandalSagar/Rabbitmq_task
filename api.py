from flask import Flask, jsonify, request
from pymongo import MongoClient
import subprocess
import datetime

app = Flask(__name__)

# Database
client = MongoClient('localhost', 27017)
db = client['status_db']
collection = db['status_collection']

@app.route('/status', methods=['GET'])
def get_status_records():
    start_time_arg = request.args.get('start_time')
    end_time_arg = request.args.get('end_time')

    if not start_time_arg or not end_time_arg:
        return jsonify({'error': 'Both start_time and end_time parameters are required in the query string.'}), 400
    
    try:
        start_time = datetime.datetime.strptime(start_time_arg, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time_arg, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid datetime format. Use format YYYY-MM-DD HH:MM:SS.'}), 400
    
    # Query MongoDB for records between start_time and end_time
    query = {
        'timestamp': {
            '$gte': start_time,
            '$lte': end_time
        }
    }
    records = list(collection.find(query, {'_id': 0}))
    status_codes = [record['status_code'] for record in records]
    status_code_counts = Counter(status_codes)
    response = dict(status_code_counts)
    return jsonify(response)

if __name__ == '__main__':
    subprocess.Popen(['python', 'consumer.py'])
    app.run(debug=False, host='0.0.0.0', port=5010)


