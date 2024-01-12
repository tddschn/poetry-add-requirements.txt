#!/usr/bin/env bash

PARENT_DIR=$(
    cd $(dirname $0)
    pwd
)
REQ_FILE=$PARENT_DIR/req.txt
REQ_FILE_2=$PARENT_DIR/req2.txt
REQ_FILE_REAL_DEPS=$PARENT_DIR/req-real-deps.txt

echo 'testing: comment'
pip install -r "${REQ_FILE_REAL_DEPS}" --dry-run
