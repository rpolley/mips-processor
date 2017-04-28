.data


	DISPLAY: .word 0x1000000
	INITIAL: .word 0x0,0x7f83bfe,0x10c004,0x230008,0x418010,0x804020,0x418010,0x230008,0x10c004,0x7f83bfe,0x0,0x40a0bf8,0x40a0844,0x40a0842,0x7fbf842,0x40a0842,0x40a0844,0x40a0bf8,0x0,0x7f80bfe,0x1080a0,0x10bfa02,0x900904,0x6008f8,0x0,0x873fbfe,0x8884222,0x8884222,0x8884222,0x8884222,0x70bfa22,0x0

.text



#temp1 = arr[i]
#temp2 = arr[i+1]
#arr[i+1] = temp1
#temp1 = temp2

la $t0, 0
la $t2, 32
init:
	lw $t1, INITIAL($t0)
	la $t1, 0xffffffff
	sw $t1, DISPLAY($t0)
	addiu $t0, $t0, 4
	bne $t0, $t2, init
la $t0, 0

lw $t1, DISPLAY($t0)
mainloop:
	addiu $t0, $t0, 4
	andi $t0, $t0, 	127
	lw $t2, DISPLAY($t0)
	sw $t1, DISPLAY($t0)
	move $t1, $t2
	beq $0, $0, mainloop
