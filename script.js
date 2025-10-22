// Global variables
let processes = [];
let quantumCallback = null;

// Colors for different processes
const colors = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
    '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B88B', '#AAB7B8'
];

// Add process to the list
function addProcess() {
    const processId = document.getElementById('processId').value.trim();
    const burstTime = parseInt(document.getElementById('burstTime').value);
    
    if (!processId) {
        alert('Process ID cannot be empty!');
        return;
    }
    
    if (isNaN(burstTime) || burstTime <= 0) {
        alert('Invalid burst time!');
        return;
    }
    
    const process = {
        pid: processId,
        arrival: processes.length,
        burst: burstTime,
        remaining: burstTime
    };
    
    processes.push(process);
    updateProcessList();
    
    // Clear inputs
    document.getElementById('processId').value = '';
    document.getElementById('burstTime').value = '';
    document.getElementById('processId').focus();
}

// Update the process list display
function updateProcessList() {
    const listElement = document.getElementById('processList');
    listElement.innerHTML = '';
    
    processes.forEach(p => {
        const item = document.createElement('div');
        item.className = 'process-item';
        item.textContent = `PID: ${p.pid.padEnd(10)} | Burst: ${p.burst}`;
        listElement.appendChild(item);
    });
}

// Clear all processes
function clearAll() {
    processes = [];
    updateProcessList();
    clearCanvas();
    clearResults();
}

// Clear canvas
function clearCanvas() {
    const canvas = document.getElementById('ganttChart');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// Clear results
function clearResults() {
    document.getElementById('resultsBody').innerHTML = '';
    document.getElementById('averageTimes').textContent = 'Run simulation to see average times';
}

// Run simulation based on selected algorithm
function runSimulation() {
    if (processes.length === 0) {
        alert('Please add at least one process!');
        return;
    }
    
    const algorithm = document.getElementById('algorithm').value;
    
    if (algorithm === 'FCFS') {
        fcfs();
    } else if (algorithm === 'SJF') {
        sjf();
    } else if (algorithm === 'RR') {
        showQuantumModal();
    }
}

// Show time quantum modal
function showQuantumModal() {
    document.getElementById('quantumModal').style.display = 'block';
    document.getElementById('timeQuantum').focus();
}

// Close time quantum modal
function closeQuantumModal() {
    document.getElementById('quantumModal').style.display = 'none';
}

// Confirm time quantum and run Round Robin
function confirmQuantum() {
    const quantum = parseInt(document.getElementById('timeQuantum').value);
    
    if (isNaN(quantum) || quantum <= 0) {
        alert('Please enter a valid positive integer!');
        return;
    }
    
    closeQuantumModal();
    roundRobin(quantum);
}

// Allow Enter key to confirm in modal
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('timeQuantum').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            confirmQuantum();
        }
    });
    
    // Allow Enter key to add process
    document.getElementById('processId').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('burstTime').focus();
        }
    });
    
    document.getElementById('burstTime').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addProcess();
        }
    });
});

// FCFS Algorithm
function fcfs() {
    const processesCopy = [...processes].sort((a, b) => a.arrival - b.arrival);
    
    let currentTime = 0;
    const ganttChart = [];
    const results = [];
    
    processesCopy.forEach(p => {
        const startTime = currentTime;
        const completionTime = currentTime + p.burst;
        const turnaroundTime = completionTime;
        const waitingTime = turnaroundTime - p.burst;
        
        ganttChart.push({
            pid: p.pid,
            start: startTime,
            end: completionTime
        });
        
        results.push({
            pid: p.pid,
            burst: p.burst,
            completion: completionTime,
            turnaround: turnaroundTime,
            waiting: waitingTime
        });
        
        currentTime = completionTime;
    });
    
    drawGanttChart(ganttChart, 'FCFS');
    displayResults(results, true);
}

// SJF Algorithm
function sjf() {
    const processesCopy = [...processes].sort((a, b) => {
        if (a.burst === b.burst) {
            return a.pid.localeCompare(b.pid);
        }
        return a.burst - b.burst;
    });
    
    let currentTime = 0;
    const ganttChart = [];
    const results = [];
    
    processesCopy.forEach(p => {
        const startTime = currentTime;
        const completionTime = currentTime + p.burst;
        const turnaroundTime = completionTime;
        const waitingTime = turnaroundTime - p.burst;
        
        ganttChart.push({
            pid: p.pid,
            start: startTime,
            end: completionTime
        });
        
        results.push({
            pid: p.pid,
            burst: p.burst,
            completion: completionTime,
            turnaround: turnaroundTime,
            waiting: waitingTime
        });
        
        currentTime = completionTime;
    });
    
    drawGanttChart(ganttChart, 'SJF');
    displayResults(results, false); // Don't sort by PID for SJF
}

