from flask import Flask, request, jsonify
import service
import milvus

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    question=request.json['message']
    print(question)
    answer = service.askGPT(question)
    return jsonify({'answer': answer})

@app.route('/files', methods=['POST'])
def receiveDocuments():
    files = request.files.getlist('files')
    for file in files:
        print("Received file:", file.filename)
        if not file.filename.endswith('.pdf'):
            return 'Invalid file type. Only PDF files are allowed.', 400
        #get pdf text

        #get text chunks

        #create vectore store

        #save to database
    service.handleFiles(files)
    return jsonify({'answer': 'Files received successfully'})

if __name__ == '__main__':
    milvus.connect()
    app.run(port=5000, debug=True)
    