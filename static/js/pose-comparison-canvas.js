/**
 * Pose Comparison Canvas
 * Visual comparison between detected pose and target pose
 * Requirements: 11.2, 11.6
 */

class PoseComparisonCanvas {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
        this.targetPose = null;
        this.detectedPose = null;
        this.errors = [];
    }
    
    /**
     * Set target pose for comparison
     * @param {Object} pose - Target pose with angles
     */
    setTargetPose(pose) {
        this.targetPose = pose;
    }
    
    /**
     * Update detected pose
     * @param {Object} landmarks - Detected pose landmarks
     */
    updateDetectedPose(landmarks) {
        this.detectedPose = landmarks;
    }
    
    /**
     * Set errors to highlight
     * @param {Array} errors - Array of error objects
     */
    setErrors(errors) {
        this.errors = errors || [];
    }
    
    /**
     * Draw skeleton with error highlighting
     * @param {Array} landmarks - Pose landmarks
     * @param {Object} options - Drawing options
     */
    drawSkeleton(landmarks, options = {}) {
        if (!this.ctx || !landmarks) return;
        
        const {
            color = '#10b981',
            lineWidth = 3,
            highlightErrors = false
        } = options;
        
        // Define connections
        const connections = [
            // Arms
            [11, 12], [11, 13], [13, 15], [12, 14], [14, 16],
            // Torso
            [11, 23], [12, 24], [23, 24],
            // Legs
            [23, 25], [25, 27], [24, 26], [26, 28],
            // Feet
            [27, 29], [28, 30], [29, 31], [30, 32],
            // Face (optional)
            [0, 1], [1, 2], [2, 3], [3, 7], [0, 4], [4, 5], [5, 6], [6, 8]
        ];
        
        const minVisibility = 0.5;
        
        // Draw connections
        connections.forEach(([start, end]) => {
            const startPoint = landmarks[start];
            const endPoint = landmarks[end];
            
            if (!startPoint || !endPoint) return;
            if (startPoint.visibility < minVisibility || endPoint.visibility < minVisibility) return;
            
            // Check if this connection involves an error joint
            const hasError = highlightErrors && this._isErrorJoint(start, end);
            
            const avgVisibility = (startPoint.visibility + endPoint.visibility) / 2;
            const alpha = Math.min(avgVisibility, 1);
            
            this.ctx.strokeStyle = hasError 
                ? `rgba(239, 68, 68, ${alpha})` 
                : `rgba(16, 185, 129, ${alpha})`;
            this.ctx.lineWidth = hasError ? lineWidth + 1 : lineWidth;
            
            this.ctx.beginPath();
            this.ctx.moveTo(
                startPoint.x * this.canvas.width, 
                startPoint.y * this.canvas.height
            );
            this.ctx.lineTo(
                endPoint.x * this.canvas.width, 
                endPoint.y * this.canvas.height
            );
            this.ctx.stroke();
        });
        
        // Draw joints
        landmarks.forEach((landmark, index) => {
            if (!landmark || landmark.visibility < minVisibility) return;
            
            const hasError = highlightErrors && this._isErrorLandmark(index);
            const alpha = Math.min(landmark.visibility, 1);
            
            this.ctx.fillStyle = hasError 
                ? `rgba(239, 68, 68, ${alpha})` 
                : `rgba(16, 185, 129, ${alpha})`;
            
            const radius = hasError ? 6 : 4 + (landmark.visibility * 2);
            
            this.ctx.beginPath();
            this.ctx.arc(
                landmark.x * this.canvas.width, 
                landmark.y * this.canvas.height, 
                radius, 
                0, 
                2 * Math.PI
            );
            this.ctx.fill();
            
            // Draw error indicator
            if (hasError) {
                this.ctx.strokeStyle = 'white';
                this.ctx.lineWidth = 2;
                this.ctx.beginPath();
                this.ctx.arc(
                    landmark.x * this.canvas.width, 
                    landmark.y * this.canvas.height, 
                    radius + 3, 
                    0, 
                    2 * Math.PI
                );
                this.ctx.stroke();
            }
        });
    }
    
    /**
     * Check if joint is involved in an error
     * @private
     */
    _isErrorJoint(start, end) {
        const jointMap = {
            11: ['leftShoulder', 'leftHip'],
            12: ['rightShoulder', 'rightHip'],
            13: ['leftShoulder', 'leftElbow'],
            14: ['rightShoulder', 'rightElbow'],
            15: ['leftElbow'],
            16: ['rightElbow'],
            23: ['leftHip', 'leftShoulder'],
            24: ['rightHip', 'rightShoulder'],
            25: ['leftHip', 'leftKnee'],
            26: ['rightHip', 'rightKnee'],
            27: ['leftKnee', 'leftAnkle'],
            28: ['rightKnee', 'rightAnkle']
        };
        
        const startJoints = jointMap[start] || [];
        const endJoints = jointMap[end] || [];
        const allJoints = [...startJoints, ...endJoints];
        
        return this.errors.some(error => 
            allJoints.some(joint => error.joint.toLowerCase().includes(joint.toLowerCase()))
        );
    }
    
    /**
     * Check if landmark is involved in an error
     * @private
     */
    _isErrorLandmark(index) {
        const landmarkMap = {
            11: ['leftShoulder', 'leftHip'],
            12: ['rightShoulder', 'rightHip'],
            13: ['leftElbow', 'leftShoulder'],
            14: ['rightElbow', 'rightShoulder'],
            15: ['leftElbow'],
            16: ['rightElbow'],
            23: ['leftHip', 'leftKnee'],
            24: ['rightHip', 'rightKnee'],
            25: ['leftKnee', 'leftHip'],
            26: ['rightKnee', 'rightHip'],
            27: ['leftKnee', 'leftAnkle'],
            28: ['rightKnee', 'rightAnkle']
        };
        
        const joints = landmarkMap[index] || [];
        
        return this.errors.some(error => 
            joints.some(joint => error.joint.toLowerCase().includes(joint.toLowerCase()))
        );
    }
    
    /**
     * Draw angle indicators
     * @param {Array} landmarks - Pose landmarks
     * @param {Object} angles - Calculated angles
     */
    drawAngleIndicators(landmarks, angles) {
        if (!this.ctx || !landmarks || !angles) return;
        
        const anglePositions = {
            leftElbow: [11, 13, 15],
            rightElbow: [12, 14, 16],
            leftKnee: [23, 25, 27],
            rightKnee: [24, 26, 28],
            leftShoulder: [13, 11, 23],
            rightShoulder: [14, 12, 24],
            leftHip: [11, 23, 25],
            rightHip: [12, 24, 26]
        };
        
        for (const [joint, [a, b, c]] of Object.entries(anglePositions)) {
            const angle = angles[joint];
            if (angle === null || angle === undefined) continue;
            
            const pointB = landmarks[b];
            if (!pointB || pointB.visibility < 0.5) continue;
            
            const hasError = this.errors.some(e => e.joint === joint);
            
            // Draw angle arc
            this._drawAngleArc(pointB, angle, hasError);
            
            // Draw angle text
            this._drawAngleText(pointB, angle, hasError);
        }
    }
    
    /**
     * Draw angle arc
     * @private
     */
    _drawAngleArc(point, angle, hasError) {
        const x = point.x * this.canvas.width;
        const y = point.y * this.canvas.height;
        const radius = 30;
        
        this.ctx.strokeStyle = hasError ? '#ef4444' : '#10b981';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(x, y, radius, 0, (angle / 180) * Math.PI);
        this.ctx.stroke();
    }
    
    /**
     * Draw angle text
     * @private
     */
    _drawAngleText(point, angle, hasError) {
        const x = point.x * this.canvas.width;
        const y = point.y * this.canvas.height;
        
        this.ctx.fillStyle = hasError ? '#ef4444' : '#10b981';
        this.ctx.font = 'bold 14px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(`${Math.round(angle)}°`, x, y - 40);
    }
    
    /**
     * Clear canvas
     */
    clear() {
        if (this.ctx) {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }
    
    /**
     * Draw comparison overlay
     * Shows both target and detected poses
     */
    drawComparison() {
        if (!this.ctx || !this.targetPose || !this.detectedPose) return;
        
        this.clear();
        
        // Draw target pose in green (semi-transparent)
        this.ctx.globalAlpha = 0.3;
        this.drawSkeleton(this.targetPose.landmarks, { 
            color: '#10b981', 
            lineWidth: 2 
        });
        
        // Draw detected pose in red/green based on errors
        this.ctx.globalAlpha = 1.0;
        this.drawSkeleton(this.detectedPose, { 
            color: this.errors.length > 0 ? '#ef4444' : '#10b981',
            lineWidth: 3,
            highlightErrors: true
        });
    }
    
    /**
     * Resize canvas to match video dimensions
     * @param {number} width - Canvas width
     * @param {number} height - Canvas height
     */
    resize(width, height) {
        if (this.canvas) {
            this.canvas.width = width;
            this.canvas.height = height;
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PoseComparisonCanvas;
}

// Make globally accessible
window.PoseComparisonCanvas = PoseComparisonCanvas;
