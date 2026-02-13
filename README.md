# PayLoad

**Autonomous Payment Rails for American Drones**

USD1 micropayments on Solana for machine-to-machine commerce.

## Demo

This demo simulates an autonomous drone making real-time micropayments as it completes a delivery:
- Airspace fees
- Weather data purchases
- Landing pad rental
- Charging
- Delivery settlement

All payments are real USD1 transactions on Solana.

## Structure

```
├── frontend/      # Web-based demo UI
├── backend/       # Flask API + Solana integration
└── README.md
```

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your Solana wallet private key
python app.py
```

### Frontend
```bash
cd frontend
# Serve with any static server
python -m http.server 8080
```

## Environment Variables

- `SOLANA_RPC_URL` - Solana RPC endpoint (default: devnet)
- `WALLET_PRIVATE_KEY` - Base58 encoded private key for payment wallet
- `USD1_MINT` - USD1 token mint address
- `RECIPIENT_WALLET` - Demo recipient for payments

## License

MIT
