// Add a click event listener to the button
document.getElementById("my-button").addEventListener("click", function() {

    // Get the input text from the textarea
    var summary = document.getElementById("summary").value;

    // Send a POST request to the Flask endpoint with the input text
    fetch('/summarize', {
        method: 'POST',
        body: JSON.stringify({text: summary}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Display the summary result in the HTML
        var result = document.createElement("p");
        result.innerHTML = data.summary;
        document.body.appendChild(result);
    })
    .catch(error => console.error(error));

});