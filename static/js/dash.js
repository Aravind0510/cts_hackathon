// Gender Distribution Chart (Donut)
const genderData = JSON.parse(document.getElementById('genderData').textContent);
const genderLabels = genderData.map(item => item['GENDER']);
const genderCounts = genderData.map(item => item['COUNT']);

const genderCtx = document.getElementById('genderChart').getContext('2d');
const genderChart = new Chart(genderCtx, {
    type: 'doughnut',
    data: {
        labels: genderLabels,
        datasets: [{
            label: 'Gender Distribution',
            data: genderCounts,
            backgroundColor: ['#ff6f61', '#ff9999', '#66b3ff'],
            borderColor: 'black',
            borderWidth: 2
        }]
    },
    options: {
        cutoutPercentage: 70, // Adjust the cutout size
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    color: '#333',
                    font: {
                        size: 12
                    }
                }
            }
        },
        elements: {
            arc: {
                borderWidth: 2,
                shadowBlur: 10,
                shadowOffsetX: 5,
                shadowOffsetY: 5,
                shadowColor: 'rgba(0, 0, 0, 0.3)'
            }
        }
    }
});

// Age Group Distribution Chart (Donut)
const ageData = JSON.parse(document.getElementById('ageData').textContent);
const ageLabels = ageData.map(item => item['AGE_GROUP']);
const ageCounts = ageData.map(item => item['COUNT']);

const ageCtx = document.getElementById('ageChart').getContext('2d');
const ageChart = new Chart(ageCtx, {
    type: 'doughnut',
    data: {
        labels: ageLabels,
        datasets: [{
            label: 'Age Group Distribution',
            data: ageCounts,
            backgroundColor: ['#e94e77', '#ffcc99', '#99ccff', '#ffcc66', '#ff9999'],
            borderColor: '#fff',
            borderWidth: 2
        }]
    },
    options: {
        cutoutPercentage: 70,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    color: '#333',
                    font: {
                        size: 14
                    }
                }
            }
        },
        elements: {
            arc: {
                borderWidth: 2,
                shadowBlur: 10,
                shadowOffsetX: 5,
                shadowOffsetY: 5,
                shadowColor: 'rgba(0, 0, 0, 0.3)'
            }
        }
    }
});

// Admission Outcome (Bar Chart)
const admissionData = JSON.parse(document.getElementById('admissionOutcomeData').textContent);
const admissionLabels = admissionData.map(item => item['ADMISSION_TYPE']);
const admissionCounts = admissionData.map(item => item['COUNT']);

const admissionCtx = document.getElementById('admissionOutcomeChart').getContext('2d');
// Create a gradient for the bars
const gradient = admissionCtx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, '#ff6f61');  // Start color (top)
gradient.addColorStop(1, '#4a90e2');  // End color (bottom)
const admissionChart = new Chart(admissionCtx, {
    type: 'bar',
    data: {
        labels: admissionLabels,
        datasets: [{
            label: 'Admission Types',
            data: admissionCounts,
            backgroundColor: gradient,
            borderColor: 'black',
            borderWidth: 3
        }]
    },
    options: {
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#333',
                    font: {
                        size: 16
                    }
                }
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                ticks: {
                    color: '#333'
                }
            },
            y: {
                beginAtZero: true,
                ticks: {
                    color: '#333'
                }
            }
        }
    }
});

// Common Medications (Line Chart)
const medicationData = JSON.parse(document.getElementById('medicationsData').textContent);
const medicationLabels = medicationData.map(item => item['MEDICATION_NAME']);
const medicationCounts = medicationData.map(item => item['COUNT']);

const medicationCtx = document.getElementById('medicationsChart').getContext('2d');
const medicationChart = new Chart(medicationCtx, {
    type: 'line',
    data: {
        labels: medicationLabels,
        datasets: [{
            label: 'Common Medications',
            data: medicationCounts,
            borderColor: '#28a745',
            backgroundColor: 'rgba(40, 167, 69, 0.2)',
            borderWidth: 5,
            shadowBlur: 10,
            shadowOffsetX: 5,
            shadowOffsetY: 5,
            shadowColor: 'rgba(0, 0, 0, 0.3)'
        }]
    },
    options: {
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#333',
                    font: {
                        size: 16
                    }
                }
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                ticks: {
                    color: '#333'
                }
            },
            y: {
                beginAtZero: true,
                ticks: {
                    color: '#333'
                }
            }
        }
    }
});

// Surgeries Performed (Scatter Chart)
const surgeryData = JSON.parse(document.getElementById('surgerydata').textContent);
const surgeryLabels = surgeryData.map(item => item['SURGERY_TYPE']);
const surgeryCounts = surgeryData.map(item => item['COUNT']);

const surgeryCtx = document.getElementById('surgeriesChart').getContext('2d');
const surgeryChart = new Chart(surgeryCtx, {
    type: 'scatter',
    data: {
        labels: surgeryLabels,
        datasets: [{
            label: 'Surgeries Performed',
            data: surgeryCounts.map((count, index) => ({ x: index, y: count })),
            backgroundColor: '#ff6f61',
            borderColor: '#ff6f61',
            borderWidth: 3,
            showLine: true,
            shadowBlur: 10,
            shadowOffsetX: 5,
            shadowOffsetY: 5,
            shadowColor: 'rgba(0, 0, 0, 0.3)'
        }]
    },
    options: {
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#333',
                    font: {
                        size: 16
                    }
                }
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                ticks: {
                    callback: function(value, index, values) {
                        return surgeryLabels[index] || '';
                    },
                    color: '#333'
                }
            },
            y: {
                beginAtZero: true,
                ticks: {
                    color: '#333'
                }
            }
        }
    }
});


