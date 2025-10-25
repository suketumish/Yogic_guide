from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.yogic_guide

# Clear existing poses
db.poses.delete_many({})

# Stretching Module Poses
stretching_poses = [
    {
        'name': 'Mountain Pose (Tadasana)',
        'module': 'stretching',
        'reference_image': 'mountain_pose.jpg',
        'benefits': ['Improves posture', 'Strengthens thighs', 'Increases awareness'],
        'cautions': ['Keep knees soft', 'Distribute weight evenly'],
        'ideal_angles': {'leftElbow': 180, 'rightElbow': 180, 'leftKnee': 180, 'rightKnee': 180},
        'hold_duration': 20,
        'instruction': 'Stand tall with feet together, arms by your sides'
    },
    {
        'name': 'Forward Bend (Uttanasana)',
        'module': 'stretching',
        'reference_image': 'forward_bend.jpg',
        'benefits': ['Stretches hamstrings', 'Calms the mind', 'Relieves stress'],
        'cautions': ['Bend knees if needed', 'Avoid if you have back injury'],
        'ideal_angles': {'leftKnee': 170, 'rightKnee': 170, 'leftShoulder': 90, 'rightShoulder': 90},
        'hold_duration': 25,
        'instruction': 'Bend forward from hips, reach towards the floor'
    },
    {
        'name': 'Warrior I (Virabhadrasana I)',
        'module': 'stretching',
        'reference_image': 'warrior1.jpg',
        'benefits': ['Strengthens legs', 'Opens chest', 'Improves balance'],
        'cautions': ['Keep front knee over ankle', 'Engage core'],
        'ideal_angles': {'leftKnee': 90, 'rightKnee': 180, 'leftShoulder': 180, 'rightShoulder': 180},
        'hold_duration': 30,
        'instruction': 'Step back, bend front knee, raise arms overhead'
    },
    {
        'name': 'Triangle Pose (Trikonasana)',
        'module': 'stretching',
        'reference_image': 'triangle.jpg',
        'benefits': ['Stretches sides', 'Strengthens legs', 'Improves digestion'],
        'cautions': ['Keep both legs straight', 'Don\'t overextend'],
        'ideal_angles': {'leftKnee': 180, 'rightKnee': 180, 'leftShoulder': 90, 'rightShoulder': 90},
        'hold_duration': 25,
        'instruction': 'Extend arms, reach to the side, look up'
    },
    {
        'name': 'Child\'s Pose (Balasana)',
        'module': 'stretching',
        'reference_image': 'childs_pose.jpg',
        'benefits': ['Relaxes body', 'Stretches back', 'Calms mind'],
        'cautions': ['Use cushion if needed', 'Breathe deeply'],
        'ideal_angles': {'leftKnee': 45, 'rightKnee': 45, 'leftShoulder': 180, 'rightShoulder': 180},
        'hold_duration': 30,
        'instruction': 'Kneel down, sit on heels, extend arms forward'
    }
]

# Surya Namaskar Poses
surya_namaskar_poses = [
    {
        'name': 'Prayer Pose (Pranamasana)',
        'module': 'surya-namaskar',
        'reference_image': 'prayer_pose.jpg',
        'benefits': ['Centers mind', 'Improves focus'],
        'cautions': ['Breathe normally'],
        'ideal_angles': {'leftElbow': 90, 'rightElbow': 90, 'leftKnee': 180, 'rightKnee': 180},
        'hold_duration': 5,
        'instruction': 'Stand with palms together at chest'
    },
    {
        'name': 'Raised Arms (Hastauttanasana)',
        'module': 'surya-namaskar',
        'reference_image': 'raised_arms.jpg',
        'benefits': ['Stretches abdomen', 'Opens chest'],
        'cautions': ['Don\'t overarch'],
        'ideal_angles': {'leftShoulder': 180, 'rightShoulder': 180, 'leftElbow': 180, 'rightElbow': 180},
        'hold_duration': 5,
        'instruction': 'Raise arms overhead, arch back slightly'
    },
    {
        'name': 'Hand to Foot (Hasta Padasana)',
        'module': 'surya-namaskar',
        'reference_image': 'hand_to_foot.jpg',
        'benefits': ['Stretches back', 'Improves flexibility'],
        'cautions': ['Bend knees if needed'],
        'ideal_angles': {'leftKnee': 170, 'rightKnee': 170, 'leftShoulder': 90, 'rightShoulder': 90},
        'hold_duration': 5,
        'instruction': 'Bend forward, touch the ground'
    },
    {
        'name': 'Equestrian Pose (Ashwa Sanchalanasana)',
        'module': 'surya-namaskar',
        'reference_image': 'equestrian.jpg',
        'benefits': ['Strengthens legs', 'Opens hip flexors'],
        'cautions': ['Keep front knee over ankle'],
        'ideal_angles': {'leftKnee': 90, 'rightKnee': 180, 'leftShoulder': 180, 'rightShoulder': 180},
        'hold_duration': 5,
        'instruction': 'Step right leg back, look up'
    },
    {
        'name': 'Plank Pose (Dandasana)',
        'module': 'surya-namaskar',
        'reference_image': 'plank.jpg',
        'benefits': ['Strengthens core', 'Builds endurance'],
        'cautions': ['Keep body straight'],
        'ideal_angles': {'leftElbow': 180, 'rightElbow': 180, 'leftKnee': 180, 'rightKnee': 180},
        'hold_duration': 5,
        'instruction': 'Step back to plank position'
    },
    {
        'name': 'Eight Limbed Pose (Ashtanga Namaskara)',
        'module': 'surya-namaskar',
        'reference_image': 'eight_limbed.jpg',
        'benefits': ['Strengthens arms', 'Opens chest'],
        'cautions': ['Keep hips up'],
        'ideal_angles': {'leftElbow': 90, 'rightElbow': 90, 'leftKnee': 90, 'rightKnee': 90},
        'hold_duration': 5,
        'instruction': 'Lower knees, chest, and chin to ground'
    },
    {
        'name': 'Cobra Pose (Bhujangasana)',
        'module': 'surya-namaskar',
        'reference_image': 'cobra.jpg',
        'benefits': ['Strengthens spine', 'Opens chest'],
        'cautions': ['Don\'t overarch neck'],
        'ideal_angles': {'leftElbow': 150, 'rightElbow': 150, 'leftKnee': 180, 'rightKnee': 180},
        'hold_duration': 5,
        'instruction': 'Lift chest, look up'
    },
    {
        'name': 'Mountain Pose (Parvatasana)',
        'module': 'surya-namaskar',
        'reference_image': 'downward_dog.jpg',
        'benefits': ['Stretches entire body', 'Energizes'],
        'cautions': ['Keep heels down'],
        'ideal_angles': {'leftKnee': 180, 'rightKnee': 180, 'leftShoulder': 90, 'rightShoulder': 90},
        'hold_duration': 5,
        'instruction': 'Lift hips up, form inverted V'
    }
]

# Breathing Exercise
breathing_poses = [
    {
        'name': 'Seated Position (Sukhasana)',
        'module': 'breathing',
        'reference_image': 'sukhasana.jpg',
        'benefits': ['Prepares for breathing', 'Calms mind', 'Opens hips'],
        'cautions': ['Keep spine straight', 'Relax shoulders'],
        'ideal_angles': {'leftKnee': 90, 'rightKnee': 90, 'leftShoulder': 180, 'rightShoulder': 180},
        'hold_duration': 300,
        'instruction': 'Sit cross-legged with straight spine'
    }
]

# Insert all poses
all_poses = stretching_poses + surya_namaskar_poses + breathing_poses
db.poses.insert_many(all_poses)

print(f"✅ Successfully seeded {len(all_poses)} poses to the database!")
print(f"   - Stretching: {len(stretching_poses)} poses")
print(f"   - Surya Namaskar: {len(surya_namaskar_poses)} poses")
print(f"   - Breathing: {len(breathing_poses)} poses")
