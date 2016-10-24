# pgbackup-docker
General Cron Jobs, originally for postgres backups.

Requires the following environment variables.

AWS_OWNER
AWS_SECRET_KEY
AWS_ACCESS_KEY
AWS_REGION
ENVIRONMENT
S3_BUCKET = location for backup file
PGDATABASE = postgres db being backed up
PGHOST = postgres host
PGUSER = postgres user
PGPORT = postgress port
PGPASS = postgress password
PREFIX = prefix for backup filename
