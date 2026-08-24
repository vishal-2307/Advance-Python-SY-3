# ==========================================================
# PAYMENT PROCESSING SYSTEM
# ==========================================================

from abc import ABC, abstractmethod
import functools
import uuid
from datetime import datetime


# ==========================================================
# Receipt Class
# ==========================================================

class Receipt:

    def __init__(self, amount, method, status):
        self.txn_id = str(uuid.uuid4())[:8]
        self.amount = amount
        self.method = method
        self.status = status
        self.timestamp = datetime.now()

    def __str__(self):
        return (
            "\n------------ RECEIPT ------------\n"
            f"Transaction ID : {self.txn_id}\n"
            f"Amount         : ₹{self.amount}\n"
            f"Method         : {self.method}\n"
            f"Status         : {self.status}\n"
            f"Date & Time    : {self.timestamp}\n"
            "---------------------------------\n"
        )


# ==========================================================
# Abstract Base Class
# ==========================================================

class PaymentStrategy(ABC):

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def pay(self, amount):
        pass

    def _make_receipt(self, amount, status):
        return Receipt(amount, self.__class__.__name__, status)


# ==========================================================
# Credit Card Payment
# ==========================================================

class CreditCardPayment(PaymentStrategy):

    def __init__(self, card_number, cvv, expiry):
        self.card_number = card_number
        self.cvv = cvv
        self.expiry = expiry

    def validate(self):
        return len(self.card_number) == 16 and len(self.cvv) == 3

    def pay(self, amount):
        if self.validate():
            print("Credit Card Payment Successful")
            return self._make_receipt(amount, "SUCCESS")
        else:
            print("Invalid Credit Card Details")
            return self._make_receipt(amount, "FAILED")


# ==========================================================
# PayPal Payment
# ==========================================================

class PayPalPayment(PaymentStrategy):

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def validate(self):
        return "@" in self.email and len(self.password) >= 6

    def pay(self, amount):
        if self.validate():
            print("PayPal Payment Successful")
            return self._make_receipt(amount, "SUCCESS")
        else:
            print("Invalid PayPal Account")
            return self._make_receipt(amount, "FAILED")


# ==========================================================
# UPI Payment
# ==========================================================

class UPIPayment(PaymentStrategy):

    def __init__(self, upi_id):
        self.upi_id = upi_id

    def validate(self):
        return "@" in self.upi_id

    def pay(self, amount):
        if self.validate():
            print("UPI Payment Successful")
            return self._make_receipt(amount, "SUCCESS")
        else:
            print("Invalid UPI ID")
            return self._make_receipt(amount, "FAILED")


# ==========================================================
# Net Banking Payment
# ==========================================================

class NetBankingPayment(PaymentStrategy):

    def __init__(self, bank_name, account_number):
        self.bank_name = bank_name
        self.account_number = account_number

    def validate(self):
        return len(self.account_number) >= 10

    def pay(self, amount):
        if self.validate():
            print("Net Banking Payment Successful")
            return self._make_receipt(amount, "SUCCESS")
        else:
            print("Invalid Account Number")
            return self._make_receipt(amount, "FAILED")


# ==========================================================
# Decorator
# ==========================================================

def log_transaction(function):

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        print("\n[LOG] Transaction Started")
        result = function(*args, **kwargs)
        print("[LOG] Transaction Finished")
        return result

    return wrapper


# ==========================================================
# Payment Processor
# ==========================================================

class PaymentProcessor:

    _registry = {}

    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy
        print(f"\n[CONFIG] Switched to {strategy.__class__.__name__}")

    @log_transaction
    def process_payment(self, amount):
        if self.strategy is None:
            print("No Payment Strategy Selected")
            return
        return self.strategy.pay(amount)

    @classmethod
    def register_strategy(cls, key, strategy_class):
        cls._registry[key] = strategy_class
        print(f"Registered -> {key}")

    @classmethod
    def available_methods(cls):
        return list(cls._registry.keys())

    @classmethod
    def create(cls, key, **kwargs):
        strategy = cls._registry[key](**kwargs)
        return cls(strategy)


# ==========================================================
# Main Program
# ==========================================================

if __name__ == "__main__":

    print("\n======= Registering Payment Methods =======")

    PaymentProcessor.register_strategy("card", CreditCardPayment)
    PaymentProcessor.register_strategy("paypal", PayPalPayment)
    PaymentProcessor.register_strategy("upi", UPIPayment)
    PaymentProcessor.register_strategy("netbanking", NetBankingPayment)

    print("\nAvailable Methods:")
    print(PaymentProcessor.available_methods())

    processor = PaymentProcessor.create(
        "upi",
        upi_id="student@oksbi"
    )

    receipt = processor.process_payment(500)
    print(receipt)

    processor.set_strategy(
        CreditCardPayment(
            "1234567890123456",
            "123",
            "12/30"
        )
    )

    receipt = processor.process_payment(1500)
    print(receipt)

    processor.set_strategy(
        PayPalPayment(
            "wrongemail",
            "123"
        )
    )

    receipt = processor.process_payment(2500)
    print(receipt)

    processor.set_strategy(
        NetBankingPayment(
            "State Bank",
            "123456789012"
        )
    )

    receipt = processor.process_payment(3200)
    print(receipt)

    print("\nProgram Finished Successfully.")