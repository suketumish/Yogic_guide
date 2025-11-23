/**
 * Voice-Over Functionality for Zen_Align
 * Provides audio instructions, pose guidance, and results
 */

class VoiceOverManager {
    constructor() {
        this.synth = window.speechSynthesis;
        this.voice = null;
        this.enabled = true;
        this.rate = 1.0;
        this.pitch = 1.0;
        this.volume = 1.0;
        this.queue = [];
        this.isSpeaking = false;
        
        this.init();
    }
    
    init() {
        // Load user preferences
        const prefs = localStorage.getItem('voiceOverPrefs');
        if (prefs) {
            const settings = JSON.parse(prefs);
            this.enabled = settings.enabled !== false;
            this.rate = settings.rate || 1.0;
            this.pitch = settings.pitch || 1.0;
            this.volume = settings.volume || 1.0;
        }
        
        // Load voices
        if (this.synth.onvoiceschanged !== undefined) {
            this.synth.onvoiceschanged = () => this.loadVoices();
        }
        this.loadVoices();
    }
    
    loadVoices() {
        const voices = this.synth.getVoices();
        // Prefer English voices
        this.voice = voices.find(v => v.lang.startsWith('en')) || voices[0];
    }
    
    speak(text, options = {}) {
        if (!this.enabled || !text) return;
        
        // Add to queue if priority is not set or if already speaking
        if (options.priority === 'high') {
            // High priority: cancel current and speak immediately
            this.synth.cancel();
            this.queue = [];
            this._speakNow(text, options);
        } else if (options.queue !== false) {
            // Queue the message
            this.queue.push({ text, options });
            if (!this.isSpeaking) {
                this._processQueue();
            }
        } else {
            // Immediate without queue
            this.synth.cancel();
            this._speakNow(text, options);
        }
    }
    
    _speakNow(text, options = {}) {
        this.isSpeaking = true;
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.voice = this.voice;
        utterance.rate = options.rate || this.rate;
        utterance.pitch = options.pitch || this.pitch;
        utterance.volume = options.volume || this.volume;
        
        utterance.onend = () => {
            this.isSpeaking = false;
            if (options.onEnd) {
                options.onEnd();
            }
            // Process next in queue
            setTimeout(() => this._processQueue(), 300);
        };
        
        utterance.onerror = () => {
            this.isSpeaking = false;
            setTimeout(() => this._processQueue(), 300);
        };
        
        this.synth.speak(utterance);
    }
    
    _processQueue() {
        if (this.queue.length === 0 || this.isSpeaking) {
            return;
        }
        
        const { text, options } = this.queue.shift();
        this._speakNow(text, options);
    }
    
    stop() {
        this.synth.cancel();
        this.queue = [];
        this.isSpeaking = false;
    }
    
    clearQueue() {
        this.queue = [];
    }
    
    /**
     * Check if voice-over is currently speaking
     * @returns {boolean} True if speaking
     */
    isBusy() {
        return this.isSpeaking || this.queue.length > 0;
    }
    
    /**
     * Get queue length
     * @returns {number} Number of queued messages
     */
    getQueueLength() {
        return this.queue.length;
    }
    
    /**
     * Pause current speech (browser support varies)
     */
    pause() {
        if (this.synth.speaking) {
            this.synth.pause();
        }
    }
    
    /**
     * Resume paused speech (browser support varies)
     */
    resume() {
        if (this.synth.paused) {
            this.synth.resume();
        }
    }
    
    toggle() {
        this.enabled = !this.enabled;
        this.savePreferences();
        return this.enabled;
    }
    
    setRate(rate) {
        this.rate = Math.max(0.5, Math.min(2.0, rate));
        this.savePreferences();
    }
    
