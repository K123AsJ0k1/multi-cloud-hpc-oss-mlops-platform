import ray

@ray.remote(
    num_gpus=1
)
class LLM_Model:
    def __init__(
        self,
        model_name
    ):
        import torch
        print('Testing LLM setup')
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print('GPU device: ' + str(device))
        print(f'Using model {model_name}')

    def inference(
        self,
        prompts: any
    ) -> any:
        print('Testing LLM inference')
        answers = []
        for prompt in prompts:
            try: 
                print('TEST')
                print(prompt)
            except Exception as e:
                print(e)
        return answers