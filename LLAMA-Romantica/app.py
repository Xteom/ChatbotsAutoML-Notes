# import gradio as gr

# gr.ChatInterface(get_llama_response).launch()

import gradio as gr

def greet(name):
    return "Hello " + name + "!!"

iface = gr.Interface(fn=greet, inputs="text", outputs="text")
iface.launch()