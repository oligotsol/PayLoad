/**
 * PayLoad - Autonomous Drone Payments Demo
 * Frontend JavaScript
 */

// API Configuration
const API_BASE = 'http://localhost:5000/api';

// State
let state = {
    running: false,
    position: 0,
    payments: [],
    totalPaid: 0,
    totalReceived: 0,
    startTime: null,
    flightInterval: null,
    timerInterval: null
};

// Waypoint definitions (must match backend)
const WAYPOINTS = [
    { position: 10, type: 'debit', name: 'Airspace Zone A', amount: 0.003 },
    { position: 25, type: 'debit', name: 'Weather Data', amount: 0.001 },
    { position: 45, type: 'debit', name: 'Airspace Zone B', amount: 0.004 },
    { position: 60, type: 'debit', name: 'Traffic Routing', amount: 0.002 },
    { position: 80, type: 'debit', name: 'Landing Pad', amount: 0.05 },
    { position: 90, type: 'debit', name: 'Charging', amount: 0.12 },
    { position: 100, type: 'credit', name: 'Delivery Complete', amount: 5.00 }
];

// DOM Elements
const elements = {
    drone: document.getElementById('drone'),
    progress: document.getElementById('progress'),
    progressPercent: document.getElementById('progress-percent'),
    paymentLog: document.getElementById('payment-log'),
    totalPaid: document.getElementById('total-paid'),
    totalReceived: document.getElementById('total-received'),
    netTotal: document.getElementById('net-total'),
    txCount: document.getElementById('tx-count'),
    flightTime: document.getElementById('flight-time'),
    startBtn: document.getElementById('start-btn'),
    resetBtn: document.getElementById('reset-btn'),
    popup: document.getElementById('payment-popup'),
    popupIcon: document.getElementById('popup-icon'),
    popupAmount: document.getElementById('popup-amount'),
    popupName: document.getElementById('popup-name'),
    popupTx: document.getElementById('popup-tx'),
    waypointsContainer: document.getElementById('waypoints')
};

// Initialize waypoint markers
function initWaypoints() {
    elements.waypointsContainer.innerHTML = '';
    
    WAYPOINTS.forEach(wp => {
        const marker = document.createElement('div');
        marker.className = `waypoint ${wp.type}`;
        marker.style.left = `${wp.position}%`;
        marker.dataset.position = wp.position;
        
        const label = document.createElement('div');
        label.className = 'waypoint-label';
        label.textContent = wp.name;
        marker.appendChild(label);
        
        elements.waypointsContainer.appendChild(marker);
    });
}

// Update drone position
function updateDronePosition(position) {
    const leftPercent = 10 + (position * 0.8); // Map 0-100 to 10-90%
    elements.drone.style.left = `${leftPercent}%`;
    elements.progress.style.width = `${position}%`;
    elements.progressPercent.textContent = `${Math.round(position)}%`;
    
    // Update route line progress
    document.querySelector('.route-line').style.setProperty('--progress', `${position}%`);
    
    // Update waypoint markers
    document.querySelectorAll('.waypoint').forEach(wp => {
        const wpPos = parseInt(wp.dataset.position);
        if (position >= wpPos) {
            wp.classList.add('passed');
        }
    });
}

// Show payment popup
function showPaymentPopup(payment) {
    const isDebit = payment.type === 'debit';
    
    elements.popupIcon.textContent = isDebit ? '💸' : '💰';
    elements.popupAmount.textContent = isDebit ? `-$${payment.amount.toFixed(3)}` : `+$${payment.amount.toFixed(2)}`;
    elements.popupAmount.className = `popup-amount ${payment.type}`;
    elements.popupName.textContent = payment.name;
    
    if (payment.tx && payment.tx.signature) {
        const explorerUrl = payment.tx.explorer_url || `https://explorer.solana.com/tx/${payment.tx.signature}?cluster=devnet`;
        elements.popupTx.innerHTML = `<a href="${explorerUrl}" target="_blank">View on Solana →</a>`;
    }
    
    elements.popup.classList.add('show');
    
    setTimeout(() => {
        elements.popup.classList.remove('show');
    }, 1500);
}

// Add payment to log
function addPaymentToLog(payment) {
    // Remove empty state if present
    const emptyState = elements.paymentLog.querySelector('.empty-state');
    if (emptyState) emptyState.remove();
    
    const item = document.createElement('div');
    item.className = `payment-item ${payment.type}`;
    
    const isDebit = payment.type === 'debit';
    const amountStr = isDebit ? `-$${payment.amount.toFixed(3)}` : `+$${payment.amount.toFixed(2)}`;
    
    item.innerHTML = `
        <div class="icon">${isDebit ? '↑' : '↓'}</div>
        <div class="details">
            <div class="name">${payment.name}</div>
            <div class="description">${payment.description || ''}</div>
        </div>
        <div class="amount">${amountStr}</div>
    `;
    
    if (payment.tx && payment.tx.signature) {
        const link = document.createElement('a');
        link.className = 'tx-link';
        link.href = payment.tx.explorer_url || '#';
        link.target = '_blank';
        link.textContent = payment.tx.signature.substring(0, 8) + '...';
        item.querySelector('.details').appendChild(link);
    }
    
    elements.paymentLog.insertBefore(item, elements.paymentLog.firstChild);
}

