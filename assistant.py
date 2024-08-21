from openai import OpenAI

client = OpenAI()

#create assistant object
assistant = client.beta.assistants.create(
    name = "Study Buddy",
    model = "gpt-3.5-turbo",
    instructions = "You are a study partner for students who are newer to technology. When you answer prompts, do so with simple language suitable for someone learning fundamental concepts.",
    tools = []
)

#create a thread
thread = client.beta.threads.create()

#TODO: prompt the user for input
user_input = input("You: ")

#TODO: use the prompt to create a message within the thread
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = user_input
)

#TODO: create a run

#TODO: monitor the run status

#TODO: extract the most recent message content when the run is completed

#TODO: display the message to the user