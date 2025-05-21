

import sys
import ray
import json

from importlib.metadata import version

from actors.llm import LLM

from functions.resources import check_clusters

@ray.remote(
    num_gpus=1
)
def gpu_test():
    try:
        # required packages
        import torch
        print('Checking GPU with torch')
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print('GPU device: ' + str(device))
        return True
    except Exception as e:
        print('GPU test error')
        print(e)
        return False 

def llm_inference(
    process_parameters: any,
    storage_parameters: any,
    data_parameters: any
):
    try:
        cluster_urls = process_parameters['cluster-urls']

        collective_resources = check_clusters(
            cluster_urls = cluster_urls
        )
        
        if 0 < collective_resources['collective']['GPU']:
            node_urls = []
            for key,values in collective_resources.items():
                if key.isnumeric():
                    if 'GPU' in values['resources']:
                        node_urls.append(cluster_urls[int(key)-1])
            for url in node_urls:
                head_url = 'ray://' + url
                # Provides packages to remote cluster 
                head_client = ray.init(
                    address = head_url, 
                    allow_multiple = True,
                    runtime_env = {
                        'pip': [
                            'torch'
                        ]
                    }
                )  
                print(head_url)
                model_name = data_parameters['model-name']
                prompts = data_parameters['prompts']
                print(model_name)
                print(prompts)
                print('Testing node')
                with head_client:
                    # Normal scheduling of functions
                    status = ray.get(gpu_test.remote())
                    print(status)
                head_client.disconnect()

        return True
    except Exception as e:
        print('LLM inference error')
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

    print('Running LLM inference')

    status = llm_inference(
        process_parameters = process_parameters,
        storage_parameters = storage_parameters,
        data_parameters = data_parameters
    )
    
    print('Job success:' + str(status))

    print('Ray job Complete')
