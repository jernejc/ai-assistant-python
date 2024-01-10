from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

assistant_id = "asst_TXgDmV8KQnQ6Xzxtbzl7p9ii"
user_prompt = "Who will the Board president call"

def get_response(message_body):

    print("create thread")
    thread = client.beta.threads.create()
    thread_id = thread.id

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    new_message = run_assistant(thread)

    return new_message


def run_assistant(thread):
    
    assistant = client.beta.assistants.retrieve(assistant_id)

    print("run assistant")

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while run.status != "completed":
        print(f"run.status {run.status}")
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value

    print(f"new_message: {new_message}")
    return new_message


new_message = get_response(user_prompt)