// Update totals
function updateTotals() {
    elements.totalPaid.textContent = `-$${state.totalPaid.toFixed(3)}`;
    elements.totalReceived.textContent = `+$${state.totalReceived.toFixed(2)}`;
    const net = state.totalReceived - state.totalPaid;
    elements.netTotal.textContent = `$${net.toFixed(2)}`;
    elements.txCount.textContent = state.payments.length;
}

// Update flight timer
function updateTimer() {
    if (!state.startTime) return;
    
    const elapsed = Math.floor((Date.now() - state.startTime) / 1000);
    const mins = Math.floor(elapsed / 60);
    const secs = elapsed % 60;
    elements.flightTime.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Advance the drone
function advanceDrone() {
    if (!state.running || state.position >= 100) {
        stopFlight();
        return;
    }
    
    // Smooth movement - small increments
    const newPosition = Math.min(100, state.position + 1);
    
    // Run in simulation mode (no backend needed)
    simulateAdvance(newPosition);
}

// Local simulation fallback
function simulateAdvance(newPosition) {
    // Check for waypoints
    WAYPOINTS.forEach(wp => {
        if (state.position < wp.position && newPosition >= wp.position) {
            const payment = {
                type: wp.type,
                name: wp.name,
                amount: wp.amount,
                description: `Simulated ${wp.name}`,
                tx: {
                    success: true,
                    signature: 'sim_' + Math.random().toString(36).substring(7),
                    simulated: true
                }
            };
            
            if (wp.type === 'debit') {
                state.totalPaid += wp.amount;
            } else {
                state.totalReceived += wp.amount;
            }
            
            state.payments.push(payment);
            addPaymentToLog(payment);
            showPaymentPopup(payment);
        }
    });
    
    state.position = newPosition;
    updateDronePosition(state.position);
    updateTotals();
    
    if (state.position >= 100) {
        stopFlight();
        elements.startBtn.innerHTML = '<span class="btn-icon">✓</span> Complete';
    }
}

// Start flight
async function startFlight() {
    if (state.running) return;
    
    state.running = true;
    state.startTime = Date.now();
    
    elements.startBtn.disabled = true;
    elements.startBtn.innerHTML = '<span class="btn-icon">◉</span> Flying...';
    elements.resetBtn.disabled = false;
    
    // Try to start via API
    try {
        await fetch(`${API_BASE}/demo/start`, { method: 'POST' });
    } catch (e) {
        console.log('Running in local simulation mode');
    }
    
    // Start the flight loop - smooth movement with small increments
    // 100 positions over ~15 seconds = ~150ms per tick
    state.flightInterval = setInterval(advanceDrone, 150);
    state.timerInterval = setInterval(updateTimer, 1000);
}

// Stop flight
function stopFlight() {
    state.running = false;
    
    if (state.flightInterval) {
        clearInterval(state.flightInterval);
        state.flightInterval = null;
    }
    
    if (state.timerInterval) {
        clearInterval(state.timerInterval);
        state.timerInterval = null;
    }
}

// Reset demo
function resetDemo() {
    stopFlight();
    
    state = {
        running: false,
        position: 0,
        payments: [],
        totalPaid: 0,
        totalReceived: 0,
        startTime: null,
        flightInterval: null,
        timerInterval: null
    };
    
    // Reset UI
    updateDronePosition(0);
    updateTotals();
    
    elements.paymentLog.innerHTML = '<div class="empty-state"><span>Waiting for flight to begin...</span></div>';
    elements.flightTime.textContent = '0:00';
    elements.txCount.textContent = '0';
    
    elements.startBtn.disabled = false;
    elements.startBtn.innerHTML = '<span class="btn-icon">▶</span> Start Flight';
    elements.resetBtn.disabled = true;
    
    // Reset waypoint markers
    document.querySelectorAll('.waypoint').forEach(wp => {
        wp.classList.remove('passed');
    });
    
    // Try to reset via API
    fetch(`${API_BASE}/demo/stop`, { method: 'POST' }).catch(() => {});
}

// Event listeners
elements.startBtn.addEventListener('click', startFlight);
elements.resetBtn.addEventListener('click', resetDemo);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initWaypoints();
    
    // Check API health
    fetch(`${API_BASE}/health`)
        .then(r => r.json())
        .then(data => {
            console.log('API connected:', data);
            document.getElementById('network').textContent = 'Solana Devnet • API Connected';
        })
        .catch(() => {
            console.log('API not available, running in simulation mode');
            document.getElementById('network').textContent = 'Simulation Mode';
        });
});

// Keyboard controls
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        e.preventDefault();
        if (!state.running && state.position < 100) {
            startFlight();
        }
    }
    if (e.code === 'KeyR') {
        resetDemo();
    }
});
