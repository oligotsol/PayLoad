# 🛸 PayLoad

**Autonomous Payment Rails for American Drones**

USD1 micropayments on Solana for machine-to-machine commerce.

![Demo](https://img.shields.io/badge/Status-Demo-blue)
![Solana](https://img.shields.io/badge/Chain-Solana-purple)
![USD1](https://img.shields.io/badge/Stablecoin-USD1-green)

---

## The Problem

Autonomous systems (drones, robots, IoT devices) need to make **billions of micropayments** without human intervention:
- Airspace access fees
- Real-time data purchases
- Charging station payments
- Delivery settlements

Traditional payment rails can't handle this. Credit cards require human approval. Bank transfers are too slow. The machine economy needs **new infrastructure**.

## The Solution

**PayLoad** provides autonomous payment rails built on USD1 and Solana:
- ⚡ Sub-second settlement
- 💸 Micropayments down to fractions of a cent
- 🤖 Zero human intervention
- 🇺🇸 USD1 stablecoin (World Liberty Financial)

## Demo

The demo simulates an autonomous drone completing a delivery while making real-time micropayments:

```
Charging Station → Airspace A → Weather Data → Airspace B → Routing → Landing Pad → Charging → Delivery ✓
```

**7 autonomous payments. ~$0.18 in fees. $5.00 delivery payment. 15 seconds.**

### Run the Demo

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/payload-demo.git
cd payload-demo

# Start the frontend
cd frontend
python -m http.server 8080

# Open http://localhost:8080
```

Press **Start Flight** (or spacebar) to begin.

## Architecture

```
┌─────────────────────────────────────┐
│  DRONE / DEVICE                     │
│  (PayLoad SDK)                      │
├─────────────────────────────────────┤
│  AGENT WALLET                       │
│  (holds USD1, signs transactions)   │
├─────────────────────────────────────┤
│  PAYMENT PROTOCOL (x402-compatible) │
│  HTTP 402 → pay → get resource      │
├─────────────────────────────────────┤
│  SOLANA + USD1                      │
│  (settlement layer)                 │
└─────────────────────────────────────┘
```

## Tech Stack

- **Chain:** Solana (fast, cheap, USD1 supported)
- **Stablecoin:** USD1 (World Liberty Financial)
- **Protocol:** x402-compatible payment flow
- **Frontend:** Vanilla JS + CSS
- **Backend:** Python/Flask + solana-py

## SDK

Install the PayLoad SDK for Python:

```bash
pip install payload-sdk
```

```python
from payload_sdk import Wallet, PayLoadClient

wallet = Wallet.from_env("PAYLOAD_PRIVATE_KEY")
client = PayLoadClient(wallet)

# Make an autonomous payment
result = client.pay(
    amount=0.003,
    recipient="...",
    memo="Airspace fee"
)
```

See [`/sdk`](./sdk) for full documentation.

## Demo Wallet

**Address:** `BiWAQV7HX4VhB19gEq3mQ44xdZmnVkSDVTsBJJ5TrhUX`

[View on Solana Explorer](https://explorer.solana.com/address/BiWAQV7HX4VhB19gEq3mQ44xdZmnVkSDVTsBJJ5TrhUX?cluster=devnet)

## Roadmap

- [x] Interactive demo
- [x] PayLoad SDK (Python)
- [x] Demo wallet on Solana Devnet
- [ ] Real Solana devnet transactions
- [ ] USD1 mainnet integration
- [ ] x402 protocol compliance
- [ ] First hardware pilot

## Why USD1?

USD1 is the stablecoin from **World Liberty Financial** — positioned to be the settlement layer for American commerce. PayLoad extends this vision to **autonomous systems**, creating new demand for USD1 as the default payment rail for drones, robots, and IoT devices.

## Contact

Building the future of autonomous payments.

---

*Powered by USD1 on Solana*
