import shlex
import subprocess


class git_prune(object):

    def __init__(self):
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
        self.shellCMD('git fetch -p')
        remoteBranches = self.shellCMD('git branch -r')
        remoteBranches = remoteBranches.split('\n')
        finalRemote = []
        for line in remoteBranches:
            if "HEAD" in line:
                pass
            else:
                branchName = line.replace('origin/', '')
                finalRemote.append(branchName.strip())
        return finalRemote

    def get_local_branches(self):
        '''
        Construct list of local branches
        '''
        mergedBranches = self.shellCMD('git branch --merged')
        unmergedBranches = self.shellCMD('git branch --no-merged')
        localBranches = []
        mergedBranches = mergedBranches.split('\n')
        for line in mergedBranches:
            if "*" in line:
                line = line.replace('*', '')
            localBranches.append(line.strip())
        unmergedBranches = unmergedBranches.split('\n')
        for line in unmergedBranches:
            if "*" in line:
                line = line.replace('*', '')
            localBranches.append(line.strip())
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
        if self.notRemote == ['']:
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
