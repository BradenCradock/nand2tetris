@R1
	D=M
	@memory
	M=D
@R2
	M=0

@
D:JEQ
@R2
D=M
@
D:JEQ

(LOOP)
	@R0
	D=M
	@R2
	M=M+D
	@memory
	D=M
	M=M-1
	@LOOP
	D:JGT

(END)
	@END
	0;JMP
	
	
	
	