# FastAPI Quotes API
This is a simple API built using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.7+.

The API provides endpoints for user authentication, registration, retrieving quotes, and favoriting quotes. It uses the following technologies:

SQLAlchemy as the ORM for database interaction.

hashlib for password hashing.

uvicorn as the ASGI server for running the app

pydantic for data validation

# Installation and Setup
Clone the repository:
```bash
git clone https://github.com/Hajiub/Quotes-API.git
```
Change dir to the Qoutes-API folder
```bash
cd Qoutes-API
```
Create a Python virtual environment and activate it:
```bash
# Create a Python virtual environment using venv
python3 -m venv env

# Activate the virtual environment (Linux/Unix)
source env/bin/activate

# Activate the virtual environment (Windows)
.\env\Scripts\activate
```
Install the required dependencies:
```bash
pip install -r requirements.txt
```
Create a new SQLite database by running the following command:

```bash
python3 setup_db.py
```
This will create the database schema and insert some default data.

Note: The default data includes a user with the username default_user and the password password, and a list of quotes that can be displayed in the application.

Run the application:
```bash

uvicorn api:app --reload
```
This will start the API server at http://localhost:8000.
# Endpoints
POST ```/login```
Log in a user with provided email or username and password.

Request body

```json

{
  "email": "example@example.com",
  "password": "example_password"
}
```
Response

```json

{
  "message": "You have successfully logged in",
  "username": "example_username",
  "access_token": "example_api_key"
}
```
POST ```/register```
Register a new user with a unique email and username.

Request body

```json

{
  "username": "example_username",
  "email": "example@example.com",
  "password": "example_password"
}
```
Response

```json
{
  "message": "Account has been registered successfully!",
  "api_key": "example_api_key"
}
```
GET ```/quotes```
Get a list of all quotes in the database.

Request header

```make
api_key: example_api_key
```
Response

```json

{
  "user": "example_username",
  "quotes": [
    {
      "id": 1,
      "text": "example_quote",
      "author": "example_author"
    },
    {
      "id": 2,
      "text": "example_quote",
      "author": "example_author"
    }
  ]
}
```
GET 
```/quote/random```
Get a random quote from the database.

Request header
```make
api_key: example_api_key
```
Response

```json
{
  "quote": "example_quote",
  "author": "example_author"
}
```
GET /quote/{quote_id}
Get a specific quote from the database by ID.

Request header

```make
api_key: example_api_key
```
Response
```json
{
  "quote": {
    "id": 1,
    "text": "example_quote",
    "author": "example_author"
  },
  "user": "example_username"
}
```
PUT 
```/quote/{quote_id}/favorite```
Favorite a specific quote for the user with the provided API key.

Request header

```make
api_key: example_api_key
```
Response

```json
{
  "message": "Quote has been favorited successfully!"
}
```
License
This project is licensed under the MIT License. See the LICENSE file for details.