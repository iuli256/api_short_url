**Steps needed to start the solution**

In order to be able to run the solution you need to have installed docker-compose because the project is using PostgreSql server to store data
Also you need a virtual environement with python 3.8

Step 1: you have to run `docker-compose up` in the root folder of the project.
Step 2: activate the virtual environement
Step 3: install dependencies by running `pip install -r requirements.txt`

**Solution now is ready to be started**

In order to start the api if all the previews steps where successful you have to be in the root folder of the application and run the command `python app.py`

The api will run on port 8081 on localhost.

The webservice (for example Flask) is exposing the following endpoints:
- POST /shorten in the body of the post you will have to send 2 parameters "url" (mandatory) and "shortcode"(optional)
- GET /<shortcode> this will return the url with redirect header
- GET /<shortcode>/stats this will return statistics on the shortcode

**Running tests**

In order to run the test you have to type following command in the root folder of the project `pytest -s tests/test_app/test_shorten.py -vvv`
