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


callChatGPT("When is the best time to plant coconut?")