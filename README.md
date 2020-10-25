# CS235Assignment2 efen563

## Description

•Searching for movies by actor, genre and director 
•Registering, logging in and logging out users
•Reviewing movies and Browsing movies

## Installation

**Installation via requirements.txt**

```shell
$ cd CS235Assignment2
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project: MovieProject' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *MovieProject* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 


## Configuration

The *CS235Assignment2/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.


## Testing

Testing requires that file *MovieProject/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *MovieProject/tests/test_data* directory. 

E.g. 

`TEST_DATA_PATH = os.path.join('/Users', 'aaa', '235', 'MovieProject', 'tests', 'test_data')`

assigns TEST_DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

`/Users/aaa/235/MovieProject/tests/test_data`

You can then run tests from within PyCharm or terminal.

 
