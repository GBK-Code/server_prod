async function submit() {
    const titleText = document.getElementById("titleInput").value;
    const detailsText = document.getElementById("detailsInput").value;

    const submittedText = document.getElementById("submitReceivedText")
    const switchType = document.getElementById("ideaSwitch").checked

    var type = ""

    if (switchType) {
        type = "Bug"
    }
    else {
        type = "Idea"
    }

    const response = await fetch("/submit", {
        method: "POST",
        headers: {"Accept": "application/json", "Content-type": "application/json"},
        body: JSON.stringify({
            title: titleText,
            details: detailsText,
            theme: type
        })
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data)
        if (data["status"] === "saved")
        {
            submittedText.textContent = "Succesfully submitted"
        }
        else
        {
            submittedText.textContent = "Already written"
        }
        
    } else {
        console.log(response);
    }

    setTimeout(resetSubmittedText, 600, submittedText)
}


function resetSubmittedText(text) {
    text.textContent = " "
}