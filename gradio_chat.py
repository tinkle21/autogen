import random
import gradio as gr

def random_response(message, history):
    return random.choice(["Yes", "No"])

history =[
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "Paris"}
]
message ="And what is its largest city?"
gr.ChatInterface(
    fn=random_response, 
    type="messages"
).launch()