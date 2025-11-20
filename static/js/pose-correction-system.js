/**
 * Strict Pose Correction System
 * Implements real-time pose validation with session pause/resume logic
 * Requirements: 11.1, 11.3, 11.4, 11.5
 */

class StrictPoseCorrectionSystem {
    constructor(session, voiceOverManager) {
        this.session = session;
        this.voiceOver = voiceOverManager;
        this.isPaused = false;
        this.currentPose = null;
        this.validationThreshold = 0.75;  // 75% accuracy required
        this.correctionAttempts = 0;
        this.maxCorrectionTime = 60;  // seconds
        this.correctionStartTime = null;
        this.lastCorrectionFeedbackTime = null;
        this.feedbackThrottleInterval = 10000;  // 10 seconds between voice feedback
        this.correctionLog = [];
        
        // Bind methods
        this.validatePose = this.validatePose.bind(this);
        this.pauseSession = this.pauseSession.bind(this);
        this.resumeSession = this.resumeSession.bind(this);
    }
    
    /**
     * Set the current pose for validation
     * @param {Object} pose - Pose object with validation criteria
     */
    setCurrentPose(pose) {
        this.currentPose = pose;
        this.isPaused = false;
        this.correctionAttempts = 0;
        this.correctionStartTime = null;
        this.lastCorrectionFeedbackTime = null;
    }
    
    /**
     * Validate detected pose against current pose criteria
     * @param {Object} detectedPose - Detected pose with landmarks
     * @returns {Object} Validation result with accuracy and status
     */
    async validatePose(detectedPose) {
        if (!this.currentPose || !detectedPose) {
            return { isValid: false, accuracy: 0, shouldPause: false };
        }
        
        // Calculate accuracy
        const accuracy = this.calculateAccuracy(
            detectedPose, 
            this.currentPose.validationCriteria || this.currentPose
        );
        
        const isValid = accuracy >= this.validationThreshold;
        
        if (!isValid) {
            // Pose is incorrect - pause session
            if (!this.isPaused) {
                this.pauseSession();
            }
            
            // Provide correction feedback
            this.provideCorrectionFeedback(detectedPose, accuracy);
            
            return { 
                isValid: false, 
                accuracy: accuracy, 
                shouldPause: true,
                errors: this.analyzePoseErrors(detectedPose)
            };
        } else {
            // Pose is correct - resume if paused
            if (this.isPaused) {
                this.resumeSession();
            }
            
            return { 
                isValid: true, 
                accuracy: accuracy, 
                shouldPause: false 
            };
        }
    }
    
    /**
     * Calculate pose accuracy based on key points
     * @param {Object} detected - Detected pose landmarks
     * @param {Object} criteria - Validation criteria with angles and thresholds
     * @returns {number} Accuracy percentage (0-1)
     */
    calculateAccuracy(detected, criteria) {
        if (!criteria.angles && !criteria.keyPoints) {
            // Fallback: use simple angle comparison
            return this._calculateSimpleAccuracy(detected, criteria);
        }
        
        const angles = criteria.angles || {};
        const tolerance = criteria.tolerance || 15;
        
        let totalPoints = 0;
        let correctPoints = 0;
        
        // Calculate angles from detected landmarks
        const detectedAngles = this._calculateAnglesFromLandmarks(detected.landmarks || detected);
        
        // Compare each angle
        for (const [joint, targetAngle] of Object.entries(angles)) {
            const detectedAngle = detectedAngles[joint];
            
            if (detectedAngle === null || detectedAngle === undefined) {
                continue; // Skip if angle couldn't be calculated
            }
            
            totalPoints++;
            
            const diff = Math.abs(detectedAngle - targetAngle);
            if (diff <= tolerance) {
                correctPoints++;
            }
        }
        
        if (totalPoints === 0) {
            return 0;
        }
        
        return correctPoints / totalPoints;
    }
    
