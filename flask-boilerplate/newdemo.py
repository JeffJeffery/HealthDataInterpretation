import openai
import numpy as np
from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

test_type = [
    {
        "name": "Lipid Panel",
        "contextFile": "/lipid_panel_context.txt",
        "subTests": [
            {
                "name": "Total Cholesterol",
                "shortened": "tc",
                "rangeFlag": 1,
                "rangeHigh": 199,
                "rangeLow": 150 
            },
            {
                "name": "Triglycerides",
                "shortened": "triglycerides",
                "rangeFlag": 1,
                "rangeHigh": 150,
                "rangeLow": 0 
            },
            {
                "name": "HDL Cholesterol",
                "shortened": "hdl",
                "rangeFlag": 1,
                "rangeHigh": np.inf,
                "rangeLow": 40 
            },
            {
                "name": "LDL Cholesterol",
                "shortened": "ldl",
                "rangeFlag": 1,
                "rangeHigh": 130,
                "rangeLow": 0 
            },
            {
                "name": "Non-HDL Cholesterol",
                "shortened": "non-hdl",
                "rangeFlag": 0,
                "rangeHigh": "none",
                "rangeLow": "none"
            },
            {
                "name": "CHOL/HDL Ratio",
                "shortened": "CHOL/HDL Ratio",
                "rangeFlag": 1,
                "rangeHigh": 5,
                "rangeLow": 0 
            }
        ]        
    },
    {
        "name": "Hemoglobin A1C",
        "contextFile": "hemoglobin_a1c_context.txt",
        "subTests": [
            {
                "name": "Hemoglobin A1C",
                "shortened": "HbA1c",
                "rangeFlag": 1,
                "rangeHigh": 8.5,
                "rangeLow": 4.7 
            }
        ]
    }
]



prompt = "Provide information on when each test was conducted and the frequency of these tests. Explain why each test was administered. Include info on the medical necessity and relevance of each test. Given, the patient's value and whether it is high, low, or within the range, include the potential impact of any deviations to the norm on the patient's health. Do not assume whether the patient's value is high or low; only use the information given"
def demo(data):
    context_file_name = test_type[data["testId"]]["contextFile"]
    file=open("flask-boilerplate/"+context_file_name,"r")
    context = "".join(file.readlines())
    for x in data["results"]:
        name = x["name"]
        value = x["value"]
        rangeFlag = 0
        rangeHigh = 0
        rangeLow = 0
        for y in test_type[data["testId"]]["subTests"]:
            if (y["name"] == name):
                rangeFlag = y["rangeFlag"]
                rangeHigh = y["rangeHigh"]
                rangeLow = y["rangeLow"]
        context += "The patient's value for " + name +  " is " +str(value) + "."
        if(rangeFlag == 1):
            if(value > rangeHigh):
                context += "The patient's value for " + name + " is high."
            elif(value < rangeLow):
                context += "The patient's value for " + name + " is low."
            else:
                 context += "The patient's value for " + name + " is within the range."

    # Step 1: send the conversation and available functions to GPT  
    messages = [{"role": "system", "content": "You are ChartChat the helpful patient data bot."},
                {"role": "assistant", "content": context},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": "if explaining a definition, answer using 1 global metaphor"},
                {"role": "assistant", "content": "answer where a young adult can understand"},
                {"role": "assistant", "content": "answer in paragraph format and use less than 250 words."}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=messages,
        temperature = 0.2
    )
    response_message = response["choices"][0]["message"]
    # response_message = demo()
    # print(response_message)
    with open('history.txt', 'a') as f:
        writeList = ['\nPrompt: ', prompt, "\nContext: ", context, '\n', "Response: ", response_message["content"], '\n']
        f.writelines(writeList)
    f.close()
    return response_message["content"]
