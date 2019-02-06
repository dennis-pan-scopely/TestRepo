import subprocess
import sys
import json
import os

# command line arguments
branches_str = sys.argv[1]
github_user = sys.argv[2]
api_token = sys.argv[3]

# constants
PR_URL = "https://api.github.com/repos/scopely/DiceUnity/pulls"


def create_pr(target_branch, base_branch):
    pr_dict = {"title": "%s to %s" % (target_branch, base_branch),
               "head": target_branch,
               "base": base_branch,
               "body": "",
               "maintainer_can_modify": True}
    json_str = json.dumps(pr_dict)
    shell = "curl -X POST -u %s:%s %s -d" % (github_user, api_token, PR_URL)
    call = shell.split(' ')
    call.append("%s" % json_str)
    print(call)
    exitcode = subprocess.call(call)
    return exitcode


def automatic_merge(branches_flow):
    print('Auto-merging through: %s' % branches_flow)
    failed = False
    next_index = 0
    for branch in branches_flow:
        next_index = next_index + 1
        if next_index < len(branches_flow):
            onto = branches_flow[next_index]
            commit_message = 'auto-merging %s onto %s' % (branch, onto)
            shell1 = 'git checkout %s' % onto
            shell2 = 'git pull'
            shell3 = 'git ; merge ; origin/%s ; -m ; %s' % (branch, commit_message)
            shell4 = 'git push'
            call1 = shell1.split(' ')
            call2 = shell2.split(' ')
            call3 = shell3.split(' ; ')
            call4 = shell4.split(' ')
            exitcode = subprocess.call(call1)
            exitcode |= subprocess.call(call2)
            exitcode |= subprocess.call(call3)
            exitcode |= subprocess.call(call4)
            if exitcode:
                print('Merge of %s onto %s failed, creating PR' % (branch, onto))
                create_pr(branch, onto)
                failed = True
                break

    if failed:
        sys.exit('Automated merges failed, reset to original state')


def main():
    if os.environ['GITHUB_PR_TARGET_BRANCH'] in branches_str:
        j = json.loads(branches_str)
        automatic_merge(j)
    else:
        print("PR target branch %s is not in branches_flow, skipping merge" % os.environ['GITHUB_PR_TARGET_BRANCH'])


if __name__ == "__main__":
    main()
