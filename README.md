# Blog_Website

## Description

Blog_website is a full featured web application build using django framework and python. It is beautified using HTML, CSS and bootstrap 4.

## Features

- Allows user to create an account.
- Allows user to create/ update/ delete a post.
- Allows user to filter posts based on an author.
- Pagination: Displaying 5 posts per page for better user experience.


## Dependencies

All the dependencies required to run this project are available in the [requirements.txt](https://github.com/chetna-ravat/Blog_Website/blob/main/requirements.txt) file.

## How to run the project

#### Create virtual environment
```shell
python3 -m venv env
```

#### Activate virtual environment
```shell
source env/bin/activate
```

#### Install required python dependencies from requirements file
```shell
pip install -r requirements.txt
```

#### Generate security key
```shell
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Update [ACTUAL_SECURITY_KEY](https://github.com/chetna-ravat/Blog_Website/blob/main/src/django_project/.env#L2) with generated security key.

#### Run the project
```shell
python3 manage.py runserver
```

Open http://localhost:8000 on web browser to access blog application.

## How to run tests

#### Run all tests
```shell
python3 manage.py test
```

#### Run individual test
```shell
python3 manage.py test blog.tests.test_views.BlogPostTests.test_blog_home_page_view_accessed_successfully
```

More detail on running test can be found [here](https://docs.djangoproject.com/en/4.1/topics/testing/overview/#running-tests)

### Setup to send email

#### Setup an APP Password in GMAIL

Follow through this [article](https://www.sitepoint.com/django-send-email/) to `Setup an App Password in Gmail`

#### Update EMAIL environment variables

Update `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in [.env](https://github.com/chetna-ravat/Blog_Website/blob/main/src/django_project/.env) file.