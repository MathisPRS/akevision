from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'update_ssl_expiration': {
        'task': 'akevision_rest.async_service.update_ssl_expiration',
        'schedule': crontab(hour=1, minute=0),
    },
    
    
}
