.text                   # Main.
.globl main

main:

addi $t0, $t0, 5 # 0x00000000
addi $t1, $t1, 2 # 0x00000004
addi $t3, $t3, 0 # 0x00000008

outerloop:
    li $t2, 0 # 0x0000000c
    beq $t3, $t1, exit # 0x00000010

innerLoop:

    add $t2, $t2, 1 # 0x00000014
    bne $t2, $t0, innerLoop # 0x00000018

endInnerLoop:
    addi $t3, $t3, 1 # 0x0000001c
    j outerloop # 0x00000020

exit:
    li $v0, 10 # 0x00000024
    syscall #  0x00000028
