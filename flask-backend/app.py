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
    
@app.route('/checkboxes', methods=['POST'])
def handlecheckboxes():
    data = request.get_json()
    checkbox_id = data.get('checkboxId')
    if checkbox_id == '1':
        print("##1#plik złoty####")
        gold='''Zamawiający nie powinien mieć prawa do zmiany lub cesji umowy bez uprzedniej pisemnej zgody Wykonawcy."Nowość" oznacza 
        zastąpienie jednej z pierwotnych stron nową stroną, na co wszystkie strony wyrażają zgodę, a następnie natychmiastowe wygaśnięcie 
        wzajemnych zobowiązań przewidzianych w umowie i zawarcie nowej wykonalnej umowy o tej samej treści."Cesja" oznacza częściowe 
        przeniesienie praw i/lub obowiązków wynikających z umowy.Cesja w celach finansowych bez zwiększenia obowiązków lub odpowiedzialności 
        Zleceniobiorcy lub ograniczenia praw jest ogólnie dopuszczalna.Umowa nie powinna zezwalać na cesję / nowację na rzecz osoby trzeciej
        (i) których działalność jest utrudniona przez międzynarodowe lub krajowe wymogi w zakresie handlu zagranicznego i celnego lub jakiekolwiek embarga;
        (ii) która sama lub jej obecni lub byli przedstawiciele prawni, dyrektorzy lub funkcjonariusze zostali skazani za przestępstwo, które mogłoby zagrozić 
        ich uczciwości zawodowej (np. korupcja, pranie pieniędzy itp.) w ciągu pięciu lat poprzedzających nowację/cesję.'''
        #print(gold)
        question=gold
        mode='file'
        try:
            answer = service.askGPT_with_knowladge_base_checkboxes(
                collection_name=mode,
                question=question,
                returned_chunks=4,
            )
            print(answer)
            return jsonify({'answer': answer})
    
        except Exception as ex:
            print(ex)

    elif checkbox_id == '2':
        print("##2#plik złoty####")
        gold='''Umowa powinna zawierać ogólne ograniczenie odpowiedzialności na rzecz Wykonawcy z limitem nieprzekraczającym 100% Ceny Kontraktowej.
            Limit ten powinien mieć zastosowanie do wszystkich odszkodowań, kar umownych, roszczeń odszkodowawczych i odszkodowawczych bez względu 
            na podstawę prawną roszczeń.Niektóre wyjątki mogą być dopuszczone w wyjątkowych okolicznościach:obowiązkowa/niezależna odpowiedzialność za produkt,
            obowiązkowe roszczenia osób trzecich z tytułu uszkodzenia ciała i śmierci,umyślne wykroczenie lub oszustwo,'''
        question=gold
        mode='file'
        try:
            answer = service.askGPT_with_knowladge_base_checkboxes(
                collection_name=mode,
                question=question,
                returned_chunks=4,
            )
            print(answer)
            return jsonify({'answer': answer})
    
        except Exception as ex:
            print(ex)
    elif checkbox_id == '3':
        print("##3#plik złoty####")
        gold='''25.4 Maksymalna łączna odpowiedzialność Wykonawcy wynikająca z niniejszej Umowy, niezależnie od teorii prawnej,
        na której się opiera, w tym między innymi odpowiedzialność kontraktowa lub deliktowa (w tym zaniedbanie i odpowiedzialność na zasadzie ryzyka),
        z tytułu rękojmi lub inna, nie może przekroczyć Całkowitej Ceny Umownej.25.8 Bez względu na jakiekolwiek odmienne postanowienia niniejszej Umowy,
        punkt 25.4 nie ogranicza żadnych:
        (i) odpowiedzialność wynikająca z naruszenia przepisów ustawowych lub wykonawczych;
        (ii) odpowiedzialność wynikająca z oszustwa, świadomego wprowadzenia w błąd, winy umyślnej;
        (iii) odpowiedzialność za śmierć lub obrażenia ciała spowodowane przez Stronę w wyniku zaniedbania, w tym jej Podmioty Stowarzyszone, członków zarządu,
        pracowników, agentów lub wykonawców;
        (iv) odpowiedzialność za inne roszczenia, których nie można wyłączyć ani ograniczyć na mocy bezwzględnie obowiązującego prawa.
        '''
        question=gold
        mode='file'
        try:
            answer = service.askGPT_with_knowladge_base_checkboxes(
                collection_name=mode,
                question=question,
                returned_chunks=4,
            )
            print(answer)
            return jsonify({'answer': answer})
            
        except Exception as ex:
                print(ex)
    return jsonify({'message': f'Dane dla {checkbox_id} zostały pomyślnie otrzymane.'})

if __name__ == '__main__':
    milvus.connect()
    app.run(port=5000)