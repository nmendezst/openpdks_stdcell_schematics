#!/usr/bin/bash

directory="Figures"

for file in "$directory"/* ; do
	if [ -f "$file" ]; then
		export filename="${file%.*}"
		echo "Current figure: $file"
		sed -i "20i \\\\\\input{$file}" append.tex
		xelatex -interaction=nonstopmode append.tex
		mv append.pdf $filename.pdf
		mv $filename.pdf ../pdf/	
		sed -i '20d' append.tex
		rm -f *.log
		rm -f *.aux
	fi
done



