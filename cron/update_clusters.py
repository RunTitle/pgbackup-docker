#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from queued.manager import QueuedManager


def update_queue():
    update_queues = ['generate_clusters', 'calculate_daily_metrics']
    queue_manager = QueuedManager(
        config={'env': os.getenv('ENVIRONMENT', 'development')},
        aws_owner=os.getenv('AWS_OWNER'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        application='titletime',
        subscriptions=['generate_clusters', 'calculate_daily_metrics'],
        publications=['generate_clusters', 'calculate_daily_metrics']
    )
    message = {'task': 'update_queue'}
    for update_queue in update_queues:
        queue_manager.publish_message(name=update_queue, raw_message=message)

if __name__ == '__main__':
    update_queue()
