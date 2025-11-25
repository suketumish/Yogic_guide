/**
 * Simple MediaPipe Pose Detector for Surya Namaskar
 * Detects poses, compares with reference angles, gives feedback in Hindi+English
 */

class SimplePoseDetector {
    constructor() {
        this.video = null;
        this.canvas = null;
        this.ctx = null;
        this.pose = null;
        this.camera = null;
        
        this.currentPoseIndex = 0;
        this.isActive = false;
        this.isPaused = false;
        
        // Pose sequences for Surya Namaskar with instructor guidance
        this.poses = [
            {
                name: 'Pranamasana (Prayer Pose)',
                nameHindi: 'प्रणामासन',
                shortName: 'Prayer Pose | प्रणामासन',
                instruction: 'Stand with palms together at chest | छाती पर हाथ जोड़कर खड़े हों',
                detailedGuidance: {
                    hindi: 'प्रणामासन। पहला आसन। सीधे खड़े हो जाएं। दोनों हाथ छाती के सामने जोड़ें। आंखें बंद करें। गहरी सांस लें।',
                    english: 'Pranamasana. First pose. Stand straight. Join both palms at chest. Close your eyes. Take a deep breath.'
                },
                breathing: {
                    hindi: 'सांस अंदर लें। सांस बाहर छोड़ें।',
                    english: 'Breathe in. Breathe out.'
                },
                holdTime: 10,
                referenceAngles: {
                    leftElbow: 90,
                    rightElbow: 90,
                    leftKnee: 175,
                    rightKnee: 175,
                    leftShoulder: 45,
                    rightShoulder: 45
                },
                tolerance: 15
            },
            {
                name: 'Hasta Uttanasana (Raised Arms)',
                nameHindi: 'हस्त उत्तानासन',
                shortName: 'Raised Arms | हस्त उत्तानासन',
                instruction: 'Raise arms overhead, arch back | हाथ ऊपर उठाएं, पीछे झुकें',
                detailedGuidance: {
                    hindi: 'हस्त उत्तानासन। दूसरा आसन। सांस अंदर लेते हुए दोनों हाथ ऊपर उठाएं। हथेलियां आपस में जोड़ें। पीछे की ओर झुकें। ऊपर देखें।',
                    english: 'Hasta Uttanasana. Second pose. Inhale and raise both arms up. Join palms together. Arch back gently. Look up.'
                },
                breathing: {
                    hindi: 'सांस अंदर लें।',
                    english: 'Breathe in.'
                },
                holdTime: 10,
                referenceAngles: {
                    leftShoulder: 180,
                    rightShoulder: 180,
                    leftElbow: 180,
                    rightElbow: 180,
                    leftKnee: 175,
                    rightKnee: 175
                },
                tolerance: 15
            },
            {
                name: 'Hasta Padasana (Forward Bend)',
                nameHindi: 'हस्त पादासन',
                shortName: 'Forward Bend | हस्त पादासन',
                instruction: 'Bend forward, touch the ground | आगे झुकें, जमीन छुएं',
                detailedGuidance: {
                    hindi: 'हस्त पादासन। तीसरा आसन। सांस बाहर छोड़ते हुए आगे की ओर झुकें। हाथों से पैरों के पास जमीन छुएं। घुटने सीधे रखें।',
                    english: 'Hasta Padasana. Third pose. Exhale and bend forward. Touch the ground near your feet. Keep knees straight.'
                },
                breathing: {
                    hindi: 'सांस बाहर छोड़ें।',
                    english: 'Breathe out.'
                },
                holdTime: 10,
                referenceAngles: {
                    leftKnee: 170,
                    rightKnee: 170,
                    leftHip: 70,
                    rightHip: 70
                },
                tolerance: 20
            },
            {
                name: 'Ashwa Sanchalanasana (Lunge)',
                nameHindi: 'अश्व संचालनासन',
                shortName: 'Lunge Pose | अश्व संचालनासन',
                instruction: 'Right leg back, left knee bent | दायां पैर पीछे, बायां घुटना मुड़ा',
                detailedGuidance: {
                    hindi: 'अश्व संचालनासन। चौथा आसन। सांस अंदर लेते हुए दायां पैर पीछे ले जाएं। बायां घुटना मोड़ें। ऊपर देखें। छाती खोलें।',
                    english: 'Ashwa Sanchalanasana. Fourth pose. Inhale and take right leg back. Bend left knee. Look up. Open your chest.'
                },
                breathing: {
                    hindi: 'सांस अंदर लें।',
                    english: 'Breathe in.'
                },
                holdTime: 10,
                referenceAngles: {
                    leftKnee: 90,
                    rightKnee: 175,
                    leftHip: 90,
                    rightHip: 170
                },
                tolerance: 15
            },
            {
                name: 'Dandasana (Plank)',
                nameHindi: 'दंडासन',
                shortName: 'Plank Pose | दंडासन',
                instruction: 'Straight body like a plank | शरीर सीधा तख्ते की तरह',
                detailedGuidance: {
                    hindi: 'दंडासन। पांचवां आसन। सांस रोकें। बायां पैर भी पीछे ले जाएं। शरीर को सीधा रखें। तख्ते की तरह।',
                    english: 'Dandasana. Fifth pose. Hold breath. Take left leg back too. Keep body straight. Like a plank.'
                },
                breathing: {
                    hindi: 'सांस रोकें।',
                    english: 'Hold breath.'
                },
                holdTime: 10,
                referenceAngles: {
                    leftElbow: 180,
                    rightElbow: 180,
                    leftKnee: 175,
                    rightKnee: 175,
                    leftShoulder: 90,
                    rightShoulder: 90
                },
                tolerance: 15
            },
            {
                name: 'Ashtanga Namaskara (Eight Points)',
                nameHindi: 'अष्टांग नमस्कार',
                shortName: 'Eight Points | अष्टांग नमस्कार',
                instruction: 'Knees, chest, chin on ground | घुटने, छाती, ठोड़ी जमीन पर',
                detailedGuidance: {
                    hindi: 'अष्टांग नमस्कार। छठा आसन। सांस बाहर छोड़ें। घुटने नीचे लाएं। छाती नीचे लाएं। ठोड़ी जमीन पर लगाएं। आठ अंग जमीन पर।',
                    english: 'Ashtanga Namaskara. Sixth pose. Exhale. Lower knees down. Lower chest down. Touch chin to ground. Eight points touching.'
                },
                breathing: {
                    hindi: 'सांस बाहर छोड़ें।',
                    english: 'Breathe out.'
                },
                holdTime: 10,
                referenceAngles: {
                    leftElbow: 90,
                    rightElbow: 90,
                    leftKnee: 90,
                    rightKnee: 90
                },
                tolerance: 20
            },
            {
                name: 'Bhujangasana (Cobra)',
                nameHindi: 'भुजंगासन',
                shortName: 'Cobra Pose | भुजंगासन',
                instruction: 'Lift chest, look up | छाती उठाएं, ऊपर देखें',
                detailedGuidance: {
                    hindi: 'भुजंगासन। सातवां आसन। सांस अंदर लेते हुए आगे की ओर खिसकें। छाती ऊपर उठाएं। कोहनी मोड़ें। ऊपर देखें। सांप की तरह।',
                    english: 'Bhujangasana. Seventh pose. Inhale and slide forward. Lift chest up. Bend elbows. Look up. Like a cobra.'
                },
                breathing: {
                    hindi: 'सांस अंदर लें।',
                    english: 'Breathe in.'
                },
                holdTime: 10,
                referenceAngles: {
                    leftElbow: 140,
                    rightElbow: 140,
                    leftKnee: 175,
                    rightKnee: 175
                },
                tolerance: 15
            },
            {
                name: 'Adho Mukha Svanasana (Downward Dog)',
                nameHindi: 'अधो मुख श्वानासन',
                shortName: 'Downward Dog | अधो मुख श्वानासन',
                instruction: 'Hips up, inverted V shape | कूल्हे ऊपर, उल्टा V आकार',
                detailedGuidance: {
                    hindi: 'अधो मुख श्वानासन। आठवां आसन। सांस बाहर छोड़ते हुए कूल्हे ऊपर उठाएं। उल्टा V बनाएं। एड़ियां जमीन की ओर। सिर नीचे।',
                    english: 'Adho Mukha Svanasana. Eighth pose. Exhale and lift hips up. Form inverted V. Heels towards ground. Head down.'
                },
                breathing: {
                    hindi: 'सांस बाहर छोड़ें।',
                    english: 'Breathe out.'
                },
                holdTime: 10,
                referenceAngles: {
                    leftKnee: 175,
                    rightKnee: 175,
                    leftShoulder: 60,
                    rightShoulder: 60,
                    leftHip: 45,
                    rightHip: 45
                },
                tolerance: 20
            },
            {
                name: 'Ashwa Sanchalanasana (Lunge)',
                nameHindi: 'अश्व संचालनासन',
                shortName: 'Lunge Pose | अश्व संचालनासन',
                instruction: 'Right foot forward | दायां पैर आगे',
                detailedGuidance: {
                    hindi: 'अश्व संचालनासन। नौवां आसन। सांस अंदर लेते हुए दायां पैर आगे लाएं। बायां पैर पीछे। ऊपर देखें।',
                    english: 'Ashwa Sanchalanasana. Ninth pose. Inhale and bring right foot forward. Left leg back. Look up.'
                },
                breathing: {
                    hindi: 'सांस अंदर लें।',
                    english: 'Breathe in.'
                },
                holdTime: 10,
                referenceAngles: {
                    leftKnee: 90,
                    rightKnee: 175,
                    leftHip: 90,
                    rightHip: 170
                },
                tolerance: 15
            },
            {
                name: 'Hasta Padasana (Forward Bend)',
                nameHindi: 'हस्त पादासन',
                shortName: 'Forward Bend | हस्त पादासन',
                instruction: 'Bend forward again | फिर से आगे झुकें',
                detailedGuidance: {
                    hindi: 'हस्त पादासन। दसवां आसन। सांस बाहर छोड़ते हुए बायां पैर भी आगे लाएं। आगे झुकें। हाथ जमीन पर।',
                    english: 'Hasta Padasana. Tenth pose. Exhale and bring left foot forward too. Bend forward. Hands on ground.'
                },
                breathing: {
                    hindi: 'सांस बाहर छोड़ें।',
                    english: 'Breathe out.'
                },
                holdTime: 10,
                referenceAngles: {
                    leftKnee: 170,
                    rightKnee: 170,
                    leftHip: 70,
                    rightHip: 70
                },
                tolerance: 20
            },
            {
                name: 'Hasta Uttanasana (Raised Arms)',
                nameHindi: 'हस्त उत्तानासन',
                shortName: 'Raised Arms | हस्त उत्तानासन',
                instruction: 'Rise up, arms overhead | उठें, हाथ ऊपर',
                detailedGuidance: {
                    hindi: 'हस्त उत्तानासन। ग्यारहवां आसन। सांस अंदर लेते हुए ऊपर उठें। हाथ ऊपर। पीछे झुकें। ऊपर देखें।',
                    english: 'Hasta Uttanasana. Eleventh pose. Inhale and rise up. Arms overhead. Arch back. Look up.'
                },
                breathing: {
                    hindi: 'सांस अंदर लें।',
                    english: 'Breathe in.'
                },
                holdTime: 10,
                referenceAngles: {
                    leftShoulder: 180,
                    rightShoulder: 180,
                    leftElbow: 180,
                    rightElbow: 180
                },
                tolerance: 15
            },
            {
                name: 'Tadasana (Mountain Pose)',
                nameHindi: 'ताड़ासन',
                shortName: 'Mountain Pose | ताड़ासन',
                instruction: 'Return to standing | खड़े होकर वापस आएं',
                detailedGuidance: {
                    hindi: 'ताड़ासन। बारहवां आसन। सांस बाहर छोड़ते हुए सीधे खड़े हो जाएं। हाथ नीचे लाएं। शांत हो जाएं। एक चक्र पूरा हुआ।',
                    english: 'Tadasana. Twelfth pose. Exhale and stand straight. Lower arms down. Relax. One cycle complete.'
                },
                breathing: {
                    hindi: 'सांस बाहर छोड़ें।',
                    english: 'Breathe out.'
                },
                holdTime: 10,
                referenceAngles: {
                    leftElbow: 180,
                    rightElbow: 180,
                    leftKnee: 175,
                    rightKnee: 175
                },
                tolerance: 15
            }
        ];
        
        this.holdTimer = 0;
        this.holdInterval = null;
        this.correctFrames = 0;
        this.requiredCorrectFrames = 3; // Need 3 consecutive correct frames
        this.lastVoiceFeedback = null; // For throttling voice feedback
        this.voicesLoaded = false; // Track if voices are loaded
    }
    
