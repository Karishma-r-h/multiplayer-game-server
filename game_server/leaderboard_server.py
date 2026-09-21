import time
import json
import redis
from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow cross-origin requests, needed since leaderboard.html is opened via file://
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def get_leaderboard():
    keys = r.keys("player:*")
    scores = []
    for key in keys:
        x = float(r.hget(key, "x") or 0.0)
        scores.append({"player": key, "score": x})
    scores.sort(key=lambda p: p["score"], reverse=True)
    return scores

@app.route("/leaderboard-stream")
def leaderboard_stream():
    def event_stream():
        while True:
            leaderboard = get_leaderboard()
            data = json.dumps(leaderboard)
            yield f"data: {data}\n\n"
            print(f"SSE push: {data}")
            time.sleep(1)

    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    print("Leaderboard SSE server running on http://localhost:8000/leaderboard-stream")
    app.run(host="localhost", port=8000, threaded=True)