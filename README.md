# DevOps Apprenticeship: Project Exercise

[Getting started](#Getting started)

[Testing](#Testing)  

[Deployment](#Deployment)  


#Getting started

We use docker to run this project, make sure docker is installed locally.

##Environment variables

Create copies of the `.env.template` file named as `.env`, `.env.development`, and `.env.test`.
To these files add your mongo db Username, Password, url, and default database.
This will setup the environment variables for both running as dev and as prod.

##Running dev


To run the tests in docker run the command:
```
docker-compose -f docker-compose.development.yml up --build
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:8000/`](http://localhost:8000/) in your web browser to view the app.

##Running prod


To run the tests in docker run the command:
```
docker-compose up --build
```

#Testing

The project uses pytest and selenium to perform unit tests, integration tests, and e2e tests. These can be run locally or using docker.

##Docker

To run the tests in docker run the command:
```
docker-compose -f docker-compose.test.yml up --build
```

##Locally

###Setup

In order to run the selenium e2e tests [Chrome driver](https://chromedriver.chromium.org/downloads) is 
needed. Download the version compatible with your chrome installation and add it to the root directory.

###Running the tests

To run the unit and integration tests run the following command:
```
pytest tests
```
To run the e2e tests run the following command: 
```
pytest tests_selenium
```

#Deployment

Any push on the master branch, e.g., after a PR, will get deployed onto the Heroku site at [https://oskwil-todo-app.herokuapp.com](https://oskwil-todo-app.herokuapp.com).

The environment variables for the live deployment are listed in trello and Heroku, and accessed in the .travis.yml file
via the env secure public key. 