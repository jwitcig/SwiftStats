import glob, os
import shutil
from subprocess import call
import sys

from . import parser
from .parser import CodeLineType

CHECKOUTS_DIRECTORY = '/checkouts'

def checkout_repo(url, username, repo_name):
    CHECKOUTS_DIRECTORY = os.path.join(os.path.dirname(__file__), 'checkouts')

    if not os.path.isdir(CHECKOUTS_DIRECTORY):
        os.makedirs(CHECKOUTS_DIRECTORY)

    repo_subdirectory = os.path.join(username, repo_name)
    # repo_subdirectory = os.path.join(username, repo_name)
    repo_directory = os.path.join(CHECKOUTS_DIRECTORY, repo_subdirectory)

    # delete repo if it already exists
    if os.path.isdir(repo_directory):
        shutil.rmtree(repo_directory)

    # clone repo to to checkouts directory
    call(['git', 'clone', url, repo_directory])
    return repo_directory
