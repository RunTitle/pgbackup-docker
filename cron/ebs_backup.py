#!/usr/bin/env python
import argparse
import boto3
import datetime
import logging
import os

from dateutil.relativedelta import relativedelta
logging.basicConfig(level=logging.INFO)


class VolumeBackups(object):
    def __init__(self, volume_ids, period, retention, aws_secret_key, aws_access_key, ec2_region):
        self.volume_ids = volume_ids
        self.period = period
        self.retention = retention
        self.aws_secret_key = aws_secret_key
        self.aws_access_key = aws_access_key
        self.ec2_region = ec2_region
        self.now = datetime.datetime.now()

        session = boto3.session.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.ec2_region,
        )

        self.ec2_conn = session.resource('ec2')

        self.backup_count = 0
        self.delete_count = 0

    def update_snapshot_tags(self, snapshot, tags, volume_id):
        tags.extend([
            {'Key': 'Name', 'Value': '{}_snapshot'.format(volume_id)},
            {'Key': 'period', 'Value': self.period},
            {'Key': 'date', 'Value': '{:%Y-%m-%d %H:%M}'.format(self.now)},
        ])
        snapshot.create_tags(Tags=tags)

    def delete_snapshots(self, volume, drop_date):
        for snapshot in volume.snapshots.all():
            snapshot_date = None
            same_period = False
            if not snapshot.tags:
                continue

            for tag in snapshot.tags:
                if tag['Key'] == 'period' and tag['Value'] == self.period:
                    same_period = True
                if tag['Key'] == 'date':
                    try:
                        snapshot_date = datetime.datetime.strptime(tag['Value'], '%Y-%m-%d %H:%M')
                    except ValueError:
                        pass

            if snapshot_date and same_period and snapshot_date < drop_date:
                logging.info(
                    'Delete snapshot {} date {:%Y-%m-%d %H:%M} exceeds {} retention of {}.'.format(
                        snapshot.id, snapshot_date, self.period, self.retention
                    )
                )
                snapshot.delete()
                self.delete_count += 1

    def process(self):
        logging.info(
            'Started taking {} snapshots at {:%Y-%m-%d %H:%M}'.format(
                self.period.replace('s', 'ly'), self.now
            )
        )

        for volume_id in self.volume_ids:
            volume = self.ec2_conn.Volume(volume_id)
            drop_date = self.now - relativedelta(**{self.period: self.retention})
            description = '{}_snapshot {} by snapshot script at {:%Y-%m-%d %H:%M}'.format(
                self.period, volume_id, self.now
            )
            snapshot = volume.create_snapshot(Description=description)
            self.update_snapshot_tags(snapshot=snapshot, tags=volume.tags, volume_id=volume.id)
            self.backup_count += 1
            self.delete_snapshots(volume, drop_date)

        logging.info(
            'Completed taking {} snapshots at {:%Y-%m-%d %H:%M}'.format(
                self.period.replace('s', 'ly'), datetime.datetime.now()
            )
        )
        logging.info(
            'Created {} and deleted {} snapshots.'.format(
                self.backup_count, self.delete_count
            )
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup EBS Volumes')
    parser.add_argument(
        'period', type=str, help='Time period.', choices=['days', 'weeks', 'months']
    )
    args = parser.parse_args()

    retention_key = '{}_RETENTION'.format(args.period.upper())
    volume_ids = os.getenv('BACKUP_VOLUMES')
    if volume_ids:
        vol_backups = VolumeBackups(
            volume_ids=volume_ids,
            period=args.period,
            retention=os.getenv(retention_key, 1),
            aws_access_key=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_key=os.getenv('AWS_SECRET_KEY'),
            ec2_region=os.getenv('AWS_REGION')
        )
        vol_backups.process()
