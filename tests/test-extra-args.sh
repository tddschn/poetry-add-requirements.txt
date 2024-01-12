#!/usr/bin/env bash

PARENT_DIR=$(
    cd $(dirname $0)
    pwd
)
REQ_FILE=$PARENT_DIR/req.txt

echo 'testing: --dry-run'
poeareq "${REQ_FILE}" --dry-run # --extra-args "--arg1 arg2 arg3 -a4"

echo 'testing: --poetry-args'
poeareq "${REQ_FILE}" --dry-run --poetry-args "--arg1 arg2 arg3 -a4"
