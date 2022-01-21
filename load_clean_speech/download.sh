#!/bin/bash

mirror="https://azureopendatastorage.blob.core.windows.net/openstt/ru_open_stt_opus"

while true; do
        for file in $(cut -f2 -d' ' small_md5sum.lst); do
                mkdir -p $(dirname ${file})
                wget -O ${file} -c "${mirror}/${file}"
        done

        echo ''
        echo '>>> Checking MD5 digests...'

        small_md5sum -c small_md5sum.lst 1>small_md5sum.log 2>/dev/null
        status=$?

        if test $status -eq 0; then
                rm small_md5sum.log
                echo '>>> Data is downloaded and checked.'
                break
        fi

        for failed in $(grep 'FAILED$' small_md5sum.log | grep -Po '^[^:]+'); do
                echo ">>> MD5 digest for ${failed} is incorrect, the file will be downloaded again."
                rm -f ${failed}
        done

        echo ''
done