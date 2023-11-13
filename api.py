from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# File path for data persistence
DATA_FILE_PATH = 'event_data.json'


# Load existing data from the file
try:
    with open(DATA_FILE_PATH, 'r') as file:
        event_store = json.load(file)
except FileNotFoundError:
    event_store = []


# Endpoint to receive and persist events
@app.route('/events', methods=['POST'])
def receive_events():
    try:
        data = request.get_json()

        event_type = data.get('event_type')
        customer_id = data.get('customer_id')
        timestamp = data.get('timestamp') or datetime.utcnow().isoformat()

        # Save the event in a simple dictionary structure
        event = {
            'event_type': event_type,
            'customer_id': customer_id,
            'timestamp': timestamp,
            'data': data
        }

        event_store.append(event)

        # Write the updated data to the file
        with open(DATA_FILE_PATH, 'w') as filename:
            json.dump(event_store, filename, indent=2)

        return jsonify({'message': 'Event received and persisted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint to retrieve events for a specific customer
@app.route('/events/<int:customer_id>', methods=['GET'])
def get_customer_events(customer_id):
    try:
        # Optional: filter events by timestamp range if provided
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        filtered_events = [event for event in event_store if event['customer_id'] == customer_id]

        if start_time and end_time:
            filtered_events = [event for event in filtered_events if start_time <= event['timestamp'] <= end_time]

        return jsonify(filtered_events), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Minimal testing for the functionality
def test_integration():
    test_event = {
        'event_type': 'email_click',
        'customer_id': 123,
        'timestamp': '2023-10-23T14:30:00',
        'email_id': 1234,
        'clicked_link': 'https://example.com/some-link'
    }

    # Clear the event_store before running the test
    event_store.clear()

    # Test event receiving endpoint
    response = app.test_client().post('/events', json=test_event)
    assert response.status_code == 200

    # Test event retrieval endpoint without time range
    response = app.test_client().get('/events/123')
    assert response.status_code == 200

    actual_json = response.get_json()
    assert len(actual_json) == 1, f"Expected length 1, but got {len(actual_json)}. Response JSON: {actual_json}"

    # Test event retrieval endpoint with time range
    response_with_time_range = app.test_client().get('/events/123?start_time=2023-10-23T14:00:00&end_time=2023-10-23T15:00:00')
    assert response_with_time_range.status_code == 200

    actual_json_with_time_range = response_with_time_range.get_json()
    assert len(actual_json_with_time_range) == 1, f"Expected length 1, but got {len(actual_json_with_time_range)}. Response JSON: {actual_json_with_time_range}"

    print("Tests passed successfully.")


if __name__ == '__main__':
    # Run the minimal testing
    test_integration()

    # Run the Flask app
    app.run(debug=True)
