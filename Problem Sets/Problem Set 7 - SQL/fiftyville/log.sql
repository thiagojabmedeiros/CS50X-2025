-- Keep a log of any SQL queries you execute as you solve the mystery.
sqlite3 fiftyville.db

-- FINDING DATA FROM 28 JULY
SELECT description FROM crime_scene_reports WHERE day = 28 AND month = 7 AND street = 'Humphrey Street';
-- the duck's theft took place at 10:15am.

-- INTERVIEWS
SELECT name, transcript FROM interviews WHERE  day = 28 AND month = 7;

-- BAKERY'S DATAS FROM SECURITY / The thief got into a car in parking lot whithin minutes after the theft (CHECK THE BAKERY PARKING LOT SECURITY FOTAGE)
SELECT hour, minute, activity, license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND hour >= 10;
--Main license_plate suspects: 0NTHK55, 94KL13X, 322W7JE.


--The thief was leaving out the bakery making a call to someone which lasted lesse than 1 minute
SELECT * FROM people WHERE phone_number IN(SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND duration < 60);
--Sofia   | (130) 555-0289 | 1695452385      | G412CB7 V
--Diana   | (770) 555-1861 | 3592750733      | 322W7JE V
--Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55 V
--Bruce   | (367) 555-5533 | 5773159633      | 94KL13X V


SELECT caller, receiver, duration FROM phone_calls WHERE day = 28 AND month = 7 AND duration < 60;
-- c:(499) 555-9472/ r:(892) 555-8872/ 36sec V
-- c:(031) 555-6622/ r:(910) 555-3251/ 38sec X
-- c:(286) 555-6063/ r:(676) 555-6554/ 43sec X
-- c:(367) 555-5533/ r:(375) 555-8161/ 45sec V
-- c: (770) 555-1861/ r:(725) 555-3243/ 49sec V


SELECT * FROM people WHERE phone_number = '(367) 555-5533';
--Bruce, passportnumber: 5773159633, license plate: 94KL13X
SELECT * FROM people WHERE phone_number = '(375) 555-8161';
--Robin, passportnumber: NULL

SELECT * FROM people WHERE phone_number = '(499) 555-9472';
--Kelsey called, passportnumber: 8294398571, license plate: 0NTHK55
SELECT * FROM people WHERE phone_number = '(892) 555-8872';
--Larry received, passportnumber: 2312901747

SELECT * FROM people WHERE phone_number = '(770) 555-1861';
--Diana called, passportnumber: 3592750733, license plate: 322W7JE
SELECT * FROM people WHERE phone_number = '(725) 555-3243';
--Phillip received, passportnumber: 3391710505

SELECT * FROM people WHERE phone_number = '(130) 555-0289';
--Sofia called, passportnumber: 1695452385, license plate: G412CB7
SELECT * FROM people WHERE phone_number = '(996) 555-8899';
--Jack received, passportnumber: 9029462229


--The thief is taking the earliest flight out of fiftyville on july 29// the other person on the end of the phone bought their ticket
SELECT * FROM flights WHERE day = 29 AND month = 7 ORDER BY hour ASC;
SELECT * FROM airports;
--8:20 flight is going to new york
--9:30 flight is going to chicago
--12:15 flight is going to san franscisco
--15:20 flight is going to tokyo
--16:00 flight is going to boston

SELECT * FROM passengers WHERE flight_id = 36;
--8:20 flight is going to new york:
--BRUCE SEAT 4A, ROBIN NULL
--KELSEY SEAT 6C, LARRY ISNT IN THE FLIGHT
--SOFIA SEAT 3B, JACK ISNT IN THE FLIGHT

--The thief was recognized by eugene ealier close to the ATM with some money on hand
SELECT * FROM atm_transactions WHERE month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street';
SELECT * FROM bank_accounts;
SELECT * FROM people;
