import csv
import sys


def compare(string, strs):
    maxvalues = []
    for i in range(len(strs)):
        # print(strs[i])
        count = 0
        longest = 0
        for a in range(len(strs[i])):
            print(strs[i])
            print(len(strs[i]))
            print(a)
            for b in range(a, len(string), len(strs[i])):
                print(b)
                j = b + len(strs[i])
                if string[b:j] == strs[i]:
                    count += 1
                else:
                    count = 0
                
                if count >= longest:
                    longest = count
        
        maxvalues.append(longest)
    return maxvalues 
            

if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py databases/...csv sequences/....txt")


peoples = []
strs = []
values = []
     
with open(sys.argv[1]) as file:
    reader = csv.reader(file)
    line_count = 0
    column = 0
    for row in reader:
        if line_count == 0:
            for i in range(1, len(row)):
                strs.append(row[i])
            line_count += 1
        else:
            
            for i in range(0, len(row)):
                if i == 0:
                    peoples.append(row[i])
                else:
                    values.append(int(row[i]))
        line_count += 1


# print(strs)
# print(peoples)
# print(values)

with open(sys.argv[2], "r") as myfile:
    string = myfile.readline()
    
#print(string)
#print(len(peoples))

result = compare(string, strs)

# print(result)


for people in range(len(peoples)):
    lenght = len(strs)
    # print(lenght)
    compare = []
    # print(peoples[people])
    
    for c in range(lenght):
        compare.append(values[people*lenght+c]) 
        
     # print(compare)
    
    winner = 0
    for i in range(len(compare)):
        if compare[i] == result[i]:
            winner += 1

    if winner == len(strs):
        print(peoples[people])
        exit()
        
print('No match')




            
                

