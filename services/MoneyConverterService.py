from currency_converter import CurrencyConverter
from datetime import datetime
import re

class MoneyConverterService:

  SYMBOLS_TO_CODE = {
    '£': 'GBP',
    '$': 'USD',
    '€': 'EUR'
  }


  MONEY_REGEX = re.compile('([£$€]|[a-zA-Z]*)\s*([\d,]*)')

  def convert_to_usd(string, money):
    # matches = re.compile()
    matches = MoneyConverterService.MONEY_REGEX.match(string)
    convert_to_date = datetime.strptime(money, '%d %B %Y')
    print(convert_to_date)
    
    currency = matches.group(1);
    amount = matches.group(2).replace(',','')
    if currency in MoneyConverterService.SYMBOLS_TO_CODE.keys():
      currency = MoneyConverterService.SYMBOLS_TO_CODE[currency] 
  
    return CurrencyConverter().convert(amount, currency, 'USD', date=convert_to_date)


