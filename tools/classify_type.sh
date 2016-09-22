#!/usr/bin/env bash
set -e

declare -a types=("diplomsko" "magistrsko" "doktorska" "projekt")
for i in "${types[@]}"; do
	documents=`grep -lir $i ./data/first-pages | wc -l`
	echo $i $documents
done
