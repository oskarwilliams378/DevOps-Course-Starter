# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On macOS and Linux
```bash
$ source setup.sh
```
### On Windows (Using Git Bash)
```bash
$ source setup.sh --windows
```

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing

The project uses pytest and selenium to perform unit tests, integration tests, and e2e tests.

### Setup

In order to run the selenium e2e tests [Gecko Driver executable](https://github.com/mozilla/geckodriver/releases) is 
needed. Download it and add it to the root directory. You will also need to have 
[Firefox](https://www.mozilla.org/en-GB/firefox/new/) installed.

### Running the tests

To run the unit and integration tests run the following command:
```
pytest tests
```
To run the e2e tests run the following command: 
```
pytest tests_selenium
```

