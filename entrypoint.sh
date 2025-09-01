#!/bin/bash

echo "Init Proyect"

if [ -f "$1" ]; then
	chmod +x "$1"
	name=$(echo "$1" | awk -F. '{print $2}')
	echo -e "$name"
	if [[ $name == "sh" ]]; then
		#Execute .sh
		./"$1"
	else
		#Execute .py
		echo "soy .py"
		python "$1"
#	./"$1"
	fi
else
	echo "Path '$1' does not exist"
	exit 1
fi
