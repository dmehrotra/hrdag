
from cltk.phonology.arabic.romanization import transliterate
import csv
import pyphen
import codecs

mode = 'buckwalter'
reverse = True # true means transliteration from arabic native script to roman script such as Buckwalter
pyphen.language_fallback('nl_NL_variant1')
dic = pyphen.Pyphen(lang='nl_NL')
names=[]


with open('data/names.csv','r',encoding='utf-8') as f:
    reader = csv.reader(f)
    # skip the header
    next(reader, None)
    for r in reader:
      ar_string = r[0]
      l=transliterate(mode, ar_string, "", reverse)
      names.append([r[0],dic.inserted(l)])

     
with open("cleaned.csv", 'w',encoding='utf-8') as csv_file:
    wr = csv.writer(csv_file, delimiter=',')
    for cdr in names:
      wr.writerow([cdr[0],cdr[1]])






