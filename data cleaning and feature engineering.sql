#data cleaning  and feature engineering

# Checking First 5 rows (head)

select * from flight
limit 5;

# Checking random 5 rows (sample)

select * from flight
order by rand(Airline) 
limit 5;


#checking unique value in each columns

#Airline

Select distinct(Airline) from flight;

#Source
Select distinct(Source) from flight;

#destination

Select distinct(Destination) from flight;

#Route  #contain inconistent value

#Total_stops

Select distinct(Total_stops) from flight;  #contain blank values

#checking null values in each column
SELECT 
    'Airline', COUNT(*) missing_value FROM flight WHERE Airline IS NULL
UNION ALL
SELECT 
    'Date_of_Journey', COUNT(*) FROM flight WHERE Date_of_Journey IS NULL
UNION ALL
SELECT 
    'Source', COUNT(*) FROM flight WHERE Source IS NULL
UNION ALL
SELECT 
    'Destination', COUNT(*) FROM flight WHERE Destination IS NULL
UNION ALL
SELECT 
    'Route', COUNT(*) FROM flight WHERE Route IS NULL
UNION ALL
SELECT 
    'Dep_Time', COUNT(*) FROM flight WHERE Dep_Time IS NULL
UNION ALL
SELECT 
    'Arrival_Time', COUNT(*) FROM flight WHERE Arrival_Time IS NULL
UNION ALL
SELECT 
    'Duration', COUNT(*) FROM flight WHERE Duration IS NULL
UNION ALL
SELECT 
    'Total_Stops', COUNT(*) FROM flight WHERE Total_Stops IS NULL
UNION ALL
SELECT 
    'Additional_Info', COUNT(*) FROM flight WHERE Additional_Info IS NULL
UNION ALL
SELECT 
    'Price', COUNT(*) FROM flight WHERE Price IS NULL;



#checking duplicate rows in each column

SELECT *, COUNT(*) AS duplicate_count
FROM flight
GROUP BY 
    MyUnknownColumn, Airline, Date_of_Journey, Source, Destination, 
    Route, Dep_Time, Arrival_Time, Duration, Total_Stops, 
    Additional_Info, Price
HAVING COUNT(*) > 1;








#data_ of journey is in text dtype instead of data
-- USE STR_TO_DATE FUNCTION TO CONVERT STR TO DATE AND COMBINING DEPTIME TO DATE OF JOURNEY


ALTER TABLE project.flight ADD COLUMN DATE_OF_JOURNEY_2 DATE;

UPDATE project.flight
SET DATE_OF_JOURNEY_2 =STR_TO_DATE(Date_of_Journey,'%d/%m/%Y');


-- NOW WANT I WILL DO I WILL SIMPLY COMBINE DATE OF JOURNEY DEPARTION TIME AND  DURATION OF FLIGHT THIS WILL BASICALLY GIVES ME ARRIVAL TIME
 -- ALTER TABLE test.`data_train.csv` DROP COLUMN ARRIVAL_TIME ;
 
  ALTER TABLE project.test ADD COLUMN DEPARTURE_TIME DATETIME;
  
  
UPDATE project.test
SET  DEPARTURE_TIME=str_to_date(CONCAT(DATE_OF_JOURNEY_2,' ',Dep_Time),'%Y-%m-%d %H:%i');



-- /* ADDING DURATION TO DAPARTURE TIME TO GET ARRIVAL TIME*/
-- BUT BEFORE THAT LETS HANDLE DURATION WHICH IS IN STRING TYPE SO CONVERTING IT TO MINUTES

-- ADDING DEPARTMIN COLUMN

ALTER TABLE project.flight  ADD COLUMN DURATIONMIN INT;

UPDATE project.flight
SET DURATIONMIN=CAST(REPLACE(
                       (CASE WHEN SUBSTRING_INDEX(Duration,' ',1)=SUBSTRING_INDEX(Duration,' ',-1) THEN 0
                       ELSE SUBSTRING_INDEX(Duration,' ',1)
                       END),'h','') AS unsigned)*60+

                       CAST(REPLACE(
                       (CASE WHEN SUBSTRING_INDEX(Duration,' ',-1)=SUBSTRING_INDEX(Duration,' ',1) THEN 0
                       ELSE SUBSTRING_INDEX(Duration,' ',-1)
                       END),'m','') AS unsigned);
                       



-- FInally Creating ARRIVAL_TIME=DEPARTURE_TIME+DURATION
 ALTER TABLE project.flight ADD COLUMN ARRIVAL_TIME DATETIME;
 
UPDATE project.flight 
SET ARRIVAL_TIME=DATE_ADD(DEPARTURE_TIME,INTERVAL DURATIONMIN MINUTE) ;




alter table flight rename to flight_dataset;

-- Remove Unwanted Columns Like Additional_Info,Route,MyUnknownColumn,Date_of_Journey


ALTER TABLE flight_dataset 
DROP COLUMN Route, 
DROP COLUMN Additional_Info, 
DROP COLUMN MyUnknownColumn,
DROP COLUMN Date_of_Journey;




select * from flight_dataset;














