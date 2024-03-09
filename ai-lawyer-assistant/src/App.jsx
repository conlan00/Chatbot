import React, { useEffect, useState } from 'react';
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [inuputFiles, setInputFiles] = useState(false);

  useEffect(() => {
    function handleVisibilityChange() {
      if (document.visibilityState === 'hidden') {
        chrome.runtime.sendMessage({ action: "executeOnClose" });
      }
    }
  
    document.addEventListener('visibilitychange', handleVisibilityChange);
  
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  const performAction = async () => {
      const response = await fetch('http://localhost:5000/collection/drop', {
          method: 'POST',
      });

      const responseData = response.json();
      console.log(responseData.answer)
      window.close()
}

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSendMessage = () => {
    setMessages([...messages, { text: input, sender: 'user' }]);
    setInput('');
  };

  const handleAskGPT = async () => {
    setMessages(prevMessages => [...prevMessages, { text: input, sender: 'user' }]);
    setInput('');

    let requestBody = {
      'message': input
    };

    requestBody.mode = inuputFiles ? 'file' : 'base';

    const jsonBody = JSON.stringify(requestBody);

    const response = await fetch('http://localhost:5000/ask/knowledge', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonBody,
    });
    const responseData = await response.json();
    console.log(responseData.answer);

    setMessages(prevMessages => [...prevMessages, { text: responseData.answer, sender: 'model' }]);
    setInput('');
  };

  const displayFileNames = () => {
    var input = document.getElementById("pdf-upload");
    var fileNames = [];
    for (var i = 0; i < input.files.length; i++) {
      fileNames.push(input.files[i].name);
    }
    document.getElementById("filenames").innerHTML = "Pliki: " + "<br />" + fileNames.join(", ");
  }

  const handleDocumentSend = async (e) => {
    e.preventDefault();

    const files = document.getElementById('pdf-upload').files;
    console.log(files.length)
    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
      formData.append(`files`, files[i])
    }

    try {
      const respone = await fetch('http://localhost:5000/files', {
        method: 'POST',
        body: formData,
      });

      const responseData = await respone.json()
      console.log("Files send successfully");
      console.log(responseData.answer);

    } catch (error) {
      console.error(error);
    }
  }
  // ja pisalem - obsluga checkboxa
  const handleCheckboxChange = (event, checkboxId) => {
    if(event.target.checked){
      switch(checkboxId) {
        case '1':
          console.log(`Checkbox ${checkboxId} został ${event.target.checked ? 'zaznaczony' : 'odznaczony'}.`);
          sendDataToEndpoint(checkboxId)
          break;
        case '2':
          console.log(`Checkbox ${checkboxId} został ${event.target.checked ? 'zaznaczony' : 'odznaczony'}.`);
          sendDataToEndpoint(checkboxId)
          break;
        case '3':
          console.log(`Checkbox ${checkboxId} został ${event.target.checked ? 'zaznaczony' : 'odznaczony'}.`);
          sendDataToEndpoint(checkboxId)
          break;
        default:
          // Domyślna logika, jeśli potrzebna
          break;
      }
    }
    

  };
  //wyslanie parametru na endpoint checkboxa
  const sendDataToEndpoint = async (checkboxId) => {
    try {
      const response = await fetch('http://localhost:5000/checkboxes', {
        method: 'POST', // lub 'GET', zależnie od wymagań API
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ checkboxId }), // Przesłanie jedynie checkboxId
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      // console.log('Success:', data);
      setMessages(prevMessages => [...prevMessages, { text: data.answer, sender: 'model' }]);
      setInput('');
    } catch (error) {
      console.error('Error:', error);
    }
  };
  return (
    <>
      <div className=" font-kanit text-slate-200 text-xl container m-auto max-w-screen-md">
        <div className='flex justify-between'>
          <h1 className=" ml-10 mt-5">Witaj w AI Lawyer Assistant</h1>
          <button className='mr-10 mt-5' onClick={() => {performAction()}}>
          <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-x" width="32" height="32" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/>
            <path d="M18 6l-12 12" />
            <path d="M6 6l12 12" />
          </svg>
          </button>
        </div>
        <FormControlLabel control={<Switch onChange={() => {setInputFiles(!inuputFiles)}} sx={{ml:5, mt:2, alignContent:'center'}}/>} label="Wgraj własne pliki"/> 
        <div className='flex flex-col border border-slate-400 rounded-xl w-85-screen max-w-screen-md pb-5 mt-5 m-auto font-light text-base'>
          <div className='flex flex-col place-self-center h-96 w-full p-5 overflow-y-auto'>
            <div className='pt-5'>
              {messages.map((message, index) => (
                <div key={index} className={`${message.sender === 'user' ? ' self-end' : ''} mb-8 break-words relative`}>
                  <div className=' absolute -top-7 left-0'>
                    <svg xmlns="http://www.w3.org/2000/svg" class={`icon icon-tabler icon-tabler-user ${message.sender === 'user' ? 'block' : 'hidden'}`} width="26" height="26" viewBox="0 0 24 24" stroke-width="1.5" stroke="#65a30d" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                      <path d="M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0" />
                      <path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" />
                    </svg>
                    <svg xmlns="http://www.w3.org/2000/svg" class={`icon icon-tabler icon-tabler-user ${message.sender === 'model' ? 'block' : 'hidden'}`} width="26" height="26" viewBox="0 0 24 24" stroke-width="1.5" stroke="#65a30d" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                      <path d="M6 5h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12a2 2 0 0 1 2 -2z" />
                      <path d="M9 16c1 .667 2 1 3 1s2 -.333 3 -1" />
                      <path d="M9 7l-1 -4" />
                      <path d="M15 7l1 -4" />
                      <path d="M9 12v-1" />
                      <path d="M15 12v-1" />
                    </svg>
                  </div>
                  {message.text}
                </div>
              ))}
            </div>
          </div>
          {/* <div className='flex justify-between mt-5'>
            <input type="text" placeholder='Zadaj pytanie...' className='w-full p-2 mx-4 rounded-xl' value={input} onChange={handleInputChange} onKeyDown={(e) => { if(e.key === 'Enter') handleAskGPT(); }}/>
            <button onClick={handleAskGPT}>
              <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-square-rounded-arrow-up-filled mr-4" width="32" height="32" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                <path d="M12 2c-.218 0 -.432 .002 -.642 .005l-.616 .017l-.299 .013l-.579 .034l-.553 .046c-4.785 .464 -6.732 2.411 -7.196 7.196l-.046 .553l-.034 .579c-.005 .098 -.01 .198 -.013 .299l-.017
                 .616l-.004 .318l-.001 .324c0 .218 .002 .432 .005 .642l.017 .616l.013 .299l.034 .579l.046 .553c.464 4.785 2.411 6.732 7.196 7.196l.553 .046l.579 .034c.098 .005 .198 .01 .299 .013l.616 .017l.642
                  .005l.642 -.005l.616 -.017l.299 -.013l.579 -.034l.553 -.046c4.785 -.464 6.732 -2.411 7.196 -7.196l.046 -.553l.034 -.579c.005 -.098 .01 -.198 .013 -.299l.017 -.616l.005 -.642l-.005 -.642l-.017
                   -.616l-.013 -.299l-.034 -.579l-.046 -.553c-.464 -4.785 -2.411 -6.732 -7.196 -7.196l-.553 -.046l-.579 -.034a28.058 28.058 0 0 0 -.299 -.013l-.616 -.017l-.318 -.004l-.324 -.001zm-.148 5.011l.058
                    -.007l.09 -.004l.075 .003l.126 .017l.111 .03l.111 .044l.098 .052l.104 .074l.082 .073l4 4a1 1 0 0 1 -1.32 1.497l-.094 -.083l-2.293 -2.292v5.585a1 1 0 0 1 -1.993 .117l-.007 -.117v-5.585l-2.293
                     2.292a1 1 0 0 1 -1.32 .083l-.094 -.083a1 1 0 0 1 -.083 -1.32l.083 -.094l4 -4a.927 .927 0 0 1 .112 -.097l.11 -.071l.114 -.054l.105 -.035l.118 -.025z" fill="currentColor" stroke-width="0" />
              </svg>
            </button>
          </div> */}
        </div>
        <div className={`${inuputFiles ? 'flex' : 'hidden'} justify-between align-top ml-10 text-base font-normal mt-5`}>
          <div className='flex flex-col'>
          <div class='flex flex-col'>
            <div class="flex items-center">
                <input type="checkbox" id="checkbox1" className="mr-2 w-auto bg-white" onChange={(e) => handleCheckboxChange(e, '1')}/>
                <label for="checkbox1">Assign "Cesja"</label>
                <input type="checkbox" id="checkbox2" className="mr-2 w-auto bg-white" onChange={(e) => handleCheckboxChange(e, '2')}/>
                <label for="checkbox2">Limitation of Liability - price </label>
                <input type="checkbox" id="checkbox3" className="w-auto bg-white" onChange={(e) => handleCheckboxChange(e, '3')}/>
                <label for="checkbox3">Maximum aggregate liability</label>
            </div>
          </div>
            <label htmlFor="pdf-upload" className='mb-3'>Prześlij pliki .pdf do modelu</label>
            <input type="file" id="pdf-upload" accept='.pdf' multiple onChange={displayFileNames}/>
            <div id='filenames' className='mt-3'></div>
          </div>
          
          <div className=' flex-shrink mr-5'>
          
            <button className='py-2 px-4 bg-slate-600 border hover:bg-slate-700 border-slate-500 rounded-xl mr-5' onClick={handleDocumentSend}>Prześlij</button>
          </div>
        </div>
      </div>
    </>
  )
}

export default App
