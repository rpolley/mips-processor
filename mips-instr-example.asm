sll $t1, $t2, 10
srl $t1, $t2, 10
sra $t1, $t2, 10
add $t1, $t2, $t3
addu $t1, $t2, $t3
addi $t1, $t2, 10
addiu $t1, $t2, 10
jal a
a:jr $t1
j b
b: slt $t1, $t2, $t3
sltu $t1, $t2, $t3
sltiu $t1, $t2, 10
slti $t1, $t2, 10
and $t1, $t2, $t3
or $t1, $t2, $t3
andi $t1, $t2, 10
ori $t1, $t2, 10
lui $t1, 10
lw $t1, 0($t2)
sw $t1, 0($t2)
beq $t1,$t2, a
bne $t1, $t2, a
bgezal $t1, a