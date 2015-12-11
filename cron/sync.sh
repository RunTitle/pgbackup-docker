#!/bin/bash

set -e

echo "Job started: $(date)"

s3cmd put "/data/$PGDATABASE.sql.gz" "s3://$S3_BUCKET"

echo "Job finished: $(date)"
