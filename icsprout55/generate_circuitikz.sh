#!/usr/bin/bash

directory="cdl"

for file in "$directory"/* ; do
	if [ -f "$file" ]; then
		export filename="${file%.*}"
		echo "Current netlist: $file"
		python3 write_tikz.py $file > $filename.tex
		mv $filename.tex circuitikz/tex
	fi
done



