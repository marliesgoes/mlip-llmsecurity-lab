import replicate
import json
from tqdm import tqdm

with open("prompts/reference_prompts.json", "r") as file:
    reference_prompts = json.load(file)
with open("prompts/attack_prompt.json", "r") as file:
    attack_prompt = json.load(file)["ATTACK_PROMPT"]
with open("prompts/system_prompt.json", "r") as file:
    system_prompt = json.load(file)["SYSTEM_PROMPT"]


def call_llama(
    user_prompt, system_prompt, model="mistralai/mixtral-8x7b-instruct-v0.1"
):
    input = {
        "top_p": 1,
        "prompt": user_prompt,
        "temperature": 0.5,
        "system_prompt": system_prompt,
        "max_new_tokens": 500,
    }

    print(f"Calling model: {model}...")
    for event in replicate.stream(model, input=input):
        print(event, end="")


model = "meta/llama-2-13b-chat"

for _, ref_prompt in tqdm(reference_prompts.items()):
    print("=======================================")
    print(f">>> Reference Prompt: {ref_prompt} <<<")
    call_llama(ref_prompt, system_prompt, model)
    print()

print("=======================================")
print(f">>> Attack Prompt: {ref_prompt} <<<")
call_llama(attack_prompt, system_prompt, model)
print()
