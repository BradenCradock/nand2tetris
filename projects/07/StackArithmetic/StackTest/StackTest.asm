@17
D = A
@SP
A = M
M = D
@SP
M = M + 1
@17
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
@PASS0
D;JEQ
D = 0
@END0
0;JMP
(PASS0)
@SP
D = -1
(END0)
@SP
A = M
M = D
@SP
M = M + 1
@17
D = A
@SP
A = M
M = D
@SP
M = M + 1
@16
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
@PASS1
D;JEQ
D = 0
@END1
0;JMP
(PASS1)
@SP
D = -1
(END1)
@SP
A = M
M = D
@SP
M = M + 1
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
@17
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
@PASS2
D;JEQ
D = 0
@END2
0;JMP
(PASS2)
@SP
D = -1
(END2)
@SP
A = M
M = D
@SP
M = M + 1
@892
D = A
@SP
A = M
M = D
@SP
M = M + 1
@891
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
@PASS3
D;JLT
D = 0
@END3
0;JMP
(PASS3)
@SP
D = -1
(END3)
@SP
A = M
M = D
@SP
M = M + 1
@891
D = A
@SP
A = M
M = D
@SP
M = M + 1
@892
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
@PASS4
D;JLT
D = 0
@END4
0;JMP
(PASS4)
@SP
D = -1
(END4)
@SP
A = M
M = D
@SP
M = M + 1
@891
D = A
@SP
A = M
M = D
@SP
M = M + 1
@891
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
@PASS5
D;JLT
D = 0
@END5
0;JMP
(PASS5)
@SP
D = -1
(END5)
@SP
A = M
M = D
@SP
M = M + 1
@32767
D = A
@SP
A = M
M = D
@SP
M = M + 1
@32766
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
@PASS6
D;JGT
D = 0
@END6
0;JMP
(PASS6)
@SP
D = -1
(END6)
@SP
A = M
M = D
@SP
M = M + 1
@32766
D = A
@SP
A = M
M = D
@SP
M = M + 1
@32767
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
@PASS7
D;JGT
D = 0
@END7
0;JMP
(PASS7)
@SP
D = -1
(END7)
@SP
A = M
M = D
@SP
M = M + 1
@32766
D = A
@SP
A = M
M = D
@SP
M = M + 1
@32766
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
@PASS8
D;JGT
D = 0
@END8
0;JMP
(PASS8)
@SP
D = -1
(END8)
@SP
A = M
M = D
@SP
M = M + 1
@57
D = A
@SP
A = M
M = D
@SP
M = M + 1
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
@53
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
M = M + D
@SP
M = M + 1
@112
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
@82
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
M = M | D
@SP
M = M + 1
@SP
AM = M - 1
M =!M
@SP
M = M + 1
