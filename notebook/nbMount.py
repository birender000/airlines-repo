# Databricks notebook source
storageAccountName = "airlinesstorageaccount"
containerName = "validate"
source = "wasbs://"+containerName+"@"+storageAccountName+".blob.core.windows.net"

mountPoint = "/mnt/AirFiles/Validated"


accountKey = dbutils.secrets.get(scope="airlines_scope", key='account-key')
confKey = "fs.azure.account.key."+storageAccountName+".blob.core.windows.net"
extraConfigs = {
    confKey : accountKey
}

  
if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
    dbutils.fs.mount(source = source,mount_point = mountPoint,extra_configs = extraConfigs)

# COMMAND ----------

dbutils.fs.ls(mountPoint)

# COMMAND ----------

dbutils.secrets.listScopes()

# COMMAND ----------

dbutils.secrets.list("airlines_scope")

# COMMAND ----------


