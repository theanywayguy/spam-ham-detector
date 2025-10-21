# config.py - stores project-wide constants and file paths

import os

# Base directory of the project (one level above app/)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Full path to the trained spam classifier model
MODEL_FILENAME = os.path.join(BASE_DIR, "spam_classifier.pkl")

# Maximum vocabulary size used in vectorizing emails
VOCABULARY_SIZE = 1000
