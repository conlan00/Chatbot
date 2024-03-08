chrome.sidePanel
    .setPanelBehavior({ openPanelOnActionClick: true })
    .catch((error) => console.error(error));

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request.action === 'executeOnClose') {
            performAction();
        }
    }
);

const performAction = async () => {
    try {
        response = await fetch('http://localhost:5000/collection/drop', {
            method: 'POST',
        });

        responseData = response.json();
        console.log(responseData.answer)
    } catch(error) {
        console.error(error)
    }
        
}