#!/bin/sh

# If there's a prestart.sh script in the /app directory or other path specified, run it before starting
PRE_START_PATH=${PRE_START_PATH:-/code/app/prestart.sh}
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi

#export APP_MODULE=${APP_MODULE-app.main:app}
#export HOST=${HOST:-0.0.0.0}
#export PORT=${PORT:-8001}


# run gunicorn
#exec gunicorn --bind $HOST:$PORT "$APP_MODULE" -k uvicorn.workers.UvicornWorker
exec fastapi run /code/app/app.py --port "${FASTAPI_PORT}"
