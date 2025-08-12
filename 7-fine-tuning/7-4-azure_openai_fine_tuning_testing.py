#!/usr/bin/env python
# coding: utf-8

# # Fine-Tuning Models with Azure OpenAI
# 
# Fine-tuning a pre-trained language model allows you to tailor it to your specific tasks, enhancing its performance for specialized applications. This process involves training the model on a custom dataset to make it more effective for your particular use case.
# 
# In this notebook, you will find a comprehensive guide to fine-tuning a model using Azure OpenAI. 
# 
# The steps covered are:
#     
# 1. Installing the OpenAI Python package
# 2. Creating datasets: Prepare your training and validation datasets in the required JSONL format.
# 3. Uploading fine-tuning files: Upload your training and validation datasets to Azure OpenAI.
# 4. Creating a fine-tuning job: Initiate the fine-tuning process using your datasets and a base model.
# 5. Monitoring the fine-tuning job: Retrieve and check the status of your fine-tuning job.
# 6. Deploying the fine-tuned model: Deploy the customized model for inference.
# 7. Using the fine-tuned model: Make inference calls using your newly fine-tuned model.
# 
# 

# In[32]:


# Step-1 : Installing the OpenAI Python package

get_ipython().system('pip install --upgrade openai')


# In[34]:


# Step 2 & 3 : Uploading fine-tuning files: Upload your training and validation datasets to Azure OpenAI.

from openai import AzureOpenAI
from dotenv import load_dotenv
import os
load_dotenv('azureopenai.env')

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),                 
  api_version="2024-05-01-preview"
)


# Define file names for the training and validation datasets.
training_file_name = 'training.jsonl'  # This is the file name for the training dataset.
validation_file_name = 'validation.jsonl'  # This is the file name for the validation dataset.


# Upload the training dataset file to Azure OpenAI using the SDK.
training_response = client.files.create(
    file=open(training_file_name, "rb"),  # Opens the training dataset file in binary read mode.
    purpose="fine-tune"  # Specifies the purpose of the file upload as fine-tuning.
)
# Store the ID of the uploaded training file.
training_file_id = training_response.id

# Upload the validation dataset file to Azure OpenAI using the SDK.
validation_response = client.files.create(
    file=open(validation_file_name, "rb"),  # Opens the validation dataset file in binary read mode.
    purpose="fine-tune"  # Specifies the purpose of the file upload as fine-tuning.
)
# Store the ID of the uploaded validation file.
validation_file_id = validation_response.id

# Print the IDs of the uploaded training and validation files.
print("Training file ID:", training_file_id)
print("Validation file ID:", validation_file_id)


# In[42]:


# Step 4: Create a fine-tuning job using the uploaded training and validation files.
response = client.fine_tuning.jobs.create(
    training_file=training_file_id,  # Use the ID of the uploaded training file.
    validation_file=validation_file_id,  # Use the ID of the uploaded validation file.
    model="gpt-35-turbo-1106"  # Specify the base model name. Note that Azure OpenAI model names use dashes and cannot contain dots.
    )

# Store the job ID for monitoring the status of the fine-tuning job.
job_id = response.id

# Print the job ID and its status.
print("Job ID:", response.id)
print("Status:", response.status)
# Print the full response in JSON format for detailed information.
print(response.model_dump_json(indent=2))


# In[44]:


# Step 5: Retrieve the status of the fine-tuning job using the job ID.

import time
while True:
    response = client.fine_tuning.jobs.retrieve(job_id)

    # Print the job ID and its status.
    print("Job ID:", response.id)
    print("Status:", response.status)


    # Check the status and break the loop if the job is not running.
    if response.status != "running":
        # Print the full response in JSON format for detailed information.
        print(response.model_dump_json(indent=2))
        break

    # Wait for 15 seconds before checking again.
    time.sleep(30)

# Get the fine-tuned model name after the job has completed.
fine_tuned_model = response.fine_tuned_model


# In[54]:


# Step 7: Use the fine-tuned model for inference.

import os  # This module provides a way to use operating system dependent functionality.
from openai import AzureOpenAI  # This imports the AzureOpenAI class from the OpenAI Python package.

#Initialize the AzureOpenAI client with your endpoint and API key.
client = AzureOpenAI(
  azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),  # Retrieve the endpoint from environment variables.
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  # Retrieve the API key from environment variables.
  api_version="2024-05-01-preview"  # Specify the API version.
)

# Create a chat completion request using the fine-tuned model.
response = client.chat.completions.create(
    model="gpt-35-turbo-1106-ft",  # Specify the custom deployment name for your fine-tuned model.
    messages=[
        {"role": "system", "content": "You are a chatbot that always responds in a humorous way."},  # System message setting the assistant's role.
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},  # User's question.
        ]
)

# Print the response from the fine-tuned model.
print(response.choices[0].message.content)


# In[ ]:




