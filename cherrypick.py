import json
import sys
import subprocess
import requests


# Github credentials
GITHUB_USER = "dennis-pan-scopely"
API_TOKEN = "YOUR_API_TOKEN"

# Github repo for API endpoints
GITHUB_REPO = "dennis-pan-scopely/TestRepo"

# Tag
PR_LABEL = "Cherry-picked"

# command line arguments
PULL_ID = sys.argv[1]
BRANCH = sys.argv[2]


def get_commits_api_url(pull_id):
    format_str = "https://api.github.com/repos/{}/pulls/{}/commits"
    api_url = format_str.format(GITHUB_REPO, str(pull_id))
    print(api_url)
    return api_url


def get_create_pull_url():
    format_str = "https://api.github.com/repos/{}/pulls"
    api_url = format_str.format(GITHUB_REPO)
    return api_url


def get_all_commit_hashes_from_api(pull_id):
    api_url = get_commits_api_url(pull_id)
    commits_response = requests.get(api_url, auth=(GITHUB_USER, API_TOKEN))
    response_obj = json.loads(commits_response.text)
    hashes = []
    for commit in response_obj:
        hashes.append(commit["sha"])
    return hashes


def cherry_pick():
    all_commits = get_all_commit_hashes_from_api(PULL_ID)
    new_branch = "cherrypick-" + PULL_ID
    subprocess.check_output(["git", "checkout", BRANCH])
    subprocess.check_output(["git", "pull"])
    subprocess.check_output(["git", "checkout", "-b", new_branch])
    for commit_hash in all_commits:
        subprocess.check_output(["git", "cherry-pick", commit_hash])
    subprocess.check_output(["git", "push", "-u", "origin", new_branch])

    return new_branch


def add_label_to_pr(pull_id):
    format_str = "https://api.github.com/repos/{}/issues/{}"
    api_url = format_str.format(GITHUB_REPO, pull_id)
    print(api_url)
    return api_url


def label_pr(pr, label):
    api_url = add_label_to_pr(pr)
    requests.post(api_url, auth=(GITHUB_USER, API_TOKEN), json={"labels":[label]})


def create_pr(new_branch):
    title = "Cherrypicked " + PULL_ID
    body = "Cherrypicked #" + PULL_ID
    request_body = {"title": title, "body": body, "head": new_branch, "base": BRANCH}
    print("body: " + json.dumps(request_body))
    api_url = get_create_pull_url()
    response = requests.post(api_url, auth=(GITHUB_USER, API_TOKEN), json=request_body)

    new_pr_number = response['number']
    return new_pr_number


def main():
    number = create_pr(cherry_pick())
    label_pr(number, PR_LABEL)


if __name__ == "__main__":
    main()

