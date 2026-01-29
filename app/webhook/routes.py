from flask import Blueprint, json, request
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    event = request.headers.get("X-GitHub-Event","").lower()
    payload = request.get_json()

    doc= parse_event(event,payload)

    if doc:
        mongo.db.events.insert_one(doc)
    return json.dumps({"status":"ok"}), 200, {"Content-Type":"application/json"}
    
def parse_event(event, payload):
    if event == "push":
        commit = payload.get("head_commit")
        if not commit:
            return None
        
        return {
            "request_id": commit.get("id"),
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": commit.get("timestamp")
        }
    
    if event == "pull_request":
        pr=payload.get("pull_request")
        action_type = payload.get("action")

        base_doc = {
            "request_id":str(pr.get("id")),
            "author": pr["user"]["login"],
            "from_branch": pr["head"]["ref"],
            "to_branch":pr["base"]["ref"]
        }

        if action_type == "opened":
            base_doc.update({
                "action": "PULL_REQUEST",
                "timestamp":pr.get("created_at")
            })
            return base_doc
        if action_type == "closed" and pr.get("merged"):
            base_doc.update({
                "action":"MERGE",
                "timestamp": pr.get("merged_at")
            })
            return base_doc
    return None

@webhook.route('/events', methods=["GET"])
def get_events():
    docs= mongo.db.events.find().sort("timestamp", -1).limit(10)
    result = []

    for d in docs:
        d["_id"]=str(d["_id"])
        result.append(d)
    return json.dumps(result), 200, {
        "Content-Type": "application/json"
    }