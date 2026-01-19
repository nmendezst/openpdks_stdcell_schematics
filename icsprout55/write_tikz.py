import pandas as pd
import math
import sys

# Ask for filename

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            content = f.read()
    #        print(f"Content of {filename}:\n{content}")
    except FileNotFoundError:
        print(f"Error: SPICE file '{filename}' not found.")
    except IndexError:
        print("Usage: python write_tikz.py <filename>")

def nearest_square(num):
  if num < 0:
    # For negative numbers, the nearest square is often considered 0.
    return 0
  
  # Calculate the square root of the number
  sqrt_num = math.sqrt(num)
  
  # Round the square root to the nearest integer
  rounded_sqrt = round(sqrt_num)
  
  # Square the rounded integer to get the nearest perfect square
  return rounded_sqrt ** 2
 
# Read just for get row length
df0 = pd.read_csv(filename)

row_length = df0.shape[0]

#print(row_length)

# Dataframe
df = pd.read_csv(filename, sep=' ', skiprows=[0, 1, row_length], header=None, names=['device_label', 'drain', 'gate', 'source', 'bulk', 'device', 'width', 'length', 'null0', 'null1', 'null2', 'null3', 'null4', 'null5'])

# Print as csv with custom header
#print(df.head())

# Count rows
num_dev = len(df)
#print(f"Number of devices using len(): {num_dev}")

num_nmos = (df['device'].str.contains('nm').sum())
#print(f"Number of NMOS transistors: {num_nmos}")

num_pmos = (df['device'].str.contains('pm').sum())
#print(f"Number of PMOS transistors: {num_pmos}")

num_dev_near = nearest_square(num_dev)
#print(f"Nearest square for amount of devices: {num_dev_near}")

# Generate list of coordinates for nearest square

coordinate = []

# 2 for a perfect square, nodes too close #og num_dev
y = 1
while y < num_dev*2 + 2:  
    x = 2
    while x < num_dev*2 + 3:
        coordinate.append((x,y))
        x += 3	# Horizontal space between transistors must be 3 to avoid overlap of node labels
    coordinate.append((x,y))
    y += 2	# Vertical space of 3, bug when there is 4 devices, change to 2

def circuitikz_header():
	print("\\begin{circuitikz}[american]")
	print("\\ctikzset{monopoles/vcc/arrow={Bar[width=5mm]}}")
	print("\\ctikzset{tripoles/mos style/arrows}")
	print("\\ctikzset{legacy transistors text}")
	print()
	print("% rm (Computer Modern), sf(Sans Serif), tt(Typewriter)")
	print("\\ttfamily")
	print()
	print("%||||||||||||||||||||Guidelines||||||||||||||||||||")
	print()
	print("\\iftrue")
	print("\\foreach \\x in {0,...,25}{")
	print("\t\\draw [dashed, gray!50] (\\x,0) node [red] {\\x} -- (\\x,25) node [red] {\\x};")
	print("}")
	print("\\foreach \\y in {0,...,25}{")
	print("\t\\draw [dashed, gray!50] (0,\\y) node [red] {\\y} -- (25,\\y) node [red] {\\y};")
	print("}")
	print("\\fi")

def transistors_header():
	print()
	print("%||||||||||||||||||||Transistors||||||||||||||||||||")
	print()
	print("\\draw")

def nodes_header():
	print()
	print("%||||||||||||||||||||Nodes||||||||||||||||||||")
	print()
	print("\\iftrue")
	
def wiring_header():
	print("\\fi")				
	print()
	print("%||||||||||||||||||||Wiring||||||||||||||||||||")
	print()

def supply_header():
	print("%||||||||||||||||||||Supply||||||||||||||||||||")
	print()
	
def circuitikz_footer():
	print(";")
	print()
	print("\\end{circuitikz}")
	
terminals = ["D", "G", "S", "bulk"]
terminals_interchanged = ["S", "G", "D", "bulk"]
terminals_inv = ["in", "out"]
terminals_tg = ["down", "up", "in", "out"]
terminals_tsinv = ["in", "up", "down", "out"]
orientation_pmos = ["below", "left", "above", "right"]
orientation_nmos = ["above", "left", "below", "right"]
orientation_pmos_interchanged = ["above", "left", "below", "right"]
orientation_nmos_interchanged = ["below", "left", "above", "right"]
orientation_inv = ["left", "right"]
orientation_tg = ["below", "above", "left", "right"]
orientation_tsinv = ["left", "above", "below", "right"]
# Location of node labels in dataframe
label_columns = [1, 2, 3, 4]
label_inv = [1, 4]
label_tsinv = [1, 2, 3, 6]

def current_device(i):
	return df.iloc[i,5]

def top_device(i):
	return df.iloc[i,8]

def top_device_inv(i):
	return df.iloc[i,6]
	
def device_label(i):
	return df.iloc[i,0]
	
def width(i):
	return df.iloc[i,6]
	
def length(i):
	return df.iloc[i,7]

def inv_pwidth(i):
	return df.iloc[i,8]

def inv_plength(i):
	return df.iloc[i,7]

def inv_nwidth(i):
	return df.iloc[i,10]

def inv_nlength(i):
	return df.iloc[i,9]
	
