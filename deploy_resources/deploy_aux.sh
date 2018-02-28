#!/bin/sh
echo "Executing auxiliar deployment script"

# Run auxiliar Python script in Django context

cd $DEPLOY_WORKDIR
python manage.py shell < $DEPLOY_RESOURCES_DIR/db_data_setup.py
