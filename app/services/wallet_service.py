from abc import ABC, abstractmethod
from typing import List

from ..models import Wallet
from ..entities.transaction import Transaction


class IWalletRepo(ABC):
    @abstractmethod
    def get_wallet_with_lock(self, wallet_id: int) -> Wallet:
        pass

    @abstractmethod
    def create_wallet(self, wallet_id) -> Wallet:
        pass

    @abstractmethod
    def get_wallet(self, wallet_id) -> Wallet:
        pass

class ITransactionRepo(ABC):
    @abstractmethod
    def save_transaction(self, transaction: Transaction, wallet_id: int) -> Transaction:
        pass

    @abstractmethod
    def get_transactions_by_wallet(self, wallet_id: int) -> List[Transaction]:
        pass
    
    @abstractmethod
    def get_transactions_by_wallet_with_lock(self, wallet_id: int):
        pass
    
    @abstractmethod
    def get_transactions_by_wallet_with_session(self, wallet_id: int) -> List[Transaction]:
        pass



class WalletService:
    def __init__(
        self, transations_repo: ITransactionRepo, wallet_repo: IWalletRepo
    ):
        self.wallet_repo = wallet_repo
        self.transaction_repo = transations_repo

    def deposit(self, wallet_id: int, amount: float):
        try:
            wallet = self.wallet_repo.get_wallet_with_lock(wallet_id)
            if not wallet:
                wallet = self.wallet_repo.create_wallet(wallet_id)

            transaction = Transaction(str(wallet_id), "deposit", amount)
            self.transaction_repo.save_transaction(transaction, wallet_id)
            return {"status": "success", "operation": "deposit", "amount": amount}

        except Exception:
            return {"status": "error", "message_text": "Операция отклонена"}

    def withdraw(self, wallet_id: int, amount: float):
        try:
            wallet = self.wallet_repo.get_wallet_with_lock(wallet_id)

            transactions = self.transaction_repo.get_transactions_by_wallet_with_lock(
                wallet_id
            )
            current_balance = wallet.initial_saldo
            for t in transactions:
                if t.transaction_type == "deposit":
                    current_balance += t.amount
                elif t.transaction_type == "withdraw":
                    current_balance -= t.amount

            if current_balance >= amount:
                transaction = Transaction(str(wallet_id), "withdraw", amount)
                self.transaction_repo.save_transaction(transaction, wallet_id)
                return {"status": "success", "operation": "withdraw", "amount": amount}
            else:
                return {"status": "error", "message_text": "Недостаточно средств"}

        except Exception:
            return {"status": "error", "message_text": "Операция отклонена"}

    def get_balance(self, wallet_id: int):
        wallet = self.wallet_repo.get_wallet(wallet_id)
        if not wallet:
            return {"status": "error", "message_text": "Кошелек не найден"}

        transactions = self.transaction_repo.get_transactions_by_wallet_with_session(
            wallet_id
        )

        balance = wallet['initial_saldo']
        for t in transactions:
            if t.type == "deposit":
                balance += t.amount
            elif t.type == "withdraw":
                balance -= t.amount

        return {"id": wallet_id, "saldo": balance}

class WalletRepoMock2(IWalletRepo):

    def create_wallet(self, wallet_id):
        return {"id": 123, "uuid": "asdf", "initial_saldo": 1000.0}

    def get_wallet(self, wallet_id):
        return {"id": 123, "uuid": "asdf", "initial_saldo": 1000.0}

class WalletRepoMock(IWalletRepo):
    def get_wallet_with_lock(self):
        return {"id": 123, "uuid": "asdf", "initial_saldo": 1000.0}

    def create_wallet(self, wallet_id):
        return {"id": 123, "uuid": "asdf", "initial_saldo": 1000.0}

    def get_wallet(self, wallet_id):
        return {"id": 123, "uuid": "asdf", "initial_saldo": 1000.0}

class TransactionRepoMock(ITransactionRepo):
    def huinya(self):
        return 

    def save_transaction(self, transaction: Transaction, wallet_id: int):
        pass

    def get_transactions_by_wallet(self, wallet_id: int) -> List[Transaction]:
        return []
    
    def get_transactions_by_wallet_with_lock(self, wallet_id: int):
        pass
    
    def get_transactions_by_wallet_with_session(self, wallet_id: int) -> List[Transaction]:
        return []


wallet = WalletService(
    transations_repo=TransactionRepoMock(), wallet_repo=WalletRepoMock()
)

print(wallet.get_balance(123))
print(wallet.deposit(123, 1100))
print(wallet.withdraw(234, 1000))
