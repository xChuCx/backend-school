#!/bin/bash

echo 'Launching couchbase' &&
/usr/sbin/runsvdir-start &

(
    resp=0; \
    while [ $resp != "200" ]; do \
        sleep 0.1; \
        resp=`curl -A "Web Check" -sL --connect-timeout 1 -w "%{http_code}\n" "http://0.0.0.0:8091" -o /dev/null`; \
    done
) &&

echo 'Check cluster' &&
list=$(couchbase-cli server-list -c 0.0.0.0 -u Administrator -p password)
echo "$list"
if [[ $list == ERROR* ]]
then
    (
         echo 'Configuring new Couchbase' &&
         echo 'Creating cluster' &&
         couchbase-cli cluster-init -c 0.0.0.0:8091 --cluster-username=Administrator --cluster-password=password --cluster-ramsize=512 --cluster-index-ramsize=512 --cluster-fts-ramsize=256 --services=data,index,query,fts &&
         echo 'Creating analitycDB bucket' &&
         couchbase-cli bucket-create -c 0.0.0.0:8091 -u Administrator -p password --bucket=analitycDB --bucket-type=couchbase --bucket-ramsize=300 &&
         echo 'Creating a user to give the gateway an access to the bucket' &&
         couchbase-cli user-manage -c 0.0.0.0 -u Administrator -p password --set --rbac-username APP --rbac-password APPpwd --roles admin --auth-domain local
    )
fi
echo 'Initialization done'
tail -f /opt/couchbase/var/lib/couchbase/logs/error.log