import openai
from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

file=open("context.txt","r")
context = "".join(file.readlines())

prompt = "Provide information on when each test was conducted and the frequency of these tests. Explain why each test was administered. Include info on the medical necessity and relevance of each test. Include the potential impact of any deviations to the norm on the patient's health."

def demo():
    # Step 1: send the conversation and available functions to GPT  
    messages = [{"role": "system", "content": "You are ChartChat the helpful patient data bot."},
                {"role": "assistant", "content": context},
                {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=messages,
        frequency_penalty = .08
    )
    response_message = response["choices"][0]["message"]
    return response_message
response_message = demo()
print(response_message)
with open('history.txt', 'a') as f:
    writeList = ['\nPrompt: ', prompt, "\nContext: ", context, '\n', "Response: ", response_message["content"], '\n']
    f.writelines(writeList)
f.close()
