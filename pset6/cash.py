from cs50 import get_float 


change = get_float("change owed: ")


if change < 0.00:
    change = get_float("change owed: ")
    

change = round(change * 100)
count = 0

while change >= 25:
    change -= 25
    count += 1
    
    
while change >= 10:
    change -= 10
    count += 1

while change >= 5:
    change -= 5
    count += 1

while change >= 1:
    change -= 1
    count += 1

print(count)