// Round Robin Algorithm
function roundRobin(quantum) {
    const processesCopy = processes.map(p => ({...p, remaining: p.burst}));
    
    let currentTime = 0;
    const ganttChart = [];
    const queue = [...processesCopy];
    const completed = [];
    
    while (queue.length > 0) {
        const currentProcess = queue.shift();
        
        const executionTime = Math.min(quantum, currentProcess.remaining);
        const startTime = currentTime;
        currentTime += executionTime;
        currentProcess.remaining -= executionTime;
        
        ganttChart.push({
            pid: currentProcess.pid,
            start: startTime,
            end: currentTime
        });
        
        if (currentProcess.remaining === 0) {
            const completionTime = currentTime;
            const turnaroundTime = completionTime;
            const waitingTime = turnaroundTime - currentProcess.burst;
            
            completed.push({
                pid: currentProcess.pid,
                burst: currentProcess.burst,
                completion: completionTime,
                turnaround: turnaroundTime,
                waiting: waitingTime
            });
        } else {
            queue.push(currentProcess);
        }
    }
    
    drawGanttChart(ganttChart, 'Round Robin');
    displayResults(completed, true);
}

// Draw Gantt Chart
function drawGanttChart(ganttChart, algorithmName) {
    const canvas = document.getElementById('ganttChart');
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (ganttChart.length === 0) return;
    
    const margin = 50;
    const chartHeight = 60;
    const yStart = (canvas.height - chartHeight) / 2;
    
    const totalTime = Math.max(...ganttChart.map(item => item.end));
    const availableWidth = canvas.width - 2 * margin;
    const timeScale = availableWidth / totalTime;
    
    const pidColors = {};
    
    // Draw title
    ctx.font = 'bold 16px Arial';
    ctx.fillStyle = '#333';
    ctx.textAlign = 'center';
    ctx.fillText(`Gantt Chart - ${algorithmName}`, canvas.width / 2, 25);
    
    // Draw Gantt chart bars
    ganttChart.forEach((item, i) => {
        if (!pidColors[item.pid]) {
            pidColors[item.pid] = colors[Object.keys(pidColors).length % colors.length];
        }
        
        const x1 = margin + item.start * timeScale;
        const x2 = margin + item.end * timeScale;
        
        // Draw rectangle
        ctx.fillStyle = pidColors[item.pid];
        ctx.fillRect(x1, yStart, x2 - x1, chartHeight);
        
        // Draw border
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 2;
        ctx.strokeRect(x1, yStart, x2 - x1, chartHeight);
        
        // Draw process ID
        ctx.fillStyle = 'white';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(item.pid, (x1 + x2) / 2, yStart + chartHeight / 2 + 5);
        
        // Draw time markers
        ctx.fillStyle = 'black';
        ctx.font = '12px Arial';
        
        // Start time
        if (i === 0 || ganttChart[i - 1].end !== item.start) {
            ctx.fillText(item.start, x1, yStart + chartHeight + 20);
        }
        
        // End time
        if (i === ganttChart.length - 1 || ganttChart[i + 1].start !== item.end) {
            ctx.fillText(item.end, x2, yStart + chartHeight + 20);
        }
    });
}

// Display Results
function displayResults(results, sortByPid) {
    const tbody = document.getElementById('resultsBody');
    tbody.innerHTML = '';
    
    // Sort results if needed
    if (sortByPid) {
        results.sort((a, b) => a.pid.localeCompare(b.pid));
    }
    
    let totalTurnaround = 0;
    let totalWaiting = 0;
    
    results.forEach(r => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${r.pid}</td>
            <td>${r.burst}</td>
            <td>${r.waiting}</td>
            <td>${r.turnaround}</td>
        `;
        tbody.appendChild(row);
        
        totalTurnaround += r.turnaround;
        totalWaiting += r.waiting;
    });
    
    const avgTurnaround = (totalTurnaround / results.length).toFixed(2);
    const avgWaiting = (totalWaiting / results.length).toFixed(2);
    
    document.getElementById('averageTimes').textContent = 
        `Average Waiting Time: ${avgWaiting}  |  Average Turnaround Time: ${avgTurnaround}`;
}
