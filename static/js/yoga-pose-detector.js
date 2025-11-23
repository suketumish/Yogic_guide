/**
 * Yoga Pose Detector Integration
 * Connects MediaPipe pose detection with trained yoga model
 */

class YogaPoseDetector {
    constructor() {
        this.isReady = false;
        this.lastDetectionTime = 0;
        this.detectionInterval = 1000; // Detect every 1 second
        this.currentPose = null;
        this.confidence = 0;
        
        this.checkSystemStatus();
    }
    
    /**
     * Check if yoga detection system is ready
     */
    async checkSystemStatus() {
        try {
            const response = await fetch('/api/yoga/status');
            const data = await response.json();
            
            this.isReady = data.ready;
            
            if (this.isReady) {
                console.log('✅ Yoga Detection System Ready');
                console.log(`📊 Available poses: ${data.available_poses}`);
            } else {
                console.warn('⚠️  Yoga Detection System Not Ready');
                console.warn(data.message);
            }
            
            return this.isReady;
        } catch (error) {
            console.error('❌ Failed to check system status:', error);
            this.isReady = false;
            return false;
        }
    }
    
    /**
     * Detect yoga pose from video frame
     * @param {HTMLCanvasElement} canvas - Canvas with current video frame
     * @returns {Promise<Object>} Detection result
     */
    async detectPoseFromCanvas(canvas) {
        if (!this.isReady) {
            return {
                success: false,
                error: 'System not ready'
            };
        }
        
        // Throttle detection
        const now = Date.now();
        if (now - this.lastDetectionTime < this.detectionInterval) {
            return {
                success: false,
                error: 'Throttled'
            };
        }
        
        try {
            // Convert canvas to base64
            const imageData = canvas.toDataURL('image/jpeg', 0.8);
            
            // Send to API
            const response = await fetch('/api/yoga/detect-realtime', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    frame: imageData
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.currentPose = result.pose_name;
                this.confidence = result.confidence;
                this.lastDetectionTime = now;
            }
            
            return result;
            
        } catch (error) {
            console.error('❌ Detection error:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    /**
     * Detect yoga pose from base64 image
     * @param {string} imageBase64 - Base64 encoded image
     * @returns {Promise<Object>} Detection result
     */
    async detectPoseFromBase64(imageBase64) {
        if (!this.isReady) {
            return {
                success: false,
                error: 'System not ready'
            };
        }
        
        try {
            const response = await fetch('/api/yoga/detect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image: imageBase64
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.currentPose = result.pose_name;
                this.confidence = result.confidence;
            }
            
            return result;
            
        } catch (error) {
            console.error('❌ Detection error:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    /**
     * Get list of available poses
     * @returns {Promise<Array>} List of pose names
     */
    async getAvailablePoses() {
        try {
            const response = await fetch('/api/yoga/poses');
            const data = await response.json();
            
            if (data.success) {
                return data.poses;
            }
            
            return [];
        } catch (error) {
            console.error('❌ Failed to get poses:', error);
            return [];
        }
    }
    
    /**
     * Get current detected pose
     * @returns {Object} Current pose info
     */
    getCurrentPose() {
        return {
            pose: this.currentPose,
            confidence: this.confidence,
            displayName: this.currentPose ? this.currentPose.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) : null
        };
    }
    
    /**
     * Set detection interval
     * @param {number} interval - Interval in milliseconds
     */
    setDetectionInterval(interval) {
        this.detectionInterval = interval;
    }
}

// Create global instance
window.yogaPoseDetector = new YogaPoseDetector();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = YogaPoseDetector;
}
