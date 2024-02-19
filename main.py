from flask import Flask,redirect,url_for,render_template,request,jsonify
import milvus_connection
app=Flask(__name__)

@app.route('/')
def hello():
    milvus_connection.connect()
    return render_template('index.html')


@app.route('/question', methods=['POST'])
def  getQuestion():
    question=request.json['message']
    print(question)
    answear=milvus_connection.ask(question)
    #print(answear)


    return jsonify({'message': answear})

if __name__=='__main__':
    app.run(debug=True)