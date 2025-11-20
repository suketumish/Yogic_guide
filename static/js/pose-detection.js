// Full Pose Detection with MediaPipe Pose
let video, canvas, ctx;
let pose, camera;
let currentPoseIndex = 0;
let poseTimer = 5;
let holdTimer = 0;
let isSessionActive = false;
let isPaused = false;
let namasteDetected = false;
let currentModule = '';
let poseSequences = {};
let sessionId = null;
let posesCompleted = 0;
let totalAccuracy = 0;
let sessionStartTime = Date.now();

// Strict Pose Correction System
let poseCorrectionSystem = null;
let poseComparisonCanvas = null;

// Pose angle thresholds - adaptive based on pose complexity
const ANGLE_TOLERANCE = {
    strict: 10,    // For simple poses
    normal: 15,    // For moderate poses
    relaxed: 20    // For complex poses
};

// Minimum visibility threshold for landmarks
const MIN_VISIBILITY = 0.5;
const MIN_CONFIDENCE = 0.6;

// Pose stability tracking
let poseStabilityFrames = 0;
const STABILITY_THRESHOLD = 5; // Frames needed for stable pose

document.addEventListener('DOMContentLoaded', async () => {
    video = document.getElementById('videoFeed');
    canvas = document.getElementById('poseCanvas');
    ctx = canvas.getContext('2d');
    
    currentModule = window.location.pathname.split('/').pop();
    loadPoseSequences();
    
    // Initialize Strict Pose Correction System
    if (typeof StrictPoseCorrectionSystem !== 'undefined' && typeof voiceOver !== 'undefined') {
        poseCorrectionSystem = new StrictPoseCorrectionSystem(
            { pause: pauseSessionInternal, resume: resumeSessionInternal },
            voiceOver
        );
    }
    
    // Initialize Pose Comparison Canvas
    if (typeof PoseComparisonCanvas !== 'undefined') {
        poseComparisonCanvas = new PoseComparisonCanvas('poseCanvas');
    }
    
    // Initialize MediaPipe Pose
    await initMediaPipe();
    
    // Button handlers
    document.getElementById('pauseBtn')?.addEventListener('click', pauseSession);
    document.getElementById('stopBtn')?.addEventListener('click', stopSession);
});

async function initMediaPipe() {
    try {
        // Load MediaPipe Pose
        pose = new Pose({
            locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
        });
        
        pose.setOptions({
            modelComplexity: 2,  // Increased for better accuracy
            smoothLandmarks: true,
            enableSegmentation: false,
            smoothSegmentation: false,
            minDetectionConfidence: 0.7,  // Increased threshold
            minTrackingConfidence: 0.7    // Increased threshold
        });
        
        pose.onResults(onPoseResults);
        
        // Get camera access with better constraints
        console.log('Requesting camera access...');
        
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('Camera API not supported in this browser');
        }
        
        const constraints = {
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'user'
            },
            audio: false
        };
        
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        console.log('Camera access granted');
        
        video.srcObject = stream;
        video.setAttribute('playsinline', true); // Important for iOS
        video.setAttribute('autoplay', true);
        video.setAttribute('muted', true);
        
        await video.play(); // Explicitly start video
        
        video.onloadedmetadata = () => {
            console.log('Video metadata loaded');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            detectPoseContinuously();
            startNamasteDetection();
        };
        
        // Fallback if metadata doesn't load
        setTimeout(() => {
            if (video.readyState >= 2) {
                canvas.width = video.videoWidth || 640;
                canvas.height = video.videoHeight || 480;
                detectPoseContinuously();
                startNamasteDetection();
            }
        }, 1000);
        
    } catch (err) {
        console.error('Camera initialization failed:', err);
        let errorMessage = 'Camera access required. ';
        
        if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
            errorMessage += 'Please allow camera permissions in your browser settings.';
        } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
            errorMessage += 'No camera found. Please connect a camera.';
        } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
            errorMessage += 'Camera is already in use by another application.';
        } else if (err.name === 'OverconstrainedError') {
            errorMessage += 'Camera does not support required settings.';
        } else {
            errorMessage += err.message || 'Unknown error occurred.';
        }
        
        alert(errorMessage);
        console.error('Full error details:', err);
    }
}

