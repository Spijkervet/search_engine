import os
import time
import pickle
import shutil
import random
from  urllib.request import urlopen


timeout_secs = 10 # after this many seconds we give up on a paper
if not os.path.exists('pdf'): os.makedirs('pdf')
have = set(os.listdir('pdf')) # get list of all pdfs we already have

numok = 0
numtot = 0
db = pickle.load(open('papers.p', 'rb'))
for pid,j in db.items():

  pdfs = [x['href'] for x in j['links'] if x['type'] == 'application/pdf']
  assert len(pdfs) == 1
  pdf_url = pdfs[0] + '.pdf'
  basename = pdf_url.split('/')[-1]
  fname = os.path.join('pdf', basename)

  # try retrieve the pdf
  numtot += 1
  try:
    if not basename in have:
      print('fetching %s into %s' % (pdf_url, fname))
      req = urlopen(pdf_url, None, timeout_secs)
      with open(fname, 'wb') as fp:
          shutil.copyfileobj(req, fp)
      time.sleep(0.05 + random.uniform(0,0.1))
    else:
      print('%s exists, skipping' % (fname, ))
    numok+=1
  except Exception as e:
    print('error downloading: ', pdf_url)
    print(e)

  print('%d/%d of %d downloaded ok.' % (numok, numtot, len(db)))

print('final number of papers downloaded okay: %d/%d' % (numok, len(db)))


