"""
LLM-based Feedback Generator
Converts technical pose analysis into natural language coaching feedback
"""

import json
import os
from typing import Dict, List
import google.generativeai as genai

class YogaFeedbackGenerator:
    def __init__(self, api_key=None):
        """Initialize LLM feedback generator"""
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.use_llm = True
        else:
            print("⚠️  No API key found. Using rule-based feedback.")
            self.use_llm = False
        
        # Ideal angles for common poses
        self.ideal_angles = {
            'warrior2': {
                'front_knee': 90,
                'back_knee': 180,
                'front_hip': 90,
                'torso_vertical': 0,
                'arms_horizontal': 180
            },
            'downdog': {
                'left_knee': 170,
                'right_knee': 170,
                'left_elbow': 180,
                'right_elbow': 180,
                'spine_alignment': 180
            },
            'tree': {
                'standing_knee': 180,
                'bent_knee': 90,
                'torso_vertical': 0
            },
            'plank': {
                'left_elbow': 180,
                'right_elbow': 180,
                'left_hip': 180,
                'right_hip': 180,
                'torso_vertical': 0
            }
        }
    
    def create_feedback_prompt(self, result: Dict, user_level: str = 'beginner') -> str:
        """Create structured prompt for LLM"""
        pose = result.get('final_prediction', 'unknown')
        confidence = result.get('final_confidence', 0)
        angles = result.get('angles', {})
        issues = result.get('issues_detected', [])
        
        # Get ideal angles for this pose
        ideal = self.ideal_angles.get(pose.lower(), {})
        
        prompt = f"""You are a certified yoga instructor providing friendly, encouraging feedback.

Pose Detected: {pose}
Confidence: {confidence:.1%}
User Level: {user_level}

Current Body Angles:
"""
        
        if angles:
            for angle_name, angle_value in angles.items():
                ideal_value = ideal.get(angle_name, None)
                if ideal_value:
                    diff = abs(angle_value - ideal_value)
                    prompt += f"- {angle_name.replace('_', ' ').title()}: {angle_value:.0f}° (ideal: {ideal_value}°, diff: {diff:.0f}°)\n"
                else:
                    prompt += f"- {angle_name.replace('_', ' ').title()}: {angle_value:.0f}°\n"
        
        if issues:
            prompt += f"\nIssues Detected:\n"
            for issue in issues:
                prompt += f"- {issue.replace('_', ' ')}\n"
        
        prompt += """
Provide 2-3 specific, actionable corrections in friendly language.
Be encouraging and supportive.
Keep response under 60 words.
Focus on the most important corrections first.
Use simple, clear language suitable for the user's level.
"""
        
        return prompt
    
    def generate_llm_feedback(self, result: Dict, user_level: str = 'beginner') -> str:
        """Generate feedback using LLM"""
        if not self.use_llm:
            return self.generate_rule_based_feedback(result)
        
        try:
            prompt = self.create_feedback_prompt(result, user_level)
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"LLM error: {e}")
            return self.generate_rule_based_feedback(result)
    
    def generate_rule_based_feedback(self, result: Dict) -> str:
        """Generate feedback using predefined rules (fallback)"""
        pose = result.get('final_prediction', 'unknown')
        confidence = result.get('final_confidence', 0)
        issues = result.get('issues_detected', [])
        angles = result.get('angles', {})
        
        # Low confidence
        if confidence < 0.5:
            return "I'm having trouble seeing your pose clearly. Try better lighting and ensure your full body is visible in the frame."
        
        # No issues detected
        if not issues or len(issues) == 0:
            return self.get_positive_feedback(pose)
        
        # Generate feedback based on issues
        feedback_parts = []
        
        if 'front_knee_too_bent' in issues:
            feedback_parts.append("Your front knee is bent too deeply. Try raising your hips slightly to achieve a 90° angle.")
        
        if 'front_knee_not_bent_enough' in issues:
            feedback_parts.append("Bend your front knee deeper until it's directly over your ankle at 90°.")
        
        if 'knee_forward_of_ankle' in issues:
            feedback_parts.append("Your knee is tracking forward past your toes. Shift your hips back to protect your knee joint.")
        
        if 'back_knee_bent' in issues:
            feedback_parts.append("Straighten your back leg and press through your heel for a strong foundation.")
        
        if 'rounded_back' in issues:
            feedback_parts.append("Your spine is rounding. Lengthen through your back and lift your chest.")
        
        if 'torso_leaning' in issues:
            feedback_parts.append("Your torso is leaning. Engage your core and stack your shoulders over your hips.")
        
        if 'hips_sagging' in issues:
            feedback_parts.append("Your hips are dropping. Engage your core and lift your belly button toward your spine.")
        
        if 'elbows_bent' in issues:
            feedback_parts.append("Straighten your arms and press firmly through your hands.")
        
        if 'shoulders_raised' in issues:
            feedback_parts.append("Relax your shoulders down away from your ears.")
        
        # Combine feedback
        if feedback_parts:
            feedback = " ".join(feedback_parts[:3])  # Max 3 corrections
            return f"Good effort! {feedback}"
        
        return self.get_positive_feedback(pose)
    
    def get_positive_feedback(self, pose: str) -> str:
        """Get encouraging feedback for good form"""
        positive_messages = {
            'warrior2': "Excellent Warrior 2! Your alignment is strong. Hold this powerful stance and breathe deeply.",
            'warrior1': "Beautiful Warrior 1! Your foundation is solid. Feel the strength in your legs.",
            'downdog': "Great Downward Dog! Your form is looking good. Focus on lengthening your spine.",
            'tree': "Wonderful Tree Pose! Your balance is impressive. Keep your gaze steady on one point.",
            'plank': "Strong Plank! Your body alignment is excellent. Maintain that straight line.",
            'triangle': "Beautiful Triangle! Your extension is lovely. Keep opening through your chest.",
            'child': "Perfect Child's Pose. This is your rest. Let your body completely relax.",
            'cobra': "Nice Cobra! Your backbend is controlled. Remember to keep your shoulders relaxed.",
            'bridge': "Excellent Bridge! Your lift is strong. Press evenly through both feet.",
            'chair': "Powerful Chair Pose! Your form is solid. Feel the burn in those thighs!"
        }
        
        for key, message in positive_messages.items():
            if key in pose.lower():
                return message
        
        return "Great job! Your pose is looking good. Keep up the excellent work!"
    
    def generate_feedback_with_json(self, result: Dict, user_level: str = 'beginner') -> Dict:
        """Generate complete feedback package"""
        feedback_text = self.generate_llm_feedback(result, user_level)
        
        feedback_package = {
            'pose': result.get('final_prediction'),
            'confidence': result.get('final_confidence'),
            'feedback_text': feedback_text,
            'issues': result.get('issues_detected', []),
            'angles': result.get('angles', {}),
            'decision_logic': result.get('decision_logic'),
            'user_level': user_level
        }
        
        return feedback_package


