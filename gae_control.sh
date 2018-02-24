#!/bin/sh

# Stop App Engine app (dev version) & first listed Cloud SQL

FIRST_LISTED_SQL=$(gcloud sql instances list \
                   | head -2 | tail -1 | cut -d" " -f 1)

case $1 in
        start)
                gcloud sql instances patch $FIRST_LISTED_SQL \
                                           --activation-policy ALWAYS
                gcloud --quiet app versions start dev
                ;;
        stop)
                gcloud --quiet app versions stop dev
                gcloud sql instances patch $FIRST_LISTED_SQL \
                                           --activation-policy NEVER
                ;;
        *)
                echo "./gae_control.sh <start, stop>"
                ;;
esac
