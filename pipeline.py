#!/Volumes/Maxtor/homes/venv-pipeline/bin/python
"""Pipeline for preparing Cloudant bulk documents for Elasticsearch ingest."""

import json
import argparse
import sys

# Read command line arguments
parser = argparse.ArgumentParser(
    description='Process JSON from Cloudant, for Elasticsearch.'
    )
parser.add_argument('inputfile',
                    metavar='INPUT',
                    help='JSON file from Cloudant bulk docs request')
parser.add_argument('--outfile', 
                    metavar='OUTPUT', 
                    default='homes_clean.json',
                    help='JSON file to send to Elasticsearch')
parser.add_argument('--index',
                    nargs='?',
                    default=None,
                    dest='index_name',
                    help='Name of index to send to, if not "homes"')
parser.add_argument('--limit',
                    nargs='?',
                    default=None,
                    dest='doclimit',
                    type=int,
                    help='Number of docs to process for Elasticsearch')

args = parser.parse_args()

# Process
with open(args.inputfile, 'r') as f:
    resp = json.load(f)

# Discard header items (total_rows and offset)
# is now an array of dicts, sliced by doclimit if given
docs = resp['rows'][:args.doclimit]


def prep_doc_for_es(doc):
    """Create action line for elasticsearch ingest for each source doc.

    Future note
    ===========
    Rearrangement of the doc id here to use as the elasticsearch
    metadata _id can also be handled with a pipeline script::

        POST /_ingest/pipeline/deathpledge
        {
          "pipeline": {
            "processors": [
              {
                "script": {
                  "lang": "painless",
                  "source": "ctx['_id'] = ctx['docid'];"
                }
              }
            ]
          }
        }

    """
    source = doc['doc']  # the actual data
    docid = source.pop('_id', None)

    # TODO: set index as whatever the doctype is (from Cloudant)
    # in the future, this will route homes, listings, and scorecards to the appropriate ES indexes
    action = {'index': {'_index': args.index_name, '_id': docid}}
    return action, source

bulk_es_list = []
for doc in docs:
    bulk_es_list.extend(prep_doc_for_es(doc))

# Feedback
print(f'Sample:')
print(json.dumps(bulk_es_list, indent=2)[1:200])
print(f'Docs in list: {len(docs)}')
cont = input('Continue? [Y/n] ')
if cont.upper() == 'N':
    sys.exit(1)

with open(args.outfile, 'w') as f:
    for line in bulk_es_list:
        f.write(json.dumps(line) + '\n')
    # Add final newline for Elasticsearch
    f.write('\n')

