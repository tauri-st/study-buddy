from openai import OpenAI
import time

client = OpenAI()

#create assistant object
assistant = client.beta.assistants.create(
    name = "Study Buddy",
    model = "gpt-3.5-turbo",
    instructions = "You are a study partner for students who are newer to technology. When you answer prompts, do so with simple language suitable for someone learning fundamental concepts.",
    tools = []
)

#check status details
def process_run(thread_id, assistant_id):
    #create a run
    new_run = client.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id = assistant_id
    )

    #monitor the run status at regular intervals until the status of the run is complete
    while True:
        #add a one-second delary between each run status check
        time.sleep(1)
        #check the status of the run
        run_check = client.beta.threads.runs.retrieve(
            thread_id = thread_id,
            run_id = new_run.id
        )
        if run_check.status in ["cancelled", "failed", "completed", "expired"]:
            return run_check

#create a thread
thread = client.beta.threads.create()

while True:
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
#extract the most recent message content when the run is completed
thread_messages = client.beta.threads.messages.list(
    thread_id = thread.id
)
message_for_user = thread_messages.data[0].content[0].text.value

#display the message to the user
print("Assistant: " + message_for_user)