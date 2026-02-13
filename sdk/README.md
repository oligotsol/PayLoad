# PayLoad SDK

**Autonomous payment rails for drones and IoT devices.**

USD1 micropayments on Solana for machine-to-machine commerce.

## Installation

```bash
pip install payload-sdk
```

## Quick Start

```python
from payload_sdk import Wallet, PayLoadClient

# Create or load wallet
wallet = Wallet.from_env("PAYLOAD_PRIVATE_KEY")
# Or: wallet = Wallet.create()

# Initialize client
client = PayLoadClient(wallet)

# Check balance
print(f"Balance: {client.get_balance()} SOL")

# Make a micropayment
result = client.pay(
    amount=0.003,  # $0.003
    recipient="recipient_wallet_address",
    memo="Airspace access fee"
)

if result.success:
    print(f"Payment sent! TX: {result.signature}")
    print(f"Explorer: {result.explorer_url}")
else:
    print(f"Payment failed: {result.error}")
```

## x402-Style Resource Payments

For autonomous resource access (HTTP 402 pattern):

```python
# Pay for a resource
result = client.pay_for_resource(
    resource_url="https://airspace.api/zone-a",
    amount=0.003,
    provider="provider_wallet_address"
)
```

## Wallet Management

```python
from payload_sdk import Wallet

# Create new wallet
wallet = Wallet.create()
print(f"Address: {wallet.address}")
print(f"Private key: {wallet.export_private_key()}")

# Load from private key
wallet = Wallet.from_private_key("5JTj9b...")

# Load from environment variable
wallet = Wallet.from_env("PAYLOAD_PRIVATE_KEY")
```

## Networks

```python
from payload_sdk import PayLoadClient, Network

# Devnet (default)
client = PayLoadClient(wallet, network=Network.DEVNET)

# Mainnet
client = PayLoadClient(wallet, network=Network.MAINNET)

# Custom RPC
client = PayLoadClient(wallet, rpc_url="https://my-rpc.com")
```

## Use Cases

- **Drone Payments**: Airspace fees, landing pads, charging stations
- **IoT Sensors**: Pay for data, bandwidth, compute
- **Autonomous Vehicles**: Tolls, parking, charging
- **AI Agents**: API calls, data purchases, service fees

## Links

- [GitHub](https://github.com/oligotsol/PayLoad)
- [Documentation](https://github.com/oligotsol/PayLoad)

## License

MIT
