#!/bin/bash

i=0
filename="randomfile"
echo >$filename
for ns in $(kubectl get namespace --no-headers | awk '{print $1}')
do
    # echo -- namespace: $ns --
    for pod in $(kubectl get pods -n $ns --no-headers 2>&1 | grep -v "No resources found" | awk '{print $1}')
    do
        # echo -- pod: $pod --
        kubectl get pod $pod -n $ns -o jsonpath='{.spec.containers[*].image}' >> $filename
        echo >> randomfile
        
        # Increase count
        i=$((i + 1))
        echo -ne "Collecting... $i images  \r"
        
    done
done
