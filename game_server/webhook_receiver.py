from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook/match-complete", methods=["POST"])
def receive_webhook():
    payload = request.get_json()
    print(f"[External Service] Received webhook: {payload}")
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    print("Simulated external service listening on http://localhost:9000/webhook/match-complete")
    app.run(host="localhost", port=9000)