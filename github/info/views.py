from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests
import json
import re
from django.contrib import messages
from requests.exceptions import ConnectionError

# Create your views here.

github_api = r'https://api.github.com/'
org_api = r'orgs/'
search_api = r'search/repositories'


def home(request):
    return render(request, 'info/home.html')

def valid_org(org_name):
    url = github_api + org_api + org_name
    response = requests.get(url)
    return (response.status_code)


def get_repositories(org_name, n):
    url = github_api + search_api + r'?q=user:' + org_name + r'&sort=forks'
    
    response = requests.get(url)
    # print(response.status_code)
    if response.status_code==200:
        resp_json = json.loads(response.text)
        n = min(n,resp_json['total_count'])
        print(n)
        repo_list = []
        org_img = resp_json['items'][0]['owner']['avatar_url']
        for repo in resp_json['items'][0:n]:
            item = {"id": repo['id'],"name": repo['name'],"forks": repo['forks'],"url": repo['html_url']}
            repo_list.append(item)
        
        if len(repo_list)==n:
            return repo_list, org_img, 200
        else:
            print('d')
            if 'Link' in response.headers:
                next_page, last_page = map(int, re.findall(r'page=(\d+)', response.headers['Link']))

                while next_page<=last_page and len(repo_list)<n:
                    remaining_repo = n - len(repo_list)
                    next_url = url + r'&page=' + str(next_page)
                    try:
                        response = requests.get(next_url)
                        resp_json = json.loads(response.text)

                        for repo in resp_json['items'][0:int(remaining_repo)]:
                            item = {"id": repo['id'],"name": repo['name'],"forks": repo['forks'],"url": repo['html_url']}
                            repo_list.append(item)
                        next_page+=1
                    except:
                        return None, None, 422
                
            return repo_list, org_img, 200
    
    else:
        return None, None, 422


def search_repo(request):
    if request.method == "POST":
        org_name = request.POST['org_name']
        n = int(request.POST['n'])
        m = int(request.POST['m'])
        valid = valid_org(org_name)
        # print(valid)
        if valid==200:
            repo_list, org_img, status_code = get_repositories(org_name,n)
            if status_code==200:
                result = {"org_name": org_name,"org_img": org_img,"repos": repo_list,"m":m}
                return render(request, 'info/searched.html', {'result': result})
            else:
                messages.success(request, 'No public repositories found in '+org_name)
                return render(request, 'info/home.html')
        elif valid==404:
            return render(request, 'info/home.html', {'error': 'Please input a valid organization'})
        else:
            return render(request, 'info/home.html', {'error': 'Some internal error occurred. Error: '+valid})

def get_committees(repo_id,m):
    url = github_api + 'repositories/' + str(repo_id) + '/contributors'

    response = requests.get(url)

    if response.status_code==200:
        resp_json = json.loads(response.text)

        contrib_list = []
        for contrib in resp_json[0:m]:
            item = {"user": contrib['login'],"url": contrib['html_url'],"commits":contrib['contributions']}
            contrib_list.append(item)
        
        if len(contrib_list)==m:
            return contrib_list, 200
        else:
            # print(response.headers['Link'])
            if 'Link' in response.headers:
                next_page, last_page = map(int, re.findall(r'page=(\d+)', response.headers['Link']))

                while next_page<=last_page and len(contrib_list)<m:
                    remaining_contrib = m - len(contrib_list)
                    next_url = url+r'?page='+str(next_page)
                    response = requests.get(next_url)
                    resp_json = json.loads(response.text)

                    for contrib in resp_json[0:remaining_contrib]:
                        item = {"user": contrib['login'],"url": contrib['html_url'],"commits":contrib['contributions']}
                        contrib_list.append(item)
                    
                    next_page+=1

            return contrib_list, 200
    else:
        return None, response.status_code


def commits(request, repo_id, m):
    
    contrib_list, status_code = get_committees(repo_id,int(m))
    result = {"contributions": contrib_list}
    if status_code==200: 
        return render(request, 'info/commits.html', {"result": result})
    else:
        messages.success(request, 'No contributors found')
        return render(request, 'info/commits.html', {"result": None})


