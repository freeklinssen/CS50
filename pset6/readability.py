from cs50 import get_string 


string = get_string("text: ")

words = 1
sentences = 0
letters = 0

for letter in string:

    if letter == " ":
        words += 1
        
    if letter == '.' or letter == '!' or letter == "?":
        sentences += 1
        
    if letter.lower() >= 'a' and letter.lower() <= 'z':
        letters += 1

# print(words)
# print(sentences)
# print(letters)

scaler = 100 / words

l = letters * scaler 

s = sentences * scaler 
    
grade = 0.0588 * l - 0.296 * s - 15.8  
    
    
if grade < 1:
    print("Before Grade 1")
elif grade > 16:
    print("Grade 16+")
else:
    print("Grade:", round(grade))