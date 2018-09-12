import dateparser
import re

class Row(object):
  """
    
  """

  def __init__(self, string):
    self.data = string
    self.dateparser = self.try_dateparser()
    self.parsable = False
    self.year = "00"
    self.month = "00"
    self.day = "00"

  def try_dateparser(self):
    return dateparser.parse(self.data, settings={'STRICT_PARSING': True,'PREFER_DATES_FROM': 'past'})

  def use_parser(self):
    self.year = self.dateparser.year
    self.month = self.dateparser.month
    self.day = self.dateparser.day

  def set_parsable(self):
    self.parsable = True

  def try_manual(self):
    std = self.standardize()
    for part in std:
      self.parse(part)

  def parse(self,part):
    # Assumption here is that if the givenpart of the string contains letters, its probably a month.
    # If the given part is greater than 31 treat it like a year
    try:
      if re.search('[a-zA-Z]', part):
        self.parse_month(part)
      elif int(part) > 31:
        self.parse_year(part)
      elif int(part) < 31 and self.month != "00":
        self.day = part
      elif int(part) < 31 and self.month == "00":
        self.month = part
    except ValueError:
      print(part)
  
  def parse_month(self,part):
    parsed = dateparser.parse(part,settings={'fuzzy': True})   
    if parsed is not None:
      self.month = parsed.month
    else:
      try:
        abbr = dateparser.parse(part[:3],settings={'fuzzy': True})
        if abbr is not None:
          self.month = abbr.month
      except ValueError:
        print(part)

  def parse_year(self,part):
    year = int(part)
    if year < 1900:
      year = year + 1900
      self.year=str(year)
    else:
      self.year=str(year)

  def standardize(self):
    # remove all non-alphanumeric and an return array
    s=re.sub('[^0-9a-zA-Z]+', '*', self.data)
    return s.split("*")

  def clean(self):
    # ugly fixes for bugs
    # 1. I'm assuming that if year that had been parsed is greater than 2019, its incorrect, and is actually from the previous century
    # 2. Strict parsing from the dateparser library is not as strict as I was hoping, so I'm assuming all 9/1/XXXX dates are incorrect. No data is probably better than incorrect in these instances.
    year = int(self.year)
    if year > 2019:
      self.year = int(self.year) - 100 
    if self.month == 1 and self.day == 9:
      self.month = "00"
      self.day = "00"
