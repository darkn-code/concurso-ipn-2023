from flask import render_template, jsonify, request,session,make_response, redirect
from app import create_app
from flask_login import login_required, current_user
from flask_socketio import emit
import openai

openai.api_key = "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"

socketio,app = create_app()

mess_dict =[ {
                "role": "system",
                "content": "Eres EduMentorBot una ai que tiene 3 años y que vives en un servidor en el EduNova y que ayuda con informacion relacionada con EduNova con tramites como inscripcion, servicios de biblioteca, informacion de profesor , y que\nEduNova cuenta con 3 posgrados académicos: Tecnología Avanzada, Física Educativa y Matemática Educativa." 
            }
            ]

def get_openai_response(prompt):
    global mess_dict
    user_dict ={
                "role": "user",
                "content": f"{prompt}"
               }
    mess_dict.append(user_dict)
    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:instituto-politecnico-nacional:edumentorbot-v1-2:83TuL9y8",
        messages=mess_dict,
        temperature=0,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    respuesta = response['choices'][0]['message']['content']
    assistant_dict ={
                "role": "assistant",
                "content": f"{respuesta}"
            }
    mess_dict.append(assistant_dict)
    return respuesta

def save_chat(username,message,bot_response):
    archivo = f"./chat/{str(username[0])}_conversacion.txt"
    mensaje_user = str(username[0]) + ": " + message +"\n"
    mensaje_bot =  "EduMentorBot: " + bot_response +"\n"
    with open(archivo, "a") as f:
        f.write(mensaje_user)
        f.write(mensaje_bot)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',error=error)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('user_message')
    bot_response = get_openai_response(user_message)
    response_data = {'user_message': user_message, 'bot_response': bot_response}
    return jsonify(response_data)

@socketio.on('user_message')
def handle_message(message):
    bot_response = get_openai_response(message)
    username = current_user.id
    save_chat(username,message,bot_response)
    emit('bot_response', {'response': bot_response})

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/main'))
    session['user_ip'] = user_ip
    return response

@app.route('/main',methods=['GET','POST'])
@login_required
def main():
    username = current_user.id
    context = {
        'username' : username
    }
    return render_template('index.html', **context)

if __name__ == '__main__':
    #app.run(host="172.20.0.3",port=8000,debug=True)
    socketio.run(app,host="172.20.0.3",port=8000,debug=True,allow_unsafe_werkzeug=True)

