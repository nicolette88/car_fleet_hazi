# how to use this project

1. clone the repo, cd into th repo, then create virtualenv:

```
git clone repo...
cd repo
virtualenv -p python3 venv
```

2. activate the virtualenv:

on mac:

`source venv/bin/activate`

on windows: 

`venv\Scripts\activate`

3. install the dependencies:

`pip install -r requirements.txt`

4. Create the environment file, and fill out the variables

`cp .flaskenv-example .flaskenv`

5. Start the app

`flask run`
