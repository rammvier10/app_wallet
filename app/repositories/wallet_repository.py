from ..models import Wallet as WalletModel
from .base import BaseRespository

class WalletRepository(BaseRespository):
    def get_wallet_with_lock(self, wallet_id: int):
        return self.connection.query(WalletModel).filter(WalletModel.id == wallet_id).with_for_update().first()
    
    def create_wallet(self, wallet_id: int):
        wallet = WalletModel(id=wallet_id, name=f"Wallet {wallet_id}", initial_saldo=0.0)
        self.connection.add(wallet)
        self.connection.flush()
        return wallet
    
    def get_wallet(self, wallet_id: int):
        return self.connection.get(WalletModel, wallet_id)