    /**
     * Calculate angles from landmarks (helper method)
     * @private
     */
    _calculateAnglesFromLandmarks(landmarks) {
        if (!landmarks || landmarks.length === 0) {
            return {};
        }
        
        return {
            leftElbow: this._calculateAngle(landmarks[11], landmarks[13], landmarks[15]),
            rightElbow: this._calculateAngle(landmarks[12], landmarks[14], landmarks[16]),
            leftKnee: this._calculateAngle(landmarks[23], landmarks[25], landmarks[27]),
            rightKnee: this._calculateAngle(landmarks[24], landmarks[26], landmarks[28]),
            leftShoulder: this._calculateAngle(landmarks[13], landmarks[11], landmarks[23]),
            rightShoulder: this._calculateAngle(landmarks[14], landmarks[12], landmarks[24]),
            leftHip: this._calculateAngle(landmarks[11], landmarks[23], landmarks[25]),
            rightHip: this._calculateAngle(landmarks[12], landmarks[24], landmarks[26]),
            leftAnkle: this._calculateAngle(landmarks[25], landmarks[27], landmarks[31]),
            rightAnkle: this._calculateAngle(landmarks[26], landmarks[28], landmarks[32]),
            torsoAngle: this._calculateTorsoAngle(landmarks),
            neckAngle: this._calculateAngle(landmarks[0], landmarks[11], landmarks[23])
        };
    }
    
    /**
     * Calculate angle between three points
     * @private
     */
    _calculateAngle(a, b, c) {
        if (!a || !b || !c) return null;
        
        // Check visibility if available
        const minVisibility = 0.5;
        if (a.visibility !== undefined && a.visibility < minVisibility) return null;
        if (b.visibility !== undefined && b.visibility < minVisibility) return null;
        if (c.visibility !== undefined && c.visibility < minVisibility) return null;
        
        // Calculate vectors
        const ba = { 
            x: a.x - b.x, 
            y: a.y - b.y, 
            z: (a.z || 0) - (b.z || 0) 
        };
        const bc = { 
            x: c.x - b.x, 
            y: c.y - b.y, 
            z: (c.z || 0) - (b.z || 0) 
        };
        
        // Calculate dot product and magnitudes
        const dotProduct = ba.x * bc.x + ba.y * bc.y + ba.z * bc.z;
        const magnitudeBA = Math.sqrt(ba.x * ba.x + ba.y * ba.y + ba.z * ba.z);
        const magnitudeBC = Math.sqrt(bc.x * bc.x + bc.y * bc.y + bc.z * bc.z);
        
        if (magnitudeBA === 0 || magnitudeBC === 0) return null;
        
        // Calculate angle
        const cosAngle = dotProduct / (magnitudeBA * magnitudeBC);
        const angle = Math.acos(Math.max(-1, Math.min(1, cosAngle))) * (180 / Math.PI);
        
        return angle;
    }
    
    /**
     * Calculate torso angle
     * @private
     */
    _calculateTorsoAngle(landmarks) {
        const shoulder = landmarks[11];
        const hip = landmarks[23];
        
        if (!shoulder || !hip) return null;
        
        const minVisibility = 0.5;
        if (shoulder.visibility !== undefined && shoulder.visibility < minVisibility) return null;
        if (hip.visibility !== undefined && hip.visibility < minVisibility) return null;
        
        const deltaY = hip.y - shoulder.y;
        const deltaX = hip.x - shoulder.x;
        const angle = Math.atan2(deltaX, deltaY) * (180 / Math.PI);
        
        return Math.abs(angle);
    }
    
    /**
     * Simple accuracy calculation fallback
     * @private
     */
    _calculateSimpleAccuracy(detected, criteria) {
        // Fallback to basic comparison
        return 0.8; // Default to 80% if no criteria
    }
    
    /**
     * Pause the session due to incorrect pose
     */
    pauseSession() {
        if (this.isPaused) return;
        
        this.isPaused = true;
        this.correctionAttempts++;
        this.correctionStartTime = Date.now();
        
        // Notify session
        if (this.session && typeof this.session.pause === 'function') {
            this.session.pause();
        }
        
        // Voice feedback
        if (this.voiceOver) {
            this.voiceOver.speak(
                "Please adjust your pose. Check the guidance on screen.",
                { priority: 'high', rate: 0.85 }
            );
        }
        
        // Show correction overlay
        this.showCorrectionOverlay();
        
        // Log correction event
        this._logCorrectionEvent('pause');
    }
    
