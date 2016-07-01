import glob, os
import shutil
from subprocess import call
import sys

import parser
from parser import CodeLineType

CHECKOUTS_DIRECTORY = '/checkouts'

def checkout_repo(url):
    CHECKOUTS_DIRECTORY = os.path.join(os.path.dirname(__file__), 'checkouts')

    if not os.path.isdir(CHECKOUTS_DIRECTORY):
        os.makedirs(CHECKOUTS_DIRECTORY)

    repo_name = 'swifttools'
    repo_subdirectory = os.path.join('username', repo_name)
    # repo_subdirectory = os.path.join(username, repo_name)
    repo_directory = os.path.join(CHECKOUTS_DIRECTORY, repo_subdirectory)

    # delete repo if it already exists
    if os.path.isdir(repo_directory):
        shutil.rmtree(repo_directory)

    # clone repo to to checkouts directory
    call(['git', 'clone', url, repo_directory])

def process():
    failed_files = []
    for root, dirs, files in os.walk(repo_directory):
        for index, file in enumerate([x for x in files if x.endswith(".swift")]):

            try:
                parsed_file = parser.parse_file(os.path.join(root, file.title()))
                types = [x for x in CodeLineType if x.value in ['extension', 'protocol', 'var']]

                quantities = {type.value: len(parsed_file.lines_of_type(type)) for type in types}
                print(quantities)
            except IndexError as e:
                # import ipdb; ipdb.set_trace()
                failed_files.append((file.title(), root, e))

    for title, root, exception in failed_files:
        print(title)


checkout_repo(sys.argv[1])
