#!/bin/bash

set -e
export FILE_TO_UPLOAD=rename_email_files_with_request_id.py.zip
rm -f $FILE_TO_UPLOAD
/usr/bin/zip $FILE_TO_UPLOAD rename_email_files_with_request_id.py
echo "$FILE_TO_UPLOAD ready to upload"
