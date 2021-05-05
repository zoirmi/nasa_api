#!/bin/sh

if [[ -n "$1" ]]; then 
	echo running with query
	python -u nasa_api.py --output db -q $1 
else 
	echo running without query
	python -u nasa_api.py --output db
fi
   	
