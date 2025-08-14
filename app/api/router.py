from fastapi import APIRouter, Body, Depends, Path
from app.repositories import transaction_repository
from app.services.wallet_service import WalletService

from app.api.dependencies import get_db, get_repository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.wallet_repository import WalletRepository

router = APIRouter(prefix="/api/v1/wallets")


@router.post("/{uuid}/operation")
def make_operation(
    operation_type: str = Body(),
    amount: float = Body(),
    uuid: int = Path(),
    wallet_repo: WalletRepository = Depends(get_repository(WalletRepository)),
    transaction_repo: TransactionRepository = Depends(
        get_repository(TransactionRepository)
    ),
):
    wallet_service = WalletService(transaction_repo, wallet_repo)
    if amount <= 0:
        return {"status": "error", "message_text": "Сумма должна быть больше нуля"}

    try:
        if operation_type == "withdraw":
            return wallet_service.withdraw(uuid, amount)
        elif operation_type == "deposit":
            return wallet_service.deposit(uuid, amount)
        else:
            return {"status": "error", "message_text": "Неверный тип операции"}
    except Exception as e:
        print(f"Error in make_operation: {e}")
        import traceback

        traceback.print_exc()
        return {"status": "error", "message_text": "Ошибка сервера"}


@router.get("/{uuid}")
def get_balance(
    uuid: int = Path(),
    wallet_repo: WalletRepository = Depends(get_repository(WalletRepository)),
):
    transaction_repo = TransactionRepository(get_db())
    wallet_service = WalletService(transaction_repo, wallet_repo)
    try:
        return wallet_service.get_balance(uuid)
    except Exception as e:
        print(f"Error in get_balance: {e}")
        import traceback

        traceback.print_exc()
        return {"status": "error", "message_text": "Ошибка сервера"}
