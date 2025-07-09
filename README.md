# Learning Management System

The objective to create a prototype web application for instructors to explore and understand student discussion data from a LMS.

## Prerequisites

You must have Docker installed. [Docker](https://www.docker.com/)

## Running the Application

1) Clone the repository

``` shell
git clone https://github.com/TQP1234/learning_management_system
```

2) cd to the project directory.

``` shell
cd learning_management_system
```

3) Build the Docker image.

``` shell
docker build -t learning_management_system .
```

4) Run the Docker image.

``` shell
docker run -d -p 5000:5000 learning_management_system
```

5) Go to http://127.0.0.1:5000 using a web browser.

## Alternative Method (Without Docker)

Note: This web application was built on Ubuntu 24.04 and some packages will not work on Windows.

1) Install dependencies.

``` shell
pip install -r requirements.txt
```

2) Run the web application.

``` shell
gunicorn --bind 0.0.0.0:5000 app:app
```
