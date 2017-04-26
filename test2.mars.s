
	addi $s0, $zero, 5
	addi $s1, $zero, 10
label1:	
	beq $s0, $s1, label2
	add $s0, $s0, 1
	j label1

label2: 
	
