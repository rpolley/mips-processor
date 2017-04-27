	ori $sp, $zero, 0x00003ffc
	add  $s0, $zero, 1
	add  $s1, $zero, 2
	
silly:  beq  $s1, $zero, end
	addi $sp, $sp, -4
        sw   $ra, 0($sp)
        jal  silly2
        lw   $ra, 0($sp)
        addi $sp, $sp, 4
        j    silly

silly2: add  $s1, $s1, -1
	jr  $ra 
end:
