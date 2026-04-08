# routes.py
from flask import Flask, request, jsonify, session
from models import Ballot

app = Flask(__name__)

@app.route("/ballot/<int:ballot_id>")
def get_ballot(ballot_id):
    # Ensure the logged-in user can only access their own ballot
    user_id = session.get("user_id")
    ballot = Ballot.query.filter_by(id=ballot_id, user_id=user_id).first()
    if not ballot:
        return jsonify({"error": "Unauthorized access"}), 403
    return jsonify({"vote": ballot.vote})
