
# About lsbatch

lsbatch is a [LeadSquared](https://www.leadsquared.com/) provided Batch Jobs software development kit that allows developers to code and test Batch Jobs offline.
It can also be used to prepare final deliverable that can uploaded to configure Batch Jobs in user's LeadSquared account.

## Getting Started

Assuming that you have Python and virtualenv installed, use the package manager [pip](https://pip.pypa.io/en/stable/) to install lsbatch.

```bash
pip install lsbatch
```

## Usage

### Initiate a new Batch Job project

To initiate a new Batch Job, execute the following command in cmd or shell.

```bash
lsbatch init
```

You will be asked to provide name of this Batch Job

```bash
>Your Batch Job Name:
```

A new folder with the provided name will be created in the current directory. 
This folder will be having all the libraries required for Batch Jobs local development.
You will find custom virtualenv in folder name with some default packages as following

* boto3
* mysql-connector-python
* pysftp
* sendgrid
* pathlib
* pandas
* pyyaml
* openpyxl
* requests
* flask
* tabulate
* numpy

> User should keep his/her Batch Job files in 'src' folder which will be created inside a folder with Batch Job name.

# General rules for writing a Batch Job

1. You Batch Job folder should have a folder by name `src` which will used to write your actual code. This folder is automatically created during the `init` process
2. `src` folder should have main.py file that is basically the starting point of your application. By default this file is created with sample code during the `init process
3. All code/files written by developer should reside in src folder only
4. Your src folder may contain a requirements.txt file which can be used to provide any custom packages

### Using inbuilt Batch Jobs function

Batch Job provides various functions for comman tasks like logging, sending notification emails or making DB queries. lsbatch packs and mocks the same functions and are listed below

#### logging
``` 
LS.log.info('Hello')
LS.log.info('Hello', {"Support Email": "support@leadsquared.com"})
LS.log.info(LS.settings.mykey)
LS.log.debug('Debug Log Example')
LS.log.error(type(err).__name__, traceback.format_exc())
LS.log.fatal(type(err).__name__, traceback.format_exc())
```
#### using Variable
``` 
LS.settings.mykey
```

#### Send Batch Job status notification email
```
LS.email.send_email_notification(<EmailType> <Subject>, <EmailBody>, isHTML =<True/False>)
```
Where
* EmailType: one of "Success" or "Failure" which corresponds to success of failure of execution status
* Subject: can be maximum 255 character, above which it will be trimmed
* EmailBody: plain text or HTML content.
* isHTML: is an optional parameter with default value as True.

#### Making DB Calls
```
LS.db.execute_DB_query(<query>, multi=False)
LS.db.execute_ETL_query(<query>, multi=False)
```
by default the function considers the query are single statement. For multiline query, pass `multi` parameter as `True`

Additionally to mock the DB result, create a file by name `query.json` in the root project folder. It contains a json where key is the DB query(exact0) and value is the csv file name that contains the result. You can create csv file by any name.
At the time of `init`, sample file is already created for your reference

###	Executing a Batch Job

After initiating batch with `lsbatch init` ,  make sure that your cmd path is not set to this new folder

```bash
cd {batch_job_folder_name}
```

To run Batch Job, run command `lsbatch run`

```bash
lsbatch run
```
This will execute the code in context of virtual environment that has already been setup

### Install LeadSquared Batch Job dependecies in current folder

The root folder already contains a `.gitignore` file that will commit only necessary files to your source code repository. If you clone the repo, run the `lsbatch install` command inside the project directory to setup the Batch environment again. 

```bash
lsbatch install
```
This command can also be used in existing projects to reset the Batch Jobs environment at any time.

> To run this command succesfully, current directory should have src folder in which user code will reside. 




### Install your custom packages

```bash
lsbatch install {package_name}
```

This installs your custom package as well as creates a `requirements.txt` file inside src folder. Same file will be used to identify dependencies at the time of actual execution of the Batch Job

> User should run this command in project directory. Ensure the folder contains `batch-virtualenv` folder

### Packaging you project for deployement

Batch Job accepts the deliverables as a zip file. 
To zip the project in correct way, use the following command

```bash
lsbatch pack
```

This command will create zip deliverable in the project directory with same name as project. Its a good practive to include the name of this zip file in .gitignore file to require the repository size


### Uninstall package

To uninstall a custom package, run the following command

```bash
lsbatch uninstall {package_name}
```