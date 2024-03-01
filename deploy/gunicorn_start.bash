//a placer dans /usr/bin et faire chmod +x
//remplacer <user> par l'utilisateur non root
#!/bin/bash

NAME="boxer"                                  # Name of the application
DJANGODIR=/home/dev/<user>/boxerback             # Django project directory
SOCKFILE=/home/<user>/run/gunicorn.sock  # we will communicte using this unix socket
USER=dev                                        # the user to run as
GROUP=dev                                    # the group to run as
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=boxer.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=boxer.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/dev/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/dev/venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-file=/home/<user>/gunicorn.log
