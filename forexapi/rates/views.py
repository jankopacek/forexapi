import json
from django.views.generic import View
from django.http import JsonResponse
from forex_python.converter import RatesNotAvailableError
from rates.main import RatesValidationException, converter

class Convert(View):
    """
    Main converter view
    """
    def get(self, request, *args, **kwargs):
        amount = request.GET.get('amount', None)
        input_currency = request.GET.get('input_currency', None)
        output_currency = request.GET.get('output_currency', None)
        if not (amount and input_currency):
            return JsonResponse({"err": "amount and input_currency get params required"})
        try:
            ret = converter(amount, input_currency, output_currency)
            return JsonResponse(ret)
        except RatesValidationException as e:
            return JsonResponse({"err": "Inpurt validation error: {}".format(e)})
        except RatesNotAvailableError:
            return JsonResponse({"err":"Problem with api connection, please try later"})