import os
import openai
from config import key
openai.organization = "org-ycDOpbikWxghu0rbHuV0uEW5"
openai.api_key = key
response = openai.Completion.create(
    model="text-davinci-003",
    prompt="letter formate",
    max_tokens=256,
    temperature=1,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
print(response)