async function detectPoseContinuously() {
    if (!isPaused && video.readyState === 4) {
        await pose.send({ image: video });
    }
    requestAnimationFrame(detectPoseContinuously);
}

function onPoseResults(results) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (results.poseLandmarks) {
        drawSkeleton(results.poseLandmarks);
        
        if (!namasteDetected) {
            checkNamasteGesture(results.poseLandmarks);
        } else if (isSessionActive && !isPaused) {
            validateCurrentPose(results.poseLandmarks);
        }
    }
}

function drawSkeleton(landmarks) {
    const connections = [
        [11, 12], [11, 13], [13, 15], [12, 14], [14, 16],
        [11, 23], [12, 24], [23, 24], [23, 25], [25, 27],
        [24, 26], [26, 28], [27, 29], [28, 30], [29, 31], [30, 32],
        [0, 1], [1, 2], [2, 3], [3, 7], [0, 4], [4, 5], [5, 6], [6, 8]  // Face landmarks
    ];
    
    // Draw connections with visibility check
    connections.forEach(([start, end]) => {
        const startPoint = landmarks[start];
        const endPoint = landmarks[end];
        
        if (startPoint.visibility > MIN_VISIBILITY && endPoint.visibility > MIN_VISIBILITY) {
            // Color based on visibility confidence
            const avgVisibility = (startPoint.visibility + endPoint.visibility) / 2;
            const alpha = Math.min(avgVisibility, 1);
            ctx.strokeStyle = `rgba(16, 185, 129, ${alpha})`;
            ctx.lineWidth = 3;
            
            ctx.beginPath();
            ctx.moveTo(startPoint.x * canvas.width, startPoint.y * canvas.height);
            ctx.lineTo(endPoint.x * canvas.width, endPoint.y * canvas.height);
            ctx.stroke();
        }
    });
    
    // Draw joints with visibility-based sizing
    landmarks.forEach((landmark, index) => {
        if (landmark.visibility > MIN_VISIBILITY) {
            const alpha = Math.min(landmark.visibility, 1);
            ctx.fillStyle = `rgba(16, 185, 129, ${alpha})`;
            const radius = 4 + (landmark.visibility * 2); // Larger for more visible points
            ctx.beginPath();
            ctx.arc(landmark.x * canvas.width, landmark.y * canvas.height, radius, 0, 2 * Math.PI);
            ctx.fill();
            
            // Draw landmark index for debugging (optional)
            if (landmark.visibility > 0.8) {
                ctx.fillStyle = 'white';
                ctx.font = '10px Arial';
                ctx.fillText(index, landmark.x * canvas.width + 8, landmark.y * canvas.height);
            }
        }
    });
}

function checkNamasteGesture(landmarks) {
    const leftWrist = landmarks[15];
    const rightWrist = landmarks[16];
    const nose = landmarks[0];
    
    const distance = Math.sqrt(
        Math.pow((leftWrist.x - rightWrist.x) * canvas.width, 2) +
        Math.pow((leftWrist.y - rightWrist.y) * canvas.height, 2)
    );
    
    const avgWristY = (leftWrist.y + rightWrist.y) / 2;
    const isNearChest = Math.abs(avgWristY - nose.y) < 0.3;
    
    if (distance < 100 && isNearChest) {
        namasteDetected = true;
        document.getElementById('feedback').textContent = '🙏 Namaste Detected!';
        document.getElementById('feedback').className = 'mt-4 text-center text-lg font-semibold text-green-600';
    }
}

async function startSession(moduleType) {
    try {
        const response = await fetch('/session/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ module_type: moduleType })
        });
        const data = await response.json();
        sessionId = data.session_id;
    } catch (err) {
        console.error('Failed to start session:', err);
    }
}

async function completeSession() {
    if (!sessionId) return;
    
    const avgAccuracy = posesCompleted > 0 ? totalAccuracy / posesCompleted : 0;
    
    try {
        await fetch('/session/complete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                duration: Math.floor((Date.now() - sessionStartTime) / 1000),
                poses_completed: posesCompleted,
                accuracy_score: Math.round(avgAccuracy),
                calories_burned: Math.round(posesCompleted * 2.5)
            })
        });
        
        window.location.href = '/session-complete';
    } catch (err) {
        console.error('Failed to complete session:', err);
        window.location.href = '/dashboard';
    }
}

