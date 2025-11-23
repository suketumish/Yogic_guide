// Session management
// Note: sessionId, currentModule, and posesCompleted are declared in pose-detection.js
// to avoid duplicate declarations
let startTime = null;
let currentPose = null;
let sessionPaused = false;

async function startSession(moduleType) {
    const response = await fetch('/session/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ module_type: moduleType })
    });
    const data = await response.json();
    window.sessionId = data.session_id;
    startTime = Date.now();
    window.currentModule = moduleType;
    sessionPaused = false;
    
    // Voice-over: Session start
    if (typeof voiceOver !== 'undefined') {
        const moduleName = formatModuleName(moduleType);
        voiceOver.onSessionStart(moduleName);
    }
}

function formatModuleName(moduleType) {
    const names = {
        'surya_namaskar': 'Surya Namaskar',
        'breathing': 'Breathing Exercises',
        'stretching': 'Stretching Routine',
        'meditation': 'Meditation Session'
    };
    return names[moduleType] || moduleType;
}

async function completeSession(accuracyScore = 85) {
    const duration = Math.floor((Date.now() - startTime) / 1000);
    const calories = Math.floor(duration / 60 * 3);
    
    const sessionData = {
        session_id: window.sessionId,
        duration: duration,
        poses_completed: window.posesCompleted || 0,
        accuracy_score: accuracyScore,
        calories_burned: calories
    };
    
    // Voice-over: Session complete
    if (typeof voiceOver !== 'undefined') {
        const results = {
            duration: duration,
            accuracy: accuracyScore,
            posesCompleted: posesCompleted
        };
        voiceOver.onSessionComplete(results);
    }
    
    // Save to localStorage for session-complete page
    localStorage.setItem('sessionStats', JSON.stringify(sessionData));
    
    await fetch('/session/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sessionData)
    });
    
    // Delay redirect to allow voice-over to complete
    setTimeout(() => {
        window.location.href = '/session-complete';
    }, 2000);
}

function pauseSession(reason = null) {
    sessionPaused = true;
    
    // Voice-over: Session paused
    if (typeof voiceOver !== 'undefined') {
        voiceOver.onSessionPause(reason);
    }
}

function resumeSession() {
    sessionPaused = false;
    
    // Voice-over: Session resumed
    if (typeof voiceOver !== 'undefined') {
        voiceOver.onSessionResume();
    }
}

function changePose(pose) {
    currentPose = pose;
    posesCompleted++;
    
    // Voice-over: Pose change
    if (typeof voiceOver !== 'undefined') {
        voiceOver.onPoseChange(pose);
    }
}

function validatePoseSuccess(poseName) {
    // Voice-over: Pose validated successfully
    if (typeof voiceOver !== 'undefined') {
        voiceOver.onPoseSuccess(poseName);
    }
}

function validatePoseCorrection(feedback, detailed = false) {
    // Voice-over: Pose correction needed
    if (typeof voiceOver !== 'undefined') {
        voiceOver.onPoseCorrection(feedback, { detailed });
    }
}

function provideTimedGuidance(guidance) {
    // Voice-over: Timed guidance after incorrect pose
    if (typeof voiceOver !== 'undefined') {
        voiceOver.onTimedGuidance(guidance);
    }
}

function poseTransitionCountdown(seconds) {
    // Voice-over: Countdown before pose transition
    if (typeof voiceOver !== 'undefined') {
        voiceOver.onPoseTransitionCountdown(seconds);
    }
}

function breathingCue(phase) {
    // Voice-over: Breathing cue
    if (typeof voiceOver !== 'undefined') {
        voiceOver.onBreathingCue(phase);
    }
}

function encouragement() {
    // Voice-over: Random encouragement
    if (typeof voiceOver !== 'undefined') {
        voiceOver.onEncouragement();
    }
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
