import os
import time
import pickle
import shutil
import random
from  urllib.request import urlopen
import time

from multiprocessing.pool import ThreadPool


class PDF:
    def __init__(self, url, basename, fname):
        self.url = url
        self.basename = basename
        self.fname = fname

def get_urls(db):
    pdf_links = []
    for pid, j in db.items():
        pdfs = [x['href'] for x in j['links'] if x['type'] == 'application/pdf']
        assert len(pdfs) == 1
        pdf_url = pdfs[0] + '.pdf'
        basename = pdf_url.split('/')[-1]
        fname = os.path.join('pdf', basename)
        pdf_links.append(PDF(pdf_url, basename, fname))
    return pdf_links

def fetch_pdf(pdf):
    global numok, numtot
    pdf_url = pdf.url
    basename = pdf.basename
    fname = pdf.fname
    numtot += 1
    # try retrieve the pdf
    error = 0
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
        print('%d/%d of %d downloaded ok.' % (numok, numtot, len(db) - len(have)))
    except Exception as e:
        print('error downloading: ', pdf_url)
        print(e)
        error = 1
    return fname, error


def main():
    pdf_links = get_urls(db)
    results = ThreadPool(4).imap_unordered(fetch_pdf, pdf_links)
    err = 0
    for path, error in results:
        if not error:
            print('downloaded', path)
        else:
            err = 1
            break

    if err:
        # 5 min sleep
        print('ERROR, SLEEPING')
        time.sleep(30)
        main()
    print('final number of papers downloaded okay: %d/%d' % (numok, len(db)))




if __name__ == '__main__':
    numok = 0
    numtot = 0
    timeout_secs = 10 # after this many seconds we give up on a paper
    if not os.path.exists('pdf'): os.makedirs('pdf')
    have = set(os.listdir('pdf')) # get list of all pdfs we already have
    db = pickle.load(open('papers.p', 'rb'))
    main()
