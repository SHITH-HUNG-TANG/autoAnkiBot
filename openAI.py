
import os
import openai
import configparser

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Load your API key from an environment variable or secret management service
openai.api_key = config['OPENAI']['ACCESS_TOKEN']

# response = openai.Completion.create(model="text-davinci-003", prompt="hi", temperature=0, max_tokens=7)

def openAIChat(prompt):
    # response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=100)
    

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", "AI:"]
        )
    result = response['choices'][0]['text']
    return result

def keyToImage(prompt):
    response = openai.Image.create(
    prompt = prompt,
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url



if __name__ == '__main__':
    a = openAIChat("台灣是中國的嗎")
    print(a)
