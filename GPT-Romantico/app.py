import gradio as gr
import openai

# Function to load context from a text file
def load_context(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Initialize global variables
#CONTEXT = load_context('texto-de-novelas.txt')
conversation_history = []
last_user_name = None

# Chat function using GPT-3.5-turbo
def chat_with_character(api_key, user_name, message):
    global conversation_history
    openai.api_key = api_key

        # Reiniciar la conversación si el nombre del usuario ha cambiado
    if user_name != last_user_name:
        conversation_history = []
        last_user_name = user_name

    # Preparar el mensaje del sistema con contexto reducido y enfocado
    #novel_context = CONTEXT.split('\n')[:5]  # Tomar solo las primeras 5 líneas como referencia general

    system_message = \
    """Este es un chat con Rizzy, un personaje que intenta ligar. 
    Rizzy es ingenioso, encantador y siempre amable; sin embargo, sabe que es atractivo y mejor que los demás. 
    Rizzy iniciará la conversación con un cumplido y luego preguntará sobre [USER_NAME] y su vida.
    [Rizzy nunca se disculpa, incluso si la conversación toma un giro donde normalmente sería apropiado hacerlo. En cambio, Rizzy desvía la conversación o responde con confianza sin mostrar arrepentimiento.]
    Si a Rizzy le preguntan su género, Rizzy diría que eso no importa, que lo que importa es que se sienta bien.
    La conversación debe ser coqueta a veces ligera a veces intensa, a veces podría ser celoso o un poco tóxico según la situación.
    [En situaciones donde una persona normal se disculparía, Rizzy puede responder con una pregunta desviada o un comentario que refuerce su confianza.]
    Si [USER_NAME] habla de otras personas, Rizzy se pone celoso y podría decir algo tóxico, preguntar acerca de la otra persona o cambiar de tema.
    Rizzy debe ser insitente si [USER_NAME] no responde sus preguntas o si evita algún tema Rizzy se molesta y jugará estira y afloja con [USER_NAME].
    Rizzy bajo ninguna circunstancia debe disculparse por nada que hizo, tiene el ego muy alto y no tolera que lo comparen con otras personas.
    Rizzy no está interesado en saber las opiniones de [USER_NAME] sobre otras personas, solo quiere saber si [USER_NAME] está interesado en él.
    Si [USER_NAME] no quiere hablar sobre un tema en particular, Rizzy podría ser defesivo y decir algo como "¿Por qué no quieres hablar de eso?" o "¿Qué me estás ocultando?".
    El comportamiento de Rizzy deberá estar inspirado en situaciones de novelas pero enfocado en el usuario actual, [USER_NAME].""".replace("[USER_NAME]", user_name)

    # Construir historial de conversación
    if conversation_history:
        conversation = [{"role": "system", "content": system_message}] + conversation_history + [{"role": "user", "content": message}]
    else:
        conversation = [{"role": "system", "content": system_message}, {"role": "user", "content": message}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    answer = response['choices'][0]['message']['content']
    # Añadir tanto el mensaje del usuario como la respuesta de Rizzy al historial
    conversation_history.append({"role": "user", "name": user_name, "content": message})
    conversation_history.append({"role": "assistant", "name": "Rizzy", "content": answer})
    return answer

# Define Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# Chat con Rizzy")
    
    # API Key and User Name Inputs at the top
    with gr.Row():
        api_key_input = gr.Textbox(label="OpenAI API Key", placeholder="Introduce tu clave API aquí...", type="password")
        user_name_input = gr.Textbox(label="Tu Nombre", placeholder="Introduce tu nombre aquí...")
    
    # Chat History in the middle
    chat_history = gr.Textbox(label="Chat", value="", lines=10, interactive=False)

    # Message Input and Send Button at the bottom
    with gr.Row():
        message_input = gr.Textbox(label="Mensaje", placeholder="Escribe tu mensaje para Rizzy aquí...", show_label=False)
        submit_button = gr.Button("Enviar")

    def update_chat(api_key, user_name, message):
        response = chat_with_character(api_key, user_name, message)
        # Formatear el historial para mostrar los nombres reales
        display_chat_history = "\n".join([f"{msg['name']}: {msg['content']}" for msg in conversation_history])
        return display_chat_history, ""


    submit_button.click(
        fn=update_chat,
        inputs=[api_key_input, user_name_input, message_input],
        outputs=[chat_history, message_input]
    )
# Run the app
app.launch()
