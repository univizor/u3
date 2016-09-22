#!/usr/bin/env bash
set -e

END=2016
for ((i=2000;i<=END;i++)); do
	documents=`grep -lir $i ./data/first-pages | wc -l`
	echo $i $documents
done