    /**
     * Resume the session after pose is corrected
     */
    resumeSession() {
        if (!this.isPaused) return;
        
        this.isPaused = false;
        
        // Calculate correction duration
        const correctionDuration = this.correctionStartTime 
            ? Math.floor((Date.now() - this.correctionStartTime) / 1000)
            : 0;
        
        // Notify session
        if (this.session && typeof this.session.resume === 'function') {
            this.session.resume();
        }
        
        // Voice feedback
        if (this.voiceOver) {
            this.voiceOver.speak(
                "Perfect! Continuing session.",
                { priority: 'high' }
            );
        }
        
        // Hide correction overlay
        this.hideCorrectionOverlay();
        
        // Log correction event
        this._logCorrectionEvent('resume', correctionDuration);
        
        // Reset correction tracking
        this.correctionStartTime = null;
        this.lastCorrectionFeedbackTime = null;
    }
    
    /**
     * Provide correction feedback to user
     * @param {Object} detectedPose - Current detected pose
     * @param {number} accuracy - Current accuracy score
     */
    provideCorrectionFeedback(detectedPose, accuracy) {
        const feedback = this.analyzePoseErrors(detectedPose);
        
        // Visual feedback
        this.displayCorrectionText(feedback.message, accuracy);
        this.highlightIncorrectAreas(feedback.errors);
        
        // Voice feedback (throttled)
        const now = Date.now();
        const shouldProvideVoiceFeedback = !this.lastCorrectionFeedbackTime || 
            (now - this.lastCorrectionFeedbackTime) >= this.feedbackThrottleInterval;
        
        if (shouldProvideVoiceFeedback && this.voiceOver) {
            this.voiceOver.speak(feedback.message, { rate: 0.85 });
            this.lastCorrectionFeedbackTime = now;
        }
    }
    
    /**
     * Analyze pose errors and generate feedback
     * @param {Object} detectedPose - Detected pose with landmarks
     * @returns {Object} Feedback with errors and message
     */
    analyzePoseErrors(detectedPose) {
        const errors = [];
        
        if (!this.currentPose || !this.currentPose.angles) {
            return {
                errors: [],
                message: "Please adjust your position to match the target pose."
            };
        }
        
        const criteria = this.currentPose;
        const tolerance = criteria.tolerance || 15;
        const detectedAngles = this._calculateAnglesFromLandmarks(
            detectedPose.landmarks || detectedPose
        );
        
        // Check each angle
        for (const [joint, targetAngle] of Object.entries(criteria.angles)) {
            const detectedAngle = detectedAngles[joint];
            
            if (detectedAngle === null || detectedAngle === undefined) {
                continue;
            }
            
            const diff = Math.abs(detectedAngle - targetAngle);
            
            if (diff > tolerance) {
                const adjustment = detectedAngle > targetAngle ? 'decrease' : 'increase';
                errors.push({
                    joint: joint,
                    expected: targetAngle,
                    actual: detectedAngle,
                    difference: diff,
                    adjustment: adjustment,
                    message: this._getErrorMessage(joint, adjustment, diff)
                });
            }
        }
        
        return {
            errors: errors,
            message: this._formatFeedbackMessage(errors)
        };
    }
    
    /**
     * Get error message for specific joint
     * @private
     */
    _getErrorMessage(joint, adjustment, difference) {
        const jointName = joint.replace(/([A-Z])/g, ' $1').trim().toLowerCase();
        return `${jointName}: ${adjustment} by ${Math.round(difference)} degrees`;
    }
    
    /**
     * Format feedback message from errors
     * @private
     */
    _formatFeedbackMessage(errors) {
        if (errors.length === 0) {
            return "Adjust your position to match the target pose.";
        }
        
        // Prioritize top 2 errors
        const topErrors = errors
            .sort((a, b) => b.difference - a.difference)
            .slice(0, 2);
        
        const messages = topErrors.map(e => {
            const jointName = e.joint.replace(/([A-Z])/g, ' $1').trim();
            return `${jointName} (${e.adjustment} by ${Math.round(e.difference)}°)`;
        });
        
        return `Adjust: ${messages.join(', ')}`;
    }
    
