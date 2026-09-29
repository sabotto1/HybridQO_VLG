# HybridQO

This is the repository on how to run the HybridQO framework  


### Setup
#### 1. Install MSSQL with Docker and Run a container as MSSQL server:

```
sudo docker pull mcr.microsoft.com/mssql/server:2022-latest

docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=YOUR_PASSWORD" \
   -p 1433:1433 --name sql_server_test --hostname sql_server_test -d mcr.microsoft.com/mssql/server:2022-latest
```
####  2. install ODBC driver and pyodbc library for SQL Server connection with Python
```
see https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline
pip install pyodbc
```
#### 3. open MSSQL terminal and create databases (e.g., TPCH)

```
 docker exec -it sql_server_test "bash" /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "YOUR_PASSWORD" -No

 create database imdb;use imdb;go
 
  create database stats;use stats;go

```

#### 4. load tables and set index: 
```
 see HybridQO/load_databases/create_table_and_index_IMDB.sql
```

#### 5. install all necessary python libraries such as sklearn, torch, numpy, etc.


### Run a Learned Query Optimizer

#### 1. Generate random subqueries and subplans as training data

````

bash LTR_enumerate_plans_VM_Random.sh RD stats_train stats None stats1000reshuff ### generate STATS training subqueries/subplans 

bash LTR_enumerate_plans_VM_Random.sh RD imdb_train imdb None imdb39reshuff  ### generate JOB training subqueries/subplans

````

#### 2. Generate vector training data

````

bash generate_train_data_VM.sh stats1000reshuff 6Q10D98pTree691628%1 1000 linearR  &    ### generate vector training data for STATS

bash generate_train_data_VM.sh imdb39reshuff Q6D10PrevTree53435600%1 1000 linearR  &   ### generate vector training data for IMDB/JOB

````

#### 3.a Training a model (our method or baselines) and then apply the trained model to doing plan enumeration on testing queries. Examples like,

````

bash train_and_enum_VM.sh linearR LTRankNet0 Ada imdb-r imdb 2thSamTrain50%FixValid20%SamSize20and6NoScheduler imdb39reshuff Q6D10PrevTree53435600%1 &  ### training our model on IMDB and test it on JOB workloads 


````
###### The model would be store under the folder starting with, e.g., *MODEL_LTRankNet0_lambdaloss_sigma_0.5_k_5_mu_1.0_NDCG_Loss2++_presort_False_TWL_imdb39reshuff_Q6D10PrevTree53435600%1_linearR_ITER_2thSamTrain50%FixValid20%SamSize20NoScheduler*


#### 3.b Assume a trained model already exists (e.g., from your last training), just do plan ennumeration on testing queries with the trained model. Examples like,

````

bash LTR_enumerate_plans_VM.sh Ada imdb-r imdb MODEL_LTRankNet0_lambdaloss_sigma_0.5_k_5_mu_1.0_NDCG_Loss2++_presort_False_TWL_imdb39reshuff_Q6D10PrevTree53435600%1_linearR_ITER_2thSamTrain50%FixValid20%SamSize20NoScheduler None   ### do enumeration on unseen JOB testing queries
  
bash LTR_enumerate_plans_VM.sh Ada job-c imdb  MODEL_LTRankNet0_lambdaloss_sigma_0.5_k_5_mu_1.0_NDCG_Loss2++_presort_False_TWL_imdb39reshuff_Q6D10PrevTree53435600%1_linearR_ITER_334thSamTrain50%FixValid20%SamSize20NoScheduler None  ### do enumeration on unseen JOB-Complex testing queries


````

###### The generated executable XML query plans would be stored in the folder starting with, e.g., *enumerated_plans_Ada_MODEL_LTRankNet0_lambdaloss_sigma_0.5_k_5_mu_1.0_NDCG_Loss2++_presort_False_TWL_imdb39reshuff_Q6D10PrevTree53435600%1_linear_ITER_2thSamTrain50%FixValid20%SamSize20NoScheduler*

###### The runtime results of testing queries would be stored in files, e.g., *dataset_imdb_workload_job-c_enum_Ada_rank_MODEL_LTRankNet0_lambdaloss_sigma_0.5_k_5_mu_1.0_NDCG_Loss2++_presort_False_TWL_imdb39reshuff_Q6D10PrevTree53435600%1_linearR_ITER_2thSamTrain50%FixValid20%SamSize20NoScheduler_iter_None_runtime.csv*

### Run a traditional Query Optimizer

````

bash LTR_enumerate_plans_VM.sh DB imdb-r imdb None None   ### SQL Server on unseen JOB testing queries
  
bash LTR_enumerate_plans_VM.sh DB job-c imdb  None None  ### SQL Server on unseen JOB-Complex testing queries

bash LTR_enumerate_plans_VM.sh DB stats-r stats  None None  ### SQL Server on unseen STATS testing queries


````

### Run a Hybrid Query Optimizer ???

````

#### 1. test if it is true that traditional QO is better at short queries and Learned QO is better at long or complext queries (i.e., tail performance) with the above scripts.


#### 2. desgin and run a classifier/router to route the input queries to different types of optimizers


#### 3.a once it is assigned to DB, use traditional query optimizer to run it

#### 3.b once it is assigned to Learned query optimizer, use learned query optimizer (may need further design for long/complex queries) to run it


````




