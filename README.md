
# Spam Email Classification with Logistic Regression — Full-Stack App

This project has been converted into a **simple full-stack web application** with a FastAPI backend and a Tailwind-based front-end. The app is **dockerized for easy deployment**.
Access the live app here: `(https://spam-detector-wxce.onrender.com/)`

---

## Spam Email Classification with Logistic Regression

This project builds a **spam detector** using raw email data from the SpamAssassin public corpus. The pipeline includes **data preprocessing, feature engineering, model training, and evaluation**.

---

### **1. Dataset**

* Downloaded ham (`easy_ham`) and spam (`spam`) emails.
* Extracted from `.tar.bz2` archives.
* Parsed emails with Python’s `email` module, preserving headers and MIME content.

---

### **2. Email Preprocessing**

* Extract text from emails:

  * Plain text: use directly.
  * HTML: cleaned using `BeautifulSoup`, removed `<head>`, replaced links with `"HYPERLINK"`.
* Normalize text:

  * Lowercasing.
  * Remove punctuation.
  * Replace URLs with `"URL"`.
  * Replace numbers with `"NUMBER"`.
  * Apply stemming (Porter Stemmer).

---

### **3. Feature Engineering**

* Convert emails → **word count dictionaries** (bag-of-words).
* Build a **shared vocabulary** of most frequent words across all emails.
* Convert word counts → **numerical vectors**:

  * Each vector dimension represents a word in the vocabulary.
  * Sparse representation used for efficiency.

---

### **4. Labels**

* Ham emails → `0`
* Spam emails → `1`
* Split dataset: 80% training, 20% testing.

---

### **5. Model Training**

* Logistic Regression classifier trained on the vectorized emails.
* Model learns **weights for each word**:

  * Positive weight → word indicative of spam.
  * Negative weight → word indicative of ham.
* Decision for new email:

  1. Compute weighted sum of word counts + bias.
  2. Apply sigmoid to get probability of spam.
  3. Predict spam if probability > 0.5, otherwise ham.

**Score formula:**

score = Σ (word_count × word_weight) + bias


---

### **6. How the Model Handles Words**

1. **Word Weights and Scoring**

   * Each email vector is multiplied by learned word weights to compute a **spam score**.
   * Words with higher positive weights push the score toward spam; negative weights push toward ham.
   * Overlapping words (present in both ham and spam emails) get weights proportional to their correlation with spam.

2. **Shared Vocabulary Across Ham and Spam**

   * Only **one vocabulary** is used; not separate for ham and spam.
   * Example:

     * `"meeting"` mostly in ham → negative weight → reduces spam score.
     * `"free"` mostly in spam → positive weight → increases spam score.
   * Neutral or rare words get small weights → minimal effect.

---

### **7. Illustrative Example**

Suppose our vocabulary has **4 words**: `["free", "meeting", "click", "project"]`.

| Word    | Weight (learned) |
| ------- | ---------------- |
| free    | +2.0             |
| meeting | -1.5             |
| click   | +1.8             |
| project | -0.5             |

#### **Email A (spam)**

```
"Free click here!"
Word counts: {"free": 1, "click": 1}
Score = 1*2.0 + 1*1.8 + 0*(-1.5) + 0*(-0.5) + bias
      = 3.8 + bias
P(spam) = sigmoid(3.8 + bias) ≈ high → classified as spam
```

#### **Email B (ham)**

```
"Meeting about the project"
Word counts: {"meeting": 1, "project": 1}
Score = 0*2.0 + 0*1.8 + 1*(-1.5) + 1*(-0.5) + bias
      = -2.0 + bias
P(spam) = sigmoid(-2.0 + bias) ≈ low → classified as ham
```

**Detailed Explanation of Email B Score:**

1. **Word Counts:** Count how many times each vocabulary word occurs:

   | Word    | Count |
   | ------- | ----- |
   | free    | 0     |
   | click   | 0     |
   | meeting | 1     |
   | project | 1     |

2. **Multiply by Learned Weights:**

   ```
   free: 0*2.0 = 0
   click: 0*1.8 = 0
   meeting: 1*(-1.5) = -1.5
   project: 1*(-0.5) = -0.5
   ```

3. **Add Bias:**

   ```
   Score = -1.5 + (-0.5) + bias = -2.0 + bias
   ```

4. **Convert to Probability:**

   ```
   P(spam) = 1 / (1 + exp(-score)) ≈ low
   ```

5. **Prediction:** Low probability → classified as ham.

**Key points demonstrated:**

* Words shared in both ham and spam (“project”) influence the score based on their **learned weight**.
* Logistic regression combines all word contributions to compute the final spam probability.
* Each word’s contribution = `count * weight`. Bias shifts overall probability to improve accuracy.

---

### **8. Evaluation**

* Cross-validation on training set to estimate performance.
* Tested on unseen test emails.
* Metrics reported:

  * **Precision:** % of predicted spam that is actually spam.
  * **Recall:** % of actual spam correctly detected.

---

**Outcome:** A classical ML spam classifier using **bag-of-words features**, logistic regression, and shared vocabulary with learned word weights, capable of distinguishing ham and spam based on word patterns, now **available as a full-stack web app with Docker deployment**.

**Live demo link:** `(https://spam-detector-wxce.onrender.com/)`
