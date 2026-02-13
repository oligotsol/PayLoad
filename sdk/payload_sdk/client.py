"""
PayLoad Client - Micropayment client for autonomous systems
"""
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer

from .wallet import Wallet


class Network(Enum):
    DEVNET = "devnet"
    MAINNET = "mainnet-beta"


@dataclass
class PaymentResult:
    """Result of a payment transaction."""
    success: bool
    signature: Optional[str] = None
    amount: float = 0.0
    recipient: Optional[str] = None
    memo: Optional[str] = None
    error: Optional[str] = None
    explorer_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "signature": self.signature,
            "amount": self.amount,
            "recipient": self.recipient,
            "memo": self.memo,
            "error": self.error,
            "explorer_url": self.explorer_url
        }


class PayLoadClient:
    """
    Micropayment client for autonomous systems.
    
    Usage:
        from payload_sdk import Wallet, PayLoadClient
        
        wallet = Wallet.from_env()
        client = PayLoadClient(wallet)
        
        # Make a payment
        result = client.pay(
            amount=0.003,
            recipient="...",
            memo="Airspace fee"
        )
        
        if result.success:
            print(f"Paid! TX: {result.signature}")
    """
    
    RPC_URLS = {
        Network.DEVNET: "https://api.devnet.solana.com",
        Network.MAINNET: "https://api.mainnet-beta.solana.com"
    }
    
    def __init__(
        self,
        wallet: Wallet,
        network: Network = Network.DEVNET,
        rpc_url: Optional[str] = None
    ):
        self.wallet = wallet
        self.network = network
        self.rpc_url = rpc_url or self.RPC_URLS[network]
        self._client = Client(self.rpc_url)
    
    def get_balance(self) -> float:
        """Get SOL balance in SOL (not lamports)."""
        try:
            response = self._client.get_balance(self.wallet.pubkey)
            return response.value / 1e9
        except Exception as e:
            print(f"Error getting balance: {e}")
            return 0.0
    
    def pay(
        self,
        amount: float,
        recipient: str,
        memo: Optional[str] = None
    ) -> PaymentResult:
        """
        Send a micropayment.
        
        Args:
            amount: Amount in USD (converted to lamports for demo)
            recipient: Recipient wallet address
            memo: Optional payment description
            
        Returns:
            PaymentResult with transaction details
        """
        try:
            recipient_pubkey = Pubkey.from_string(recipient)
            
            # For demo: convert USD amount to lamports
            # In production: this would be USD1 SPL token transfer
            # Using 1 USD = 10000 lamports for demo visibility
            lamports = max(1000, int(amount * 10000))
            
            # Build transaction
            tx = Transaction()
            tx.add(transfer(TransferParams(
                from_pubkey=self.wallet.pubkey,
                to_pubkey=recipient_pubkey,
                lamports=lamports
            )))
            
            # Send transaction
            response = self._client.send_transaction(
                tx,
                self.wallet.keypair
            )
            
            signature = str(response.value)
            
            # Build explorer URL
            cluster_param = "" if self.network == Network.MAINNET else f"?cluster={self.network.value}"
            explorer_url = f"https://explorer.solana.com/tx/{signature}{cluster_param}"
            
            return PaymentResult(
                success=True,
                signature=signature,
                amount=amount,
                recipient=recipient,
                memo=memo,
                explorer_url=explorer_url
            )
            
        except Exception as e:
            return PaymentResult(
                success=False,
                amount=amount,
                recipient=recipient,
                memo=memo,
                error=str(e)
            )
    
    def pay_for_resource(
        self,
        resource_url: str,
        amount: float,
        provider: str
    ) -> PaymentResult:
        """
        x402-style payment for a resource.
        
        This is the pattern for autonomous resource access:
        1. Request resource
        2. Get 402 Payment Required + payment details
        3. Pay
        4. Access granted
        
        Args:
            resource_url: URL of the resource being paid for
            amount: Payment amount
            provider: Provider wallet address
            
        Returns:
            PaymentResult
        """
        return self.pay(
            amount=amount,
            recipient=provider,
            memo=f"x402:{resource_url}"
        )
    
    def __repr__(self) -> str:
        return f"PayLoadClient(wallet={self.wallet}, network={self.network.value})"
