# Almabase Task
Django Implementation of Almabase SDE 6 months task. The website is running on production with gunicorn+nginx on [13.233.175.55:8000](http://13.233.175.55:8000)

## Content

- [Pre-requisites](https://github.com/srijansingh53/almaabse-task#pre-requisites)
- [Tools Used](https://github.com/srijansingh53/almaabse-task#tools-used)
- [Run Locally](https://github.com/srijansingh53/almaabse-task#run-locally)
- [Results](https://github.com/srijansingh53/IP_project#results)
    - [Search](https://github.com/srijansingh53/IP_project#search)
    - [Repositories](https://github.com/srijansingh53/IP_project#repositories)
    - [Committees](https://github.com/srijansingh53/IP_project#committees)


## Pre-requisites

Create a python3 virtual environment
```
python3 -m venv almabase
source almabase/bin/activate
``` 
Clone and install the dependencies for the project.
```
git clone https://github.com/srijansingh53/almabase-task.git
cd almabase-task/
pip install -r requirements.txt
```

## Tools Used
The official github API has been used. The following 3 endpoints were used using GET:
```
https://api.github.com/search/repositories?q=user:{org_name}&sort=forks - to search all repos ordered by most forks
https://api.github.com/orgs/{org_name} - to verify if it is an organization
https://api.github.com/repositories/{repo_id}/contributions - to get all committees ordered by most commits
```

## Run Locally

Run the following command to run locally on [127.0.0.1:8000](http://127.0.0.1:8000)
```
python manage.py runserver
```

## Results
The following are the screenshots of different web-pages

### Search

<img src="/outputs/search.png"  width="150" height="300">


### Repositories

<img src="/outputs/repo.png"  width="150" height="300">

### Committees

<img src="/outputs/commits.png"  width="150" height="300">


