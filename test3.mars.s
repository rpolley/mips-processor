	add $s0, $zero, 8
	sll $s1, $s0, 2
label1:	srl $s1, $s1, 4
	or $s2, $s1, $s0
	bgezal $s1, label2
	addiu  $s2, $s1, 1000

label2: bne $s2, $s0, label1
	add $s2, $s2, -1
	slt $s1, $s2, $s0
