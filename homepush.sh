#!/bin/bash
RAWFILEPATH="$PWD/homes_raw.json"
CLEANFILEPATH="$PWD/homes_clean.json"
CREDSFILEPATH="$PWD/service_creds.json"
PYPATH="$PWD/venv-pipeline/bin/python"

# Doc limit arg passed on command line, but optional
if
		[ $# \> 0 ]; then
		DOCLIMIT=true
fi

# Download documents from Cloudant
curl \
		-u "`$PYPATH get_creds.py $CREDSFILEPATH`" \
		-X GET "https://b0872728-906f-4b36-8ec6-83e7eb5ae492-bluemix.cloudantnosqldb.appdomain.cloud/deathpledge_clean/_all_docs?include_docs=True" \
		-o $RAWFILEPATH

# Ensure cURL completes
if [ $? -eq 0 ]; then
		echo OK
else
		exit
fi

# Process JSON response into JSONlines
if [ "$DOCLIMIT" = true ]; then
		$PYPATH pipeline.py $RAWFILEPATH --outfile=$CLEANFILEPATH --limit=$1
else
		$PYPATH pipeline.py $RAWFILEPATH --outfile=$CLEANFILEPATH
fi

if [ $? -eq 0 ]; then
		echo OK
else
		exit
fi

# Print summary
echo
ls -lh | grep json

# Send to Elasticsearch
curl \
		-H "Content-Type: application/x-ndjson" \
		-XPOST "synapse:9200/homes/_bulk?pretty" \
		--data-binary "@$CLEANFILEPATH"