    setPitch(pitch) {
        this.pitch = Math.max(0.5, Math.min(2.0, pitch));
        this.savePreferences();
    }
    
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1.0, volume));
        this.savePreferences();
    }
    
    savePreferences() {
        localStorage.setItem('voiceOverPrefs', JSON.stringify({
            enabled: this.enabled,
            rate: this.rate,
            pitch: this.pitch,
            volume: this.volume
        }));
    }
    
    // Predefined messages
    welcomeMessage() {
        this.speak("Welcome to Zen_Align. Let's begin your wellness journey.");
    }
    
    sessionStart(moduleName) {
        this.speak(`Starting ${moduleName} session. Please get ready.`);
    }
    
    poseInstruction(poseName, instruction) {
        this.speak(`${poseName}. ${instruction}`);
    }
    
    poseCorrection(feedback) {
        this.speak(feedback);
    }
    
    poseSuccess(poseName) {
        this.speak(`Excellent! ${poseName} completed successfully.`);
    }
    
    poseIncorrect(poseName) {
        this.speak(`Please adjust your ${poseName}. Check your alignment.`);
    }
    
    sessionPaused() {
        this.speak("Session paused. Take your time.");
    }
    
    sessionResumed() {
        this.speak("Resuming session. Let's continue.");
    }
    
    sessionComplete(stats) {
        const message = `Session complete! You practiced for ${stats.duration} minutes with ${stats.accuracy}% accuracy. Great work!`;
        this.speak(message);
    }
    
    countdown(number) {
        this.speak(number.toString());
    }
    
    breathingCue(phase) {
        const messages = {
            'inhale': 'Breathe in',
            'hold': 'Hold',
            'exhale': 'Breathe out',
            'rest': 'Rest'
        };
        this.speak(messages[phase] || phase);
    }
    
    encouragement() {
        const messages = [
            "You're doing great!",
            "Keep it up!",
            "Excellent form!",
            "Stay focused!",
            "Beautiful pose!",
            "Perfect alignment!"
        ];
        const message = messages[Math.floor(Math.random() * messages.length)];
        this.speak(message);
    }
    
    error(message) {
        this.speak(`Error: ${message}`);
    }
    
    // ===== Enhanced Session Lifecycle Methods =====
    
    /**
     * Called when a session starts
     * @param {string} module - Module name (e.g., "Surya Namaskar", "Breathing", "Stretching")
     */
    onSessionStart(module) {
        const message = `Starting ${module} session. Please get into position and prepare yourself.`;
        this.speak(message, { priority: 'high' });
    }
    
    /**
     * Called when transitioning to a new pose
     * @param {Object} pose - Pose object with name and instruction
     */
    onPoseChange(pose) {
        const poseName = pose.name || pose.poseName || 'next pose';
        const instruction = pose.voiceInstruction || pose.instruction || '';
        
        let message = `Next pose: ${poseName}.`;
        if (instruction) {
            message += ` ${instruction}`;
        }
        
        this.speak(message, { rate: 0.9 });
    }
    
    /**
     * Called when pose validation detects an error
     * @param {string} feedback - Correction feedback message
     * @param {Object} options - Additional options
     */
    onPoseCorrection(feedback, options = {}) {
        const message = options.detailed 
            ? `Correction needed: ${feedback}. Please adjust your position.`
            : feedback;
        
        this.speak(message, { rate: 0.85, priority: 'high' });
    }
    
    /**
     * Called when pose is validated successfully
     * @param {string} poseName - Name of the pose
     */
    onPoseSuccess(poseName) {
        const messages = [
            `Perfect! ${poseName} completed successfully.`,
            `Excellent! Moving to the next pose.`,
            `Great form! Well done.`,
            `Beautiful ${poseName}!`
        ];
        const message = messages[Math.floor(Math.random() * messages.length)];
        this.speak(message);
    }
    
    /**
     * Called when session is paused
     * @param {string} reason - Optional reason for pause
     */
    onSessionPause(reason) {
        const message = reason 
            ? `Session paused: ${reason}. Take your time.`
            : 'Session paused. Resume when you are ready.';
        
        this.speak(message, { priority: 'high' });
    }
    
    /**
     * Called when session is resumed
     */
    onSessionResume() {
        this.speak('Resuming session. Let\'s continue your practice.', { priority: 'high' });
    }
    
    /**
     * Called when session completes
     * @param {Object} results - Session results with duration, accuracy, poses completed
     */
    onSessionComplete(results) {
        const duration = results.duration || 0;
        const accuracy = results.accuracy || results.accuracyScore || 0;
        const posesCompleted = results.posesCompleted || results.poses_completed || 0;
        
        let message = 'Session complete! ';
        
        if (duration > 0) {
            const minutes = Math.floor(duration / 60);
            const seconds = duration % 60;
            if (minutes > 0) {
                message += `You practiced for ${minutes} minute${minutes > 1 ? 's' : ''}`;
                if (seconds > 0) {
                    message += ` and ${seconds} seconds. `;
                } else {
                    message += '. ';
                }
            } else {
                message += `You practiced for ${seconds} seconds. `;
            }
        }
        
        if (posesCompleted > 0) {
            message += `You completed ${posesCompleted} pose${posesCompleted > 1 ? 's' : ''}. `;
        }
        
        if (accuracy > 0) {
            message += `Your accuracy was ${Math.round(accuracy)}%. `;
        }
        
        // Add encouraging message based on accuracy
        if (accuracy >= 90) {
            message += 'Outstanding performance!';
        } else if (accuracy >= 75) {
            message += 'Great work!';
        } else if (accuracy >= 60) {
            message += 'Good effort! Keep practicing.';
        } else {
            message += 'Keep practicing, you\'re improving!';
        }
        
        this.speak(message, { rate: 0.95 });
    }
    
    /**
     * Provides timed guidance after user has been in incorrect pose
     * @param {string} guidance - Specific guidance message
     */
    onTimedGuidance(guidance) {
        const message = `Guidance: ${guidance}`;
        this.speak(message, { rate: 0.85, priority: 'high' });
    }
    
    /**
     * Announces pose transition countdown
     * @param {number} seconds - Seconds remaining
     */
    onPoseTransitionCountdown(seconds) {
        if (seconds <= 3) {
            this.speak(seconds.toString(), { queue: false });
        }
    }
    
    /**
     * Provides breathing cues during poses
     * @param {string} phase - 'inhale', 'exhale', 'hold'
     */
    onBreathingCue(phase) {
        const cues = {
            'inhale': 'Breathe in deeply',
            'exhale': 'Breathe out slowly',
            'hold': 'Hold your breath',
            'relax': 'Relax and breathe naturally'
        };
        
        const message = cues[phase] || phase;
        this.speak(message, { rate: 0.8 });
    }
    
    /**
     * Provides encouragement during session
     */
    onEncouragement() {
        const messages = [
            "You're doing wonderfully!",
            "Keep up the excellent work!",
            "Your form is improving!",
            "Stay focused and breathe!",
            "Beautiful practice!",
            "You're making great progress!"
        ];
        
        const message = messages[Math.floor(Math.random() * messages.length)];
        this.speak(message);
    }
}

// Create global instance
const voiceOver = new VoiceOverManager();

// Global audio conflict prevention
// Ensure only one audio source is active at a time
window.addEventListener('beforeunload', function() {
    if (voiceOver) {
        voiceOver.stop();
    }
});

// Prevent multiple speech synthesis instances
if (window.speechSynthesis) {
    // Cancel any existing speech when page loads
    window.speechSynthesis.cancel();
    
    // Handle visibility change to pause/resume appropriately
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            // Page is hidden, pause voice-over
            if (voiceOver && voiceOver.isSpeaking) {
                voiceOver.pause();
            }
        } else {
            // Page is visible, resume voice-over
            if (voiceOver && window.speechSynthesis.paused) {
                voiceOver.resume();
            }
        }
    });
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoiceOverManager;
}

// Make voiceOver globally accessible
window.voiceOver = voiceOver;
