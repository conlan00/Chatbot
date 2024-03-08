from flask import Flask,render_template,request,jsonify,session
import milvus_connection
from flask_session import Session
 
app=Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
@app.route('/')
def hello():
    session['conversation_history'] = []
    milvus_connection.connect()
    return render_template('index.html')


@app.route('/question', methods=['POST'])
def  getQuestion():
    question=request.json['message']
    print(question)
    #inicjalizacja sesji
    if 'conversation_history' not in session:
        print("nie ma w sesji")
        session['conversation_history'] = []
    conversation_history = session['conversation_history']
    answear=None
    stored_chat=None
    if len(conversation_history)==0:
        
        #print('Session is empty'+str(len(conversation_history)))
        #print('Sesja'+str(conversation_history))
        conversation_history.append(f"Użytkownik: {question}")
        answear = milvus_connection.ask(question)
        conversation_history.append(f"Bot: {answear}")
        session['conversation_history'] = conversation_history
        stored_chat = "\n".join(conversation_history)
       
    else:
        #print("")
        """tu napisać ze jezeli juz jest cos w sesji to w metodzie ask musi byc to z sesji podawane do chata aby miał informacje o poprzednich informacjach"""
        conversation_history=session['conversation_history']
        stored_chat = "\n".join(conversation_history)
        #print("=========Przechowywany chat"+stored_chat)
        answear=milvus_connection.ask(question,conversation_history=stored_chat)
        conversation_history.append(f"Użytkownik: {question}")
        conversation_history.append(f"Bot: {answear}")
        session['conversation_history'] = conversation_history
        # conversation_history.append(f"Użytkownik: {question}")
        # print('Session is not empty'+str(conversation_history))
        # print('Sesja'+str(conversation_history))
        
        #print(answear)

    return jsonify({'message':  answear})

if __name__=='__main__':
    app.run(debug=True)