#!/bin/bash

set -e

echo "Job started: $(date)"

mongodump --host "$MONGO_HOST" --port "$MONGO_PORT" -u "$MONGO_USER" -p "$MONGO_PASSWORD" --authenticationDatabase admin --gzip --archive="/data/$1_$ENVIRONMENT.gz" -d $1
s3cmd put "/data/$1_$ENVIRONMENT.gz" "s3://$S3_BUCKET"

echo "Job ended: $(date)"
