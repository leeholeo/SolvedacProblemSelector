'''
error logging needed in github_issue_creation module
'''
import json
import requests
import time
from env import FULL_TOKEN, OWNER, REPO
import issue_body_form


# error exception NEEDED
def all_issues_request():
    headers = { 'Authorization': f'Bearer {FULL_TOKEN}' }
    url = 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/issues'
    response = requests.get(url, headers=headers)
    response = response.json()
    return response


def get_week_number() -> int:
    response = all_issues_request()
    for res in response:
        splited_html_url = res["html_url"].split('/')
        if 'issues' in splited_html_url:
            week_number_str = res["title"].lstrip("week")
            try:
                week_number = int(week_number_str)
            except ValueError:
                continue
            return week_number + 1
    return '1'


def create_issue_request(problems: dict, problems_names: dict) -> dict or bool:
    headers = { 'Authorization': f'Bearer {FULL_TOKEN}' }
    url = 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/issues'
    week_number = get_week_number()
    body = { 'title': f'week{week_number}' }
    body['body'] = issue_body_form.get_problem_table(problems, problems_names)
    request_time = time.time()
    response = requests.post(url, headers=headers, data=json.dumps(body))
    response_time = time.time()
    print(f"issue_create_request: {response_time-request_time:.2f}")
    if not (200 <= response.status_code < 300):
        return False
    response = response.json()
    return response
