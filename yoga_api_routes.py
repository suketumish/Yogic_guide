"""
Yoga Pose Detection API Routes
Add these routes to your Flask app
"""

from flask import jsonify, request
from yoga_pose_api import detect_pose, get_available_poses, is_system_ready

def register_yoga_api_routes(app):
    """
    Register yoga pose detection API routes with Flask app
    
    Usage in app.py:
        from yoga_api_routes import register_yoga_api_routes
        register_yoga_api_routes(app)
    """
    
    @app.route('/api/yoga/detect', methods=['POST'])
    def api_detect_yoga_pose():
        """
        Detect yoga pose from uploaded image
        
        Request body:
            {
                "image": "base64_encoded_image_data"
            }
            
        Response:
            {
                "success": true,
                "pose_name": "tadasana",
                "confidence": 0.95,
                "feedback": "Excellent pose!"
            }
        """
        try:
            data = request.get_json()
            
            if not data or 'image' not in data:
                return jsonify({
                    'success': False,
                    'error': 'No image data provided'
                }), 400
            
            # Detect pose
            result = detect_pose(image_base64=data['image'])
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/yoga/poses', methods=['GET'])
    def api_get_available_poses():
        """
        Get list of all available yoga poses
        
        Response:
            {
                "success": true,
                "poses": ["tadasana", "vriksasana", ...]
            }
        """
        try:
            poses = get_available_poses()
            return jsonify({
                'success': True,
                'poses': poses,
                'count': len(poses)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/yoga/status', methods=['GET'])
    def api_yoga_system_status():
        """
        Check if yoga detection system is ready
        
        Response:
            {
                "ready": true,
                "message": "System ready"
            }
        """
        try:
            ready = is_system_ready()
            
            if ready:
                poses = get_available_poses()
                return jsonify({
                    'ready': True,
                    'message': 'Yoga detection system is ready',
                    'available_poses': len(poses)
                }), 200
            else:
                return jsonify({
                    'ready': False,
                    'message': 'Yoga detection system not initialized. Please train models first.',
                    'help': 'Run: cd yoga_hybrid_system && python train_image_model.py'
                }), 503
                
        except Exception as e:
            return jsonify({
                'ready': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/yoga/detect-realtime', methods=['POST'])
    def api_detect_yoga_pose_realtime():
        """
        Real-time pose detection endpoint for video frames
        Optimized for low latency
        
        Request body:
            {
                "frame": "base64_encoded_frame_data"
            }
            
        Response:
            {
                "success": true,
                "pose_name": "tadasana",
                "confidence": 0.95,
                "display_name": "Tadasana (Mountain Pose)"
            }
        """
        try:
            data = request.get_json()
            
            if not data or 'frame' not in data:
                return jsonify({
                    'success': False,
                    'error': 'No frame data provided'
                }), 400
            
            # Detect pose
            result = detect_pose(image_base64=data['frame'])
            
            if result['success']:
                # Add display name
                pose_name = result['pose_name']
                display_name = pose_name.replace('_', ' ').title()
                result['display_name'] = display_name
                
                # Simplify response for real-time
                return jsonify({
                    'success': True,
                    'pose_name': pose_name,
                    'display_name': display_name,
                    'confidence': result['confidence'],
                    'method': result.get('method', 'hybrid')
                }), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    print("✅ Yoga API routes registered")
