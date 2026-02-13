"""
PayLoad Wallet - Autonomous payment wallet for machines
"""
import os
import base58
from typing import Optional
from solders.keypair import Keypair
from solders.pubkey import Pubkey


class Wallet:
    """
    Autonomous wallet for machine-to-machine payments.
    
    Usage:
        # Create new wallet
        wallet = Wallet.create()
        
        # Load from private key
        wallet = Wallet.from_private_key("5JTj9b...")
        
        # Load from environment
        wallet = Wallet.from_env("PAYLOAD_PRIVATE_KEY")
    """
    
    def __init__(self, keypair: Keypair):
        self._keypair = keypair
    
    @classmethod
    def create(cls) -> "Wallet":
        """Create a new random wallet."""
        return cls(Keypair())
    
    @classmethod
    def from_private_key(cls, private_key: str) -> "Wallet":
        """Load wallet from base58-encoded private key."""
        keypair = Keypair.from_bytes(base58.b58decode(private_key))
        return cls(keypair)
    
    @classmethod
    def from_env(cls, env_var: str = "PAYLOAD_PRIVATE_KEY") -> "Wallet":
        """Load wallet from environment variable."""
        private_key = os.environ.get(env_var)
        if not private_key:
            raise ValueError(f"Environment variable {env_var} not set")
        return cls.from_private_key(private_key)
    
    @property
    def pubkey(self) -> Pubkey:
        """Get the public key."""
        return self._keypair.pubkey()
    
    @property
    def address(self) -> str:
        """Get the wallet address as string."""
        return str(self._keypair.pubkey())
    
    @property
    def keypair(self) -> Keypair:
        """Get the underlying keypair (for signing)."""
        return self._keypair
    
    def export_private_key(self) -> str:
        """Export the private key as base58 string."""
        return base58.b58encode(bytes(self._keypair)).decode('utf-8')
    
    def __repr__(self) -> str:
        return f"Wallet({self.address[:8]}...{self.address[-4:]})"
