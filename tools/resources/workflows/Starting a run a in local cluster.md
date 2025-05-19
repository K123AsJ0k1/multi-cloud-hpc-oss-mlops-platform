# Starting a run in a local cluster

## SECURITY NOTICE

**The self-hosted GitHub actions runner runs on YOUR machine. If you create automations that for example auto-merge pull requests, someone could inject malicious code to the repository and run it on YOUR machine. It would be advisable to keep the repository private but GitHub requires forked repositories to be public.**

## Requirements

1. Install and run the self-hosted GitHub actions runner
- Repository Settings > Actions > Runners > New self-hosted runner
  - Tested on Windows 10 installing the Linux x64 version of the runner to the WSL environment with default values (just press enter on promt) of the installer and already inplace SSH key pair with GitHub.
  - Useful tutorial YouTube video: https://www.youtube.com/watch?v=aLHyPZO0Fy0
  - Start the runner:
```
/run.cmd
```

2. You need to have the local cluster of the MLOPS-platform running on your machine.
 - You can check the pods:
```
kubectl get pods --all-namespaces
```
 - Forward the ports:
```
kubectl -n mlflow port-forward svc/mlflow 5000:5000
```

```
kubectl port-forward svc/ml-pipeline-ui -n kubeflow 8080:80
```
3. The Notebook with the run is currently expected to be located in `local/` folder along with it's components in `local/components/` folder.
  - You may want to rename the run from `demo-run` to something more descriptive in the Submit run part of the Notebook.

## Action .yml

Needs to be placed in a folder system `/.github/workflows/` in the repo's root for GitHub to recoqnize it as GitHub action. As this is connecting to the local cluster it should be in the development branch.

## GitHub Actions .yml file

```
name: Start a run from Jupyter Notebook on local server via self-hosted Github Actions runner

on:
  push:
    branches:
      - development

jobs:
  run-in-development-environment:
    runs-on: self-hosted
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install jupyter
        
    - name: Connect to local server and run the Notebook
      run: |       
        # Execute the Jupyter Notebook and overwrite the existing file with the results
        jupyter nbconvert --execute --to notebook --inplace notebooks/local/demo-pipeline.ipynb

```
