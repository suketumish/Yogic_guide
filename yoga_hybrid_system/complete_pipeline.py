"""
Complete Hybrid Yoga Posture Detection Pipeline
End-to-end inference with image + keypoint + LLM feedback
"""

import os
import sys
import json
import argparse
from hybrid_inference import HybridYogaClassifier
from llm_feedback import YogaFeedbackGenerator

class YogaPoseAnalyzer:
    def __init__(self, use_llm=True):
        """Initialize complete pipeline"""
        print("🧘 Initializing Yoga Pose Analyzer...")
        
        self.hybrid_classifier = HybridYogaClassifier()
        self.hybrid_classifier.load_models()
        
        self.feedback_generator = YogaFeedbackGenerator() if use_llm else None
        
        print("✅ Pipeline ready!\n")
    
    def analyze_pose(self, image_path, user_level='beginner', verbose=True):
        """Complete analysis pipeline"""
        if not os.path.exists(image_path):
            return {'error': f'Image not found: {image_path}'}
        
        # Step 1: Hybrid inference
        result = self.hybrid_classifier.predict(image_path)
        
        # Step 2: Generate feedback
        if self.feedback_generator:
            feedback_package = self.feedback_generator.generate_feedback_with_json(
                result, user_level
            )
        else:
            feedback_package = {
                'pose': result['final_prediction'],
                'confidence': result['final_confidence'],
                'feedback_text': 'Feedback generation disabled',
                'issues': result.get('issues_detected', []),
                'angles': result.get('angles', {})
            }
        
        # Step 3: Create complete output
        complete_result = {
            'image_path': image_path,
            'analysis': {
                'image_model': {
                    'prediction': result['image_prediction'],
                    'confidence': result['image_confidence']
                },
                'keypoint_model': {
                    'prediction': result['keypoint_prediction'],
                    'confidence': result['keypoint_confidence']
                },
                'hybrid': {
                    'prediction': result['final_prediction'],
                    'confidence': result['final_confidence'],
                    'logic': result['decision_logic']
                }
            },
            'body_angles': result.get('angles', {}),
            'issues_detected': result.get('issues_detected', []),
            'feedback': feedback_package['feedback_text'],
            'user_level': user_level
        }
        
        if verbose:
            self.print_result(complete_result)
        
        return complete_result
    
    def print_result(self, result):
        """Pretty print analysis result"""
        print("\n" + "="*60)
        print("🧘 YOGA POSE ANALYSIS RESULT")
        print("="*60)
        
        print(f"\n📸 Image: {result['image_path']}")
        
        print(f"\n🎯 FINAL PREDICTION: {result['analysis']['hybrid']['prediction'].upper()}")
        print(f"   Confidence: {result['analysis']['hybrid']['confidence']:.1%}")
        print(f"   Logic: {result['analysis']['hybrid']['logic']}")
        
        print(f"\n📊 Model Breakdown:")
        print(f"   Image Model: {result['analysis']['image_model']['prediction']} "
              f"({result['analysis']['image_model']['confidence']:.1%})")
        print(f"   Keypoint Model: {result['analysis']['keypoint_model']['prediction']} "
              f"({result['analysis']['keypoint_model']['confidence']:.1%})")
        
        if result['body_angles']:
            print(f"\n📐 Body Angles:")
            for angle_name, angle_value in result['body_angles'].items():
                print(f"   {angle_name.replace('_', ' ').title()}: {angle_value:.1f}°")
        
        if result['issues_detected']:
            print(f"\n⚠️  Issues Detected:")
            for issue in result['issues_detected']:
                print(f"   • {issue.replace('_', ' ').title()}")
        else:
            print(f"\n✅ No major issues detected!")
        
        print(f"\n💬 Feedback:")
        print(f"   {result['feedback']}")
        
        print("\n" + "="*60 + "\n")
    
    def analyze_batch(self, image_dir, output_json='batch_results.json'):
        """Analyze multiple images"""
        results = []
        
        image_files = [f for f in os.listdir(image_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        print(f"📁 Processing {len(image_files)} images from {image_dir}\n")
        
        for img_file in image_files:
            img_path = os.path.join(image_dir, img_file)
            result = self.analyze_pose(img_path, verbose=False)
            results.append(result)
            
            print(f"✓ {img_file}: {result['analysis']['hybrid']['prediction']} "
                  f"({result['analysis']['hybrid']['confidence']:.1%})")
        
        # Save results
        with open(output_json, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n✅ Batch analysis complete! Results saved to {output_json}")
        
        return results


def main():
    parser = argparse.ArgumentParser(description='Hybrid Yoga Pose Analysis')
    parser.add_argument('--image', type=str, help='Path to single image')
    parser.add_argument('--batch', type=str, help='Path to directory of images')
    parser.add_argument('--level', type=str, default='beginner', 
                       choices=['beginner', 'intermediate', 'advanced'],
                       help='User skill level')
    parser.add_argument('--no-llm', action='store_true', 
                       help='Disable LLM feedback generation')
    parser.add_argument('--output', type=str, default='result.json',
                       help='Output JSON file for batch processing')
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = YogaPoseAnalyzer(use_llm=not args.no_llm)
    
    # Single image analysis
    if args.image:
        result = analyzer.analyze_pose(args.image, user_level=args.level)
        
        # Save result
        with open('single_result.json', 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"💾 Result saved to single_result.json")
    
    # Batch analysis
    elif args.batch:
        results = analyzer.analyze_batch(args.batch, output_json=args.output)
    
    else:
        print("❌ Please provide --image or --batch argument")
        parser.print_help()


if __name__ == '__main__':
    main()
