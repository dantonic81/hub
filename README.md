# Integration Hub for Third-Party Events

This is a simple integration hub for working with third-party systems. It receives events via a web hook, persists them in a local file, and allows querying of stored data.

## Requirements

- Python (3.6 or higher)
- Flask (install with `pip install Flask`)

## Installation

1. Clone the repository:

       git clone https://github.com/your-username/integration-hub.git

2. Navigate to the project directory:

       cd integration-hub
   
3. Create and activate a virtual environment:

       python -m venv venv      # Create virtual environment
       source venv/bin/activate  # Activate virtual environment (use venv\Scripts\activate on Windows)

4. Install dependencies:

       pip install -r requirements.txt


## Usage

### Running the Server

    python api.py

The API will be available at http://127.0.0.1:5000/.

### Endpoints

- Receive and Persist Events:
  - Endpoint: /events (HTTP POST)
  - Example:

        curl -X POST -H "Content-Type: application/json" -d '{"customer_id": 123, "event_type": "email_open", "timestamp": "2023-10-24T11:30:00", "email_id": 998}' http://127.0.0.1:5000/events

- Retrieve Email Events for a Customer:
  - Endpoint: /events/<int:customer_id> (HTTP GET)
  - Example:

        # Retrieve all events for customer ID 123
        curl http://127.0.0.1:5000/events/123
  
        # Retrieve events for customer ID 123 within a specific time range
        curl http://127.0.0.1:5000/events/123?start_time=2023-10-24T11:00:00&end_time=2023-10-24T12:00:00


## Testing

Run the minimal testing script:

    python api.py

## Data Persistence

Events are persisted in a local file named event_data.json.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


Feel free to modify the content according to your project's specific details.

