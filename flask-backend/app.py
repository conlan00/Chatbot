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

@app.route('/collection/drop', methods=['POST'])
def drop_collection():
    print("Try dropping collection...")
    response = service.drop_collection(name="file")
    print(response)
    return jsonify({'answer': response})
    
@app.route('/files', methods=['POST'])
def receiveDocuments():
    files = request.files.getlist('files')
    for file in files:
        print("Received file:", file.filename)
        if not file.filename.endswith('.pdf'):
            return 'Invalid file type. Only PDF files are allowed.', 400
    service.handleFiles(files)
    return jsonify({'answer': 'Files received successfully'})

@app.route('/ask/knowledge', methods=['POST'])
def ask_knowledge():
    question = request.json['message']
    mode = request.json['mode']
    
    print("Pytanie: " + question, "\n","Tryb: " + mode)
    
    try:
        answer = service.askGPT_with_knowladge_base(
            collection_name=mode,
            question=question,
            returned_chunks=4,
        )
        
        return jsonify({'answer': answer})
    
    except Exception as ex:
        print(ex)
        return jsonify({'answer': 'SERVER ERROR'})
        
if __name__ == '__main__':
    milvus.connect()
    app.run(port=5000, debug=True)