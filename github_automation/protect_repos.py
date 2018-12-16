'''
Hacky script to bulk change protection on multiple repos.

Modify ORGANIZATION and BRANCHES before running
'''

import os

from github import Github, GithubException

from opsutilshelpers.cli import confirm


if __name__ == '__main__':
    GITHUB_CLIENT = Github(os.environ['GITHUB_API_KEY'])
    ORGANIZATION = ''
    BRANCHES = ['develop']

    # Get all repos in ORGANIZATION
    repos = GITHUB_CLIENT.get_organization(ORGANIZATION).get_repos()
    # repos = GITHUB_CLIENT.get_repos()  # Get all repos you have access to

    for repo in repos:
        for branch_name in BRANCHES:
            try:
                branch = repo.get_branch(branch_name)
            except GithubException:
                print(f"Branch {branch_name} not found in {repo.name}")

        if not confirm(f'Update protection for {branch.name} in {repo.name} [y/N]? '):
            continue

        branch.edit_protection(
            required_approving_review_count=1,
            enforce_admins=False)
        # branch.add_required_signatures()
        print(f'  Updated {branch.name} in {repo.name}')
