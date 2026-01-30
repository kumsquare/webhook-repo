# Dev Assessment - Webhook Receiver

Please use this repository for constructing the Flask webhook receiver.

*******************

## Setup

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

You need to use this as the base and setup the flask app. Integrate this with MongoDB (commented at `app/extensions.py`)

*******************

# Base Code Customization
This repository is cloned from the provided base code and customized as per the assessment requirements.

*******************

## Repository Structure

- **action-repo**: GitHub repository configured with webhooks to emit Push, Pull Request, and Merge events.
- **webhook-repo** (this repository): Flask application that receives GitHub webhooks, stores events in MongoDB, and exposes APIs consumed by the frontend.

*******************

## MongoDB Configuration

This application uses MongoDB to persist GitHub webhook events.

Create a `.env` file at the project root

*******************

## Supported GitHub Webhook Events

The receiver currently supports the following GitHub events:

- Push
- Pull Request (opened)
- Pull Request Merge (closed + merged)

Each event is normalized and stored in MongoDB as per the provided schema.

*******************

## MongoDB Schema

Each webhook event is stored in MongoDB using the following schema:

- id: ObjectId (default MongoDB uid)
- request_id: string (commit hash or PR ID)
- author: string
- action: enum ["PUSH", "PULL_REQUEST", "MERGE"]
- from_branch: string | null
- to_branch: string
- timestamp: UTC datetime string

*******************

## Frontend 

The frontend is a minimal web UI that displays GitHub repository events captured via the webhook.  
- Built using **plain HTML, CSS, and JavaScript** for simplicity and easy explanation.  
- Polls the backend every **15 seconds** to fetch the latest events from MongoDB.  
- Displays events in chronological order, showing details for **PUSH**, **PULL_REQUEST**, and **MERGE** actions.  
- Designed to be clean, minimal, and focused only on the necessary information from the webhook.

*******************

## Testing the Webhook Receiver

### Local Testing
Run the Flask app and send requests to:
POST http://127.0.0.1:5000/webhook/receiver
used to insert webhook payload data into MongoDB  
GET http://127.0.0.1:5000/webhook/events
used retrieve stored webhook events from MongoDB
Using curl or Postman or Thunderclient with sample GitHub payloads.

### GitHub Webhook Testing
1. Expose the local server using ngrok
2. Configure a webhook in the action-repo:
   - Payload URL: `<ngrok-url>/webhook/receiver`
   - Content-Type: application/json
   - Events: Push, Pull Request
3. Trigger push, PR open, and merge actions
4. Verify MongoDB documents are created

### Frontend Testing
Fetches and displays formatted event data, polled every 15 seconds from the backend.
The frontend is served separately (e.g., via a local static server or VS Code Live Server) and consumes the backend API.

### Integration Testing 
when i push any updates to the action-repo or make a pull request or merge the pull request the UI shows it cleanly and sorts to show the latest update at the first

*******************

