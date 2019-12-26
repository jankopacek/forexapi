import os
import json
import forex_python
from forex_python.converter import CurrencyRates
from forex_python.converter import get_currency_code_from_symbol

MAX_LENGTH_CURRENCY = 3

class RatesValidationException(Exception):
    """
    Validation Exceptions
    """

class MyCurrencyCodes:
    """
    Loads currency info from forex_python raw_data
    """

    def __init__(self):
        """
        Preload currencies.json
        """
        self.currency_data = self._get_currency_data()

    def _get_currency_data(self):
        file_path = os.path.dirname(forex_python.__file__)
        with open(file_path+'/raw_data/currencies.json') as f:
            return json.loads(f.read())

    def get_currency_symbol_mapping(self):
        """
        return dict <symbol>: <currency>
        """
        ret = dict()
        for cur in self.currency_data:
            ret[cur['symbol']] = cur['cc']
        return ret

    def get_available_currency_codes(self):
        return [ cur['cc'] for cur in self.currency_data ]

class MyCurrencyRates(CurrencyRates):
    """
    Add convert to all
    """
    def convert_to_all(self, base_cur, amount):
        rates = self.get_rates(base_cur)
        ret = dict()
        for k,v in rates.items():
            ret[k] = v * amount
        return ret

class Convert():
    def __init__(self):
        self.currency_codes = MyCurrencyCodes()
        self.currency_rates = MyCurrencyRates()

    def get_currency_code(self, currency):
        if len(currency) > MAX_LENGTH_CURRENCY:
            raise RatesValidationException("Currency input too long! Should be max {}".format(MAX_LENGTH_CURRENCY))
        mapping = self.currency_codes.get_currency_symbol_mapping()
        if currency in mapping.values():
            # is valid code
            return currency
        elif currency in mapping.keys():
            # is valid symbol
            return mapping[currency]
        else:
            raise RatesValidationException("Not valid currency symbol or code!")

    def get_amount(self, amount):
        try:
            ret = float(amount)
        except (ValueError, TypeError):
            raise RatesValidationException("Amount not float!")
        if ret < 0:
            raise RatesValidationException("Amount should be positive!")
        return ret

    def __call__(self, amount, input_currency, output_currency=None):
        amount = self.get_amount(amount)
        input_currency_code = self.get_currency_code(input_currency)
        if output_currency:
            output_currency_code = self.get_currency_code(output_currency)
            output = { output_currency: self.currency_rates.convert(input_currency_code, output_currency_code, amount)}
        else:
            output = self.currency_rates.convert_to_all(input_currency_code, amount)

        return {"input": {"amount": amount, "currency": input_currency_code}, "output":output}

# from rates.main import converter
# converter(10, "EUR", "CZK")
converter = Convert()