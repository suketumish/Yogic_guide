// Session management
let sessionId = null;
let startTime = null;
let posesCompleted = 0;

async function startSession(moduleType) {
    const response = await fetch('/session/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ module_type: moduleType })
    });
    const data = await response.json();
    sessionId = data.session_id;
    startTime = Date.now();
}

async function completeSession() {
    const duration = Math.floor((Date.now() - startTime) / 1000);
    const calories = Math.floor(duration / 60 * 3);
    
    const sessionData = {
        session_id: sessionId,
        duration: duration,
        poses_completed: posesCompleted,
        accuracy_score: 85,
        calories_burned: calories
    };
    
    // Save to localStorage for session-complete page
    localStorage.setItem('sessionStats', JSON.stringify(sessionData));
    
    await fetch('/session/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sessionData)
    });
    
    window.location.href = '/session-complete';
}

// Text-to-speech with queue management
let speechQueue = [];
let isSpeaking = false;

function speak(text) {
    if ('speechSynthesis' in window) {
        speechQueue.push(text);
        if (!isSpeaking) {
            speakNext();
        }
    }
}

function speakNext() {
    if (speechQueue.length === 0) {
        isSpeaking = false;
        return;
    }
    
    isSpeaking = true;
    const text = speechQueue.shift();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 0.8;
    
    utterance.onend = () => {
        setTimeout(speakNext, 500);
    };
    
    window.speechSynthesis.speak(utterance);
}

// Stop all speech
function stopSpeaking() {
    window.speechSynthesis.cancel();
    speechQueue = [];
    isSpeaking = false;
}
