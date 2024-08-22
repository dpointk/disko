#!/bin/bash


for ns in $(kubectl get namespace --no-headers | awk '{print $1}')
do
    for pod in $(kubectl get pods -n $ns --no-headers 2>&1 | grep -v "No resources found" | awk '{print $1}')
    do
        kubectl get pod $pod -n $ns -o jsonpath='{.spec.containers[*].image}'
        echo # Ensure each image is on a new line
    done
done
