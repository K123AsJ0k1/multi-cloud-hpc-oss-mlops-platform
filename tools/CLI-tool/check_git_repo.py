import sys
import git

try:
    # Check if git repository exists in current or parent directories
    git.Repo('.', search_parent_directories=True)
    print("Error: git repository exists in this directory.")
    # exit with error if repository is found
    sys.exit(1)
except git.exc.InvalidGitRepositoryError:
    # exit without error if repository is not found
    sys.exit(0)
