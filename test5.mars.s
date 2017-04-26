add   $s0, $zero, 0x7fffffff
addu $s0, $s0, 1000
andi  $s0, $s0, 0x7fff
sra   $s1, $s0, 8
sltu  $s2, $s1, $s0
sltiu $s2, $s0, 1
 
