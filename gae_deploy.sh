#!/bin/sh

# Mostly a script which executes normal deploy preceded by static files upload

echo "\n** This script executes manage.py commands, so maybe run virtualenv"
echo "** And run clouq_sql_proxy for migrations in production\n"
read -p 'Write "deploy" to continue: ' INPUT
if [ "$INPUT" != "deploy" ]; then
    exit 0
fi

# Collect static and upload them to Google Cloud Storage
python manage.py collectstatic --no-input
gsutil -m rsync -r ./static gs://torpeeker/static

# Migrate, but using production DB through cloud_sql_proxy (lol)
mv torpeekerback/local_settings.py torpeekerback/local_settings.py.bak
cp deploy_resources/local_settings.py torpeekerback/local_settings.py
python manage.py migrate
mv torpeekerback/local_settings.py.bak torpeekerback/local_settings.py

gcloud app deploy --version dev
