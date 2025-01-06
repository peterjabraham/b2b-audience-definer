document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('inputForm');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const input = document.getElementById('userInput').value;

        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: input }),
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = `<p>${data.result}</p>`;
        })
        .catch((error) => {
            console.error('Error:', error);
            resultDiv.innerHTML = '<p>An error occurred. Please try again.</p>';
        });
    });
});
