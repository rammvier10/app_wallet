class Transaction:
    def __init__(self, uuid: str, type: str, amount: float):
        self.uuid = uuid
        self.type = type
        self.amount = amount