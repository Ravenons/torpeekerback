#!/bin/sh
echo "Executing auxiliar deployment script"

cd $DEPLOY_WORKDIR
python manage.py migrate
# Run auxiliar Python script in Django context
python manage.py shell < $DEPLOY_RESOURCES_DIR/db_data_setup.py
