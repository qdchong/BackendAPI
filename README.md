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

## REST API Endpoints

### **Create Household**

Create a household.

- **URL**
  /api/v1/households
- **Method:**
  `POST`
- **Data Params**

  **Required:**
  `"housingType": "HDB/Condominium/Landed"`

- **Success Response:**

  - **Code:** 201 <br />
    **Content:** `{ "msg" : "successfully created household" }`

- **Sample Call:**

`curl -X POST -d "{\"housingType\":\"HDB\"}" localhost:5000/api/v1/households --header "Content-Type:application/json"`

### **Delete Household**

Delete a household.

- **URL**
  /api/v1/households/:id
- **Method:**
  `DELETE`
- **URL Params**

  **Required:**
  `id=[integer]`

- **Success Response:**

  - **Code:** 200 <br />
    **Content:** `{ "msg" : "successfully deleted household" }`

- **Sample Call:**

`curl -X DELETE localhost:5000/api/v1/households/1`

### **List All Household**

List all households.

- **URL**
  /api/v1/households/
- **Method:**
  `GET`

- **Success Response:**

  - **Code:** 200 <br />
    **Content:** `{ "data" : [ { "HouseholdId": 1, "HouseholdType": "HDB", "FamilyMembers": [ { "Name": "John", "Gender": "Male", "MaritalStatus": "Married", "Spouse": "Alice", "OccupationType": "Employed", "AnnualIncome": "200000.00", "DOB": "1967-10-14" },] } ]}`

- **Sample Call:**

`curl -X GET localhost:5000/api/v1/households`

### **Show Household**

Get details of a household.

- **URL**
  /api/v1/households/:id
- **Method:**
  `GET`
- **URL Params**

  **Required:**
  `id=[integer]`

- **Success Response:**

  - **Code:** 200 <br />
    **Content:** `{ "data" : [ { "HouseholdId": 1, "HouseholdType": "HDB", "FamilyMembers": [ { "Name": "John", "Gender": "Male", "MaritalStatus": "Married", "Spouse": "Alice", "OccupationType": "Employed", "AnnualIncome": "200000.00", "DOB": "1967-10-14" },] } ]}`

- **Sample Call:**

`curl -X GET localhost:5000/api/v1/households/1`

### **Create Family Member**

Create a family member.

- **URL**
  /api/v1/households/:id/family_members
- **Method:**
  `PUT`
- **URL Params**

  **Required:**
  `id=[integer]`

- **DATA Params**

  **Required:**
  `"name": <name>`,
  `"gender": <gender>`,
  `"maritalStatus": "Single/Married/Widowed/Divorced"`,
  `"occupationType": "Unemployed/Student/Employed"`,
  `"dob": <dob>`
  **Optional**
  `"spouseName: <name>"`,
  `"annualIncome: <income = int>"`

- **Success Response:**

  - **Code:** 201 <br />
    **Content:** `{ "msg" : "successfully created family member" }`

- **Sample Call:**

`curl -X PUT -d "{\"name\":\"Minnie\",\"gender\":\"Female\",\"maritalStatus\":\"Married\",\"spouseName\":\"Mickey\",\"annualIncome\" : 40000, \"occupationType\" : \"Employed\",\"dob\":\"1987-07-15\"}" http://localhost:5000/api/v1/households/6/family_members --header "Content-Type:application/json"`

### **Delete Family Member**

Delete a family member.

- **URL**
  /api/v1/households/:id/family_members
- **Method:**
  `DELETE`

- **DATA Params**

  **Required:**
  `"name": <name>`,

- **Success Response:**

  - **Code:** 201 <br />
    **Content:** `{ "msg" : "successfully deleted family member" }`

- **Sample Call:**

`curl -X DELETE -d "{\"name\":\"mickey\"}" http://localhost:5000/api/v1/households/1/family_members --header "Content-Type:application/json"`

## Grants API Endpoints

### **Student Encouragement Bonus**

List household and qualifying family members eligible for grant

- **URL**
  /api/v1/households/grants/student_encouragement_bonus
- **Method:**
  `GET`

- **Query Params**

  **Required:**
  `income_limit=[int]`
  `age_limit=[int]`

