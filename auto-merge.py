import subprocess
import sys
import json
import os
import datetime

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
            intermediate_branch_name = branch + '_to_' + onto + str(time.time())
            commit_message = 'auto-merging %s onto %s' % (branch, onto)
            command_array = [
                ['git', 'checkout', onto],
                ['git', 'pull'],
                ['git', 'merge', 'origin/%s' % branch, '-m', commit_message],
                ['git', 'push']
            ]

            exitcode = 0
            for command in command_array:
                exitcode |= subprocess.call(command)

            if exitcode:
                print('Merge of %s onto %s failed, creating PR' % (branch, onto))
                # create an intermediate branch:
                subprocess.call(['git', 'reset', '--hard'])
                subprocess.call(['git', 'clean', '-df'])
                subprocess.call(['git', 'checkout', branch])
                subprocess.call(['git', 'checkout', '-b', intermediate_branch_name])
                subprocess.call(['git', 'push', '-u', 'origin', intermediate_branch_name])
                create_pr(intermediate_branch_name, onto)
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
