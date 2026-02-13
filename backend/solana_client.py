"""
Solana client for PayLoad micropayments
"""
import os
import base58
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from spl.token.instructions import transfer_checked, TransferCheckedParams
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID
import struct

class PayLoadClient:
    def __init__(self):
        self.rpc_url = os.getenv('SOLANA_RPC_URL', 'https://api.devnet.solana.com')
        self.client = Client(self.rpc_url)
        self.network = os.getenv('SOLANA_NETWORK', 'devnet')
        
        # Load wallet from private key
        private_key = os.getenv('WALLET_PRIVATE_KEY')
        if private_key:
            self.wallet = Keypair.from_bytes(base58.b58decode(private_key))
        else:
            # Generate ephemeral wallet for demo
            self.wallet = Keypair()
            print(f"⚠️  No wallet configured. Generated ephemeral: {self.wallet.pubkey()}")
        
        # Token configuration
        self.usd1_mint = Pubkey.from_string(
            os.getenv('USD1_MINT', '4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU')
        )
        self.recipient = Pubkey.from_string(
            os.getenv('RECIPIENT_WALLET', '11111111111111111111111111111111')
        )
        
        # USD1 has 6 decimals (like USDC)
        self.decimals = 6
    
    def get_balance(self):
        """Get SOL balance of payment wallet"""
        try:
            response = self.client.get_balance(self.wallet.pubkey())
            return response.value / 1e9  # Convert lamports to SOL
        except Exception as e:
            print(f"Error getting balance: {e}")
            return 0
    
    def get_token_balance(self):
        """Get USD1 token balance"""
        try:
            # Find associated token account
            from spl.token.client import Token
            # This is simplified - in production use proper ATA lookup
            response = self.client.get_token_accounts_by_owner(
                self.wallet.pubkey(),
                {"mint": self.usd1_mint}
            )
            if response.value:
                balance = response.value[0].account.data.parsed['info']['tokenAmount']['uiAmount']
                return balance
            return 0
        except Exception as e:
            print(f"Error getting token balance: {e}")
            return 0
    
    def send_micropayment(self, amount_usd: float, memo: str = ""):
        """
        Send a USD1 micropayment
        
        Args:
            amount_usd: Amount in USD (e.g., 0.003)
            memo: Description of payment
            
        Returns:
            dict with transaction signature and details
        """
        try:
            # For demo purposes on devnet without real tokens,
            # we'll simulate with a minimal SOL transfer and return success
            # In production, this would be a real SPL token transfer
            
            if self.network == 'devnet':
                # Simulate payment with tiny SOL transfer (or just log)
                # This proves the concept without needing real USD1
                
                # Convert to lamports (1 SOL = 1B lamports)
                # We'll transfer equivalent lamports for demo
                lamports = max(1, int(amount_usd * 1000))  # Minimal amount
                
                # For true demo mode, we can just simulate
                # Uncomment below for real transactions:
                """
                tx = Transaction()
                tx.add(transfer(TransferParams(
                    from_pubkey=self.wallet.pubkey(),
                    to_pubkey=self.recipient,
                    lamports=lamports
                )))
                
                response = self.client.send_transaction(tx, self.wallet)
                signature = str(response.value)
                """
                
                # Simulated response for demo
                import hashlib
                import time
                fake_sig = hashlib.sha256(f"{time.time()}{amount_usd}{memo}".encode()).hexdigest()[:88]
                
                return {
                    "success": True,
                    "signature": fake_sig,
                    "amount": amount_usd,
                    "memo": memo,
                    "network": self.network,
                    "explorer_url": f"https://explorer.solana.com/tx/{fake_sig}?cluster={self.network}",
                    "simulated": True  # Flag that this is demo mode
                }
            
            else:
                # Production: Real USD1 SPL token transfer
                # This requires proper token account setup
                amount_raw = int(amount_usd * (10 ** self.decimals))
                
                # Build SPL token transfer
                # (Full implementation would go here)
                
                return {
                    "success": False,
                    "error": "Production mode not yet implemented"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_wallet_info(self):
        """Get wallet public info for display"""
        return {
            "pubkey": str(self.wallet.pubkey()),
            "network": self.network,
            "rpc": self.rpc_url,
            "sol_balance": self.get_balance()
        }


# Singleton instance
_client = None

def get_client():
    global _client
    if _client is None:
        _client = PayLoadClient()
    return _client
