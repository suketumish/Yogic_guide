/**
 * Enhanced Pose Correction Logic
 * Session stops immediately if pose is incorrect
 * Session continues only when pose matches
 */

class PoseCorrectionEngine {
    constructor(options = {}) {
        this.strictMode = options.strictMode !== false; // Default: strict
        this.accuracyThreshold = options.accuracyThreshold || 75; // Minimum 75% accuracy
        this.maxRetries = options.maxRetries || 3;
        this.currentRetries = 0;
        this.sessionActive = false;
        this.currentPose = null;
        this.poseHistory = [];
        
        // Callbacks
        this.onPoseCorrect = options.onPoseCorrect || (() => {});
        this.onPoseIncorrect = options.onPoseIncorrect || (() => {});
        this.onSessionStop = options.onSessionStop || (() => {});
        this.onMaxRetriesReached = options.onMaxRetriesReached || (() => {});
    }
    
    startSession() {
        this.sessionActive = true;
        this.currentRetries = 0;
        this.poseHistory = [];
        console.log('✅ Session started with strict pose correction');
    }
    
    stopSession(reason = 'manual') {
        this.sessionActive = false;
        this.currentPose = null;
        console.log(`⏹️ Session stopped: ${reason}`);
        this.onSessionStop(reason, this.poseHistory);
    }
    
    validatePose(poseData, expectedPose) {
        if (!this.sessionActive) {
            console.warn('⚠️ Session not active');
            return { valid: false, reason: 'Session not active' };
        }
        
        this.currentPose = expectedPose;
        
        // Calculate pose accuracy
        const accuracy = this.calculatePoseAccuracy(poseData, expectedPose);
        
        // Record in history
        this.poseHistory.push({
            pose: expectedPose.name,
            accuracy: accuracy,
            timestamp: new Date().toISOString(),
            valid: accuracy >= this.accuracyThreshold
        });
        
        // Check if pose meets threshold
        if (accuracy >= this.accuracyThreshold) {
            // Pose is correct - continue session
            this.currentRetries = 0;
            console.log(`✅ Pose correct: ${expectedPose.name} (${accuracy}%)`);
            
            // Voice feedback
            if (typeof voiceOver !== 'undefined') {
                voiceOver.poseSuccess(expectedPose.name);
            }
            
            this.onPoseCorrect({
                pose: expectedPose.name,
                accuracy: accuracy,
                feedback: this.generatePositiveFeedback(accuracy)
            });
            
            return {
                valid: true,
                accuracy: accuracy,
                canContinue: true,
                feedback: this.generatePositiveFeedback(accuracy)
            };
            
        } else {
            // Pose is incorrect - STOP session immediately
            this.currentRetries++;
            console.log(`❌ Pose incorrect: ${expectedPose.name} (${accuracy}%) - Retry ${this.currentRetries}/${this.maxRetries}`);
            
            const feedback = this.generateCorrectionFeedback(poseData, expectedPose, accuracy);
            
            // Voice feedback
            if (typeof voiceOver !== 'undefined') {
                voiceOver.poseIncorrect(expectedPose.name);
                voiceOver.poseCorrection(feedback);
            }
            
            this.onPoseIncorrect({
                pose: expectedPose.name,
                accuracy: accuracy,
                retries: this.currentRetries,
                maxRetries: this.maxRetries,
                feedback: feedback
            });
            
            // Check if max retries reached
            if (this.currentRetries >= this.maxRetries) {
                console.log('🛑 Max retries reached - stopping session');
                this.onMaxRetriesReached({
                    pose: expectedPose.name,
                    attempts: this.currentRetries
                });
                this.stopSession('max_retries_reached');
                
                return {
                    valid: false,
                    accuracy: accuracy,
                    canContinue: false,
                    sessionStopped: true,
                    reason: 'Maximum retry attempts reached',
                    feedback: feedback
                };
            }
            
            // STOP session immediately in strict mode
            if (this.strictMode) {
                console.log('🛑 Strict mode: Stopping session due to incorrect pose');
                this.stopSession('incorrect_pose');
                
                return {
                    valid: false,
                    accuracy: accuracy,
                    canContinue: false,
                    sessionStopped: true,
                    reason: 'Pose does not match required position',
                    feedback: feedback,
                    retryAllowed: this.currentRetries < this.maxRetries
                };
            }
            
            return {
                valid: false,
                accuracy: accuracy,
                canContinue: false,
                feedback: feedback,
                retryAllowed: true
            };
        }
    }
    
