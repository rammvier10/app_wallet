from typing import List

from ..models import Transaction as TransactionModel
from ..entities.transaction import Transaction
from .base import BaseRespository

class TransactionRepository(BaseRespository):
    def save_transaction(self, transaction: Transaction, wallet_id: int):
        db_transaction = TransactionModel(
            amount=transaction.amount,
            transaction_type=transaction.type,
            wallet_id=wallet_id
        )
        self.connection.add(db_transaction)
        self.connection.commit()
        return transaction

    def get_transactions_by_wallet(self, wallet_id: int) -> List[Transaction]:
            transactions = self.connection.query(TransactionModel).filter(TransactionModel.wallet_id == wallet_id).all()
            return [Transaction(str(t.id), t.transaction_type, t.amount) for t in transactions]
    
    def get_transactions_by_wallet_with_lock(self, wallet_id: int):
        return self.connection.query(TransactionModel).filter(TransactionModel.wallet_id == wallet_id).with_for_update().all()
    
    def get_transactions_by_wallet_with_session(self, wallet_id: int) -> List[Transaction]:
        transactions = self.connection.query(TransactionModel).filter(TransactionModel.wallet_id == wallet_id).all()
        return [Transaction(str(t.id), t.transaction_type, t.amount) for t in transactions]
