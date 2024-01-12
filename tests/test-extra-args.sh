#!/usr/bin/env bash

PARENT_DIR=$(
    cd $(dirname $0)
    pwd
)
REQ_FILE=$PARENT_DIR/req.txt
REQ_FILE_2=$PARENT_DIR/req2.txt

echo 'testing: --dry-run'
poeareq "${REQ_FILE}" --dry-run

echo 'testing: --poetry-args'
poeareq "${REQ_FILE}" --dry-run --poetry-args "--arg1 arg2 arg3 -a4"

echo 'testing: --poetry-args in the middle' # this won't work, positional args get into poetry args
poeareq "${REQ_FILE}" --dry-run --poetry-args "--arg1 arg2 arg3 -a4" -D "${REQ_FILE_2}"

echo 'testing: multiple req files'
poeareq "${REQ_FILE}" "${REQ_FILE_2}" --dry-run

echo 'testing: multiple req files with -D'
poeareq "${REQ_FILE}" "${REQ_FILE_2}" --dry-run -D

echo 'testing: multiple req files, passing --dry-run to poetry'
poeareq "${REQ_FILE}" "${REQ_FILE_2}" --dry-run -p --dry-run --extras=EXTRAS
