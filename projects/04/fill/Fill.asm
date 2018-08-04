// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
@index
M=0

@SCREEN
M=0
D=A

@indexscreen
M=D
	
(CHECKFILL)
	@indexscreen     
	D=M
	@24575
	D=D-A			// Is screen filled?
	@CHECKEMPTY
	D;JEQ
	
	@KBD
	D=M
	@FILL			// Jump to fill if button is pressed
	D;JGT

(CHECKEMPTY)	
	@indexscreen
	D=M
	@SCREEN
	D=D-A			// Is screen empty?
	@CHECKFILL
	D;JEQ
	
	@KBD
	D=M
	@CHECKFILL
	D;JGT
	
	@EMPTY
	0;JMP			// Empty if screen not empty 

(FILL)
	@index
	D=M
	@SCREEN
	D=D+A
	@indexscreen
	M=D
	@indexscreen
	A=M
	M=-1
	@index
	M=M+1
	@CHECKFILL
	0;JMP
	
(EMPTY)
	@index
	D=M
	@SCREEN
	D=D+A
	@indexscreen
	M=D
	@indexscreen
	A=M
	M=0
	@index
	M=M-1
	@CHECKFILL
	0;JMP
	


