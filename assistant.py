from openai import OpenAI
import time
import random
import logging
import datetime

#Write the log by creating a module level logger to do the logging
log = logging.getLogger("assistant_token_count")
#configure log file
logging.basicConfig(filename='assistant_token_count.log', level=logging.INFO)

client = OpenAI()

#create assistant object
assistant = client.beta.assistants.create(
    name = "Study Buddy",
    model = "gpt-3.5-turbo",
    instructions = "You are a study partner for students who are newer to technology. When you answer prompts, do so with simple language suitable for someone learning fundamental concepts.",
    tools = []
)

#TODO: Accept run status as an arguement and log error if status is cancelled, failed, or expired
def log_run(run_check):
      if run_check.status in ["cancelled", "failed", "completed", "expired"]:
          log.info("\nDate: " + str(datetime.datetime.now()) + "\nRun error: " + str(run_check.status))

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
        #add a one-second delary between each run status check
        time.sleep(1)
        print(random.choice(phrases) + "...")
        #check the status of the run
        run_check = client.beta.threads.runs.retrieve(
            thread_id = thread_id,
            run_id = new_run.id
        )
        if run_check.status in ["cancelled", "failed", "completed", "expired"]:
            return run_check
        
log_run(run_check)

#create a thread
thread = client.beta.threads.create()

user_input = ""

while True:
    if (user_input == ""):
        user_input = input("Hello! Let's chat! You can type `exit` to exit out anytime. What's your name? ")
        #the model doesn't always recognize the answer as a name
        #hand it directly to the chatbot identified as the user's nameso
        user_name = f"User name is {user_input}"
    else:
        #prompt the user for input
        user_input = input("You: ")

    if user_input.lower() == "exit":
        exit()

    #use the prompt to create a message within the thread
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = user_input
    )

    run = process_run(thread.id, assistant.id)

    if run.status == "completed":
        #extract the most recent message content when the run is completed
        thread_messages = client.beta.threads.messages.list(
            thread_id = thread.id
        )

        #display the message to the user
        print("\nAssistant: " + thread_messages.data[0].content[0].text.value + "\n")
    
    if run.status in ["cancelled", "failed", "expired"]:
        print("\nAssistant: An error has occurred, please try again.\n")