CREATE OR REPLACE DATABASE weatherapi;

USE DATABASE weatherapi;

CREATE OR REPLACE SCHEMA weather_schema;

USE SCHEMA weather_schema;

-- STORAGE INTEGRATION


CREATE OR REPLACE STORAGE INTEGRATION s3_int
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = S3
ENABLED = TRUE
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::205825744150:role/snowflake-s3-role'
STORAGE_ALLOWED_LOCATIONS = ('s3://weatherfnashwii/');


-- CHECK INTEGRATION


DESC STORAGE INTEGRATION s3_int;

-- STAGE


CREATE OR REPLACE STAGE weather_stage
URL='s3://weatherfnashwii/'
STORAGE_INTEGRATION = s3_int
FILE_FORMAT = (TYPE = JSON);


-- VERIFY FILES

LIST @weather_stage;


-- FINAL TABLE


CREATE OR REPLACE TABLE weather_table (
    city STRING,
    timestamp TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT
);

-- CLEAR OLD DATA


TRUNCATE TABLE weather_table;

-- LOAD DATA


INSERT INTO weather_table
SELECT
    value:city::STRING AS city,
    value:timestamp::TIMESTAMP AS timestamp,
    value:temperature::FLOAT AS temperature,
    value:humidity::FLOAT AS humidity
FROM @weather_stage/all_cities_weather.json,
LATERAL FLATTEN(input => $1);


-- VERIFY


SELECT * FROM weather_table;