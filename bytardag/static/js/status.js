"use strict";

let ctx, chart;

document.addEventListener("DOMContentLoaded", function () {
    console.log('DOM Ready...');

    ctx = document.getElementById('chart').getContext('2d');

    setupChart();
    setInterval(updateChart, 120000);
    updateChart();
});

function setupChart() {
    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Registrerade', 'Verifierade'],
            datasets: [{
                label: 'Antal ark',
                data: [0, 0],
                backgroundColor: [
                    'rgba(62, 209, 175, 0.8)',
                    'rgba(224, 174, 18, 0.8)'
                ],
                borderColor: [
                    'rgba(62, 209, 175, 1)',
                    'rgba(224, 174, 18, 1)'
                ],
                borderWidth: 3
            }]
        },
        options: {
            aspectRatio: 3/2,
            maintainAspectRatio: true,
            title: {
                display: false,
                text: "Antal ark"
            },
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function updateChart() {
    fetch(document.URL, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        chart.data.datasets[0].data = data.values;
        chart.update();
    })
    .catch((error) => {
      console.error('Error:', error);
      // Update UI with error message
    });
}