function speak(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1;
        window.speechSynthesis.speak(utterance);
    }
}

function startNamasteDetection() {
    startSession(currentModule);
    speak('Please show Namaste gesture to begin');
    
    const countdown = setInterval(() => {
        document.getElementById('timer').textContent = poseTimer;
        
        if (namasteDetected || poseTimer <= 0) {
            clearInterval(countdown);
            speak('Starting your session');
            setTimeout(() => startPoseSequence(), 1000);
        }
        poseTimer--;
    }, 1000);
}

function startPoseSequence() {
    isSessionActive = true;
    currentPoseIndex = 0;
    loadCurrentPose();
}

function loadCurrentPose() {
    const sequence = poseSequences[currentModule];
    if (!sequence || currentPoseIndex >= sequence.length) {
        completeSession();
        return;
    }
    
    // Reset stability counter for new pose
    poseStabilityFrames = 0;
    
    const currentPose = sequence[currentPoseIndex];
    holdTimer = currentPose.holdDuration;
    
    // Update UI
    document.getElementById('poseName').textContent = currentPose.name;
    document.getElementById('timer').textContent = holdTimer;
    document.getElementById('benefits').innerHTML = currentPose.benefits.map(b => `<li>• ${b}</li>`).join('');
    document.getElementById('cautions').innerHTML = currentPose.cautions.map(c => `<li>⚠ ${c}</li>`).join('');
    
    // Update progress
    document.getElementById('poseProgress').textContent = `${currentPoseIndex + 1}/${sequence.length}`;
    const progressPercent = ((currentPoseIndex + 1) / sequence.length) * 100;
    document.getElementById('progressBar').style.width = `${progressPercent}%`;
    
    // Show next pose
    if (currentPoseIndex + 1 < sequence.length) {
        document.getElementById('nextPose').textContent = sequence[currentPoseIndex + 1].name;
    } else {
        document.getElementById('nextPose').textContent = 'Session Complete!';
    }
    
    speak(`${currentPose.name}. ${currentPose.instruction}`);
    
    const timerInterval = setInterval(() => {
        if (!isPaused && isSessionActive) {
            holdTimer--;
            document.getElementById('timer').textContent = holdTimer;
            
            if (holdTimer <= 0) {
                clearInterval(timerInterval);
                posesCompleted++;
                currentPoseIndex++;
                speak('Well done! Moving to next pose');
                setTimeout(() => loadCurrentPose(), 2000);
            }
        }
    }, 1000);
}

