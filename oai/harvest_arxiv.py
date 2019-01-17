#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# arXiv harvester - Fetches metadata from arXiv for article metadata.
#------------------------------------------------------------------------------
# Copyright (c) 2015 University of Helsinki
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#------------------------------------------------------------------------------

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import argparse
import time
import sys
import os

#------------------------------------------------------------------------------

# Harvest from given set, e.g. cs=computer science
# see http://export.arxiv.org/oai2?verb=ListSets
harvest_set = "cs"

# Harvest result format, see http://arxiv.org/help/oa/index
# and http://export.arxiv.org/oai2?verb=ListMetadataFormats
harvest_format = "oai_dc"

# Base API url
harvest_base_url = "http://export.arxiv.org/oai2"

# API request for getting records, see documentation at
# http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#ListRecords
harvest_url = harvest_base_url + "?verb=ListRecords" \
              "&set={0}&metadataPrefix={1}". \
              format(harvest_set, harvest_format)

harvest_url_continue = harvest_base_url + "?verb=ListRecords&resumptionToken={0}"

sleep_time = 2

#------------------------------------------------------------------------------

def fetch(resumptionToken = "", part=0, from_date="", outdir=""):
    # Set to starting url, or use the resumptionToken if that is set
    get_url = harvest_url

    # Set from date if given
    if from_date:
        get_url += "&from=" + from_date

    # If a resumption token is given, we use that only
    if resumptionToken:
        get_url = harvest_url_continue.format(urllib.parse.quote(resumptionToken))

    try:
        # Request from API
        print("GET", get_url)
        response = urllib.request.urlopen(get_url)
        data = response.read()

        # Parse XML
        root = ET.fromstring(data)

        # Get resumptionToken element from the XML
        namespaces = {'oai': 'http://www.openarchives.org/OAI/2.0/'}
        rtNode = root.find('./oai:ListRecords/oai:resumptionToken', namespaces)

        cursor = 0
        resumptionToken = None

        if rtNode is not None:
            resumptionToken = rtNode.text
            cursor = rtNode.attrib['cursor']

        # Form filename
        if outdir != '' and outdir[-1] != '/':
            outdir += '/'
        filename = outdir + "arxiv-{0}-{1}-cursor{2}.xml".format(harvest_set,
                                                                 harvest_format,
                                                                 cursor)
        # Write to file
        print("Writing to", filename)
        with open(filename, 'wb') as fp:
            fp.write(data)

        if not resumptionToken:
            print("No resumptionToken, stopping ...")
            return 1

        print("Sleeping {0} seconds ...".format(sleep_time))
        time.sleep(sleep_time)
        return fetch(resumptionToken, part + 1, "", outdir)

    except urllib.error.HTTPError as error:
        # If we are fetching too fast the server will give an HTTP 503
        # then we just wait the specified time and try again
        if error.code == 503:
            h = error.headers
            if 'retry-after' in h:
                ra = int(h['retry-after'])
                print("Got HTTP 503, Retry-after: {0}".format(ra))
                print("Sleeping {0} seconds ...".format(ra))
                time.sleep(ra)
                return fetch(resumptionToken, part, from_date)

        # Any other errors than 503 are fatal.
        print("ERROR: HTTP returned status {0}!".format(rstat))
        return 1

#------------------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--resumptionToken', metavar='TOKEN')
    parser.add_argument('-d', '--outdir', metavar='DIR',
                        help='place xml files in this directory')
    parser.add_argument('-f', '--from', dest='from_date', metavar='DATE',
                        help='Fetch records updated since FROM datestamp, ' +
                        'e.g. "2014-12-01"')
    args = parser.parse_args()

    if args.resumptionToken:
        fetch(args.resumptionToken, outdir=args.outdir)
    elif args.from_date:
        fetch("", 0, args.from_date, outdir=args.outdir)
    else:
        fetch(outdir=args.outdir)


