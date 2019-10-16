# pylint: disable=unidiomatic-typecheck,unnecessary-pass


class DifferentCurrencyError(Exception):
    pass

class NegativeOperandError(Exception):
    pass


class Currency:
    """
    Represents a currency. Does not contain any exchange rate info.
    """

    def __init__(self, name, code, symbol=None, digits=2):
        """
        Parameters:
        - name -- the English name of the currency
        - code -- the ISO 4217 three-letter code for the currency
        - symbol - optional symbol used to designate currency
        - digits -- number of significant digits used
        """
        self.name = name
        self.code = code
        self.symbol = symbol
        self.digits = digits

    def __str__(self):
        """
        Should return the currency code, or code with symbol in parentheses.
        """
        if self.symbol is None:
            return self.code
        elif self.symbol is not None:
            return self.code + " (" + self.symbol + ")"

    def __eq__(self, other):
        """
        All fields must be equal to for the objects to be equal.
        """
        return (type(self) == type(other) and self.name == other.name and
                self.code == other.code and self.symbol == other.symbol and
                self.digits == other.digits)


class Money:
    """
    Represents an amount of money. Requires an amount and a currency.
    """

    def __init__(self, amount, currency):
        """
        Parameters:
        - amount -- quantity of currency
        - currency -- type of currency
        """
        self.amount = amount
        self.currency = currency

    def __str__(self):
        """
        Should use the currency symbol if available, else use the code.
        Use the currency digits to determine number of digits to show.
        """
        if self.currency.symbol is None:
            return self.currency.code + " {:.{prec}f}".format(self.amount, prec=self.currency.digits)
        elif self.currency.symbol is not None:
            return self.currency.symbol + "{:.{prec}f}".format(self.amount, prec=self.currency.digits)

    def __repr__(self):
        return f"<Money {str(self)}>"

    def __eq__(self, other):
        """
        All fields must be equal to for the objects to be equal.
        """

        return (type(self) == type(other) and self.amount == other.amount and
                self.currency == other.currency)

    def __add__(self, other):
        if self.currency.code != other.currency.code:
            raise DifferentCurrencyError
        else:
            total_money = self.amount + other.amount
            return Money(total_money, self.currency)

    def add(self, other):
        """
        Add two money objects of the same currency. If they have different
        currencies, raise a DifferentCurrencyError.
        """
        if self.currency.code != other.currency.code:
            raise DifferentCurrencyError
        else:
            return Money(self.amount+other.amount, self.currency)

    def __sub__(self, other):
        if self.currency.code != other.currency.code:
            raise DifferentCurrencyError
        else:
            total_money = self.amount - other.amount
            return Money(total_money, self.currency)

    def sub(self, other):
        """
        Subtract two money objects of the same currency. If they have different
        currencies, raise a DifferentCurrencyError.
        """
        if self.currency.code != other.currency.code:
            raise DifferentCurrencyError
        else:
            return Money(self.amount-other.amount, self.currency)

    def mul(self, multiplier):
        """
        Multiply a money object by a number to get a new money object.
        """
        if multiplier < 0:
            raise NegativeOperandError
        else:
            return Money(self.amount*multiplier, self.currency)

    def __mul__(self, multiplier):
        if multiplier < 0:
            raise NegativeOperandError
        else:
            total_money = self.amount*multiplier
            return Money(total_money, self.currency)

    def div(self, divisor):
        """
        Divide a money object by a number to get a new money object.
        """
        if divisor is 0:
            raise ZeroDivisionError
        elif divisor < 0:
            raise NegativeOperandError
        else:
            return Money(self.amount/divisor, self.currency)

    def __div__(self, multiplier):
        if multiplier < 0:
            raise NegativeOperandError
        else:
            total_money = self.amount/multiplier
            return Money(total_money, self.currency)