function validateCurrentPose(landmarks) {
    const sequence = poseSequences[currentModule];
    if (!sequence || currentPoseIndex >= sequence.length) return;
    
    const currentPose = sequence[currentPoseIndex];
    
    // Check if key landmarks are visible
    if (!checkLandmarkVisibility(landmarks, currentPose)) {
        document.getElementById('feedback').textContent = '⚠ Please position yourself fully in frame';
        document.getElementById('feedback').className = 'mt-4 text-center text-lg font-semibold text-yellow-600';
        poseStabilityFrames = 0;
        return;
    }
    
    const angles = calculateAngles(landmarks);
    const tolerance = currentPose.tolerance || ANGLE_TOLERANCE.normal;
    
    let correctAngles = 0;
    let totalAngles = 0;
    let feedback = [];
    let angleDisplay = '';
    
    for (const [joint, targetAngle] of Object.entries(currentPose.angles)) {
        const currentAngle = angles[joint];
        if (currentAngle === null) continue; // Skip if angle couldn't be calculated
        
        totalAngles++;
        const diff = Math.abs(currentAngle - targetAngle);
        const isCorrect = diff <= tolerance;
        
        if (isCorrect) correctAngles++;
        
        // Enhanced angle display with color coding
        const status = isCorrect ? '✓' : '✗';
        angleDisplay += `${status} ${joint}: ${Math.round(currentAngle)}° (target: ${targetAngle}° ±${tolerance}°)\n`;
        
        if (!isCorrect) {
            const adjustment = currentAngle > targetAngle ? 'decrease' : 'increase';
            feedback.push(`${joint.replace(/([A-Z])/g, ' $1').trim()} (${adjustment} by ${Math.round(diff)}°)`);
        }
    }
    
    // Calculate accuracy percentage
    const accuracy = totalAngles > 0 ? Math.round((correctAngles / totalAngles) * 100) : 0;
    const isCorrect = accuracy >= 85; // 85% threshold for "correct" pose
    
    // Display angles with accuracy
    document.getElementById('angleDisplay').textContent = angleDisplay + `\nAccuracy: ${accuracy}%`;
    
    // Pose stability check - require multiple consecutive correct frames
    if (isCorrect) {
        poseStabilityFrames++;
        
        if (poseStabilityFrames >= STABILITY_THRESHOLD) {
            ctx.strokeStyle = '#10b981';
            document.getElementById('feedback').textContent = `✓ Perfect form! (${accuracy}%)`;
            document.getElementById('feedback').className = 'mt-4 text-center text-lg font-semibold text-green-600';
            canvas.style.border = '3px solid #10b981';
            
            // Voice-over: Pose validated successfully (only once when threshold reached)
            if (poseStabilityFrames === STABILITY_THRESHOLD && typeof voiceOver !== 'undefined') {
                voiceOver.onPoseSuccess(currentPose.name || 'pose');
            }
        } else {
            document.getElementById('feedback').textContent = `⏳ Hold steady... ${poseStabilityFrames}/${STABILITY_THRESHOLD}`;
            document.getElementById('feedback').className = 'mt-4 text-center text-lg font-semibold text-blue-600';
            canvas.style.border = '3px solid #3b82f6';
        }
    } else {
        poseStabilityFrames = 0;
        ctx.strokeStyle = '#ef4444';
        
        // Prioritize top 2 adjustments
        const topFeedback = feedback.slice(0, 2);
        document.getElementById('feedback').textContent = `✗ Adjust: ${topFeedback.join(', ')} (${accuracy}%)`;
        document.getElementById('feedback').className = 'mt-4 text-center text-lg font-semibold text-red-600';
        canvas.style.border = '3px solid #ef4444';
        canvas.classList.add('blink-red');
        
        // Voice-over: Pose correction needed (throttled to avoid spam)
        if (typeof voiceOver !== 'undefined' && !window.lastCorrectionTime) {
            window.lastCorrectionTime = Date.now();
            voiceOver.onPoseCorrection(topFeedback.join(', '), { detailed: false });
        } else if (window.lastCorrectionTime && Date.now() - window.lastCorrectionTime > 10000) {
            // Provide timed guidance after 10 seconds of incorrect pose
            window.lastCorrectionTime = Date.now();
            voiceOver.onTimedGuidance(topFeedback.join(', '));
        }
        
        setTimeout(() => {
            canvas.classList.remove('blink-red');
            canvas.style.border = 'none';
        }, 500);
    }
    
    // Reset correction timer when pose is correct
    if (isCorrect && window.lastCorrectionTime) {
        window.lastCorrectionTime = null;
    }
}

function calculateAngles(landmarks) {
    return {
        leftElbow: calculateAngle(landmarks[11], landmarks[13], landmarks[15]),
        rightElbow: calculateAngle(landmarks[12], landmarks[14], landmarks[16]),
        leftKnee: calculateAngle(landmarks[23], landmarks[25], landmarks[27]),
        rightKnee: calculateAngle(landmarks[24], landmarks[26], landmarks[28]),
        leftShoulder: calculateAngle(landmarks[13], landmarks[11], landmarks[23]),
        rightShoulder: calculateAngle(landmarks[14], landmarks[12], landmarks[24]),
        leftHip: calculateAngle(landmarks[11], landmarks[23], landmarks[25]),
        rightHip: calculateAngle(landmarks[12], landmarks[24], landmarks[26]),
        leftAnkle: calculateAngle(landmarks[25], landmarks[27], landmarks[31]),
        rightAnkle: calculateAngle(landmarks[26], landmarks[28], landmarks[32]),
        torsoAngle: calculateTorsoAngle(landmarks),
        neckAngle: calculateAngle(landmarks[0], landmarks[11], landmarks[23])
    };
}

