#!/bin/bash

set -e

echo "Job started: $(date)"

echo "$PGHOST:$PGPORT:$PGDATABASE:$PGUSER:$PGPASS" > /root/.pgpass

chmod 600 /root/.pgpass

pg_dump -U "$PGUSER" -h "$PGHOST" -w -c -Fp --compress 4 "$PGDATABASE" > "/dump/$PREFIX_$PGDATABASE.sql.gz"

echo "Job finished: $(date)"
