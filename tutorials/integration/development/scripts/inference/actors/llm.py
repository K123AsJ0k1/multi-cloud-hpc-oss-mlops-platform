import ray

@ray.remote(
    num_gpus=1
)
class LLM_Model:
    def __init__(
        self,
        model_name
    ):
        print('LLM setup')
        import torch
        from transformers import pipeline
        print(f'Using model {model_name}')
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f'GPU device: {device}')
        
        self.generator = pipeline(
            'text-generation',
            model = model_name,
            device = device
        )
        
    def inference(
        self,
        prompts: any
    ) -> any:
        print('LLM inference')
        answers = []
        for prompt in prompts:
            try: 
                result = self.generator(
                    prompt,
                    max_new_tokens = 50,
                    temperature = 0.7,
                    top_k = 50, 
                    top_p = 0.95,
                    do_sample = True
                )
                answers.append(result[0]['generated_text'])
            except Exception as e:
                print(e)
        return answers