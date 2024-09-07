# Zillow Data Pipeline | AWS Project

## 🚀 Project Overview
This project showcases an automated data pipeline that extracts property listings from Zillow using their official API, processes the data through AWS services, and visualizes the insights using AWS QuickSight. The entire workflow is orchestrated using Apache Airflow on AWS EC2, utilizing AWS Lambda for data processing and AWS Redshift for data storage.

## 📐 Architecture
![Zillow Data Pipeline Architecture](https://github.com/MJshah001/Zillow-Data-Analytics/blob/main/ZIllow%20Data%20Pipeline%20Project%20Architecture.jpg)

The diagram illustrates the flow and interaction between different AWS services ensuring a seamless data pipeline operation.

## 🛠 Technologies Used
- **AWS EC2** - Hosts Apache Airflow for workflow orchestration.
- **AWS S3** - Stores raw and processed data.
- **AWS Lambda** - Executes data transformation scripts.
- **AWS Redshift** - Acts as the data warehousing solution.
- **AWS QuickSight** - Used for data visualization and analytics.
- **Apache Airflow** - Manages the sequence of tasks from extraction to loading.
- **Python** - Scripts the data extraction and transformation processes.

## 🔧 Setup and Configuration
### Initial Setup
- **Zillow Rapid API** : Get access to Zillow rapid API. [click here](https://rapidapi.com/s.mahmoud97/api/zillow56)
- **AWS Account**: Set up an AWS account with necessary billing configurations. [click here](https://signin.aws.amazon.com/signup?request_type=register)
- **IAM Configuration**: Includes a user group with `AdministratorAccess`. [click here](https://github.com/MJshah001/Zillow-Data-Analytics/blob/main/Resources/IAM%20config%20screenshots.docx)
- **EC2 Instance**: Ubuntu Server 24.04 LTS, t2.medium.

### Security Configuration
Ensure the web server port (8080) is open to access the Airflow UI.

### Open the port for Airflow UI access
Edit inbound rules > Add rule > TCP port 8080 > Source: Anywhere


### Software Installation
Execute the following commands on the EC2 instance to prepare the environment which involves installation of python pip , creation of virtual enviornment, installing apache airflow and starting airflow server:
```bash
sudo apt update
sudo apt install python3-pip python3.12-venv
python3 -m venv zillow_venv
source zillow_venv/bin/activate
pip install --upgrade awscli apache-airflow
airflow standalone
```

## 📋 Airflow DAG Configuration
The `zillow_analytics_dag` ensures seamless automation across tasks. checkout python file for dag [zillowanalytics.py](https://github.com/MJshah001/Zillow-Data-Analytics/blob/main/zillowanalytics.py) :

The Airflow Directed Acyclic Graph (DAG), named `zillow_analytics_dag`, is central to automating and managing the data pipeline's workflow in this project. Each task in the DAG is designed to handle specific aspects of the data processing sequence, ensuring a smooth and efficient pipeline execution. Below is a detailed breakdown of each task, the operators used, and the rationale behind their selection.

### DAG Details
- **DAG ID**: `zillow_analytics_dag`
- **Schedule Interval**: Configured to run daily to ensure up-to-date data processing.

![zillow_dag](https://github.com/MJshah001/Zillow-Data-Analytics/blob/main/Resources/dag_zillow.png)

### Task 1: Extract Data
- **Operator Used**: `PythonOperator`
- **Purpose**: This task calls the Zillow API to extract real estate data. The Python operator is used here for its flexibility in executing Python code, allowing for dynamic generation of the API request based on parameters like date and location.
- **Functionality**: The task fetches data from the Zillow API and writes the JSON response to a local file. This setup is particularly useful for preliminary data capture and subsequent diagnostics or reruns.

### Task 2: Load to S3
- **Operator Used**: `BashOperator`
- **Purpose**: The main goal of this task is to transfer the locally stored data to AWS S3, which serves as a reliable and scalable storage solution. The Bash operator is ideal for executing simple shell commands directly, in this case, to move files into S3 using the AWS CLI.
- **Functionality**: Executes a command that moves the extracted JSON data from the local environment to the first S3 bucket (landing zone), ensuring that the data is securely stored and distributed across multiple facilities.

### Task 3: Data Availability Check
- **Operator Used**: `S3KeySensor`
- **Purpose**: This task uses the S3KeySensor to monitor for the presence of the new data file in the S3 bucket. It's crucial for coordinating the workflow, as it ensures that downstream tasks only proceed once the necessary data is available.
- **Functionality**: Continuously checks the third bucket (processed data zone) for the designated key (csv file), effectively pausing the DAG's progression until the file appears, preventing errors in subsequent data processing steps.

### Task 4: Transfer to Redshift
- **Operator Used**: `S3ToRedshiftOperator`
- **Purpose**: This task handles the loading of processed data from S3 into AWS Redshift. The S3ToRedshiftOperator is used for its efficiency in bulk data loading from S3 to Redshift, supporting direct data insertion without intermediate steps.
- **Functionality**: Configures the transfer of CSV files from S3 to a table in Redshift, utilizing copy options to handle specifics like CSV formatting and headers. This setup is key for enabling complex queries and analytics within Redshift.


## 🔄 Lambda Functions
Function roles:
- `copyRawJsonFile-lambdaFunction`: Triggeres when new data arrives in the raw data bucket, copies data to an intermediate bucket.

[code](https://github.com/MJshah001/Zillow-Data-Analytics/blob/main/copyRawJsonFile-lambdaFunction.py)
  
  ![lambdafunction1](https://github.com/MJshah001/Zillow-Data-Analytics/blob/main/Resources/copyrawjsonlambdafunction.png)
  
- `transformation-convert-to-csv-lambdaFunction`: Transforms data to CSV format, filters required features and uploads csv it to the processed data bucket.

[code](https://github.com/MJshah001/Zillow-Data-Analytics/blob/main/transformation-convert-to-csv-lambdaFunction.py)
  
  ![lambdafunction2](https://github.com/MJshah001/Zillow-Data-Analytics/blob/main/Resources/converttocsvlambdafunction.png)

**`Note`** : To use pandas we have added a `AWSSDKPandas-Python312` layer to this lambda function.

## 📊 Redshift Schema

Redshift table creation:
```bash
CREATE TABLE zillowdata(
    bathrooms NUMERIC,
    bedrooms NUMERIC,
    city VARCHAR(255),
    homeStatus VARCHAR(255),
    homeType VARCHAR(255),
    livingArea NUMERIC,
    price NUMERIC,
    rentZestimate NUMERIC,
    zipcode INT
);
```
![redshift](https://github.com/MJshah001/Zillow-Data-Analytics/blob/main/Resources/redshitqueryinterface.png)

## 📈 Visualization with QuickSight

![dashboard](https://github.com/MJshah001/Zillow-Data-Analytics/blob/main/Resources/Quicksight_Dashboard.png)

## 📝 Conclusion
The Zillow Data Pipeline project exemplifies a high-throughput, scalable solution for real-time data handling, showcasing the effective use of cloud technologies in real estate analytics.


