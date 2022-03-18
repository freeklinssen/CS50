-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE street = "Chamberlin Street" AND year = 2020 AND day = 28 AND month = 7;

-- witness check 
SELECT transcript FROM interviews WHERE year = 2020 AND day = 28 AND month = 7 AND transcript LIKE "%courthouse%";

--check parking

SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND day = 28 AND month = 7 AND hour = 10 AND minute < 25 AND minute > 15;

--check atm_transactions

SELECT account_number,transaction_type FROM atm_transactions WHERE year = 2020 AND day = 28 AND month = 7 AND atm_location = "Fifer Street" AND transaction_type = "withdraw";

--check flights -> flight id = 36
SELECT id, origin_airport_id, destination_airport_id, hour, minute from flights WHERE year = 2020 AND day = 29 AND month = 7 AND origin_airport_id IN (SELECT id FROM airports WHERE  city = "Fiftyville");

--caller
SELECT caller, receiver FROM phone_calls WHERE year = 2020 AND day = 28 AND month = 7 AND duration < 60;


--check dader
SELECT name, id FROM  people WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND day = 28 AND month = 7 AND hour = 10 AND minute < 25 AND minute > 15) 
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)
AND id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2020 AND day = 28 AND month = 7 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"))
AND phone_number IN (SELECT caller FROM phone_calls WHERE year = 2020 AND day = 28 AND month = 7 AND duration < 60);


--escapd to

SELECT city from airports WHERE id IN (SELECT destination_airport_id from flights WHERE id = 36);


--ACCOMPLICE
SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE caller = ( select phone_number FROM people WHERE id = 686048) AND year = 2020 AND day = 28 AND month = 7 AND duration < 60); 
