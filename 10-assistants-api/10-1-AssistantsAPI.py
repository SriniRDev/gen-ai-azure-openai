#!/usr/bin/env python
# coding: utf-8

# # ASSISTANTS API
# 
# This notebook demonstrates the use of the Assistants API from Azure OpenAI to create and interact with a custom AI assistant. The Assistants API enables the creation and management of conversational assistants with specific instructions and tools.
# 
# Steps Covered:
# 
# 1. Assistant Creation: Define a new assistant by specifying its custom instructions and selecting a model. Tools like the Code Interpreter are enabled to enhance the assistant's capabilities.
# 
# 2. Thread Creation: Initialize a new conversation thread where interactions with the assistant will take place.
# 
# 3. Message Addition: Send messages to the thread, simulating user queries or prompts that the assistant will respond to.
# 
# 4. Running the Assistant: Execute the assistant on the thread to generate responses based on the provided instructions and user inputs. The notebook handles the response retrieval and displays the text content.
# 
# 5. Chat Completions API needs the full conversation to be passed as the body to OpenAI for getting the context but in Assitant API we just need to pass assitant id and thread id.

# In[1]:


get_ipython().system('pip install openai')


# In[2]:


# Step 2: Set up your environment variables for the Azure OpenAI endpoint and API key.
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
load_dotenv('azureopenai.env')
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
print (azure_endpoint)
print (azure_endpoint)


# In[3]:


import os
from openai import AzureOpenAI

# Initialize the Azure OpenAI client with environment variables for the endpoint, API key, and API version
client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),                 
  api_version="2024-05-01-preview"
)

# Create a new assistant with specific instructions and tools
assistant = client.beta.assistants.create(
  name="Math Tutor",  # Name of the assistant
  instructions="You are a personal maths tutor. Write and run code to answer maths questions.",  # Instructions for the assistant
  tools=[] , # Specify the tool to be used by the assistant ({"type": "code_interpreter"})
model="gpt-aoai-text",  # Specify the deployment name to use
)


# In[4]:


# Create a new thread to hold the conversation
thread = client.beta.threads.create()
#thread is an object type which contains a field id which is the unique identifier 
#of the conversation/thread we have created


# In[6]:


# Send a message from the user to thread
message = client.beta.threads.messages.create(
  thread_id=thread.id,  # The ID of the thread to send the message to
  role="user",  # Role of the sender (user in this case)
  content="I need to solve the equation `3x + 11 = 14`. Can you help me?"  # Content of the message
)

# Run the assistant to process the thread and respond
run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,  # The ID of the thread to run the assistant on
  assistant_id=assistant.id,  # The ID of the assistant to use
  instructions="Please give step by step explanation."  # Instructions for the assistant
)


# In[7]:


# Check if the run status is 'completed'
if run.status == 'completed':
  # Fetch the list of messages from the thread
  messages = client.beta.threads.messages.list(
    thread_id=thread.id  # The ID of the thread to fetch messages from
  )
  # Extract and print the text content from the messages
  for msg in messages.data:  # Iterate over each message in the list of messages
        for content_block in msg.content:  # Iterate over each content block in the message
            if content_block.type == 'text':  # Check if the content block is of type 'text'
                print(content_block.text.value)  # Print the text content value
else:
  # Print the status of the run if it is not 'completed'
  print(run.status)


# In[8]:


while True:
    # Get user input
    user_input = input("Enter your question (or type 'exit' to quit): ")

    # Exit the loop if the user types 'exit'
    if user_input.lower() == 'exit':
        print("Exiting the chat.")
        break

    # Send a message to the thread from the user
    message = client.beta.threads.messages.create(
        thread_id=thread.id,  # The ID of the thread to send the message to
        role="user",  # Role of the sender (user in this case)
        content=user_input  # Content of the message from the user
    )

    # Run the assistant to process the thread and respond
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,  # The ID of the thread to run the assistant on
        assistant_id=assistant.id,  # The ID of the assistant to use
        instructions="Give Step by Step explanation."  # Instructions for the assistant
    )

    # Check if the run status is 'completed'
    if run.status == 'completed':
        # Fetch the list of messages from the thread
        messages = client.beta.threads.messages.list(
            thread_id=thread.id  # The ID of the thread to fetch messages from
        )
        # Extract and print only the last message from the assistant
        last_message = messages.data[0].content[0].text.value
        print("Assistant:", last_message)
    else:
        # Print the status of the run if it is not 'completed'
        print("Run status:", run.status)


# In[ ]:




