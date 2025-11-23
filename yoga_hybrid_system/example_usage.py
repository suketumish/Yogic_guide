"""
Example Usage Script
Demonstrates all features of the Yoga Hybrid System
"""

import os
import json
from complete_pipeline import YogaPoseAnalyzer

def example_1_single_image():
    """Example 1: Analyze a single yoga pose image"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Single Image Analysis")
    print("="*60)
    
    analyzer = YogaPoseAnalyzer(use_llm=True)
    
    # Analyze a single image
    image_path = 'data/test/warrior2/example.jpg'  # Replace with your image
    
    if os.path.exists(image_path):
        result = analyzer.analyze_pose(
            image_path=image_path,
            user_level='beginner',
            verbose=True
        )
        
        # Access specific results
        print("\nAccessing specific results:")
        print(f"Detected Pose: {result['analysis']['hybrid']['prediction']}")
        print(f"Confidence: {result['analysis']['hybrid']['confidence']:.1%}")
        print(f"Feedback: {result['feedback']}")
    else:
        print(f"⚠️  Image not found: {image_path}")
        print("Please provide a valid image path")

def example_2_batch_processing():
    """Example 2: Process multiple images"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Batch Processing")
    print("="*60)
    
    analyzer = YogaPoseAnalyzer(use_llm=False)  # Faster without LLM
    
    # Process all images in a directory
    image_dir = 'data/test/warrior2'  # Replace with your directory
    
    if os.path.exists(image_dir):
        results = analyzer.analyze_batch(
            image_dir=image_dir,
            output_json='batch_results.json'
        )
        
        # Analyze results
        print("\nBatch Analysis Summary:")
        poses = {}
        for result in results:
            pose = result['analysis']['hybrid']['prediction']
            poses[pose] = poses.get(pose, 0) + 1
        
        for pose, count in poses.items():
            print(f"  {pose}: {count} images")
    else:
        print(f"⚠️  Directory not found: {image_dir}")

def example_3_custom_feedback():
    """Example 3: Generate custom feedback for different user levels"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Feedback by User Level")
    print("="*60)
    
    analyzer = YogaPoseAnalyzer(use_llm=True)
    image_path = 'data/test/warrior2/example.jpg'
    
    if os.path.exists(image_path):
        for level in ['beginner', 'intermediate', 'advanced']:
            print(f"\n--- {level.upper()} Level ---")
            result = analyzer.analyze_pose(
                image_path=image_path,
                user_level=level,
                verbose=False
            )
            print(f"Feedback: {result['feedback']}")
    else:
        print(f"⚠️  Image not found: {image_path}")

def example_4_angle_analysis():
    """Example 4: Detailed angle analysis"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Detailed Angle Analysis")
    print("="*60)
    
    analyzer = YogaPoseAnalyzer(use_llm=False)
    image_path = 'data/test/warrior2/example.jpg'
    
    if os.path.exists(image_path):
        result = analyzer.analyze_pose(
            image_path=image_path,
            verbose=False
        )
        
        print("\nBody Angle Measurements:")
        angles = result.get('body_angles', {})
        
        if angles:
            # Group angles by body part
            arm_angles = {k: v for k, v in angles.items() if 'elbow' in k or 'shoulder' in k}
            leg_angles = {k: v for k, v in angles.items() if 'knee' in k or 'hip' in k}
            torso_angles = {k: v for k, v in angles.items() if 'torso' in k or 'spine' in k}
            
            if arm_angles:
                print("\n  Arms:")
                for angle_name, angle_value in arm_angles.items():
                    print(f"    {angle_name.replace('_', ' ').title()}: {angle_value:.1f}°")
            
            if leg_angles:
                print("\n  Legs:")
                for angle_name, angle_value in leg_angles.items():
                    print(f"    {angle_name.replace('_', ' ').title()}: {angle_value:.1f}°")
            
            if torso_angles:
                print("\n  Torso:")
                for angle_name, angle_value in torso_angles.items():
                    print(f"    {angle_name.replace('_', ' ').title()}: {angle_value:.1f}°")
        else:
            print("  No angles detected (keypoint extraction may have failed)")
    else:
        print(f"⚠️  Image not found: {image_path}")

def example_5_model_comparison():
    """Example 5: Compare image vs keypoint model predictions"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Model Comparison")
    print("="*60)
    
    analyzer = YogaPoseAnalyzer(use_llm=False)
    image_path = 'data/test/warrior2/example.jpg'
    
    if os.path.exists(image_path):
        result = analyzer.analyze_pose(
            image_path=image_path,
            verbose=False
        )
        
        print("\nModel Predictions:")
        print(f"\n  Image Model:")
        print(f"    Prediction: {result['analysis']['image_model']['prediction']}")
        print(f"    Confidence: {result['analysis']['image_model']['confidence']:.1%}")
        
        print(f"\n  Keypoint Model:")
        print(f"    Prediction: {result['analysis']['keypoint_model']['prediction']}")
        print(f"    Confidence: {result['analysis']['keypoint_model']['confidence']:.1%}")
        
        print(f"\n  Hybrid Decision:")
        print(f"    Final Prediction: {result['analysis']['hybrid']['prediction']}")
        print(f"    Final Confidence: {result['analysis']['hybrid']['confidence']:.1%}")
        print(f"    Decision Logic: {result['analysis']['hybrid']['logic']}")
        
        # Check agreement
        if result['analysis']['image_model']['prediction'] == result['analysis']['keypoint_model']['prediction']:
            print("\n  ✅ Models agree on prediction")
        else:
            print("\n  ⚠️  Models disagree - hybrid logic resolved conflict")
    else:
        print(f"⚠️  Image not found: {image_path}")

def example_6_issue_detection():
    """Example 6: Detect and report posture issues"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Posture Issue Detection")
    print("="*60)
    
    analyzer = YogaPoseAnalyzer(use_llm=False)
    image_path = 'data/test/warrior2/example.jpg'
    
    if os.path.exists(image_path):
        result = analyzer.analyze_pose(
            image_path=image_path,
            verbose=False
        )
        
        issues = result.get('issues_detected', [])
        
        if issues:
            print(f"\n⚠️  {len(issues)} issue(s) detected:")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue.replace('_', ' ').title()}")
        else:
            print("\n✅ No issues detected - excellent form!")
        
        # Show which angles caused issues
        if issues and result.get('body_angles'):
            print("\nRelated angles:")
            angles = result['body_angles']
            
            if 'knee' in str(issues):
                print(f"  Left Knee: {angles.get('left_knee', 'N/A'):.1f}°")
                print(f"  Right Knee: {angles.get('right_knee', 'N/A'):.1f}°")
            
            if 'torso' in str(issues) or 'back' in str(issues):
                print(f"  Torso Vertical: {angles.get('torso_vertical', 'N/A'):.1f}°")
                print(f"  Spine Alignment: {angles.get('spine_alignment', 'N/A'):.1f}°")
    else:
        print(f"⚠️  Image not found: {image_path}")

def example_7_save_results():
    """Example 7: Save results to JSON file"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Save Results to JSON")
    print("="*60)
    
    analyzer = YogaPoseAnalyzer(use_llm=True)
    image_path = 'data/test/warrior2/example.jpg'
    
    if os.path.exists(image_path):
        result = analyzer.analyze_pose(
            image_path=image_path,
            verbose=False
        )
        
        # Save to JSON
        output_file = 'outputs/analysis_result.json'
        os.makedirs('outputs', exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"\n✅ Results saved to: {output_file}")
        print(f"File size: {os.path.getsize(output_file)} bytes")
        
        # Load and verify
        with open(output_file, 'r') as f:
            loaded_result = json.load(f)
        
        print(f"Verified: Pose = {loaded_result['analysis']['hybrid']['prediction']}")
    else:
        print(f"⚠️  Image not found: {image_path}")

def example_8_no_llm_mode():
    """Example 8: Use without LLM (rule-based feedback)"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Rule-Based Feedback (No LLM)")
    print("="*60)
    
    # Initialize without LLM
    analyzer = YogaPoseAnalyzer(use_llm=False)
    image_path = 'data/test/warrior2/example.jpg'
    
    if os.path.exists(image_path):
        result = analyzer.analyze_pose(
            image_path=image_path,
            verbose=False
        )
        
        print(f"\nPose: {result['analysis']['hybrid']['prediction']}")
        print(f"Confidence: {result['analysis']['hybrid']['confidence']:.1%}")
        print(f"\nRule-based Feedback:")
        print(f"  {result['feedback']}")
        
        print("\n💡 This mode is faster and doesn't require API key")
    else:
        print(f"⚠️  Image not found: {image_path}")

def main():
    """Run all examples"""
    print("\n" + "🧘 "*20)
    print("  YOGA HYBRID SYSTEM - EXAMPLE USAGE")
    print("🧘 "*20)
    
    examples = [
        ("Single Image Analysis", example_1_single_image),
        ("Batch Processing", example_2_batch_processing),
        ("Custom Feedback by Level", example_3_custom_feedback),
        ("Detailed Angle Analysis", example_4_angle_analysis),
        ("Model Comparison", example_5_model_comparison),
        ("Issue Detection", example_6_issue_detection),
        ("Save Results to JSON", example_7_save_results),
        ("Rule-Based Feedback", example_8_no_llm_mode)
    ]
    
    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nRunning all examples...\n")
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {str(e)}")
            print("This may be due to missing models or test images")
    
    print("\n" + "="*60)
    print("Examples complete!")
    print("="*60)
    print("\n💡 Tip: Modify these examples for your specific use case")
    print("📚 See USAGE_GUIDE.md for more details\n")

if __name__ == '__main__':
    main()
