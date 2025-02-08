;  
;  Test for formatter.asm
;  

;  Created: 2/6/2025 8:03:24 PM
;  Author : malon
;  

;  Replace with your application code
start:
consts:     .DB      0      ,  255    ,  0b01010101,  -128   ,  0xaa    ;  evil comment
start2:     INC      r16    
start2:     INC      r16    
start2:     INC      r16    
start2:     INC      r16    
start2:     INC      r16    
start2:     INC      r16    
start2:     INC      r16    
start2:     INC      r16    
start2:     INC      r16    
start2:     INC      r16    
start2:     INC      r16    
start2:     INC      r16    
start3:     INC      r16                    ;  This line has a comment
start4:     BREQ     r16    ,  r22          ;  This line has a comment too
start5:     BREQ     r16    ,  r2fkdsajlflkasj2 ;  This line has a comment too
start6:     BREQ     r1fkdjsalkfjsa6,  r2fkdsajlflkasj2 ;  This line has a comment too
            NEG      

            RJMP     start  