def top_pwidth(i):
	return df.iloc[i,10]

def top_plength(i):
	return df.iloc[i,9]

def top_nwidth(i):
	return df.iloc[i,12]

def top_nlength(i):
	return df.iloc[i,11]
	
def draw_nmos(i,j):
	print (f"\t{j} node [nmos, bulk] ({device_label(i)}) {{{device_label(i)}}} node [above right] {{\\tiny {{{width(i)} {length(i)}}}}}")
	
def draw_pmos(i,j):
	print (f"\t{j} node [pmos, bulk] ({device_label(i)}) {{{device_label(i)}}} node [above right] {{\\tiny {{{width(i)} {length(i)}}}}}")	
	
def draw_inv(i,j):
	print (f"\t{j} node [ieeestd not port] ({device_label(i)}) {{{device_label(i)}}} node [above right, align=left, font=\\tiny, outer sep=3pt] {{{inv_pwidth(i)} {inv_plength(i)} \\\\ {inv_nwidth(i)} {inv_nlength(i)}}}")

def draw_tg(i,j):
	print (f"\t{j} node [ieeestd tgate] ({device_label(i)}) {{{device_label(i)}}} node [above right, align=left, font=\\tiny, outer sep=3pt] {{{top_pwidth(i)} {top_plength(i)} \\\\ {top_nwidth(i)} {top_nlength(i)}}}") 
	
def draw_tsinv(i,j):
	print (f"\t{j} node [ieeestd not port, fill=cyan] ({device_label(i)}) {{{device_label(i)}}} node [above right, align=left, font=\\tiny, outer sep=3pt] {{{top_pwidth(i)} {top_plength(i)} \\\\ {top_nwidth(i)} {top_nlength(i)}}}") 

def node_label(i,l):
	return df.iloc[i,l]
	
def draw_nodes(i,j,k,l):
	print(f"\t({device_label(i)}.{j}) node [{k}]	{{{node_label(i,l)}}}")

def mos_source(i):
	return df.iloc[i,3]
	
def mos_gate(i):
	return df.iloc[i,2]
	
def mos_drain(i):
	return df.iloc[i,1]
	
def inv_power(i):
	return df.iloc[i,2]

def inv_ground(i):
	return df.iloc[i,3]

def inv_input(i):
	return df.iloc[i,1]

def inv_output(i):
	return df.iloc[i,4]	

def draw_supply(i):
#	if "pm" or "nm" in current_device(i):
		for i in range(num_dev):
			match mos_source(i):	
				case "VDD":
					print(f"\t({device_label(i)}.S) node [vdd] (VDD) {{VDD}}")
				case "VSS":
					print(f"\t({device_label(i)}.S) node [ground] {{}}")
										
def inv_draw_supply(i):
#	if "INV" in top_device_inv(i):
		for i in range(num_dev):
			if "VDD" in inv_power(i) and "VSS" in inv_ground(i):
					print(f"\t({device_label(i)}.up) node [vdd] (VDD) {{VDD}}")
					print(f"\t({device_label(i)}.down) node [ground] {{}}")	
					
def top_draw_supply(i):
#	if "TG" or "TSINV" in top_device(i):
		for i in range(num_dev):
			match mos_source(i):
				case "VDD":
					print(f"\t({device_label(i)}.up) node [vdd] (VDD) {{VDD}}")
				case "VSS":
					print(f"\t({device_label(i)}.down) node [ground] {{}}")	
					
circuitikz_header()
transistors_header()
			
for i,j in zip(range(num_dev), coordinate):
		match current_device(i):
			case pfet if "pm" in current_device(i):
				draw_pmos(i,j)
			case nfet if "nm" in current_device(i):
				draw_nmos(i,j)

for i,j in zip(range(num_dev), coordinate):
		match top_device_inv(i):
			case "INV":
				draw_inv(i,j)

for i,j in zip(range(num_dev), coordinate):		
		match top_device(i):
			case TG if "TG" in top_device(i):
				draw_tg(i,j)
			case TSINV if "TSINV" in top_device(i):
				draw_tsinv(i,j)
				
nodes_header()

for i in range(num_dev):
	match current_device(i):
		case pfet if "pm" in current_device(i):
			for j, k, l in zip(terminals, orientation_pmos, label_columns):
				draw_nodes(i,j,k,l)
		case nfet if "nm" in current_device(i):
			for j, k, l in zip(terminals, orientation_nmos, label_columns):
				draw_nodes(i,j,k,l)

for i in range(num_dev):
	match top_device_inv(i):
		case "INV":
			for j, k, l in zip(terminals_inv, orientation_inv, label_inv):
				draw_nodes(i,j,k,l)
				
for i in range(num_dev):
	match top_device(i):
		case TG if "TG" in top_device(i):
			for j, k, l in zip(terminals_tg, orientation_tg, label_columns):
				draw_nodes(i,j,k,l)
		case TSINV if "TSINV" in top_device(i):
			for j, k, l in zip(terminals_tsinv, orientation_tsinv, label_tsinv):
				draw_nodes(i,j,k,l)
				
wiring_header()
supply_header()
draw_supply(i)
inv_draw_supply(i)
circuitikz_footer()

