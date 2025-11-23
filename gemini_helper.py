"""
Gemini API Helper Module
Provides functions to interact with Google's Gemini API for AI-powered features
"""

import os
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai not installed. Install with: pip install google-generativeai")


class GeminiHelper:
    """Helper class for Gemini API interactions"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = 'gemini-pro'):
        """
        Initialize Gemini helper
        
        Args:
            api_key: Gemini API key (if None, tries to get from env)
            model: Model to use ('gemini-pro' or 'gemini-pro-vision')
        """
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai package is not installed")
        
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not provided")
        
        self.model_name = model
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
        logger.info(f"Gemini API initialized with model: {model}")
    
    def generate_feedback(self, pose_name: str, accuracy: float, errors: Optional[List[str]] = None) -> str:
        """
        Generate AI-powered feedback for pose correction
        
        Args:
            pose_name: Name of the yoga pose
            accuracy: Accuracy percentage (0-100)
            errors: List of specific errors detected
            
        Returns:
            Generated feedback string
        """
        errors_text = ", ".join(errors) if errors else "general alignment issues"
        
        prompt = f"""You are a professional yoga instructor. A student is practicing the {pose_name} pose 
        and achieved {accuracy}% accuracy. They have issues with: {errors_text}.
        
        Provide encouraging, specific, and actionable feedback to help them improve. Keep it concise (2-3 sentences).
        Be supportive and focus on one or two key corrections."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating feedback: {e}")
            return self._fallback_feedback(pose_name, accuracy, errors)
    
    def analyze_pose_safety(self, pose_name: str, user_history: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze if a pose is safe for the user based on their history
        
        Args:
            pose_name: Name of the pose to analyze
            user_history: User's practice history (injuries, experience level, etc.)
            
        Returns:
            Dictionary with safety analysis
        """
        history_text = ""
        if user_history:
            history_text = f"User history: {user_history}"
        
        prompt = f"""You are a yoga safety expert. Analyze if {pose_name} is appropriate and safe.
        {history_text}
        
        Provide:
        1. Safety level (safe, caution, not_recommended)
        2. Potential risks
        3. Modifications if needed
        
        Format as JSON with keys: safety_level, risks, modifications"""
        
        try:
            response = self.model.generate_content(prompt)
            # Parse response (simplified - in production, use proper JSON parsing)
            return {
                "safety_level": "safe",
                "risks": [],
                "modifications": [],
                "ai_analysis": response.text
            }
        except Exception as e:
            logger.error(f"Error analyzing pose safety: {e}")
            return {
                "safety_level": "safe",
                "risks": [],
                "modifications": [],
                "ai_analysis": None
            }
    
    def generate_practice_recommendation(self, user_level: str, goals: List[str], session_count: int) -> str:
        """
        Generate personalized practice recommendations
        
        Args:
            user_level: User's experience level (beginner, intermediate, advanced)
            goals: List of user goals
            session_count: Number of sessions completed
            
        Returns:
            Personalized recommendation text
        """
        goals_text = ", ".join(goals)
        
        prompt = f"""You are a yoga instructor creating a personalized practice plan.
        
        User level: {user_level}
        Goals: {goals_text}
        Sessions completed: {session_count}
        
        Provide a brief, motivating recommendation for their next practice session (3-4 sentences)."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating recommendation: {e}")
            return "Continue practicing regularly to improve your yoga journey!"
    
    def chat_about_yoga(self, user_question: str, context: Optional[str] = None) -> str:
        """
        Answer user questions about yoga
        
        Args:
            user_question: User's question
            context: Additional context (current pose, practice history, etc.)
            
        Returns:
            AI-generated answer
        """
        context_text = f"\nContext: {context}" if context else ""
        
        prompt = f"""You are a knowledgeable yoga instructor and guide. Answer this question helpfully and accurately:
        
        Question: {user_question}
        {context_text}
        
        Provide a clear, concise answer (2-4 sentences)."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return "I'm sorry, I couldn't process your question right now. Please try again later."
    
    def analyze_pose_from_image(self, image_path: str, expected_pose: str) -> Dict[str, Any]:
        """
        Analyze a pose from an image using Gemini Vision
        
        Args:
            image_path: Path to the image file
            expected_pose: Name of the expected pose
            
        Returns:
            Dictionary with analysis results
        """
        if self.model_name != 'gemini-pro-vision':
            logger.warning("Model is not gemini-pro-vision, cannot analyze images")
            return {"error": "Vision model not configured"}
        
        try:
            import PIL.Image
            
            img = PIL.Image.open(image_path)
            prompt = f"""Analyze this yoga pose image. The expected pose is {expected_pose}.
            Provide:
            1. Pose name (if recognized)
            2. Alignment quality (good, needs_improvement, poor)
            3. Key corrections needed
            4. Confidence level (0-100)"""
            
            response = self.model.generate_content([prompt, img])
            return {
                "analysis": response.text,
                "pose_name": expected_pose,
                "model": "gemini-pro-vision"
            }
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return {"error": str(e)}
    
    def _fallback_feedback(self, pose_name: str, accuracy: float, errors: Optional[List[str]]) -> str:
        """Fallback feedback when AI generation fails"""
        if accuracy >= 85:
            return f"Great job with {pose_name}! Keep maintaining your alignment."
        elif accuracy >= 70:
            return f"Good attempt at {pose_name}. Focus on alignment to improve your form."
        else:
            error_msg = f" with {errors[0]}" if errors else ""
            return f"Keep practicing {pose_name}{error_msg}. Take your time and focus on proper alignment."


# Convenience function to get initialized Gemini helper
def get_gemini_helper(api_key: Optional[str] = None, model: str = 'gemini-pro') -> Optional[GeminiHelper]:
    """
    Get an initialized Gemini helper instance
    
    Args:
        api_key: Optional API key (uses env if not provided)
        model: Model name
        
    Returns:
        GeminiHelper instance or None if not available
    """
    if not GEMINI_AVAILABLE:
        logger.warning("Gemini not available")
        return None
    
    try:
        api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.warning("GEMINI_API_KEY not found")
            return None
        
        return GeminiHelper(api_key=api_key, model=model)
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")
        return None