    /**
     * Show correction overlay UI
     */
    showCorrectionOverlay() {
        // Check if overlay already exists
        let overlay = document.getElementById('correction-overlay');
        
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'correction-overlay';
            overlay.className = 'correction-overlay';
            overlay.innerHTML = `
                <div class="correction-panel">
                    <div class="correction-icon">⚠️</div>
                    <h3 class="correction-title">Pose Adjustment Needed</h3>
                    <div id="correction-feedback" class="correction-feedback"></div>
                    <div class="correction-tips">
                        <p>💡 Follow the guide overlay on your video feed</p>
                        <p>🎯 Match your body position to the target angles</p>
                    </div>
                </div>
            `;
            document.body.appendChild(overlay);
        }
        
        overlay.style.display = 'flex';
    }
    
    /**
     * Hide correction overlay UI
     */
    hideCorrectionOverlay() {
        const overlay = document.getElementById('correction-overlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }
    
    /**
     * Display correction text in UI
     * @param {string} message - Correction message
     * @param {number} accuracy - Current accuracy percentage
     */
    displayCorrectionText(message, accuracy) {
        const feedbackDiv = document.getElementById('correction-feedback');
        if (feedbackDiv) {
            const accuracyPercent = Math.round(accuracy * 100);
            feedbackDiv.innerHTML = `
                <p class="correction-message">${message}</p>
                <div class="accuracy-display">
                    <span class="accuracy-label">Current Accuracy:</span>
                    <span class="accuracy-value">${accuracyPercent}%</span>
                    <span class="accuracy-target">(Target: ${Math.round(this.validationThreshold * 100)}%)</span>
                </div>
            `;
        }
    }
    
    /**
     * Highlight incorrect body areas on canvas
     * @param {Array} errors - Array of error objects
     */
    highlightIncorrectAreas(errors) {
        // This will be called from the main pose detection loop
        // Store errors for rendering
        this.currentErrors = errors;
    }
    
    /**
     * Get current errors for rendering
     * @returns {Array} Current errors
     */
    getCurrentErrors() {
        return this.currentErrors || [];
    }
    
    /**
     * Log correction event for analytics
     * @private
     */
    _logCorrectionEvent(eventType, duration = null) {
        const event = {
            type: eventType,
            timestamp: new Date().toISOString(),
            pose: this.currentPose ? this.currentPose.name : 'unknown',
            attempt: this.correctionAttempts,
            duration: duration
        };
        
        this.correctionLog.push(event);
    }
    
    /**
     * Get correction log for session
     * @returns {Array} Correction log entries
     */
    getCorrectionLog() {
        return this.correctionLog;
    }
    
    /**
     * Get correction statistics
     * @returns {Object} Statistics about corrections
     */
    getCorrectionStats() {
        const totalCorrections = this.correctionLog.filter(e => e.type === 'pause').length;
        const totalDuration = this.correctionLog
            .filter(e => e.type === 'resume' && e.duration)
            .reduce((sum, e) => sum + e.duration, 0);
        
        return {
            totalCorrections: totalCorrections,
            totalCorrectionDuration: totalDuration,
            averageCorrectionDuration: totalCorrections > 0 ? totalDuration / totalCorrections : 0,
            correctionLog: this.correctionLog
        };
    }
    
    /**
     * Reset correction system for new session
     */
    reset() {
        this.isPaused = false;
        this.currentPose = null;
        this.correctionAttempts = 0;
        this.correctionStartTime = null;
        this.lastCorrectionFeedbackTime = null;
        this.correctionLog = [];
        this.currentErrors = [];
        this.hideCorrectionOverlay();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StrictPoseCorrectionSystem;
}

// Make globally accessible
window.StrictPoseCorrectionSystem = StrictPoseCorrectionSystem;
