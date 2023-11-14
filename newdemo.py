import openai
import numpy as np
from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

test_type = [
    {
        "name": "lipid panel",
        "contextFile": "lipid_panel_context.txt",
        "subTests": [
            {
                "name": "total cholesterol",
                "shortened": "tc",
                "rangeFlag": 1,
                "rangeHigh": 199,
                "rangeLow": 150 
            },
            {
                "name": "low-density lipoprotein cholesterol",
                "shortened": "ldl",
                "rangeFlag": 1,
                "rangeHigh": 130,
                "rangeLow": 0 
            },
            {
                "name": "high-density lipoprotein cholesterol",
                "shortened": "hdl",
                "rangeFlag": 1,
                "rangeHigh": np.inf,
                "rangeLow": 40 
            },
            {
                "name": "triglycerides",
                "shortened": "triglycerides",
                "rangeFlag": 1,
                "rangeHigh": 150,
                "rangeLow": 0 
            }
        ]        
    },
    {
        "name": "hemoglobin a1c",
        "contextFile": "hemoglobin_a1c_context.txt",
        "subTests": [
            {
                "name": "hemoglobin a1c",
                "shortened": "HbA1c",
                "rangeFlag": 1,
                "rangeHigh": 8.5,
                "rangeLow": 4.7 
            }
        ]
    }
]



prompt = "Provide information on when each test was conducted and the frequency of these tests. Explain why each test was administered. Include info on the medical necessity and relevance of each test. Include the potential impact of any deviations to the norm on the patient's health."

def demo(data):
    context_file_name = test_type[data["testId"]]["contextFile"]
    file=open(context_file_name,"r")
    context = "".join(file.readlines())

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
