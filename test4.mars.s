	ori   $s1, $zero, 3
	addi  $s2, $zero, 1
hello:  addiu $s1, $s1, -1
	sll   $s2, $s2, 1
	bne   $s1, $zero, hello
	
	addiu $s2, $s2, 1
end:	or    $s0, $zero, $s2
