

import sys
import ray
import json

import torch
from importlib.metadata import version

@ray.remote(
    num_gpus=1
)
def gpu_test():
    try:
        print('Checking GPU with torch')
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print('GPU device: ' + str(device))
        return True
    except Exception as e:
        print('GPU test error')
        print(e)
        return False 
    
if __name__ == "__main__":
    print('Starting ray job')
    print('Python version is:' + str(sys.version))
    print('Ray version is:' + version('ray'))
    print('Torch version is:' + version('torch'))

    input = json.loads(sys.argv[1])

    process_parameters = input['process-parameters']
    storage_parameters = input['storage-parameters']
    data_parameters = input['data-parameters']

    print('Running GPU test')

    status = ray.get(gpu_test.remote())
    
    print('Job success:' + str(status))

    print('Ray job Complete')
