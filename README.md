# Cloudant to Elastic
Grab docs from a Cloudant database, prep them for bulk ingest in Elasticsearch

## Authentication
1. Get Cloudant service credentials from the **Service Details** page in IBM Cloud.
2. Copy them and save to a `service_creds.json` file

### Great resources on authentication: 
* [IBM Cloud identity and access management](https://cloud.ibm.com/docs/services/Cloudant/guides?topic=cloudant-ibm-cloud-identity-and-access-management-iam-)
* [Cloudant authentication](https://cloud.ibm.com/docs/services/Cloudant/api?topic=cloudant-authentication)

## Usage
```
# Push a small sampling of documents
./homepush.sh 5

# Or, to push all of them
./homepush.sh
```

When prompted, hit enter to continue.

## Notes
You may need to edit `pipeline.py` shebang to point to the correct python executable
if you intend on running it by itself (for testing), but otherwise the shell
script just calls `python` normally.

## Index mapping
For now, until I put together a good bash script, paste the mapping JSON into the dev console under

```
PUT /homes/home/_mapping
```
because Elasticsearch 6.5 requires the mapping to be defined per `_type` (whereas they did away
with that field in later versions).

