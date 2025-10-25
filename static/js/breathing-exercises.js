// Breathing Exercises Module
let breathingExercise = null;
let breathingTimer = 0;
let cycleCount = 0;
let isBreathing = false;

const breathingExercises = {
    'anulom-vilom': {
        name: 'Anulom Vilom (Alternate Nostril Breathing)',
        duration: 120,
        instruction: 'Close right nostril, inhale through left. Close left, exhale through right. Repeat.',
        benefits: ['Balances nervous system', 'Reduces stress', 'Improves lung capacity']
    },
    'bhramari': {
        name: 'Bhramari (Bee Breathing)',
        duration: 60,
        instruction: 'Inhale deeply, exhale while making a humming sound like a bee.',
        benefits: ['Calms mind', 'Reduces anger', 'Lowers blood pressure']
    },
    'kapalbhati': {
        name: 'Kapalbhati (Skull Shining Breath)',
        duration: 90,
        instruction: 'Forceful exhalations through nose, passive inhalations.',
        benefits: ['Energizes body', 'Cleanses respiratory system', 'Improves digestion']
    },
    'meditation': {
        name: 'Silent Meditation',
        duration: 300,
        instruction: 'Sit quietly, focus on your natural breath.',
        benefits: ['Deep relaxation', 'Mental clarity', 'Stress relief']
    }
};

function startBreathingExercise(exerciseType) {
    breathingExercise = breathingExercises[exerciseType];
    breathingTimer = breathingExercise.duration;
    cycleCount = 0;
    isBreathing = true;
    
    speak(breathingExercise.name);
    setTimeout(() => speak(breathingExercise.instruction), 2000);
    
    updateBreathingUI();
    startBreathingTimer();
}

function startBreathingTimer() {
    const interval = setInterval(() => {
        if (!isBreathing || isPaused) return;
        
        breathingTimer--;
        updateBreathingUI();
        
        if (breathingTimer <= 0) {
            clearInterval(interval);
            speak('Exercise complete. Well done!');
            setTimeout(() => completeSession(), 2000);
        }
    }, 1000);
}

function updateBreathingUI() {
    const minutes = Math.floor(breathingTimer / 60);
    const seconds = breathingTimer % 60;
    document.getElementById('timer').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    document.getElementById('cycleCount').textContent = cycleCount;
}

// Breathing animation
function animateBreathing() {
    const breathCircle = document.getElementById('breathCircle');
    if (!breathCircle) return;
    
    setInterval(() => {
        if (!isBreathing || isPaused) return;
        
        // Inhale (expand)
        breathCircle.style.transform = 'scale(1.5)';
        breathCircle.style.transition = 'transform 4s ease-in-out';
        
        setTimeout(() => {
            // Exhale (contract)
            breathCircle.style.transform = 'scale(1)';
            cycleCount++;
            updateBreathingUI();
        }, 4000);
    }, 8000);
}
