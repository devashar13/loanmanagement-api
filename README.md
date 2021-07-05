[![Issues][issues-shield]][issues-url]

<br />
<p align="center">
  <!-- <a href="https://github.com/devashar13">
    
  </a> -->

  <h3 align="center">LoanManagement System</h3>

  <p align="center">
    YOUR_SHORT_DESCRIPTION
    <br />
    <a href="https://github.com/roerohan/Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/roerohan/Template">View Demo</a>
    ·
    <a href="https://github.com/roerohan/Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/roerohan/Template/issues">Request Feature</a>
  </p>
</p>



### Built With

* Django
* Djangorestframework
* MySQL
* docker-compose
* Docker


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Docker


### Installation
 
1. Clone the Repo
```sh
git clone https://github.com/devashar13/redcarpetup-loanmanagement
```
2. Build The Docker Containers
```sh
docker-compose build
```
3. Run The Docker Containers
```sh
docker-compose up
```
## Authentication Routes
1. Login [POST]
```sh
/api/auth/login
```
* Query Parameters
```sh
  {
    "email":"yourregisteredemail@email.com"
    "password":"password"
  }
```
I have set up the api with the following admin credentials initially:

Email: admin@admin.com<br/>
password: admin

return  : JWT token and status code

2. Register User[POST]
```sh
/api/auth/register
```
* Query Parameters
```sh
  {
    "email":"yourregisteredemail@email.com"
    "password":"password",
    "name":"name",
    "phone":"phone"
  }
```
3. Register Agent[POST]
```sh
/api/auth/agentregister
```
I have set up seperate registration for agents but an agent is not verified just by registration, an agent needs to be verified by the admin until then agent=user

```sh
  {
    "email":"yourregisteredemail@email.com"
    "password":"password",
    "name":"name",
    "phone":"phone"
  }
```

4. Verify Agent[POST,PUT]
```sh
/api/auth/verifyagent
```
```sh
-H Bearer Token {token}
{
  "agent_email":"email"
}
```
5. List Users[GET]
```sh
/api/auth/listusers
```
```sh
-H Bearer Token {token}
{
  
}
```

## Loan Management Routes

1. Create Loan[POST]
```sh
/api/loans/createloan
```
```sh
-H Bearer Token {token}
{
  "user_email":"email",
  "principal":100.00,
  "interest":10.00,
  "tenure":15 (in months)
}
```
2. Update Loan State[PUT]
```sh
/api/loans/updateloanstate
```
```sh
-H Bearer Token {token}
{
  "id":"loan id",
  "state":"ACCEPTED/REJECTED"
}
3. Update Loan[PUT]
All the fields except id are optional
<br/>
The agent who has created the loan is only allowed to edit it
```sh
/api/loans/updateloan
```
```sh
-H Bearer Token {token}
{
  "id":"loan id",
   "amount":"",
   "interest",
   "tenure":""
}
``````
4. View Loans[GET]

```sh
/api/loans/listloans
```
```sh
-H Bearer Token {token}
{
  "id":"loan id",
   "amount":"",
   "interest",
   "tenure":""
}
``````

