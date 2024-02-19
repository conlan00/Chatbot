const node = document.getElementById("userInput");
				
node.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        sendMessage()
    }

});