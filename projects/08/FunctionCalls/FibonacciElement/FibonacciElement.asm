@256
D = A
@SP
M = D
@RA$0
D = A
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
@5
D = A
@SP
D = M - D
@ARG
M = D
@SP
D = M
@LCL
M = D
@Sys.init
0;JMP
(RA$0)
(Main.fibonacci)
@ARG
D = M
@0
A = D + A
D = M
@SP
A = M
M = D
@SP
M = M + 1
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D = M - D
@PASS$0
D;JLT
D = 0
@END$0
0;JMP
(PASS$0)
@SP
D = -1
(END$0)
@SP
A = M
M = D
@SP
M = M + 1
@SP
AM = M - 1
D = M
@IF_TRUE
D;JNE
@IF_FALSE
0;JMP
(IF_TRUE)
@ARG
D = M
@0
A = D + A
D = M
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@R14
M = D
@5
A = D - A
D = M
@R15
M = D
@SP
AM = M - 1
D = M
@ARG
A = M
M = D
D = A
@SP
M = D + 1
@R14
M = M - 1
A = M
D = M
@THAT
M = D
@R14
M = M - 1
A = M
D = M
@THIS
M = D
@R14
M = M - 1
A = M
D = M
@ARG
M = D
@R14
M = M - 1
A = M
D = M
@LCL
M = D
@R15
A = M
0;JMP
(IF_FALSE)
@ARG
D = M
@0
A = D + A
D = M
@SP
A = M
M = D
@SP
M = M + 1
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M - D
@SP
M = M + 1
@RA$1
D = A
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
@6
D = A
@SP
D = M - D
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0;JMP
(RA$1)
@ARG
D = M
@0
A = D + A
D = M
@SP
A = M
M = D
@SP
M = M + 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M - D
@SP
M = M + 1
@RA$2
D = A
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
@6
D = A
@SP
D = M - D
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0;JMP
(RA$2)
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M + D
@SP
M = M + 1
@LCL
D = M
@R14
M = D
@5
A = D - A
D = M
@R15
M = D
@SP
AM = M - 1
D = M
@ARG
A = M
M = D
D = A
@SP
M = D + 1
@R14
M = M - 1
A = M
D = M
@THAT
M = D
@R14
M = M - 1
A = M
D = M
@THIS
M = D
@R14
M = M - 1
A = M
D = M
@ARG
M = D
@R14
M = M - 1
A = M
D = M
@LCL
M = D
@R15
A = M
0;JMP
@256
D = A
@SP
M = D
@RA$3
D = A
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
@5
D = A
@SP
D = M - D
@ARG
M = D
@SP
D = M
@LCL
M = D
@Sys.init
0;JMP
(RA$3)
(Sys.init)
@4
D = A
@SP
A = M
M = D
@SP
M = M + 1
@RA$4
D = A
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
@6
D = A
@SP
D = M - D
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0;JMP
(RA$4)
(WHILE)
@WHILE
0;JMP
