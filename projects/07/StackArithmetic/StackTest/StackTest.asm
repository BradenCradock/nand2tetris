@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M + D
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M + D
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M + D
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D = D - M
@PASS0
D;JLT
@SP
M = -1
@END0
0;JMP
(PASS0)
@SP
M = 0
(END0)
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D = D - M
@PASS1
D;JLT
@SP
M = -1
@END1
0;JMP
(PASS1)
@SP
M = 0
(END1)
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D = D - M
@PASS2
D;JLT
@SP
M = -1
@END2
0;JMP
(PASS2)
@SP
M = 0
(END2)
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D = D - M
@PASS3
D;JGT
@SP
M = -1
@END3
0;JMP
(PASS3)
@SP
M = 0
(END3)
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D = D - M
@PASS4
D;JGT
@SP
M = -1
@END4
0;JMP
(PASS4)
@SP
M = 0
(END4)
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D = D - M
@PASS5
D;JGT
@SP
M = -1
@END5
0;JMP
(PASS5)
@SP
M = 0
(END5)
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M + D
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
@SP
AM = M - 1
M =-M
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M & D
@SP
M = M + 1
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M | D
@SP
M = M + 1
@SP
AM = M - 1
M =!M
@SP
M = M + 1
