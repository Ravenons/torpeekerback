#!/bin/sh

# Mostly a script which executes normal deploy preceded by static files upload

echo "\n** This script executes manage.py commands, so maybe run virtualenv"
read -p 'Write "deploy" to continue: ' INPUT
if [ "$INPUT" != "deploy" ]; then
    exit 0
fi

# Collect static and upload them to Google Cloud Storage
python manage.py collectstatic --no-input
gsutil -m rsync -r ./static gs://torpeeker/static

gcloud app deploy --version dev
