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

## MongoDB Configuration

This application uses MongoDB to persist GitHub webhook events.

Create a `.env` file at the project root with the following:

## Supported GitHub Webhook Events

The receiver currently supports the following GitHub events:

- Push
- Pull Request (opened)
- Pull Request Merge (closed + merged)

Each event is normalized and stored in MongoDB as per the provided schema.

## MongoDB Schema

Each webhook event is stored in MongoDB using the following schema:

- request_id: string (commit hash or PR ID)
- author: string
- action: enum ["PUSH", "PULL_REQUEST", "MERGE"]
- from_branch: string | null
- to_branch: string
- timestamp: UTC datetime string

## Testing the Webhook Receiver

### Local Testing
Run the Flask app and send POST requests to:
POST http://127.0.0.1:5000/webhook/receiever
Using curl or Postman or Thunderclient with sample GitHub payloads.

### GitHub Webhook Testing
1. Expose the local server using ngrok
2. Configure a webhook in the action-repo:
   - Payload URL: `<ngrok-url>/webhook/receiver`
   - Content-Type: application/json
   - Events: Push, Pull Request
3. Trigger push, PR open, and merge actions
4. Verify MongoDB documents are created
