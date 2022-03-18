from cs50 import get_int 


height = get_int("height: ")

if height < 1 or height > 8:
    height = get_int("height: ")
    

height = height + 1

for i in range(1, height):
    
    for a in range(1, height-i):
        print(" ", end="")
    
    for b in range(i):
        
        print("#", end="")
    
    print("")  
