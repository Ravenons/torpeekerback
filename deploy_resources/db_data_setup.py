from django.conf import settings
import sys

from django.contrib.auth.models import User
celery_user = settings.CELERY_TASKS_USER
existing_celery_users = User.objects.filter(username=celery_user)

if len(existing_celery_users) > 1:
    print("There are two Celery users already (WTF?)")
    sys.exit(1)
    
if len(existing_celery_users) == 1:
    user = existing_celery_users[0]
    print("Celery user already existed")
else:
    user = User.objects.create_user(celery_user)
    print("Celery user created")

from rest_framework.authtoken.models import Token
celery_token = settings.CELERY_TASKS_TOKEN
existing_celery_tokens = Token.objects.filter(user=user)

if len(existing_celery_tokens) > 1:
    print("There are two Celery user tokens already (WTF?)")
    sys.exit(1)

if len(existing_celery_tokens) == 1:
    token =  existing_celery_tokens[0]
    token.key = celery_token
    token.save()
    print("Existing token for Celery user was overwritten")
else:
    token = Token.objects.create(user=user, key=celery_token)
    token.save()
    print("Created token for Celery user")
