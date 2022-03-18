# The scrabble helper
#### Video Demo:  <https://youtu.be/AhqjhQ73exc>
#### Description:
my project is inspired on the scrabble-related assignment in problem set 2, and makes use of the dictionary we already used for the speller in problem set 5.

I made a website that helps users with scrabble in several ways. It simply can show the user how many points a word is worth, like we had to do in scrabble assignment in problem set 2. But I added some more advanced scrabble related functionalities to the website that can be uses in order to find the optimal scrabble words in every situation!

it is a website with three functionalities:
first, the website is able to show you, like in problem set 2, how many points a word in worth. 
second, given a combination of letters and blank spots, the website can show you what the optimal word is you can play, if there is one, regardless of the letters you can play.
last and most useful, the website is able to show you the optimal word, if there is one, for a combination of letters and black spots and given the letters you can play.

a combination of letters and empty spots has to be filled in with a point on the place of the blank spots, so like this: le..on. If a user submits here something else than letters or points, the website will attend the user to the fact that it is only possible to fill in letters and points in this input window. 

if you try the find the score of a non-existing word, the website will show you that this word does not exist according to the dictionary we used in problem set 5.
for the second and third functionality, if it is not possible to find a word in the dictionary based on the combination of letters and blank spots (and in case of functionality three the usable letters) the user submitted, the website will notify the user about this. 
and for the last functionality, if the user submits something else than letters for "Letters you can play", the website will show an error that this is not accepted.

the program is insensitive to upper- and lower-case, so it does not matter if a user submits a full word or a combination of letters with empty spots with upper case letters or with lower case letters. 

To make this project I made manly use of python in order to find the optimal words and corresponding scores and Flask in python is used as a basis for the website. Furthermore, I used HTML, CSS, and Jinja in order to connect the back end to the front end, some bootstrap is also implemented in order to make the web site visibly more attractive. 

The website solely works for the English language, this means that users can only submit and find English word, if the user inputs a word from another language, the website will reply that this word does not exist in the English dictionary. 

 
Thank for making CS50 public to everyone,
Freek 

