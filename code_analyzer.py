import requests
import json

import env


class GitHubRepoAnalyzer:
    def __init__(self, username, exclude=[]):
        self.username = username
        self.exclude = exclude
        self.token = env.GITHUB_TOKEN
    
    def analyze(self):
        response = requests.get(
            f'https://api.github.com/users/{self.username}/repos',
            auth=('token', self.token)
        )
        repos = response.json()
        print(response.status_code)

        # Create a dictionary to keep track of the language counts
        languages = {}

        # Loop through each repository and increment the count for its primary language
        for repo in repos:
            if repo['language'] and repo['language'] not in self.exclude:
                language = repo['language']
                if language in languages:
                    languages[language] += 1
                else:
                    languages[language] = 1

        # Calculate the total number of repositories and the percentage for each language
        total_repos = len(repos)
        percentages = {language: count/total_repos*100 for language, count in languages.items()}

        # Print the results
        print(f'Languages used in {self.username}\'s GitHub repositories (excluding {self.exclude}):')
        for language, percentage in percentages.items():
            print(f'{language}: {percentage:.1f}%')

    def analyze_code_usage(self):
        # Make an API request to get the list of repositories for the user
        repos = []
        page_num = 1
        while True:
            response = requests.get(f'https://api.github.com/users/{self.username}/repos?per_page=100&page={page_num}', auth=('token', self.token))
            new_repos = response.json()
            if not new_repos:
                break
            repos += new_repos
            page_num += 1

        languages = {}
        total_code_size = 0

        # Loop through each repository and increment the count for its primary language and code size
        for repo in repos:
            if repo['language'] and repo['language'] not in self.exclude:
                language = repo['language']
                code_size = repo['size']
                if language in languages:
                    languages[language]['count'] += 1
                    languages[language]['code_size'] += code_size
                else:
                    languages[language] = {'count': 1, 'code_size': code_size}
                total_code_size += code_size

        # Create a list of all languages that appear in the repositories
        all_languages = list(set(repo['language'] for repo in repos if repo['language']))

        # Calculate the percentage of code for each language
        percentages = {language: data['code_size']/total_code_size*100 for language, data in languages.items()}

        # Print the results
        print(f'Percentage of code used in {self.username}\'s GitHub repositories (excluding {self.exclude}):')
        for language in all_languages:
            percentage = percentages.get(language, 0)
            print(f'{language}: {percentage:.1f}%')


if __name__ == '__main__':
    analyzer = GitHubRepoAnalyzer('JamesonWelch', ['HTML', 'CSS'])
    analyzer.analyze_code_usage()
    