from openai import OpenAI
import time
import random
import logging
import datetime
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#Write the log by creating a module level logger to do the logging
log = logging.getLogger("assistant")
#configure log file
logging.basicConfig(filename='assistant.log', level=logging.INFO)

client = OpenAI()

#create assistant object, with file ids passed to it
assistant = client.beta.assistants.retrieve(
    assistant_id = "asst_ndwvfyrmD9ACUGBp4o94D3pw"
)

# Update the assistant with the new file
# To make the files accessible to your assistant, update the assistant’s tool_resources with the new vector_store id.
assistant = client.beta.assistants.update(
    assistant_id = assistant.id,
    tool_resources={"file_search": {"vector_store_ids": ["vs_k2nCdJ1xhYkJKkLAU9H7nRx2"]}},
)

#print(assistant)

#upload file for assistants
#rb stands for "read" "binary"
#open() returns a file object
#curriculum_knowledge = client.files.create(
    #file = open("OpenAIChatCompletionsAPICheatsheet.pdf", "rb"),
    #purpose = "assistants"
#)

#print(curriculum_knowledge)

#assistant_files = client.beta.assistants.files.list(
    #"asst_ndwvfyrmD9ACUGBp4o94D3pw"
#)

#print(assistant_files)
#exit()

#Return appropriate response based on status value
def status_message(run_status):
    if run_status == "completed":
        #extract the most recent message content when the run is completed
        thread_messages = client.beta.threads.messages.list(
            thread_id = thread.id
        )
        message = thread_messages.data[0].content[0].text.value

    if run.status in ["cancelled", "failed", "expired"]:
        message = "An error has occurred, please try again."

    return message

#check status details
def process_run(thread_id, assistant_id):
    #create a run
    new_run = client.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id = assistant_id
    )

    phrases = ["Thinking", "Pondering", "Dotting the i's", "Achieving world peace"]

    #monitor the run status at regular intervals until the status of the run is complete
    while True:
        #add a one-second delay between each run status check
        time.sleep(1)
        print(random.choice(phrases) + "...")
        #check the status of the run
        run_check = client.beta.threads.runs.retrieve(
            thread_id = thread_id,
            run_id = new_run.id
        )
        if run_check.status in ["cancelled", "failed", "completed", "expired"]:
            return run_check
        
#log error if status is cancelled, failed, or expired
def log_run(run_status):
    if run_status in ["cancelled", "failed", "completed", "expired"]:
        log.error("\nDate: " + str(datetime.datetime.now()) + "\nRun status: " + str(run_status))

#create a thread
thread = client.beta.threads.create()

user_input = ""

while True:
    if (user_input == ""):
        print("Assistant: Hello there! Just so you know, you can type exit to end our chat. What's your name? ")
        #the model doesn't always recognize the answer as a name
        #hand it directly to the chatbot identified as the user's nameso
        user_name = input("You: ")
        print("Assistant: Hey, " + user_name + "! How can I help you?")
        #prompt the user for their question and assign that to user_input
        user_input = input("You: ")
    else:
        #prompt the user for input
        user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bye bye now, have a good one!")
        exit()

    #use the prompt to create a message within the thread
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = user_input
    )

    run = process_run(thread.id, assistant.id)

    log_run(run.status)

    message = status_message(run.status)

    print("\nAssistant: " + message + "\n")

    # Use the create and poll SDK helper to create a run and poll the status of
    # the run until it's in a terminal state.

    #run = client.beta.threads.runs.create_and_poll(
        #thread_id=thread.id, assistant_id=assistant.id
    #)

    #messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

    #message_content = messages[0].content[0].text
    #annotations = message_content.annotations
    #annotations = message.annotations
    #citations = []
    #for index, annotation in enumerate(annotations):
        #message.value = message.value.replace(annotation.text, f"[{index}]")
        #if file_citation := getattr(annotation, "file_citation", None):
            #cited_file = client.files.retrieve(file_citation.file_id)
            #citations.append(f"[{index}] {cited_file.filename}")

    #print(message.value)
    #print("\n".join(citations))
    #citations = []
    #for index, annotation in enumerate(annotations):
        #message.value = message.value.replace(annotation.text, f"[{index}]")
        #if file_citation := getattr(annotation, "file_citation", None):
            #cited_file = client.files.retrieve(file_citation.file_id)
            #citations.append(f"[{index}] {cited_file.filename}")

    #print(message.value)
    #print("\n".join(citations))