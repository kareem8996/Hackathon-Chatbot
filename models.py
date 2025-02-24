
from groq import Groq
from tenacity import retry, stop_never, wait_exponential, RetryError
import streamlit as st
import streamlit as st

messages=[
        {
            "role": "system",
            "content": st.secrets['info']
        },]

client = Groq(api_key=st.secrets['api_key'])
main_model='llama-3.3-70b-versatile'

# @retry(stop_never,wait_exponential(5))
def generic_response(user_prompt,messages=messages):

    if len(messages)>10:
        messages=clean_messages(messages,3)

    messages.append({
            "role": "user",
            "content": user_prompt,
        })
    response = client.chat.completions.create(
        model=main_model,
        messages=messages,
        stream=True
                )
    return response


def clean_messages(messages, times):
    """
    Removes elements from a list of messages until it reaches and includes an 'assistant' role.
    Repeats the process for a specified number of times.

    Parameters:
    - messages: List of message dictionaries.
    - times: Number of times to repeat the cleanup.

    Returns:
    - A list of cleaned messages.
    """
    # Always keep the first message as the system instruction
    cleaned_messages = [messages[0]] 
    counter=0
    for i in range(1, len(messages)):
        if messages[i]['role'] == 'assistant':
            counter+=1
        
        if counter==times:
            cleaned_messages.extend(messages[i+1:])
            return cleaned_messages
    
    return messages