"""
Sentinel-X Vision Model Training Utility
========================================
Runs vision model training on user-provided datasets:
1. room.v1i.folder (702 room images)
2. 90-Degree Turn Detection.v1i.folder (672 turn/angle images)
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.core.dataset_trainer import vision_dataset_trainer

def main():
    print("================================================================")
    print("SENTINEL-X VISION MODEL TRAINING & CALIBRATION ENGINE")
    print("================================================================")
    print("Loading datasets:")
    print(" - room.v1i.folder")
    print(" - 90-Degree Turn Detection.v1i.folder")
    print("Extracting color profiles, Gabor edge signatures, and angle turns...")

    results = vision_dataset_trainer.execute_full_training()

    print("\nTraining Complete!")
    print(f"Total Images Processed: {results['metrics']['total_training_images']}")
    print(f"Room Classification Accuracy: {results['datasets']['room']['learned_room_signature']['room_classification_accuracy']}%")
    print(f"90-Degree Turn Accuracy: {results['datasets']['turn_detection']['learned_turn_signature']['turn_classification_accuracy']}%")
    print(f"Reality Fidelity Score: {results['metrics']['reality_fidelity_score']}%")
    print(f"Weights Exported to: {os.path.abspath('backend/app/models/trained_vision_weights.json')}")

if __name__ == "__main__":
    main()
