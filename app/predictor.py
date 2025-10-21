# predictor.py - Loads the trained model and provides a helper function for email prediction

import os
import joblib
from app.models import EmailToWordCounterTransformer, WordCounterToVectorTransformer

# Path to the saved pipeline + classifier
MODEL_FILENAME = os.path.join(os.path.dirname(__file__), "..", "spam_model.pkl")

# Load pipeline and classifier
pipeline, classifier = joblib.load(MODEL_FILENAME)

def predict_email(text: str, subject: str = None):
    """
    Accepts raw email text (and optional subject), transforms it using the
    saved preprocessing pipeline, and returns spam prediction + probability.
    """
    from app.preprocess import make_email_message_from_text, email_to_text

    # Wrap text into EmailMessage and convert to plain text
    msg = make_email_message_from_text(text, subject)
    X = [email_to_text(msg)]

    # Transform to numerical vector and predict
    X_vec = pipeline.transform(X)
    pred = int(classifier.predict(X_vec)[0])
    prob = classifier.predict_proba(X_vec)[0][1]

    return {"prediction": pred, "spam_probability": float(prob)}
