# Summary information
___
### System that processes the information of a user's transactions from a `csv` mounted in a directory and sends an email with the summary ###
- For sending mail the `sendgrid` api is used 
- The file can be mounted to an `S3` bucket or locally
- Transactions are saved in a Postgresql database
- Use the peewee ORM to generate the operations
- A `zip` file can be generated to be imported into an aws lambda

## Run Project
1. Copy the `.env.example` to `.env`
```
cp .env.example .env
```

2. Update the values of the variables in the `.env` file
```
# SENDGRID
SENDGRID_API_KEY=<YOUR SENDGRID API KEY>
SENDGRID_SUMMARY_TEMPLATE_ID=<YOUR SENDGRID TEMPLATE ID>

# EMAIL
FROM_EMAIL=<ISSUER MAIL>
TO_EMAIL=<EMAIL RECIPIENT>

# DB
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=

# PROJECT
FILE_DIRECTORY=<"S3" FOR USE S3>

# S3 (in case of mounting the csv in a bucket)
S3_ACCESS_KEY_ID=<YOUR AWS KEY ID>
S3_SECRET_ACCESS_KEY=<YOUR AWS SECRET ACCESS KEY>
S3_BUCKET_NAME=<BUCKET NAME>
S3_REGION=<REGION>
S3_KEY="<FILE PATH WITHOUT / AT START>"

```
4. Use `Make` to run with docker:
```
make build # Build the image
make start # Start the containers
make stop # Stop the containers
```

## Usage
### Run the script ###
Use `make run-script` to execute the script `lambda_function`

## Export `zip` to an aws lambda
- Use `make create-zip` to generate the zip
- We needed to compile psycopg2 with the PostgreSQL. You can download the `psycopg2` package from [awslambda-psycopg2](https://github.com/jkehler/awslambda-psycopg2)
- After generating the zip, add the downloaded library `psycopg2`
- Don't forget to add your environment variables to the lambda
