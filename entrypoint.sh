#!/bin/bash

echo "Init Proyect"

if [ -f "$1" ]; then
	chmod +x "$1"
	./"$1"
else
	echo "No exist path '$1'"
	exit 1
fi
