# openpdks stdcell schematics

Transistor level schematics of standard cells for each PDK available. Schematics are drawn with [circuitikz](https://github.com/circuitikz/circuitikz) from the SPICE/CDL circuit description. Functional/logic schematics are generated with yosys + [netlistsvg](https://github.com/nturley/netlistsvg) from Verilog description.

Structure:

```
PDK/
├──	circuitikz/
|	├── pdf/
|	├── svg/
|	└── tex/
├── netlistsvg/
| 	├── json/
|	└── svg/
├──	spice/cdl/
└── verilog/
```

## GF180MCU

Standard cell count: 

## ICSprout55

Standard cell count: 748

## IHP-SG13G2

Standard cell count: 84

## SKY130

Standard cell count: 437

### Notes

This website made by Graham Petley was (is) super helpful to get a consistent style.

[VLSI and ASIC Technology Standard Cell Library Design](https://www.vlsitechnology.org/index.html)

Old datasheets (Fairchild, Motorola, TI) found in [bitsavers.org](https://bitsavers.org/components/)

[`NOT`, `NOR`, `NAND` gates](https://www.ti.com/lit/ds/symlink/cd4572ub.pdf)

`awk` script adapted from [here](https://community.unix.com/t/perl-help-to-split-big-verilog-file-into-smaller-ones-for-each-module/239951/7)
