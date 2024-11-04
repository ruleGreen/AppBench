class Payment:
    def __init__(self):
        self.desc = {
            "desc": "the fast, simple way to pay in apps, on the web, and in millions of stores",
            "base_required_arguments": {},
            "APIs": {
                "requestpayment": {
                    "desc": "request payment from someone",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "receiver (str)": "name of the contact or account to make the transaction with",
                        "amount (float)": "the amount of money to send or request"
                    },
                    "optional_arguments": {
                        "private_visibility (bool)": "whether the transaction is private or not"
                    },
                    "result_arguments": {
                        "amount (float)": "the amount of money to send or request",
                        "receiver (str)": "name of the contact or account to make the transaction with",
                        "private_visibility (bool)": "whether the transaction is private or not"
                    }
                },
                "makepayment": {
                    "desc": "send money to your friends",
                    "is_transactional": True,
                    "additional_required_arguments": {
                        "payment_method (str)": "the source of money used for making the payment, value can only be one of follows: app balance, credit card, or debit card",
                        "amount (float)": "the amount of money to send or request",
                        "receiver (str)": "name of the contact or account to make the transaction with"
                    },
                    "optional_arguments": {
                        "private_visibility (bool)": "whether the transaction is private or not"
                    },
                    "result_arguments": {
                        "payment_method (str)": "the source of money used for making the payment, value can only be one of follows: app balance, credit card, or debit card",
                        "amount (float)": "the amount of money to send or request",
                        "receiver (str)": "name of the contact or account to make the transaction with",
                        "private_visibility (bool)": "whether the transaction is private or not"
                    }
                }
            }
        }