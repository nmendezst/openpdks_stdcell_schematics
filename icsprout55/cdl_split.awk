awk -F '[ (]' '$1 == ".SUBCKT" { file= $2 ".cdl" } file != ""{print > file} $1 == ".ENDS" {close(file); file=""}' ics55_LLSC_H7CR.cdl
