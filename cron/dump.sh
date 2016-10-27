#!/bin/bash

set -e

echo "Job started: $(date)"

echo "$PGHOST:$PGPORT:$PGDATABASE:$PGUSER:$PGPASS" > /root/.pgpass

chmod 600 /root/.pgpass

pg_dump -U "$PGUSER" -h "$PGHOST" -w -c -Fp --compress 4 "$PGDATABASE" > "/data/$PGDATABASE.sql.gz"

s3cmd put "/data/$PGDATABASE.sql.gz" "s3://$S3_BUCKET"

echo "Job finished: $(date)"
