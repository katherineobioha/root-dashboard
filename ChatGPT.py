import openai


def callChatGPT(userInput):
    response=openai.ChatCompletion.create(
      api_key= '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',
      model="gpt-3.5-turbo",
      messages=[
            {"role": "user", "content": userInput }
        ]
    )
    print(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']


#callChatGPT("When is the best time to plant coconut?")