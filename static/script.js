let currentExpression = '';
let lastResult = '';

const expressionEl = document.getElementById('expression');
const resultEl = document.getElementById('result');

function updateDisplay() {
    expressionEl.textContent = currentExpression || '';
    resultEl.textContent = lastResult || '0';
}

function appendToExpression(value) {
    currentExpression += value;
    updateDisplay();
}

function appendFunction(func) {
    currentExpression += func + '(';
    updateDisplay();
}

function clear() {
    currentExpression = '';
    lastResult = '';
    updateDisplay();
}

function deleteLast() {
    currentExpression = currentExpression.slice(0, -1);
    updateDisplay();
}

async function calculate() {
    if (!currentExpression) return;

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression: currentExpression })
        });

        const data = await response.json();

        if (data.error) {
            resultEl.textContent = 'Error: ' + data.error;
            resultEl.style.color = '#ff6b6b';
        } else {
            lastResult = data.result;
            currentExpression = data.result.toString();
            resultEl.style.color = '#e94560';
        }
        updateDisplay();
    } catch (err) {
        resultEl.textContent = 'Error: Network issue';
        resultEl.style.color = '#ff6b6b';
    }
}

document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const action = btn.dataset.action;
        const value = btn.dataset.value;

        if (action === 'clear') {
            clear();
        } else if (action === 'delete') {
            deleteLast();
        } else if (action === 'calculate') {
            calculate();
        } else if (action === 'sin' || action === 'cos' || action === 'tan' ||
                   action === 'asin' || action === 'acos' || action === 'atan' ||
                   action === 'sqrt' || action === 'log' || action === 'ln' ||
                   action === 'factorial' || action === 'abs' ||
                   action === 'floor' || action === 'ceil') {
            appendFunction(action);
        } else if (action === 'pow') {
            appendToExpression('**');
        } else if (action === 'pi') {
            appendToExpression('pi');
        } else if (action === 'e') {
            appendToExpression('e');
        } else if (value) {
            appendToExpression(value);
        }
    });
});

document.addEventListener('keydown', (e) => {
    if (e.key >= '0' && e.key <= '9' || e.key === '.') {
        appendToExpression(e.key);
    } else if (['+', '-', '*', '/', '(', ')', '**'].includes(e.key)) {
        appendToExpression(e.key);
    } else if (e.key === 'Enter' || e.key === '=') {
        e.preventDefault();
        calculate();
    } else if (e.key === 'Backspace') {
        deleteLast();
    } else if (e.key === 'Escape') {
        clear();
    }
});
