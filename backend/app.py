"""
PayLoad - Autonomous Payment Rails for Drones
Flask API for drone micropayment simulation
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import time
import threading

load_dotenv()

app = Flask(__name__)
CORS(app)

# Import our Solana client
from solana_client import get_client

# Track demo state
demo_state = {
    "running": False,
    "drone_position": 0,
    "payments": [],
    "total_paid": 0,
    "total_received": 0
}

# Payment waypoints in the drone journey
WAYPOINTS = [
    {
        "position": 10,
        "type": "payment",
        "name": "Airspace Zone A",
        "amount": 0.003,
        "description": "FAA airspace access fee"
    },
    {
        "position": 25,
        "type": "payment", 
        "name": "Weather Data",
        "amount": 0.001,
        "description": "Real-time weather feed"
    },
    {
        "position": 45,
        "type": "payment",
        "name": "Airspace Zone B", 
        "amount": 0.004,
        "description": "Commercial corridor access"
    },
    {
        "position": 60,
        "type": "payment",
        "name": "Traffic Routing",
        "amount": 0.002,
        "description": "Optimal path calculation"
    },
    {
        "position": 80,
        "type": "payment",
        "name": "Landing Pad",
        "amount": 0.05,
        "description": "Rooftop pad reservation"
    },
    {
        "position": 90,
        "type": "payment",
        "name": "Charging",
        "amount": 0.12,
        "description": "Battery top-up"
    },
    {
        "position": 100,
        "type": "receive",
        "name": "Delivery Complete",
        "amount": 5.00,
        "description": "Payment received for delivery"
    }
]


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "PayLoad API"})


@app.route('/api/wallet', methods=['GET'])
def wallet_info():
    """Get wallet information"""
    client = get_client()
    return jsonify(client.get_wallet_info())


@app.route('/api/demo/start', methods=['POST'])
def start_demo():
    """Start a new drone delivery demo"""
    global demo_state
    
    demo_state = {
        "running": True,
        "drone_position": 0,
        "payments": [],
        "total_paid": 0,
        "total_received": 0,
        "start_time": time.time()
    }
    
    return jsonify({
        "success": True,
        "message": "Demo started",
        "waypoints": WAYPOINTS
    })


@app.route('/api/demo/stop', methods=['POST'])
def stop_demo():
    """Stop the current demo"""
    global demo_state
    demo_state["running"] = False
    
    return jsonify({
        "success": True,
        "message": "Demo stopped"
    })


@app.route('/api/demo/status', methods=['GET'])
def demo_status():
    """Get current demo status"""
    return jsonify(demo_state)


@app.route('/api/demo/advance', methods=['POST'])
def advance_drone():
    """
    Advance the drone position.
    Called by frontend to move drone and trigger payments.
    """
    global demo_state
    
    if not demo_state.get("running"):
        return jsonify({"error": "Demo not running"}), 400
    
    # Get new position from request or auto-advance
    data = request.json or {}
    new_position = data.get("position", demo_state["drone_position"] + 5)
    
    # Cap at 100
    new_position = min(100, new_position)
    
    # Check for waypoints crossed
    triggered_payments = []
    client = get_client()
    
    for waypoint in WAYPOINTS:
        wp_pos = waypoint["position"]
        # If we crossed this waypoint
        if demo_state["drone_position"] < wp_pos <= new_position:
            # Process payment
            if waypoint["type"] == "payment":
                result = client.send_micropayment(
                    waypoint["amount"],
                    waypoint["name"]
                )
                payment_record = {
                    "timestamp": time.time(),
                    "waypoint": waypoint["name"],
                    "amount": waypoint["amount"],
                    "type": "debit",
                    "description": waypoint["description"],
                    "tx": result
                }
                demo_state["payments"].append(payment_record)
                demo_state["total_paid"] += waypoint["amount"]
                triggered_payments.append(payment_record)
                
            elif waypoint["type"] == "receive":
                # Receiving payment for delivery
                payment_record = {
                    "timestamp": time.time(),
                    "waypoint": waypoint["name"],
                    "amount": waypoint["amount"],
                    "type": "credit",
                    "description": waypoint["description"],
                    "tx": {
                        "success": True,
                        "signature": f"delivery_{int(time.time())}",
                        "simulated": True
                    }
                }
                demo_state["payments"].append(payment_record)
                demo_state["total_received"] += waypoint["amount"]
                triggered_payments.append(payment_record)
    
    # Update position
    demo_state["drone_position"] = new_position
    
    # Check if demo complete
    if new_position >= 100:
        demo_state["running"] = False
        demo_state["complete"] = True
    
    return jsonify({
        "position": new_position,
        "triggered_payments": triggered_payments,
        "total_paid": round(demo_state["total_paid"], 4),
        "total_received": round(demo_state["total_received"], 2),
        "net": round(demo_state["total_received"] - demo_state["total_paid"], 4),
        "complete": demo_state.get("complete", False)
    })


@app.route('/api/pay', methods=['POST'])
def make_payment():
    """
    Direct payment endpoint (x402-style)
    For manual/custom payments outside the demo flow
    """
    data = request.json
    
    if not data or "amount" not in data:
        return jsonify({"error": "Amount required"}), 400
    
    amount = float(data["amount"])
    memo = data.get("memo", "PayLoad payment")
    
    client = get_client()
    result = client.send_micropayment(amount, memo)
    
    if result["success"]:
        return jsonify(result)
    else:
        return jsonify(result), 500


@app.route('/api/waypoints', methods=['GET'])
def get_waypoints():
    """Get all waypoints for the demo route"""
    return jsonify({
        "waypoints": WAYPOINTS,
        "total_cost": sum(w["amount"] for w in WAYPOINTS if w["type"] == "payment"),
        "total_revenue": sum(w["amount"] for w in WAYPOINTS if w["type"] == "receive")
    })


if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║   PayLoad - Autonomous Drone Payments     ║
    ║   USD1 Micropayments on Solana            ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    """)
    
    client = get_client()
    info = client.get_wallet_info()
    print(f"  Wallet: {info['pubkey'][:20]}...")
    print(f"  Network: {info['network']}")
    print(f"  Balance: {info['sol_balance']} SOL")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
