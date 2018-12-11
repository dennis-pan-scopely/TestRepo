import subprocess
import sys
import json

# command line arguments
branches_str = sys.argv[1]


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
