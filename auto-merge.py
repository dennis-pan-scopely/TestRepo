import subprocess
import sys
import json

# command line arguments
branches_str = sys.argv[1]


def automatic_merge(branches_flow):
    print('Auto-merging through: %s' % branches_flow)
    failed = False
    for branch in branches_flow:
        onto = next(branch, branches_flow)
        if onto:
            exitcode = subprocess.call('git checkout %s ＆＆ git merge refs/heads/%s' % (onto, branch))
            if exitcode:
                print('Merge of %s onto %s failed, must reset to original state' % (branch, onto))
                failed = True
                break

    if failed:
        sys.exit('Automated merges failed, reset to original state')


def main():
    j = json.loads(branches_str)
    automatic_merge(j)


if __name__ == "__main__":
    main()