- **Success Response:**

  - **Code:** 201 <br />
    **Content:** `{ "data" : [ { "HouseholdId": 1, "HouseholdType": "HDB", "FamilyMembers": [ { "Name": "John", "Gender": "Male", "MaritalStatus": "Single", "OccupationType": "Unemployed", "AnnualIncome": "0", "DOB": "2008-10-14" },] } ]}`

- **Sample Call:**

`curl -X GET "http://localhost:5000/api/v1/households/grants/student_encouragement_bonus?income_limit=150000&age_limit=16"`

### **Family Togetherness Bonus**

List household and qualifying family members eligible for grant

- **URL**
  /api/v1/households/grants/family_together_scheme
- **Method:**
  `GET`

- **Query Params**

  **Required:**
  `has_husband_wife=[bool]`
  `age_limit=[int]`

- **Success Response:**

  - **Code:** 201 <br />
    **Content:** `{ "data" : [ { "HouseholdId": 1, "HouseholdType": "HDB", "FamilyMembers": [ { "Name": "John", "Gender": "Male", "MaritalStatus": "Married", "Spouse": "Alice", "OccupationType": "Employed", "AnnualIncome": "200000.00", "DOB": "1967-10-14" }, { "Name": "Alice", "Gender": "Female", "MaritalStatus": "Married", "Spouse": "John", "OccupationType": "Unemployed", "AnnualIncome": "0.00", "DOB": "1987-10-11" }, { "Name": "Sherry", "Gender": "Female", "MaritalStatus": "Single", "OccupationType": "Student", "AnnualIncome": "0.00", "DOB": "2003-10-11" }] } ]}`

- **Sample Call:**

`curl -X GET "http://localhost:5000/api/v1/households/grants/family_together_scheme?has_husband_wife=true&age_limit=18"`

### **Elder Bonus**

List household and qualifying family members eligible for grant

- **URL**
  /api/v1/households/grants/elder_bonus
- **Method:**
  `GET`

- **Query Params**

  **Required:**
  `household_type="HDB/Landed/Condominium"`
  `age_limit=[int]`

- **Success Response:**

  - **Code:** 201 <br />
    **Content:** `{ "data" : [ { "HouseholdId": 1, "HouseholdType": "HDB", "FamilyMembers": [ { "Name": "John", "Gender": "Male", "MaritalStatus": "Single", "OccupationType": "Unemployed", "AnnualIncome": "0", "DOB": "1950-10-14" },] } ]}`

- **Sample Call:**

`curl -X GET "http://localhost:5000/api/v1/households/grants/elder_bonus?household_type=HDB&age_limit=50`

### **Baby Sunshine Grant**

List household and qualifying family members eligible for grant

- **URL**
  /api/v1/households/grants/baby_sunshine_grant
- **Method:**
  `GET`

- **Query Params**

  **Required:**
  `age_limit=[int]`

- **Success Response:**

  - **Code:** 201 <br />
    **Content:** `{ "data" : [ { "HouseholdId": 1, "HouseholdType": "HDB", "FamilyMembers": [ { "Name": "John", "Gender": "Male", "MaritalStatus": "Single", "OccupationType": "Unemployed", "AnnualIncome": "0", "DOB": "2020-10-14" },] } ]}`

- **Sample Call:**

`curl -X GET "http://localhost:5000/api/v1/households/grants/baby_sunshine_grant?age_limit=5"`

### **YOLO GST Grant**

List household and qualifying family members eligible for grant
-- income less than $100,000
-- HDB

- **URL**
  /api/v1/households/grants/yolo_gst_grant
- **Method:**
  `GET`

- **Query Params**

  **Required:**
  `income_limit=[int]`
  `household_type="HDB/Landed/Condominium"`

- **Success Response:**

  - **Code:** 201 <br />
    **Content:** `{ "data" : [ { "HouseholdId": 1, "HouseholdType": "HDB", "FamilyMembers": [ { "Name": "John", "Gender": "Male", "MaritalStatus": "Single", "OccupationType": "Unemployed", "AnnualIncome": "0", "DOB": "1950-10-14" },] } ]}`

- **Sample Call:**

`curl -X GET "http://localhost:5000/api/v1/households/grants/yolo_gst_grant?income_limit=100000&household_type=HDB"`
