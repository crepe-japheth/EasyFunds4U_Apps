# app/tasks.py
from celery import shared_task

@shared_task
def multiply(a, b):
    return a * b
