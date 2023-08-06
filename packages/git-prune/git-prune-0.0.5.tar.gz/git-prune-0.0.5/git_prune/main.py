import shlex
import subprocess
import re


class git_prune(object):

    def __init__(self):
        self.shellCMD('git fetch -p')
        self.remoteBranches = self.get_remote_branches()
        self.localBranches = self.get_local_branches()
        self.notRemote = list(set(self.localBranches) -
                              set(self.remoteBranches))

    def shellCMD(self, cmd):
        '''
        Run a shell command. 
        Command should be a single string. 
        Function will create the necessary list before running subprocess.
        Response will be the stripped results.
        '''
        try:
            cmd = shlex.split(cmd)
            results = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, shell=False)
            results = results.strip()
            return results.decode('UTF-8')
        except subprocess.CalledProcessError as e:
            errorText = e.output.strip()
            return errorText.decode('UTF-8')

    def get_remote_branches(self):
        '''
        Construct list of remote branches
        '''
        remoteBranches = self.shellCMD('git for-each-ref')
        remoteBranches = re.findall(
            r'refs/remotes/[a-zA-Z]*/(.*)', remoteBranches)
        for line in remoteBranches:
            if "HEAD" in line:
                remoteBranches.remove(line)
            else:
                pass
        return remoteBranches

    def get_local_branches(self):
        '''
        Construct list of local branches
        '''
        localBranches = self.shellCMD('git for-each-ref')
        localBranches = re.findall(r'refs/heads/(.*)', localBranches)
        return localBranches

    def delete_branches(self):
        '''
        Delete all branches on notRemote list
        '''
        self.shellCMD('git checkout master')
        for branch in self.notRemote:
            self.shellCMD(f'git branch -D {branch}')

    def prune_local_branches(self):
        '''
        Confirm which branches will be removed. Remove them.
        '''
        if (self.notRemote == [''] or self.notRemote == []):
            print('Local git branches match remote. No pruning needed.')
            exit(0)
        else:
            deleteBranches = input(
                f'Branch(es) {self.notRemote} do not exist in the origin repository. Would you like to delete them? y/n: ')
            if deleteBranches == 'y':
                self.delete_branches()
            else:
                print(f'Branch(es) {self.notRemote} will not be deleted.')


def main():
    gitPrune = git_prune()
    gitPrune.prune_local_branches()


if __name__ == "__main__":
    main()
