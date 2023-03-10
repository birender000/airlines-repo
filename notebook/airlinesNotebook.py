# Databricks notebook source
# MAGIC %sql
# MAGIC --create database raw and mart
# MAGIC 
# MAGIC create database if not exists raw;
# MAGIC create database if not exists mart;

# COMMAND ----------


# create dataframe and read data and avoid malformed data

airlinePath = "/mnt/AirFiles/Validated/airlines/airlines.csv"
airportPath = "/mnt/AirFiles/Validated/airports/airports.csv"
flightPath = "/mnt/AirFiles/Validated/flights/flights.csv"

df_airlines = spark.read.csv(path=airlinePath, header=True, inferSchema=True, sep=",", mode ="DROPMALFORMED")
df_airports = spark.read.csv(path=airportPath, header=True, inferSchema=True, sep=",", mode ="DROPMALFORMED")
df_flights = spark.read.csv(path=flightPath, header=True, inferSchema=True, sep=",", mode ="DROPMALFORMED")



# save in db as table.
df_airports.write.format("delta").mode("overwrite").saveAsTable("raw.airport_tbl")
df_flights.write.format("delta").mode("overwrite").saveAsTable("raw.flight_tbl")
df_airlines.write.format("delta").mode("overwrite").saveAsTable("raw.airline_tbl")

# COMMAND ----------

# to check the count of data frames.

print("airlines count" , df_airlines.count())
print("airports count" , df_airports.count())
print("flights count" , df_flights.count())




# COMMAND ----------

# drop dulicates

df_airlines_withoutDuplicate = df_airlines.dropDuplicates()
df_airports_withoutDuplicate = df_airports.dropDuplicates()
df_flights_withoutDuplicate = df_flights.dropDuplicates()
      

# COMMAND ----------

# deal with null value.

df_airlines_cleandata = df_airlines_withoutDuplicate.fillna(value = 0)
df_airlines_cleandata = df_airlines_withoutDuplicate.fillna(value = "unknown")

df_airports_cleandata = df_airports_withoutDuplicate.fillna(value = 0)
df_airports_cleandata = df_airports_cleandata.fillna(value = "unknown")

df_flights_cleandata = df_flights_withoutDuplicate.fillna(value = 0)
df_flights_cleandata = df_flights_cleandata.fillna(value = "unknown")

# COMMAND ----------

df_airline_mart = df_airlines_cleandata.withColumnRenamed("IATA_CODE","airlineCode")
df_airports_cleandata = df_airports_cleandata.withColumnRenamed("IATA_CODE","airportCode")

df_airport_mart = df_airports_cleandata.drop("CITY","STATE","COUNTRY","LATITUDE","LONGITUDE")
df_flight_mart = df_flights_cleandata.drop("DAY_OF_WEEK","TAIL_NUMBER","SCHEDULED_DEPARTURE","DEPARTURE_TIME","DEPARTURE_DELAY","TAXI_OUT","WHEELS_OFF","SCHEDULED_TIME","LAPSED_TIME","AIR_TIME","DISTANCE","WHEELS_ON","TAXI_IN","SCHEDULED_ARRIVAL","ARRIVAL_TIME","DIVERTED","AIR_SYSTEM_DELAY","SECURITY_DELAY","AIRLINE_DELAY","LATE_AIRCRAFT_DELAY","WEATHER_DELAY")

# COMMAND ----------

df_airport_mart.write.format("delta").mode("overwrite").saveAsTable("mart.airport_tbl")
df_flight_mart.write.format("delta").mode("overwrite").saveAsTable("mart.flight_tbl")
df_airline_mart.write.format("delta").mode("overwrite").saveAsTable("mart.airline_tbl")

# COMMAND ----------

# connect to sql db

jdbcHostName = "airline-sql-server.database.windows.net"
jdbcPort = 1433
jdbcDatabase = "airlinedb"
jdbcUserName = dbutils.secrets.get(scope = "airlines_scope",key = "serverusername")
jdbcPassword = "airline@123"
jdbcDriver = "com.microsoft.sqlserver.jdbc.SQLServerDriver"

url= f"jdbc:sqlserver://{jdbcHostName}:{jdbcPort};database={jdbcDatabase};user={jdbcUserName};password={jdbcPassword}"


# COMMAND ----------

df_airport_mart.write.jdbc(url=url, table="airport_tbl",mode="overwrite")
df_flight_mart.write.jdbc(url=url, table="flight_tbl",mode="overwrite")
df_airline_mart.write.jdbc(url=url, table="airline_tbl",mode="overwrite")

# COMMAND ----------