    calculatePoseAccuracy(poseData, expectedPose) {
        // This is a simplified calculation
        // In production, this would use ML model predictions
        
        if (!poseData || !poseData.keypoints) {
            return 0;
        }
        
        let totalScore = 0;
        let keypointCount = 0;
        
        // Check key body landmarks
        const criticalKeypoints = [
            'nose', 'left_shoulder', 'right_shoulder',
            'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist',
            'left_hip', 'right_hip', 'left_knee', 'right_knee',
            'left_ankle', 'right_ankle'
        ];
        
        criticalKeypoints.forEach(keypoint => {
            if (poseData.keypoints[keypoint]) {
                const confidence = poseData.keypoints[keypoint].confidence || 0;
                totalScore += confidence * 100;
                keypointCount++;
            }
        });
        
        const accuracy = keypointCount > 0 ? totalScore / keypointCount : 0;
        return Math.round(accuracy);
    }
    
    generatePositiveFeedback(accuracy) {
        if (accuracy >= 95) {
            return "Perfect form! Excellent alignment!";
        } else if (accuracy >= 85) {
            return "Great job! Your pose looks good!";
        } else {
            return "Good! Keep maintaining this position!";
        }
    }
    
    generateCorrectionFeedback(poseData, expectedPose, accuracy) {
        const feedback = [];
        
        if (accuracy < 50) {
            feedback.push("Please adjust your entire body position.");
        } else if (accuracy < 65) {
            feedback.push("Your pose needs significant adjustment.");
        } else {
            feedback.push("You're close! Minor adjustments needed.");
        }
        
        // Add specific corrections based on pose type
        if (expectedPose.name.toLowerCase().includes('warrior')) {
            feedback.push("Check your stance width and arm position.");
        } else if (expectedPose.name.toLowerCase().includes('tree')) {
            feedback.push("Focus on your balance and leg placement.");
        } else if (expectedPose.name.toLowerCase().includes('downward')) {
            feedback.push("Ensure your hips are lifted and arms are straight.");
        } else if (expectedPose.name.toLowerCase().includes('plank')) {
            feedback.push("Keep your body in a straight line.");
        }
        
        feedback.push("Please correct your pose to continue.");
        
        return feedback.join(' ');
    }
    
    resetRetries() {
        this.currentRetries = 0;
    }
    
    getSessionStats() {
        const totalPoses = this.poseHistory.length;
        const correctPoses = this.poseHistory.filter(p => p.valid).length;
        const avgAccuracy = totalPoses > 0
            ? this.poseHistory.reduce((sum, p) => sum + p.accuracy, 0) / totalPoses
            : 0;
        
        return {
            totalPoses,
            correctPoses,
            incorrectPoses: totalPoses - correctPoses,
            avgAccuracy: Math.round(avgAccuracy),
            successRate: totalPoses > 0 ? Math.round((correctPoses / totalPoses) * 100) : 0,
            history: this.poseHistory
        };
    }
    
    setStrictMode(enabled) {
        this.strictMode = enabled;
        console.log(`Strict mode: ${enabled ? 'enabled' : 'disabled'}`);
    }
    
    setAccuracyThreshold(threshold) {
        this.accuracyThreshold = Math.max(50, Math.min(100, threshold));
        console.log(`Accuracy threshold set to: ${this.accuracyThreshold}%`);
    }
}

// Create global instance
const poseCorrectionEngine = new PoseCorrectionEngine({
    strictMode: true,
    accuracyThreshold: 75,
    maxRetries: 3,
    onPoseCorrect: (data) => {
        console.log('✅ Pose correct:', data);
        // Update UI
        if (typeof updatePoseStatus === 'function') {
            updatePoseStatus('correct', data);
        }
    },
    onPoseIncorrect: (data) => {
        console.log('❌ Pose incorrect:', data);
        // Update UI
        if (typeof updatePoseStatus === 'function') {
            updatePoseStatus('incorrect', data);
        }
    },
    onSessionStop: (reason, history) => {
        console.log('🛑 Session stopped:', reason);
        // Handle session stop
        if (typeof handleSessionStop === 'function') {
            handleSessionStop(reason, history);
        }
    },
    onMaxRetriesReached: (data) => {
        console.log('⚠️ Max retries reached:', data);
        // Show retry limit message
        if (typeof showRetryLimitMessage === 'function') {
            showRetryLimitMessage(data);
        }
    }
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PoseCorrectionEngine;
}
