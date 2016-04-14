import os
from queued.manager import QueuedManager


def update_queue():
    update_queue = 'generate_clusters'
    queue_manager = QueuedManager(
        config={'env': os.getenv('ENVIRONMENT')},
        aws_owner=os.getenv('AWS_OWNER'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        application='titletime',
        subscriptions=[],
        publications=[]
    )
    message = {'task': 'update_queue'}
    queue_manager.publish_message(name=update_queue, raw_message=message)

if __name__ == '__main__':
    update_queue()
