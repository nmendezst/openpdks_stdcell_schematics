#!/usr/bin/bash

directory=../pdf

for file in "$directory"/* ; do
	if [ -f "$file" ]; then
		export filename="${file%.*}"
		echo "Converting $filename PDF to SVG: $filename.svg"
		pdf2svg $file $filename.svg
		mv $filename.svg .
	fi
done



