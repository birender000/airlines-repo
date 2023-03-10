# airlines-repo

Services used
===============

1. Azure data factory (integration)
2. Key vault (secrets)
3. Databricks ( data cleaning, database creation and table creation)
4. azure sql database.(query)
5. blob storage.(storage)

Architecture
===============

1. get the data from storage.
2. filename and schema validation and unzip files if any
3. copy unwanted file to reject folder.
4. mount databricks
5. create database raw and mart and required tables.
6. put all data to raw database.
5. remove malformend data, deal with null, rename column, deal with duplicates, remove unwanted columns.
6. put clean data to mart.
7. connect sql database using jdbc and push data to azure sql database.


Learnings
===========================

1. File name validation
2. Schema validation
3. App registration
4. Creation of secrets keys in key vault
5. Databricks scope creation and link to key vault
6. Mount storage in Databricks
6. Database and table creation in Databricks
6. Data cleaning
7. Data transformation and analysis
8. Integration with azure SQL database using jdbc
9. integration with github and azure devops.


