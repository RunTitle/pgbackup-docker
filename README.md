# pgbackup-docker
postgres backup and s3 sync docker image

Requires the following environment variables.

AWS_SECRET_KEY
AWS_ACCESS_KEY
S3_BUCKET = location for backup file
PGDATABASE = postgres db being backed up
PGHOST = postgres host
PGUSER = postgres user
PGPORT = postgress port
PGPASS = postgress password
PREFIX = prefix for backup filename
