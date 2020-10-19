# General Notes
The Data Model, System Design and Input/Output files are located in the file folder.  To test execute the program, 
run the main.py file. The only file needed for the Data Model from the raw input is movies_metadata.csv. There are a few
rows that error out, but the program catches them and adds them to a log (and a list) which I push to csv at the end of 
execution.  

# Data Model
This is the basic data model to be able to answer the questions asked. Used a simple snowflake design to improve
referential integrity and to keep size down in the bridge tables. 

Example SQL statement to answer one of the questions (profit by genre by year): 
SELECT g.genre_name, m.movie_year, sum(m.profit) as total_profit
FROM genres g 
LEFT JOIN movie_genre mg ON g.genre_id = mg.genre_id
LEFT JOIN movie m ON mg.movie_id = m.movie_id
GROUP By g.genre_name, m.year

# ETL Implementation
I kept this relatively simple using lists, dictionaries and pandas. I initially created custom classes to use sets with 
Genres and Production Companies to remove duplicates. However, I switched that out for pandas DataFrames due to it 
being more complex and time consuming especially for transferring to csv files. 

This solution could be improved by moving most functions to modules, but I decided to keep this more simple and closer 
to a proof of concept. If this was going to be used in production, I would move the setup functions to their own 
folder/module and work towards a more object oriented design. 

# System Design
The System Design I went with is more of the DIY/OpenSource variety. Cheap storage via S3 for input and output files,
Airflow running on an AWS EC2 instance, Postgres either using Aurora or RDS on EC2, or Redshift. The API Gateway covers
most of the detail for how it is structured, either Python with different modules or Microservices. If more heavily 
focused on AWS, I would swap out Airflow for Glue, use S3 as a Data Lake with Redshift as the Data Warehouse and utilize
AWS's API Gateway. More expensive, but much easier to manage and implement.

Note: If the database was available and Postgres, instead of Step 2 and 3 in the Design Process, 
I would have converted the DataFrames to CSVs in a buffer string and then used the copy_from function from 
the package psycopg2 in the ETL Program. This would save storage costs and unnecessary steps.

To answer more of the questions for this portion: 
Data will be stored in S3 for files and Postgres or Redshift for the data model data depending on the size and/or 
number of records.
All users will interact with the API Gateway via REST APIs. The Gateway will handle authentication, monitoring and 
logging, caching, failure prevention and load balancing. 

As for issues with an API Gateway, it has to be highly available and managed as such. If it isn't developed correctly,
it can be incredibly frustrating to update when keeping up with each endpoint, often causing a bottleneck for 
development.
Scaling should be done horizontally, adding additional nodes as needed. A drawback to this would be cost of spinning up 
more servers for the nodes. I would use Docker and Kubernetes to handle this process.
The API Gateway can mask failures in the backend services by returning cached or default data. 

