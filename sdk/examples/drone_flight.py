"""
Example: Autonomous Drone Flight with Micropayments

This simulates a drone making autonomous payments during a delivery flight.
"""
import os
import sys
import time

# Add parent directory to path for local development
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from payload_sdk import Wallet, PayLoadClient, Network


def simulate_drone_delivery():
    """Simulate an autonomous drone delivery with micropayments."""
    
    print("=" * 50)
    print("🛸 PayLoad - Autonomous Drone Delivery Demo")
    print("=" * 50)
    print()
    
    # Initialize wallet and client
    # In production, load from secure storage
    wallet = Wallet.from_env("PAYLOAD_PRIVATE_KEY")
    client = PayLoadClient(wallet, network=Network.DEVNET)
    
    print(f"Drone Wallet: {wallet.address}")
    print(f"Balance: {client.get_balance():.4f} SOL")
    print()
    
    # Define the flight waypoints with payment requirements
    waypoints = [
        {"name": "Takeoff", "payment": None},
        {"name": "Airspace Zone A", "payment": 0.003, "recipient": wallet.address},
        {"name": "Weather Data", "payment": 0.001, "recipient": wallet.address},
        {"name": "Airspace Zone B", "payment": 0.004, "recipient": wallet.address},
        {"name": "Traffic Routing", "payment": 0.002, "recipient": wallet.address},
        {"name": "Landing Pad", "payment": 0.05, "recipient": wallet.address},
        {"name": "Charging Station", "payment": 0.12, "recipient": wallet.address},
        {"name": "Delivery Complete", "payment": None},
    ]
    
    total_paid = 0.0
    successful_payments = 0
    
    print("Starting delivery flight...")
    print("-" * 50)
    
    for i, waypoint in enumerate(waypoints):
        # Simulate flight time
        time.sleep(1)
        
        print(f"\n📍 Waypoint {i+1}/{len(waypoints)}: {waypoint['name']}")
        
        if waypoint.get("payment"):
            amount = waypoint["payment"]
            recipient = waypoint["recipient"]
            
            print(f"   💸 Payment required: ${amount:.3f}")
            
            result = client.pay(
                amount=amount,
                recipient=recipient,
                memo=waypoint["name"]
            )
            
            if result.success:
                print(f"   ✅ Paid! TX: {result.signature[:16]}...")
                print(f"   🔗 {result.explorer_url}")
                total_paid += amount
                successful_payments += 1
            else:
                print(f"   ❌ Payment failed: {result.error}")
        else:
            print(f"   ✓ No payment required")
    
    print()
    print("=" * 50)
    print("📊 Flight Summary")
    print("=" * 50)
    print(f"Total Payments: {successful_payments}")
    print(f"Total Paid: ${total_paid:.3f}")
    print(f"Final Balance: {client.get_balance():.4f} SOL")
    print()
    print("✅ Delivery complete!")


if __name__ == "__main__":
    simulate_drone_delivery()
