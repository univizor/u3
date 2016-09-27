#!/usr/bin/env bash
set -e

USER=$HADOOP_USER
PASS=$HADOOP_PASS
WEBHDFS_URL=$HADOOP_WEBHDFS_URL

function create_file_location {
  REMOTE_PATH=$1
  CREATE_OUT=`curl -i -L -k -s --user $USER:$PASS \
    --max-time 45 --max-redirs 1 -X PUT "$WEBHDFS_URL/user/$USER/$REMOTE_PATH?op=CREATE&overwrite=true" | grep -oE 'Location: .*' | sed 's/Location: //' | tr -d '\r' | tr -d '\n'`
  curl -i -s --user $USER:$PASS -X PUT -T $1 "$CREATE_OUT" | grep Created
}

create_file_location $1
