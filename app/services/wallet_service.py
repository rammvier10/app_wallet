from ..entities.transaction import Transaction
from ..repositories.transaction_repository import TransactionRepository
from ..repositories.wallet_repository import WalletRepository


class WalletService:
    def __init__(
        self, transations_repo: TransactionRepository, wallet_repo: WalletRepository
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

        balance = wallet.initial_saldo
        for t in transactions:
            if t.type == "deposit":
                balance += t.amount
            elif t.type == "withdraw":
                balance -= t.amount

        return {"id": wallet_id, "saldo": balance}