function calculateAngle(a, b, c) {
    // Check visibility of all three points
    if (!a || !b || !c || 
        a.visibility < MIN_VISIBILITY || 
        b.visibility < MIN_VISIBILITY || 
        c.visibility < MIN_VISIBILITY) {
        return null;
    }
    
    // Calculate vectors
    const ba = { x: a.x - b.x, y: a.y - b.y, z: a.z - b.z };
    const bc = { x: c.x - b.x, y: c.y - b.y, z: c.z - b.z };
    
    // Calculate dot product and magnitudes (3D)
    const dotProduct = ba.x * bc.x + ba.y * bc.y + ba.z * bc.z;
    const magnitudeBA = Math.sqrt(ba.x * ba.x + ba.y * ba.y + ba.z * ba.z);
    const magnitudeBC = Math.sqrt(bc.x * bc.x + bc.y * bc.y + bc.z * bc.z);
    
    // Calculate angle using dot product formula
    const cosAngle = dotProduct / (magnitudeBA * magnitudeBC);
    const angle = Math.acos(Math.max(-1, Math.min(1, cosAngle))) * (180 / Math.PI);
    
    return angle;
}

function calculateTorsoAngle(landmarks) {
    // Calculate torso angle relative to vertical
    const shoulder = landmarks[11];
    const hip = landmarks[23];
    
    if (!shoulder || !hip || 
        shoulder.visibility < MIN_VISIBILITY || 
        hip.visibility < MIN_VISIBILITY) {
        return null;
    }
    
    const deltaY = hip.y - shoulder.y;
    const deltaX = hip.x - shoulder.x;
    const angle = Math.atan2(deltaX, deltaY) * (180 / Math.PI);
    
    return Math.abs(angle);
}

function checkLandmarkVisibility(landmarks, pose) {
    // Check if key landmarks for the current pose are visible
    const keyLandmarks = [0, 11, 12, 13, 14, 23, 24, 25, 26]; // Core body landmarks
    
    let visibleCount = 0;
    keyLandmarks.forEach(index => {
        if (landmarks[index] && landmarks[index].visibility > MIN_VISIBILITY) {
            visibleCount++;
        }
    });
    
    // Require at least 80% of key landmarks to be visible
    return (visibleCount / keyLandmarks.length) >= 0.8;
}

function pauseSession() {
    isPaused = !isPaused;
    document.getElementById('pauseBtn').textContent = isPaused ? 'Resume' : 'Pause';
    document.getElementById('pauseBtn').className = isPaused 
        ? 'bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600'
        : 'bg-yellow-500 text-white px-4 py-2 rounded-lg hover:bg-yellow-600';
}

function stopSession() {
    if (confirm('Are you sure you want to stop the session?')) {
        isSessionActive = false;
        completeSession();
    }
}

