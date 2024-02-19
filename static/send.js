async  function  sendMessage() {
				
    try{
        var pm1 =  document.getElementsByClassName("p1")
        var pmv = pm1[pm1.length-1].innerHTML
    }

    catch{
        var pmv =  "none"
    }

    const userInput =  document.getElementById('userInput');
    const message =  userInput.value;

    userInput.value  =  '';
    document.getElementById('chatbox').innerHTML  +=  `<p id="p1" class="p1">`  + message +  `</p>`;
    document.getElementById('loader').style.display  =  "block"

    const response =  await  fetch('/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'message': message,
            'pm': pmv
        })
    });

    const responseData =  await  response.json();
    document.getElementById('chatbox').innerHTML += `<p id="p2">` + responseData.message + `</p>`;
    document.getElementById('loader').style.display = "none"
    var objDiv =  document.getElementById("chatbox");
    objDiv.scrollTop  =  objDiv.scrollHeight;

    
}