# Sample feedback messages for reference
SAMPLE_FEEDBACK_MESSAGES = [
    {
        'pose': 'warrior2',
        'scenario': 'perfect_form',
        'feedback': "Excellent Warrior 2! Your front knee is perfectly aligned over your ankle at 90°, and your back leg is strong and straight. Your arms are beautifully extended. Hold this for 5 more breaths!"
    },
    {
        'pose': 'warrior2',
        'scenario': 'knee_forward',
        'feedback': "Nice effort! Your front knee is tracking a bit forward (95°). Try shifting your hips back slightly so your knee stays directly over your ankle. This protects your knee joint."
    },
    {
        'pose': 'downdog',
        'scenario': 'rounded_back',
        'feedback': "Good start! I notice your spine is slightly rounded (25° curve). Try bending your knees a bit and lifting your tailbone higher. Focus on lengthening your spine rather than straightening your legs."
    },
    {
        'pose': 'tree',
        'scenario': 'balance_issue',
        'feedback': "You're doing great! Your standing leg is strong. If you're wobbling, try focusing on a fixed point ahead and engaging your core. It's okay to use a wall for support while building strength."
    },
    {
        'pose': 'plank',
        'scenario': 'hips_low',
        'feedback': "Strong plank! Your hips are dipping about 15° below neutral. Engage your core and imagine a straight line from head to heels. Think about lifting your belly button toward your spine."
    },
    {
        'pose': 'triangle',
        'scenario': 'torso_rotation',
        'feedback': "Beautiful extension! Your torso is rotated about 30° forward. Try opening your chest more toward the ceiling by stacking your shoulders. Imagine your body between two panes of glass."
    },
    {
        'pose': 'cobra',
        'scenario': 'shoulders_tense',
        'feedback': "Nice backbend! Your shoulders are slightly elevated (15° higher than ideal). Roll them back and down, away from your ears. This opens your chest and protects your neck."
    },
    {
        'pose': 'chair',
        'scenario': 'knees_forward',
        'feedback': "Powerful Chair Pose! Your knees are tracking forward past your toes (105° angle). Sit back more like you're sitting in a chair, keeping your weight in your heels. You should be able to see your toes."
    },
    {
        'pose': 'warrior1',
        'scenario': 'hip_alignment',
        'feedback': "Strong stance! Your back hip is open about 35° to the side. Try rotating your back foot in slightly and squaring both hips forward. This deepens the hip flexor stretch."
    },
    {
        'pose': 'child',
        'scenario': 'tension',
        'feedback': "Restful pose! I notice some tension in your shoulders (20° elevation). Let your forehead rest completely on the mat and allow your shoulders to melt down. This is your recovery pose—fully surrender."
    },
    {
        'pose': 'bridge',
        'scenario': 'knees_wide',
        'feedback': "Great lift! Your knees are splaying outward about 25°. Place a block between your thighs or imagine squeezing a ball. This engages your inner thighs and protects your lower back."
    },
    {
        'pose': 'pigeon',
        'scenario': 'uneven_hips',
        'feedback': "Deep stretch! Your hips are tilted about 18° to one side. Try placing a folded blanket under your right hip to level your pelvis. Even hips = safer, deeper stretch."
    },
    {
        'pose': 'crow',
        'scenario': 'weight_distribution',
        'feedback': "Brave attempt! Your weight is too far back (center of gravity 12cm behind hands). Shift forward more, bringing your shoulders over your wrists. Look forward, not down!"
    },
    {
        'pose': 'camel',
        'scenario': 'neck_compression',
        'feedback': "Beautiful backbend! Be careful not to drop your head too far back (35° hyperextension). Keep length in your neck by lifting through your chest first. Your gaze can be slightly upward."
    },
    {
        'pose': 'side_plank',
        'scenario': 'hip_drop',
        'feedback': "Strong hold! Your hips are sagging about 20° below alignment. Engage your obliques and lift your hips higher. Imagine pushing the floor away with your supporting hand."
    }
]


def main():
    """Demo feedback generation"""
    generator = YogaFeedbackGenerator()
    
    # Example result from hybrid inference
    example_result = {
        'final_prediction': 'warrior2',
        'final_confidence': 0.89,
        'angles': {
            'left_knee': 95,
            'right_knee': 178,
            'left_hip': 88,
            'torso_vertical': 8
        },
        'issues_detected': ['front_knee_slightly_forward', 'torso_slight_lean']
    }
    
    feedback = generator.generate_feedback_with_json(example_result, user_level='beginner')
    print(json.dumps(feedback, indent=2))


if __name__ == '__main__':
    main()