    loadVoices() {
        // Load available voices for Indian English
        if ('speechSynthesis' in window) {
            const loadVoicesHandler = () => {
                const voices = window.speechSynthesis.getVoices();
                console.log('📢 Available voices:', voices.length);
                
                // Log Indian English voices
                const indianVoices = voices.filter(voice => 
                    voice.lang === 'en-IN' || 
                    voice.name.includes('Indian') ||
                    voice.name.includes('India')
                );
                
                if (indianVoices.length > 0) {
                    console.log('✅ Indian English voices found:');
                    indianVoices.forEach(voice => {
                        console.log(`  - ${voice.name} (${voice.lang})`);
                    });
                } else {
                    console.log('⚠️ No Indian English voice found, will use slower en-US');
                }
                
                this.voicesLoaded = true;
            };
            
            // Load voices
            if (window.speechSynthesis.getVoices().length > 0) {
                loadVoicesHandler();
            } else {
                window.speechSynthesis.onvoiceschanged = loadVoicesHandler;
            }
        }
    }
    
    async initialize() {
        console.log('🚀 Initializing Simple Pose Detector...');
        
        // Load voices for Indian English accent
        this.loadVoices();
        
        this.video = document.getElementById('videoFeed');
        this.canvas = document.getElementById('poseCanvas');
        
        if (!this.video || !this.canvas) {
            console.error('❌ Video or canvas element not found');
            return false;
        }
        
        this.ctx = this.canvas.getContext('2d');
        
        try {
            // Initialize MediaPipe Pose
            this.pose = new Pose({
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
            });
            
            this.pose.setOptions({
                modelComplexity: 1,
                smoothLandmarks: true,
                minDetectionConfidence: 0.5,
                minTrackingConfidence: 0.5
            });
            
            this.pose.onResults((results) => this.onPoseResults(results));
            
            // Get camera
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480, facingMode: 'user' }
            });
            
            this.video.srcObject = stream;
            await this.video.play();
            
            this.canvas.width = this.video.videoWidth || 640;
            this.canvas.height = this.video.videoHeight || 480;
            
            // Start detection loop
            this.detectLoop();
            
            console.log('✅ Pose detector initialized');
            return true;
            
        } catch (error) {
            console.error('❌ Failed to initialize:', error);
            this.showError('Camera access denied. Please allow camera permission.');
            return false;
        }
    }
    
    async detectLoop() {
        if (this.video && this.video.readyState === 4) {
            await this.pose.send({ image: this.video });
        }
        requestAnimationFrame(() => this.detectLoop());
    }
    
    onPoseResults(results) {
        if (!this.ctx || !this.canvas) return;
        
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        if (results.poseLandmarks) {
            // Draw skeleton
            this.drawSkeleton(results.poseLandmarks);
            
            // Check pose if session is active
            if (this.isActive && !this.isPaused) {
                this.checkPose(results.poseLandmarks);
            }
        }
    }
    
    drawSkeleton(landmarks) {
        const connections = [
            [11, 12], [11, 13], [13, 15], [12, 14], [14, 16],
            [11, 23], [12, 24], [23, 24], [23, 25], [25, 27],
            [24, 26], [26, 28], [27, 31], [28, 32]
        ];
        
        // Draw connections
        this.ctx.strokeStyle = '#10b981';
        this.ctx.lineWidth = 3;
        
        connections.forEach(([start, end]) => {
            const startPoint = landmarks[start];
            const endPoint = landmarks[end];
            
            if (startPoint && endPoint) {
                this.ctx.beginPath();
                this.ctx.moveTo(startPoint.x * this.canvas.width, startPoint.y * this.canvas.height);
                this.ctx.lineTo(endPoint.x * this.canvas.width, endPoint.y * this.canvas.height);
                this.ctx.stroke();
            }
        });
        
        // Draw joints
        this.ctx.fillStyle = '#10b981';
        landmarks.forEach((landmark) => {
            if (landmark) {
                this.ctx.beginPath();
                this.ctx.arc(
                    landmark.x * this.canvas.width,
                    landmark.y * this.canvas.height,
                    5, 0, 2 * Math.PI
                );
                this.ctx.fill();
            }
        });
        
        // Draw angle indicators if session is active
        if (this.isActive && !this.isPaused) {
            this.drawAngleIndicators(landmarks);
        }
    }
    
    drawAngleIndicators(landmarks) {
        const currentPose = this.poses[this.currentPoseIndex];
        if (!currentPose) return;
        
        const angles = this.calculateAngles(landmarks);
        const refAngles = currentPose.referenceAngles;
        const tolerance = currentPose.tolerance;
        
        // Define joint positions for angle display
        const anglePositions = {
            leftElbow: { joint: 13, label: 'L Elbow' },
            rightElbow: { joint: 14, label: 'R Elbow' },
            leftKnee: { joint: 25, label: 'L Knee' },
            rightKnee: { joint: 26, label: 'R Knee' },
            leftShoulder: { joint: 11, label: 'L Shoulder' },
            rightShoulder: { joint: 12, label: 'R Shoulder' },
            leftHip: { joint: 23, label: 'L Hip' },
            rightHip: { joint: 24, label: 'R Hip' },
            leftAnkle: { joint: 27, label: 'L Ankle' },
            rightAnkle: { joint: 28, label: 'R Ankle' }
        };
        
        // Draw angle values at joint positions
        for (const [jointName, refAngle] of Object.entries(refAngles)) {
            const currentAngle = angles[jointName];
            if (currentAngle === null) continue;
            
            const position = anglePositions[jointName];
            if (!position) continue;
            
            const landmark = landmarks[position.joint];
            if (!landmark) continue;
            
            const x = landmark.x * this.canvas.width;
            const y = landmark.y * this.canvas.height;
            
            const diff = Math.abs(currentAngle - refAngle);
            const isCorrect = diff <= tolerance;
            
            // Draw background circle
            this.ctx.fillStyle = isCorrect ? 'rgba(16, 185, 129, 0.8)' : 'rgba(239, 68, 68, 0.8)';
            this.ctx.beginPath();
            this.ctx.arc(x, y, 25, 0, 2 * Math.PI);
            this.ctx.fill();
            
            // Draw angle text
            this.ctx.fillStyle = 'white';
            this.ctx.font = 'bold 12px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(Math.round(currentAngle) + '°', x, y);
            
            // Draw label below
            this.ctx.fillStyle = isCorrect ? '#10b981' : '#ef4444';
            this.ctx.font = 'bold 10px Arial';
            this.ctx.fillText(position.label, x, y + 35);
            
            // Draw target angle
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            this.ctx.font = '9px Arial';
            this.ctx.fillText(`Target: ${refAngle}°`, x, y + 48);
        }
    }
    
    checkPose(landmarks) {
        const currentPose = this.poses[this.currentPoseIndex];
        if (!currentPose) return;
        
        // Calculate current angles
        const angles = this.calculateAngles(landmarks);
        
        // Compare with reference angles
        const { isCorrect, accuracy, feedback, detailedAngles } = this.compareAngles(angles, currentPose);
        
        // Update UI
        this.updateFeedback(isCorrect, accuracy, feedback, currentPose, detailedAngles);
        
        // Track correct frames
        if (isCorrect) {
            this.correctFrames++;
            
            if (this.correctFrames >= this.requiredCorrectFrames) {
                // Pose is correct and stable
                this.canvas.style.border = '5px solid #10b981';
                this.showSuccess();
            } else {
                // Getting close
                this.canvas.style.border = '5px solid #3b82f6';
            }
        } else {
            this.correctFrames = 0;
            
            // Provide voice feedback for major corrections (throttled)
            if (accuracy < 60 && !this.lastVoiceFeedback) {
                this.lastVoiceFeedback = Date.now();
                if (feedback.length > 0) {
                    const topCorrection = feedback[0];
                    this.speakBilingual(topCorrection.hindi, topCorrection.english);
                }
            } else if (this.lastVoiceFeedback && Date.now() - this.lastVoiceFeedback > 8000) {
                // Reset after 8 seconds
                this.lastVoiceFeedback = null;
            }
            
            this.canvas.style.border = '5px solid #ef4444';
        }
    }
    
    calculateAngles(landmarks) {
        return {
            leftElbow: this.calculateAngle(landmarks[11], landmarks[13], landmarks[15]),
            rightElbow: this.calculateAngle(landmarks[12], landmarks[14], landmarks[16]),
            leftKnee: this.calculateAngle(landmarks[23], landmarks[25], landmarks[27]),
            rightKnee: this.calculateAngle(landmarks[24], landmarks[26], landmarks[28]),
            leftShoulder: this.calculateAngle(landmarks[13], landmarks[11], landmarks[23]),
            rightShoulder: this.calculateAngle(landmarks[14], landmarks[12], landmarks[24]),
            leftHip: this.calculateAngle(landmarks[11], landmarks[23], landmarks[25]),
            rightHip: this.calculateAngle(landmarks[12], landmarks[24], landmarks[26]),
            leftAnkle: this.calculateAngle(landmarks[25], landmarks[27], landmarks[31]),
            rightAnkle: this.calculateAngle(landmarks[26], landmarks[28], landmarks[32])
        };
    }
    
    calculateAngle(a, b, c) {
        if (!a || !b || !c) return null;
        
        const radians = Math.atan2(c.y - b.y, c.x - b.x) - Math.atan2(a.y - b.y, a.x - b.x);
        let angle = Math.abs(radians * 180.0 / Math.PI);
        
        if (angle > 180.0) {
            angle = 360 - angle;
        }
        
        return angle;
    }
    
    compareAngles(currentAngles, pose) {
        const refAngles = pose.referenceAngles;
        const tolerance = pose.tolerance;
        
        let correctCount = 0;
        let totalCount = 0;
        const feedback = [];
        const detailedAngles = [];
        
        for (const [joint, refAngle] of Object.entries(refAngles)) {
            const currentAngle = currentAngles[joint];
            
            if (currentAngle === null) continue;
            
            totalCount++;
            const diff = Math.abs(currentAngle - refAngle);
            
            // Store detailed angle info
            detailedAngles.push({
                joint: joint,
                current: Math.round(currentAngle),
                target: refAngle,
                diff: Math.round(diff),
                isCorrect: diff <= tolerance
            });
            
            if (diff <= tolerance) {
                correctCount++;
            } else {
                const hindiName = this.getJointNameHindi(joint);
                const englishName = this.getJointNameEnglish(joint);
                
                let adjustment, adjustmentEng;
                if (currentAngle > refAngle) {
                    adjustment = 'कम करें';
                    adjustmentEng = 'decrease';
                } else {
                    adjustment = 'बढ़ाएं';
                    adjustmentEng = 'increase';
                }
                
                feedback.push({
                    hindi: `${hindiName}: ${adjustment} (${Math.round(diff)}°)`,
                    english: `${englishName}: ${adjustmentEng} (${Math.round(diff)}°)`,
                    text: `${hindiName}: ${adjustment} (${Math.round(diff)}°)`
                });
            }
        }
        
        const accuracy = totalCount > 0 ? Math.round((correctCount / totalCount) * 100) : 0;
        const isCorrect = accuracy >= 80;
        
        return { isCorrect, accuracy, feedback, detailedAngles };
    }
    
    getJointNameHindi(joint) {
        const names = {
            leftElbow: 'बायां कोहनी',
            rightElbow: 'दायां कोहनी',
            leftKnee: 'बायां घुटना',
            rightKnee: 'दायां घुटना',
            leftShoulder: 'बायां कंधा',
            rightShoulder: 'दायां कंधा',
            leftHip: 'बायां कूल्हा',
            rightHip: 'दायां कूल्हा',
            leftAnkle: 'बायां टखना',
            rightAnkle: 'दायां टखना'
        };
        return names[joint] || joint;
    }
    
    getJointNameEnglish(joint) {
        const names = {
            leftElbow: 'Left Elbow',
            rightElbow: 'Right Elbow',
            leftKnee: 'Left Knee',
            rightKnee: 'Right Knee',
            leftShoulder: 'Left Shoulder',
            rightShoulder: 'Right Shoulder',
            leftHip: 'Left Hip',
            rightHip: 'Right Hip',
            leftAnkle: 'Left Ankle',
            rightAnkle: 'Right Ankle'
        };
        return names[joint] || joint;
    }
    
    updateFeedback(isCorrect, accuracy, feedback, pose, detailedAngles) {
        const feedbackEl = document.getElementById('feedback');
        if (!feedbackEl) return;
        
        if (isCorrect) {
            if (this.correctFrames >= this.requiredCorrectFrames) {
                feedbackEl.textContent = `✅ बहुत बढ़िया! Perfect! (${accuracy}%)`;
            } else {
                feedbackEl.textContent = `⏳ Hold steady... ${this.correctFrames}/${this.requiredCorrectFrames} (${accuracy}%)`;
            }
            feedbackEl.className = 'mt-4 text-center text-lg font-semibold text-green-600';
        } else {
            const topFeedback = feedback.slice(0, 2).map(f => f.text).join(', ');
            feedbackEl.textContent = `⚠️ ${topFeedback} (${accuracy}%)`;
            feedbackEl.className = 'mt-4 text-center text-lg font-semibold text-orange-600';
        }
        
        // Update angle display with detailed comparison
        this.updateAngleDisplay(accuracy, feedback, pose, detailedAngles);
    }
    
    updateAngleDisplay(accuracy, feedback, pose, detailedAngles) {
        const angleEl = document.getElementById('angleDisplay');
        if (!angleEl) return;
        
        let displayText = `📊 Accuracy: ${accuracy}%\n`;
        displayText += `🎯 ${pose.nameHindi}\n`;
        displayText += `⏱️ Time: ${this.holdTimer}s\n`;
        displayText += `━━━━━━━━━━━━━━━━\n\n`;
        
        if (detailedAngles && detailedAngles.length > 0) {
            displayText += '📐 Angle Details:\n';
            detailedAngles.forEach((angle) => {
                const status = angle.isCorrect ? '✅' : '❌';
                const hindiName = this.getJointNameHindi(angle.joint);
                displayText += `${status} ${hindiName}\n`;
                displayText += `   Current: ${angle.current}°\n`;
                displayText += `   Target: ${angle.target}°\n`;
                displayText += `   Diff: ${angle.diff}°\n\n`;
            });
        }
        
        if (feedback.length === 0) {
            displayText += '✅ सभी angles सही हैं!\n';
            displayText += '✅ All angles perfect!\n';
        } else {
            displayText += '⚠️ सुधार चाहिए:\n';
            feedback.forEach((item, index) => {
                displayText += `${index + 1}. ${item.hindi}\n`;
                displayText += `   ${item.english}\n`;
            });
        }
        
        angleEl.textContent = displayText;
    }
    
    showSuccess() {
        const feedbackEl = document.getElementById('feedback');
        if (feedbackEl) {
            feedbackEl.textContent = '🎉 बहुत बढ़िया! Perfect! अगले pose के लिए तैयार!';
            feedbackEl.className = 'mt-4 text-center text-lg font-semibold text-green-600 animate-pulse';
        }
        
        // Speak success in both languages
        this.speakBilingual('बहुत बढ़िया! बिल्कुल सही!', 'Perfect! Excellent!');
    }
    
    speak(text, lang = 'hi-IN') {
        if ('speechSynthesis' in window) {
            // Cancel any ongoing speech
            window.speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.85;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;
            utterance.lang = lang;
            
            window.speechSynthesis.speak(utterance);
        }
    }
    
    speakBilingual(hindiText, englishText) {
        // Speak Hindi first, then English with Indian accent
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            
            // Hindi part
            const hindiUtterance = new SpeechSynthesisUtterance(hindiText);
            hindiUtterance.rate = 0.85;
            hindiUtterance.pitch = 1.0;
            hindiUtterance.lang = 'hi-IN';
            
            // English part with Indian accent
            const englishUtterance = new SpeechSynthesisUtterance(englishText);
            englishUtterance.rate = 0.75;  // Slower for Indian accent
            englishUtterance.pitch = 1.1;   // Slightly higher pitch
            englishUtterance.lang = 'en-IN'; // Indian English
            
            // Try to select Indian English voice if available
            const voices = window.speechSynthesis.getVoices();
            const indianVoice = voices.find(voice => 
                voice.lang === 'en-IN' || 
                voice.name.includes('Indian') ||
                voice.name.includes('India')
            );
            
            if (indianVoice) {
                englishUtterance.voice = indianVoice;
                console.log('Using Indian English voice:', indianVoice.name);
            } else {
                // Fallback: Use en-US but with slower rate for Indian accent feel
                englishUtterance.lang = 'en-US';
                englishUtterance.rate = 0.7; // Even slower
                console.log('Indian voice not found, using slower en-US');
            }
            
            // Speak Hindi first
            window.speechSynthesis.speak(hindiUtterance);
            
            // Then speak English after a short pause
            hindiUtterance.onend = () => {
                setTimeout(() => {
                    window.speechSynthesis.speak(englishUtterance);
                }, 400); // Slightly longer pause
            };
        }
    }
    
    showError(message) {
        const errorDiv = document.getElementById('cameraError');
        if (errorDiv) {
            errorDiv.style.display = 'flex';
            const errorText = errorDiv.querySelector('p');
            if (errorText) {
                errorText.textContent = message;
            }
        }
    }
    
    startSession() {
        this.isActive = true;
        this.currentPoseIndex = 0;
        
        // Welcome message like a yoga instructor
        this.speakBilingual(
            'नमस्ते। सूर्य नमस्कार शुरू करते हैं। बारह आसन हैं। तैयार हो जाएं।',
            'Namaste. Let us begin Surya Namaskar. Twelve poses. Get ready.'
        );
        
        // Load first pose after welcome
        setTimeout(() => {
            this.loadPose();
        }, 4000);
        
        console.log('✅ Session started');
    }
    
    loadPose() {
        const pose = this.poses[this.currentPoseIndex];
        if (!pose) {
            this.completeSession();
            return;
        }
        
        // Update UI - Show pose name prominently
        const poseNameEl = document.getElementById('poseName');
        if (poseNameEl) {
            poseNameEl.textContent = pose.shortName || `${pose.name} | ${pose.nameHindi}`;
        }
        
        const timerEl = document.getElementById('timer');
        if (timerEl) {
            timerEl.textContent = pose.holdTime;
        }
        
        // Update reference image
        const refImg = document.getElementById('poseReferenceImg');
        if (refImg) {
            refImg.src = `/static/Module_suryanamaskar/Surya-Namaskar-Pose-${this.currentPoseIndex + 1}.png`;
        }
        
        // Instructor-style guidance with detailed instructions
        this.speakInstructorGuidance(pose);
        
        // Reset
        this.correctFrames = 0;
        this.holdTimer = pose.holdTime;
        this.canvas.style.border = 'none';
        
        // Start hold timer
        if (this.holdInterval) clearInterval(this.holdInterval);
        
        this.holdInterval = setInterval(() => {
            if (this.isPaused) return;
            
            this.holdTimer--;
            if (timerEl) timerEl.textContent = this.holdTimer;
            
            // Give breathing reminder at halfway point
            if (this.holdTimer === Math.floor(pose.holdTime / 2) && pose.breathing) {
                this.speakBilingual(pose.breathing.hindi, pose.breathing.english);
            }
            
            if (this.holdTimer <= 0) {
                this.nextPose();
            }
        }, 1000);
    }
    
    speakInstructorGuidance(pose) {
        // Speak like a yoga instructor with detailed guidance
        if (pose.detailedGuidance) {
            // First announce the pose name clearly
            const poseName = `${pose.nameHindi}. ${pose.name}.`;
            this.speak(poseName, 'hi-IN');
            
            // Wait a moment, then give detailed instructions
            setTimeout(() => {
                this.speakBilingual(
                    pose.detailedGuidance.hindi,
                    pose.detailedGuidance.english
                );
            }, 2000);
        } else {
            // Fallback to simple instruction
            const instructions = pose.instruction.split('|');
            if (instructions.length === 2) {
                this.speakBilingual(instructions[1].trim(), instructions[0].trim());
            } else {
                this.speak(pose.instruction);
            }
        }
    }
    
    nextPose() {
        if (this.holdInterval) clearInterval(this.holdInterval);
        
        this.currentPoseIndex++;
        
        if (this.currentPoseIndex >= this.poses.length) {
            this.completeSession();
        } else {
            // Announce transition like an instructor
            const nextPose = this.poses[this.currentPoseIndex];
            const transitionMessage = {
                hindi: `बहुत अच्छा। अब ${nextPose.nameHindi}।`,
                english: `Very good. Now ${nextPose.name}.`
            };
            
            this.speakBilingual(transitionMessage.hindi, transitionMessage.english);
            setTimeout(() => this.loadPose(), 2500);
        }
    }
    
    completeSession() {
        this.isActive = false;
        if (this.holdInterval) clearInterval(this.holdInterval);
        
        // Completion message like a yoga instructor
        this.speakBilingual(
            'बहुत बढ़िया! सूर्य नमस्कार पूरा हुआ। आप बहुत अच्छा कर रहे हैं। नमस्ते।',
            'Excellent! Surya Namaskar complete. You are doing very well. Namaste.'
        );
        
        setTimeout(() => {
            window.location.href = '/dashboard';
        }, 5000);
    }
    
    pause() {
        this.isPaused = true;
    }
    
    resume() {
        this.isPaused = false;
    }
    
    stop() {
        this.isActive = false;
        this.isPaused = false;
        if (this.holdInterval) clearInterval(this.holdInterval);
    }
}

// Initialize globally
window.simplePoseDetector = new SimplePoseDetector();
