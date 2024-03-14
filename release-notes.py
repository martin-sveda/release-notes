import subprocess
import requests
import os
import re
import base64
import json



# Azure DevOps Details
server = 'jupiter.tfs.siemens.net/tfs'

project = 'IPS/IO-Systems'
repository_id = 'et200.imck.device'
personal_access_token = os.environ.get('PERSONAL_ACCESS_TOKEN')


api_base_url = f'https://{server}/{project}/_apis'

# Function to run git commands
def run_git_command(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Git error: {stderr.decode('utf-8')}")
        return None
    return stdout.decode('utf-8').strip()


# Function to make Azure DevOps REST API calls
def make_devops_api_call(api_endpoint, method='GET'):
    # Encode the Personal Access Token (PAT)
    pat_encoded = base64.b64encode(f':{personal_access_token}'.encode('utf-8')).decode('utf-8')
    
    # Set up the headers for Azure DevOps REST API calls
    headers = {
        'Authorization': f'Basic {pat_encoded}',
        'Content-Type': 'application/json'
    }
     
    response = requests.request(method, api_endpoint, headers=headers)
    if response.status_code != 200:
        print('Error authorization\n')
        print(f"Error: {response.json()}")
        return None
    return response.json()

# Function to get commits for a tag
def get_commits_for_tag(tag):
   
    os.chdir('..//et200.imck.device')
    current_dir = os.getcwd()
    print('Current directory: ' + current_dir)
    
    cmd = ['git', 'log', f'{tag}', '--pretty=format:%H %s']
    #print(cmd)
    return run_git_command(cmd).split('\n')


# Function to extract pull request ID from commit message
def extract_pr_id(commit_message):
    match = re.search(r'Merged PR (\d+)', commit_message)
    if match:
        return match.group(1)
    return None
    
    pass


# Function to get work items linked to a pull request
def get_work_items_for_pr(pr_id):
    api_endpoint = f'{api_base_url}/git/repositories/{repository_id}/pullRequests/{pr_id}/workitems'
    return make_devops_api_call(api_endpoint)


# Main logic
def main():
    tag = 'mfd_1.1.3..mfd_1.1.4'
    commit_cnt = 0

    commits = get_commits_for_tag(tag)
    
    pr_work_items = {}
    for commit in commits:
        commit_hash, commit_message = commit.split(' ', 1)
        pr_id = extract_pr_id(commit_message)
        if pr_id:
            #print('PR ID = ' + pr_id)
            work_items = get_work_items_for_pr(pr_id)
            pr_work_items[pr_id] = work_items
            commit_cnt += 1
    
    print(f'Commits: {commit_cnt}' )

    for pr_id, work_items in pr_work_items.items():
        print(f'PR: {pr_id}')
        print(f'  Count of related work items: ', {work_items["count"]})
        work_items_list = work_items["value"];
        for work_item in work_items_list:
            print(f'  Work Item: {work_item["id"]}, {work_item["url"]}')



if __name__ == "__main__":
    main()


