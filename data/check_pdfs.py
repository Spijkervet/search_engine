import os
from tqdm import tqdm
from PyPDF2 import PdfFileReader

rootdir = 'pdf'
deleted = 0
for subdir, dirs, files in os.walk(rootdir):
    total = len(files)
    for file in tqdm(files):
        path = os.path.join(subdir, file)
        # print('opening {}'.format(path))
        try:
            doc = PdfFileReader(open(path, "rb"))
            # print('success - pages: {}'.format(doc.getNumPages()))
        except Exception as e:
            deleted += 1
            # print(e)
            # print('deleting {}'.format(path))
            os.system('rm {}'.format(path))

print('deleted {}/{} files'.format(deleted, total))
