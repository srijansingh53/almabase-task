from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests
import json
import re

# Create your views here.

github_api = r'https://api.github.com/'
org_api = r'orgs/'
search_api = r'search/repositories'


def home(request):
    return render(request, 'info/home.html')

def valid_org(org_name):
    url = github_api + org_api + org_name
    response = requests.get(url)

    return (response.status_code == 200)


def get_repositories(org_name, n):
    url = github_api + search_api + r'?q=user:' + org_name + r'&sort=forks'
    print(url)
    response = requests.get(url)
    resp_json = json.loads(response.text)
    # print(resp_json)
    repo_list = []

    for repo in resp_json['items'][0:n]:
        item = {"id": repo['id'],"name": repo['name'],"forks": repo['forks'],"url": repo['html_url']}
        repo_list.append(item)
    
    if len(repo_list)==n:
        return repo_list
    else:
        # print(response.headers['Link'])
        next_page, last_page = map(int, re.findall(r'page=(\d+)', response.headers['Link']))

        while next_page<=last_page and len(repo_list)<n:
            remaining_repo = n - len(repo_list)
            next_url = url + r'&page=' + str(next_page)
            response = requests.get(next_url)
            resp_json = json.loads(response.text)

            for repo in resp_json['items'][0:int(remaining_repo)]:
                item = {"id": repo['id'],"name": repo['name'],"forks": repo['forks'],"url": repo['html_url']}
                repo_list.append(item)
            next_page+=1
        
        return repo_list
        


def search_repo(request):
    if request.method == "POST":
        org_name = request.POST['org_name']
        n = int(request.POST['n'])
        m = int(request.POST['m'])
    
        if valid_org(org_name):
            repo_list = get_repositories(org_name,n)
            
            result = {"org_name": org_name, "repos": repo_list}
            return render(request, 'info/searched.html', {'result': result})
