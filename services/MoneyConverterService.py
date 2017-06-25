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

  def convert_to_usd(string, date):
    matches = MoneyConverterService.MONEY_REGEX.match(string)
    convert_to_date = datetime.strptime(date, '%d %B %Y')
    default_date = datetime.strptime('6 April 2017', '%d %B %Y')
    convert_to_date = convert_to_date if convert_to_date < default_date else default_date
    
    currency = matches.group(1);
    amount = matches.group(2).replace(',','')
    if currency in MoneyConverterService.SYMBOLS_TO_CODE.keys():
      currency = MoneyConverterService.SYMBOLS_TO_CODE[currency] 
  
    return CurrencyConverter().convert(amount, currency, 'USD', date=convert_to_date)


