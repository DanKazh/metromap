document.getElementById('calculateButton').addEventListener('click', function() {
    const fromStation = document.getElementById('fromStation').value;
    const toStation = document.getElementById('toStation').value;

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ from: fromStation, to: toStation })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = `${data.time}`;
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});
