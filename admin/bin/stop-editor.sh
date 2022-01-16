#!/usr/bin/env bash

function kill_and_wait {
  local NAME=$1
  local PATTERN=$2
  local SIGNAL=$3
  local NUM_TRIES=$4

  KILL_CMD="pkill -$SIGNAL -f \"$PATTERN\""
  echo -n "Stopping $NAME..."
  eval $KILL_CMD

  PGREP_CMD="pgrep -f \"$PATTERN\""

  for i in $(seq 1 $NUM_TRIES); do
    PIDS=$(${!PGREP_CMD})
    if [ -z "$PIDS" ]; then
      echo "  $NAME was stopped"
      exit 0
    fi
    sleep 1
    echo -n '.'
  done

  echo "Failed to stop $NAME gracefully"
  echo -n "Force stopping $NAME..."
  FORCE_KILL_CMD="pkill -SIGKILL -f \"$PATTERN\""
  eval $FORCE_KILL_CMD
  PIDS=$(${!PGREP_CMD})
  if [ -z "$PIDS" ]; then
    echo "  $NAME was stopped forcefully"
    exit 0
  else
    echo "  Failed to force stop $NAME"
    exit 1
  fi
}

kill_and_wait Profiler "prof:app.server" SIGKILL 30