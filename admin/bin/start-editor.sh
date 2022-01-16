#!/bin/bash

BASE_DIR=$(cd $(dirname ${BASH_SOURCE[0]}); pwd)
echo "$BASE_DIR"

INI_FILE=$BASE_DIR/../profiler/resources/rca_config.ini

function get_prop_value {
    KEY=$1
    DEFAULT=$2
    VALUE=$(grep -v '#' $INI_FILE | grep "^$1" | cut -d'=' -f2 | tr -d '[:space:]')
    if [[ -z $VALUE && -n $DEFAULT ]]
    then
        VALUE=$DEFAULT
    fi
    echo $VALUE
}

BIND_ADDRESS=$(get_prop_value bind_address 0.0.0.0)
PORT=$(get_prop_value port 8053)

BIND_OPTS="--bind $BIND_ADDRESS:$PORT"

# Parse optional SSL parameters
PROTOCOL=$(get_prop_value protocol)
KEY_FILE=$(get_prop_value key_file)
CERT_FILE=$(get_prop_value cert_file)

SSL_OPTS=

if [[ $PROTOCOL == "https" || $PROTOCOL == "HTTPS" ]]; then
  if [[ -z $KEY_FILE || -z CERT_FILE ]]; then
    echo "SSL is enabled.  You must specify both key_file and cert_file properties under the [server] section in $INI_FILE".
    exit 1
  fi
  SSL_OPTS="--keyfile $KEY_FILE --certfile $CERT_FILE"
fi

# Parse optional log file path
LOG_FILE=$(get_prop_value log_file $BASE_DIR/../logs/profiler.log)

PYTHON3=$BASE_DIR/../python3

GUNICORN_CMD="PYTHONPATH=$BASE_DIR/../profiler $PYTHON3/bin/python -m gunicorn.app.wsgiapp prof:app.server"
PROFILER_CMD="$GUNICORN_CMD $BIND_OPTS $SSL_OPTS --timeout 120 --log-file $LOG_FILE --capture-output --daemon"

echo "Starting Unravel Profiler: $PROFILER_CMD"
eval $PROFILER_CMD
echo
echo "To see the log: tail -f $LOG_FILE"
echo "To stop Unravel Profiler: ./stop-profiler.sh"
