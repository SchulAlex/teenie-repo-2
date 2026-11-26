document.addEventListener('DOMContentLoaded', function () {
    // Tooltips
    document.querySelectorAll('[data-tooltip]').forEach(function (element) {
        let tooltip = null;

        element.addEventListener('mouseenter', function () {
            tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.innerText = element.getAttribute('data-tooltip');
            document.body.appendChild(tooltip);
            const rect = element.getBoundingClientRect();
            tooltip.style.left = `${rect.left + window.scrollX}px`;
            tooltip.style.top = `${rect.bottom + window.scrollY}px`;
        });

        element.addEventListener('mouseleave', function () {
            if (tooltip) {
                tooltip.remove();
                tooltip = null;
            }
        });
    });

    // Quiz: evaluated client-side (polls are submitted normally to the server)
    const quizForm = document.getElementById('quiz-form');
    const quizResult = document.getElementById('quiz-result');
    if (quizForm && quizResult) {
        const messages = {
            a: ['\u{1F917}', 'You seek connection: talking to others helps you most. Keep reaching out!'],
            b: ['\u{1F33F}', 'You recharge on your own. Just make sure you can ask for help when you need it.'],
            c: ['\u{1F3A7}', 'You tend to distract yourself. A short break is fine, but talking about it can help too.']
        };
        quizForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const counts = { a: 0, b: 0, c: 0 };
            new FormData(quizForm).forEach(function (value) {
                if (value in counts) counts[value] += 1;
            });
            const best = Object.keys(counts).reduce(function (x, y) {
                return counts[y] > counts[x] ? y : x;
            });
            quizResult.textContent = '';
            const emoji = document.createElement('span');
            emoji.className = 'big-emoji';
            emoji.textContent = messages[best][0];
            quizResult.appendChild(emoji);
            quizResult.appendChild(document.createTextNode(messages[best][1]));
            quizResult.hidden = false;
            quizResult.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }
});
