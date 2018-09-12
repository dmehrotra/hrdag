
import csv
import dateparser
from row import Row

cleaned_rows=[]

with open('data/dates.csv','rb') as f:
    reader = csv.reader(f)
    # skip the header
    next(reader, None)
    for r in reader:
      print ("cleaning: "+r[0])
      data = Row(r[0])
      if data.dateparser is None:
        data.try_manual()
      else:
        data.use_parser()
        data.set_parsable()

      data.clean()
      print("parsed: "+ str(data.year) + " "+ str(data.month) + " " + str(data.day))
      cleaned_rows.append(data)
     
with open("cleaned.csv", 'wb') as csv_file:
    wr = csv.writer(csv_file, delimiter=',')
    for cdr in cleaned_rows:
      wr.writerow([cdr.data,cdr.year,cdr.month,cdr.day])
