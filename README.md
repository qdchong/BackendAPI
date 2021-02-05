## Backend Technical Assessment

### Government Grant Disbursement API

### Assumptions

1.  Each household is uniquely represented by an incremental ID assigned by the DB. Due to the questions not requiring to list the household ID, deletion of household which require the ID is already known upon usage of API

2.  Each household will not have a family member with the same name. This is to facilitate for the API to delete family members, as name is being pass in as a argument to delete the family member from the specified household.

3.  With regards to Q5, 5 endpoints are created for each grant scheme instead of a single endpoint. This is to faciliate restriction of the search parameters pertaining to a grant i.e. adding of another search parameter, (e.g. gender) to Student Encouragement Bonus is not allowed. Another reason being that having a single endpoint with multiple search parameters will result in many conditions in the code which will be hard to maintain when new search parameters are required.

4.  With regards to Q5, children are assumed to have 0 annual income.

5.  With Regards to Q5, part ii, it is assumed that for every married member, the spouse will be staying in the same household. For member with divorced or widowed marital status, the spouse field will be empty.

### To set up the app locally on your system, do the following

##### Set up your virtual environment and install app dependencies

- `python 3 -m venv env `
- `source env/bin/activate `
- `pip install -r requirements.txt`

##### Add environment variables, create a new .env in your root folder directory , add the following

- `FLASK_APP=main.py`
- `FLASK_DEBUG=1 `
- `FLASK_ENV=development`

##### Upgrade database and run your flask app

- `flask db upgrade`
- `flask run`

##### Run tests locally

`python -m unittest`

### REST API Endpoints

## **Create Household**

Create a household.

- **URL**

  /api/v1/households

- **Method:**

  `POST`

- **URL Params**

  None

- **Data Params**

  **Required:**

  "housingType": <householdType>

- **Success Response:**

  - **Code:** 200 <br />
    **Content:** `{ "msg" : "successfully created household" }`
