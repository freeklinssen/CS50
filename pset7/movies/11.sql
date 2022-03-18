SELECT title FROM people
JOIN stars ON stars.person_id = people.id
JOIN ratings ON ratings.movie_id = stars.movie_id 
JOIN movies ON stars.movie_id = movies.id
WHERE name = "Chadwick Boseman"
order by rating DESC
LIMIT 5;