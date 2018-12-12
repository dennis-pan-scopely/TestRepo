import subprocess
import sys
import json

# command line arguments
branches_str = sys.argv[1]
github_user = sys.argv[2]
api_token = sys.argv[3]

# constants
PR_URL = "https://api.github.com/repos/dennis-pan-scopely/TestRepo/pulls"


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
            shell1 = 'git checkout %s' % onto
            shell2 = 'git merge refs/heads/%s' % branch
            shell3 = 'git push'
            call1 = shell1.split(' ')
            call2 = shell2.split(' ')
            call3 = shell3.split(' ')
            exitcode = subprocess.call(call1)
            exitcode |= subprocess.call(call2)
            exitcode |= subprocess.call(call3)
            if exitcode:
                print('Merge of %s onto %s failed, creating PR' % (branch, onto))
                # TODO create PR
                failed = True
                break

    if failed:
        sys.exit('Automated merges failed, reset to original state')


def main():
    # j = json.loads(branches_str)
    # automatic_merge(j)
    create_pr("bugs/rc001", "releases/v0.1")


if __name__ == "__main__":
    main()
