## Empty My Fridge (Django)

A web application that tells users recipes they can make based on ingredients in their fridge

## Github link

[Empty My Fridge](https://github.com/edwarddubi/empty_my_fridge_django)

## PYPI

[empty-my-fridge 1.0.7](https://pypi.org/project/empty-my-fridge/)

### Install using command
  - pip3 install empty-my-fridge

### Run app using
  - empty_my_fridge

## Python FrameWork

- [Django](https://pypi.org/project/Django/)

## Libraries/Tools

[Pyrebase](https://pypi.org/project/Pyrebase/)

[BeautifulSoup](https://pypi.org/project/beautifulsoup4/)

Semantic Ui or fomantic Ui css (currently, Semantic Ui)

## Templates

- HTML, CSS, and JS (Snippets)

## Using Semantic Ui

- Add this to your HTMl file in the head tag. You can ignore the semantic.min.js in the script tag

```html
<link
  rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css"
/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>
```

- It should look like this. Remember, this is just an example to help you know where it needs to put in the HTML file

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Sign Up</title>
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css"
    />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>
  </head>
  <body>
    <!--Your semantic UI here. Example below-->
    <button style="margin: 10;" type="submit" class="ui button fluid red">
      Create Account
    </button>
  </body>
</html>
```

- [Implementation? Read from docs](https://semantic-ui.com/elements/)

## Steps

pip install Django==3.0.7

pip install pyrebase

pip install beautifulsoup4

## Get Firebase Database Config file Set up

Create a config file in the cpanel/cpanel folder. Also, make sure you get the snippet for your app's Firebase config object--this is found in your project settings

- [Firebase config object](https://firebase.google.com/docs/web/setup?authuser=0#from-hosting-urls)

For security reasons, you should exclude the config.py module when exporting project into Github (Don't mind this since gitignore does it anyways)

Example:

```py
def myConfig():
  config = {
    'apiKey': "api-key",
    'authDomain': "project-id.firebaseapp.com",
    'databaseURL': "https://project-id.firebaseio.com",
    'projectId': "project-id",
    'storageBucket': "project-id.appspot.com",
    'messagingSenderId': "sender-id",
    'appId': "app-id",
    'measurementId': "G-measurement-id"
  }
  return config
```

## Get the App running for the first time

- python manage.py

## Using Github

Each of us will create their own respective branches apart from MASTER

use command -> git checkout -b < branchName >

- To pull from Github, use: git pull origin < branchName >

### Deploy from local to remote

- git add .
- git commit -m "message that represents your recent changes"
- git push origin < branchName >

### Note:

Refrain from pushing to master. push to your branch and allow the scrum master to review your work before pushing to master


## SetUp file
 - python3 -m pip install -U wheel twine setuptools
 - python3 setup.py sdist
 - python3 setup.py bdist_wheel
 - twine upload dist/*

## Gitignore
 - git rm -r --cached .
 - git add .
