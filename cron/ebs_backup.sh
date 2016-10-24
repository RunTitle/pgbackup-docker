#!/bin/bash

set -e

if [ "$ENVIRONMENT" == 'production' ]; then
    automated-ebs-snapshots --region "$AWS_REGION" --access-key-id "$AWS_ACCESS_KEY" --secret-access-key "$AWS_SECRET_KEY" --watch-file /cron/volumes.conf
    automated-ebs-snapshots --region "$AWS_REGION" --access-key-id "$AWS_ACCESS_KEY" --secret-access-key "$AWS_SECRET_KEY" --run
fi;
