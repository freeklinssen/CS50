import os
import glob

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True



#--------------------------#

         
@app.route("/", methods=[ "GET" , "POST"])
def index():
    
    dictionary = set()

    def load(large):
        file = open(large, 'r')
        for line in file:
            dictionary.add(line.rstrip().lower())
        file.close()
        return True
    
    load("large.txt")
    
    points = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10]
         
    
    if request.method == "POST":
        
        if not request.form.get("get_points") and not request.form.get("word") and not request.form.get("word2") and not request.form.get("letters"):
           
            return render_template("index.html")
            
        if not request.form.get("word") and not request.form.get("get_points") and not (request.form.get("word2") or not request.form.get("letters")):
            
            apology3 = "You need to fill in both inputs"
            return render_template("index.html", apology3=apology3)
            
        if request.form.get("word2") and request.form.get("letters"):
                    
            word = request.form.get("word2").lower()
            letters = request.form.get("letters").lower()
            
            for letter in word:
                if letter != "." and letter != "'" and (letter > "z" or letter < "a"): 
                    apology3 = "You used caractars that are not allowed"
                    return render_template("index.html", apology3=apology3)
            
            for letter in letters:
                if letter != "." and letter != "'" and (letter > "z" or letter < "a"): 
                    apology3 = "You used caractars that are not allowed"
                    return render_template("index.html", apology3=apology3)
                    
                    
            options = []
            for letter in letters:
                options.append(letter)
            
            print(word)
            lenght = len(word)
            
            helper = []

            
            result2 = []
            tmp_score = 0
            score3 = 0
            
            for line in dictionary:
                if len(line) == lenght:
                    helper.append(line)
            
            
            helper2 = []
                    
            punten = 0 
                
            for letter in word:
                if letter == ".":
                    punten += 1
                    
                
            for item in helper:
                a = len(word) - punten
                b = 0
                for i in range(len(word)):
                    if item[i] == word[i]:
                         b += 1
                if a == b:
                    helper2.append(item)
            
            print(helper2)
            
            helper3 = []
            
            
            def find_letter(letter, lst):
                return any(letter in word for word in lst)
    
            for item in helper2:
                a = 0 
                for i in range(len(word)):
                    if word[i] == ".":
                       if find_letter(item[i], options):
                         a += 1
                         
                if a == punten:
                    helper3.append(item)
            
            helper4 = helper3
            
            for item in helper3:
                options2 = options
                for i in range(len(word)):
                    if word[i] == ".":
                        try:
                            options2.remove(item[i])
                        except:
                            helper4.remove(item)
                            break;
                        
            print(helper4)
            
            if helper4 == []:
                result2 = ["No solution possible"]
                return render_template("index.html", result2=result2)
            
            for item in helper4:
                for letter in item:
                    num = ord(letter)
                    if num >= 97 and num <= 122:
                        num = num - 97
                        tmp_score += points[num]
                    
                if tmp_score > score3:  
                    result2.clear()
                    result2.append(item)
                    score3 = tmp_score
                    tmp_score = 0 
                elif tmp_score == score3:
                    result2.append(item)
                    tmp_score = 0 
                else:
                    tmp_score = 0
            
            return render_template("index.html", result2=result2, score3=score3)
            
            ##############################
            
        if request.form.get("word"):
            
           word = request.form.get("word").lower()
           
           for letter in word:
                if letter != "." and letter != "'" and (letter > "z" or letter < "a"): 
                    apology2 = "You used caractars that are not allowed"
                    return render_template("index.html", apology2=apology2)
            
            
           print(word)
           lenght = len(word)
            
           helper = []

           
           result = []
           tmp_score = 0
           score2 = 0
            
           for line in dictionary:
                if len(line) == lenght:
                    helper.append(line)
            
            
           helper2 = []
                    
           punten = 0 
                
           for letter in word:
                if letter == ".":
                    punten += 1
                    
                
           for item in helper:
                a = len(word) - punten
                b = 0
                for i in range(len(word)):
                    if item[i] == word[i]:
                         b += 1
                if a == b:
                    helper2.append(item)
            
           print(helper2)
            
           if helper2 == []:
                result = ["No solution possible"]
                return render_template("index.html", result=result)
                
           for item in helper2:
                for letter in item:
                    num = ord(letter)
                    if num >= 97 and num <= 122:
                        num = num - 97
                        tmp_score += points[num]
                    
                if tmp_score > score2:  
                    result.clear()
                    result.append(item)
                    score2 = tmp_score
                    tmp_score = 0 
                elif tmp_score == score2:
                    result.append(item)
                    tmp_score = 0 
                else:
                    tmp_score = 0
                    

           return render_template("index.html", result=result, score2=score2)

            ####################

            
        if request.form.get("get_points"):
            
            get_points = request.form.get("get_points").lower()
            
            if get_points not in dictionary:
                apology1 = "Not a valid word :(, at least acording to the English dictionary"
                
                return render_template("index.html", apology1=apology1)
            
            score = 0
            
            for letter in get_points:
                num = ord(letter.lower())
                if num >= 97 and num <= 122:
                    num = num - 97
                    
                    score += points[num]
        
            return render_template("index.html", score = score)
        
    else:
        return render_template("index.html" )
        
        
        
        
        
        
        
        
        """
            
            punten = 0 
            for letter in word:
                if letter == ".":
                    punten += 1
                    
                if punten > 7:
                    return render_template("index.html", lalalala)
                    
            blank = []
            for i in range(punten):
                blank.append(".")
                
            options = ["a", "p", "e", ]
                    
                    
            def finder(blank, options, punten):
                for i in range(len(blank) if counter == punten:
                    for i in range
                
            
            finder(blank, options, punten)
            """
            
                    #for i in range(len(word)):
             #   print(i)
              #  helper2.clear()
               # print(helper)
               # for item in helper:
                 #   if word[i] == item[i]:
                        #if item[i] = word[i]:
                        #print(word[i] + "__" + item[i])
                  #      helper2.append(item)
                #helper.clear()
               # helper = helper2
               # print(helper2)
