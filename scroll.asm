.data
	DISPLAY: .word 0x1000000
.text

#temp1 = arr[i]
#temp2 = arr[i+1]
#arr[i+1] = temp1
#temp1 = temp2


lw $t1, DISPLAY($t0)
mainloop:
	addiu $t0, $t0, 4
	andi $t0, $t0, 	127
	lw $t2, DISPLAY($t0)
	sw $t1, DISPLAY($t0)
	move $t1, $t2
	beq $0, $0, mainloop
