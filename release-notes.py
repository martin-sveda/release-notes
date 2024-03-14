import subprocess
import requests
import os
import re
import base64

# Azure DevOps Details
server = 'https://jupiter.tfs.siemens.net/tfs'
project = 'IPS/IO-Systems'
repository_id = 'et200.imck.device'
api_base_url = f'{server}/{project}/_apis'
work_item_url = f'{server}/{project}/_workitems/edit'
pull_request_url = f'{server}/{project}/_git/{repository_id}/pullrequest'

# Personal Access Token (PAT)
personal_access_token = os.environ.get('PERSONAL_ACCESS_TOKEN')

#Branch filter
branch_filter = 'feature/sys.fieldbus'


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
    # Get the current directory
    current_dir = os.getcwd()
    
    #change to desired directory - hardcoded for now                !!!!!!!!
    os.chdir('..//et200.imck.device')
    current_dir = os.getcwd()
    
    #run the git command
    print(f'Getting commits for tag {tag}')
    cmd = ['git', 'log', f'{tag}', '--pretty=format:%H %s']

    # Change the dir back
    os.chdir(current_dir)

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


# Function to get work item information
def get_work_item_info(work_item_id):
    api_endpoint = f'{api_base_url}/wit/workitems/{work_item_id}'
    return make_devops_api_call(api_endpoint)


# Print work item information
def print_work_item_info(work_item):
    print(f' - [{work_item["id"]}]({work_item_url}/{work_item["id"]}), {work_item["fields"]["System.WorkItemType"]}, {work_item["fields"]["System.Title"]}')

# Get PR info
def get_pr_info(pr_id):
    api_endpoint = f'{api_base_url}/git/repositories/{repository_id}/pullRequests/{pr_id}'
    return make_devops_api_call(api_endpoint)

# Print PR info
def print_pr_info(pr):
    print(f'\n[PR {pr["pullRequestId"]}]({pull_request_url}/{pr["pullRequestId"]}), {pr["title"]}')
   
# Main logic
def main():
    tag = 'mfd_1.1.7..mfd_1.1.8'
    
    # Get list of commit messages for the tag
    commits = get_commits_for_tag(tag)
    
    pr_work_items = {}
    for commit in commits:
        commit_hash, commit_message = commit.split(' ', 1)
        pr_id = extract_pr_id(commit_message)
        if pr_id:
            work_items = get_work_items_for_pr(pr_id)
            pr_work_items[pr_id] = work_items
        
    
    for pr_id, work_items in pr_work_items.items():
        # Print PR work item information  - title etc. and make it a link in markdown
        pr = get_pr_info(pr_id);

        # Filtering to specic branch feature/sys.fieldbus
        if (branch_filter != "") and (branch_filter not in pr["sourceRefName"]):
            continue

        print_pr_info(pr);
        # Get the list of workitems linked to the PR 
        work_items_list = work_items["value"]
        for work_item in work_items_list:
            wi = get_work_item_info(work_item["id"]);
            print_work_item_info(wi)


if __name__ == "__main__":
    main()

# End of file
    