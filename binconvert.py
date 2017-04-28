b = open("display.txt", "r")
h = open("display_hex_vals.txt","w")
for line in b:
	h.write(hex(int(line.strip(), 2)))
	h.write("\n")