function loadPoseSequences() {
    poseSequences = {
        'stretching': [
            {
                name: 'Mountain Pose (Tadasana)',
                instruction: 'Stand tall with feet together, arms by your sides',
                holdDuration: 20,
                benefits: ['Improves posture', 'Strengthens thighs', 'Increases awareness'],
                cautions: ['Keep knees soft', 'Distribute weight evenly'],
                tolerance: ANGLE_TOLERANCE.strict,
                angles: { 
                    leftElbow: 180, 
                    rightElbow: 180, 
                    leftKnee: 175, 
                    rightKnee: 175,
                    leftShoulder: 180,
                    rightShoulder: 180,
                    torsoAngle: 0
                }
            },
            {
                name: 'Forward Bend (Uttanasana)',
                instruction: 'Bend forward from hips, reach towards the floor',
                holdDuration: 25,
                benefits: ['Stretches hamstrings', 'Calms the mind', 'Relieves stress'],
                cautions: ['Bend knees if needed', 'Avoid if you have back injury'],
                tolerance: ANGLE_TOLERANCE.relaxed,
                angles: { 
                    leftKnee: 170, 
                    rightKnee: 170, 
                    leftHip: 70,
                    rightHip: 70,
                    torsoAngle: 80
                }
            },
            {
                name: 'Warrior I (Virabhadrasana I)',
                instruction: 'Step back, bend front knee, raise arms overhead',
                holdDuration: 30,
                benefits: ['Strengthens legs', 'Opens chest', 'Improves balance'],
                cautions: ['Keep front knee over ankle', 'Engage core'],
                tolerance: ANGLE_TOLERANCE.normal,
                angles: { 
                    leftKnee: 90, 
                    rightKnee: 175, 
                    leftShoulder: 180, 
                    rightShoulder: 180,
                    leftHip: 90,
                    rightHip: 170
                }
            },
            {
                name: 'Triangle Pose (Trikonasana)',
                instruction: 'Extend arms, reach to the side, look up',
                holdDuration: 25,
                benefits: ['Stretches sides', 'Strengthens legs', 'Improves digestion'],
                cautions: ['Keep both legs straight', 'Don\'t overextend'],
                tolerance: ANGLE_TOLERANCE.normal,
                angles: { 
                    leftKnee: 175, 
                    rightKnee: 175, 
                    leftShoulder: 90, 
                    rightShoulder: 160,
                    leftHip: 90,
                    rightHip: 170
                }
            },
            {
                name: 'Child\'s Pose (Balasana)',
                instruction: 'Kneel down, sit on heels, extend arms forward',
                holdDuration: 30,
                benefits: ['Relaxes body', 'Stretches back', 'Calms mind'],
                cautions: ['Use cushion if needed', 'Breathe deeply'],
                tolerance: ANGLE_TOLERANCE.relaxed,
                angles: { 
                    leftKnee: 45, 
                    rightKnee: 45, 
                    leftShoulder: 160, 
                    rightShoulder: 160,
                    leftHip: 45,
                    rightHip: 45
                }
            }
        ],
        'breathing': [
            {
                name: 'Seated Position (Sukhasana)',
                instruction: 'Sit cross-legged with straight spine',
                holdDuration: 300,
                benefits: ['Prepares for breathing', 'Calms mind', 'Opens hips'],
                cautions: ['Keep spine straight', 'Relax shoulders'],
                tolerance: ANGLE_TOLERANCE.relaxed,
                angles: { 
                    leftKnee: 90, 
                    rightKnee: 90, 
                    leftShoulder: 180, 
                    rightShoulder: 180,
                    torsoAngle: 0
                }
            }
        ],
        'surya-namaskar': [
            {
                name: 'Prayer Pose (Pranamasana)',
                instruction: 'Stand with palms together at chest',
                holdDuration: 5,
                benefits: ['Centers mind', 'Improves focus'],
                cautions: ['Breathe normally'],
                tolerance: ANGLE_TOLERANCE.strict,
                angles: { 
                    leftElbow: 90, 
                    rightElbow: 90, 
                    leftKnee: 175, 
                    rightKnee: 175,
                    torsoAngle: 0
                }
            },
            {
                name: 'Raised Arms (Hastauttanasana)',
                instruction: 'Raise arms overhead, arch back slightly',
                holdDuration: 5,
                benefits: ['Stretches abdomen', 'Opens chest'],
                cautions: ['Don\'t overarch'],
                tolerance: ANGLE_TOLERANCE.normal,
                angles: { 
                    leftShoulder: 180, 
                    rightShoulder: 180, 
                    leftElbow: 180, 
                    rightElbow: 180,
                    leftKnee: 175,
                    rightKnee: 175
                }
            },
            {
                name: 'Hand to Foot (Hasta Padasana)',
                instruction: 'Bend forward, touch the ground',
                holdDuration: 5,
                benefits: ['Stretches back', 'Improves flexibility'],
                cautions: ['Bend knees if needed'],
                tolerance: ANGLE_TOLERANCE.relaxed,
                angles: { 
                    leftKnee: 170, 
                    rightKnee: 170, 
                    leftHip: 70,
                    rightHip: 70,
                    torsoAngle: 80
                }
            },
            {
                name: 'Equestrian Pose (Ashwa Sanchalanasana)',
                instruction: 'Step right leg back, look up',
                holdDuration: 5,
                benefits: ['Strengthens legs', 'Opens hip flexors'],
                cautions: ['Keep front knee over ankle'],
                tolerance: ANGLE_TOLERANCE.normal,
                angles: { 
                    leftKnee: 90, 
                    rightKnee: 175, 
                    leftShoulder: 180, 
                    rightShoulder: 180,
                    leftHip: 90,
                    rightHip: 170
                }
            },
            {
                name: 'Plank Pose (Dandasana)',
                instruction: 'Step back to plank position',
                holdDuration: 5,
                benefits: ['Strengthens core', 'Builds endurance'],
                cautions: ['Keep body straight'],
                tolerance: ANGLE_TOLERANCE.strict,
                angles: { 
                    leftElbow: 180, 
                    rightElbow: 180, 
                    leftKnee: 175, 
                    rightKnee: 175,
                    leftShoulder: 90,
                    rightShoulder: 90,
                    torsoAngle: 0
                }
            },
            {
                name: 'Eight Limbed Pose (Ashtanga Namaskara)',
                instruction: 'Lower knees, chest, and chin to ground',
                holdDuration: 5,
                benefits: ['Strengthens arms', 'Opens chest'],
                cautions: ['Keep hips up'],
                tolerance: ANGLE_TOLERANCE.normal,
                angles: { 
                    leftElbow: 90, 
                    rightElbow: 90, 
                    leftKnee: 90, 
                    rightKnee: 90,
                    leftShoulder: 45,
                    rightShoulder: 45
                }
            },
            {
                name: 'Cobra Pose (Bhujangasana)',
                instruction: 'Lift chest, look up',
                holdDuration: 5,
                benefits: ['Strengthens spine', 'Opens chest'],
                cautions: ['Don\'t overarch neck'],
                tolerance: ANGLE_TOLERANCE.normal,
                angles: { 
                    leftElbow: 140, 
                    rightElbow: 140, 
                    leftKnee: 175, 
                    rightKnee: 175,
                    leftShoulder: 60,
                    rightShoulder: 60
                }
            },
            {
                name: 'Mountain Pose (Parvatasana)',
                instruction: 'Lift hips up, form inverted V',
                holdDuration: 5,
                benefits: ['Stretches entire body', 'Energizes'],
                cautions: ['Keep heels down'],
                tolerance: ANGLE_TOLERANCE.normal,
                angles: { 
                    leftKnee: 175, 
                    rightKnee: 175, 
                    leftShoulder: 60, 
                    rightShoulder: 60,
                    leftHip: 45,
                    rightHip: 45
                }
            },
            {
                name: 'Equestrian Pose (Ashwa Sanchalanasana)',
                instruction: 'Step left foot forward, look up',
                holdDuration: 5,
                benefits: ['Strengthens legs', 'Opens hip flexors'],
                cautions: ['Keep front knee over ankle'],
                tolerance: ANGLE_TOLERANCE.normal,
                angles: { 
                    leftKnee: 90, 
                    rightKnee: 175, 
                    leftShoulder: 180, 
                    rightShoulder: 180,
                    leftHip: 90,
                    rightHip: 170
                }
            },
            {
                name: 'Hand to Foot (Hasta Padasana)',
                instruction: 'Step forward, bend down',
                holdDuration: 5,
                benefits: ['Stretches back', 'Calms mind'],
                cautions: ['Breathe deeply'],
                tolerance: ANGLE_TOLERANCE.relaxed,
                angles: { 
                    leftKnee: 170, 
                    rightKnee: 170, 
                    leftHip: 70,
                    rightHip: 70,
                    torsoAngle: 80
                }
            },
            {
                name: 'Raised Arms (Hastauttanasana)',
                instruction: 'Rise up, arms overhead',
                holdDuration: 5,
                benefits: ['Stretches body', 'Energizes'],
                cautions: ['Keep breathing'],
                tolerance: ANGLE_TOLERANCE.normal,
                angles: { 
                    leftShoulder: 180, 
                    rightShoulder: 180, 
                    leftElbow: 180, 
                    rightElbow: 180,
                    leftKnee: 175,
                    rightKnee: 175
                }
            },
            {
                name: 'Mountain Pose (Tadasana)',
                instruction: 'Return to standing, palms together',
                holdDuration: 5,
                benefits: ['Completes cycle', 'Centers energy'],
                cautions: ['Relax and breathe'],
                tolerance: ANGLE_TOLERANCE.strict,
                angles: { 
                    leftElbow: 180, 
                    rightElbow: 180, 
                    leftKnee: 175, 
                    rightKnee: 175,
                    torsoAngle: 0
                }
            }
        ]
    };
}
