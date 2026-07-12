# Scam Communication Agent

Production inference layer for SMS scam detection and phishing URL detection.

## Pipelines

### SMS Scam Detection
- **Model**: `CalibratedClassifierCV(LinearSVC(C=1))` — wraps a Linear SVM with isotonic calibration so `predict_proba` is available.
- **Vectorizer**: `TfidfVectorizer(max_features=10000, ngram_range=(1,2), sublinear_tf=True, lowercase=False)`
- **Preprocessing** (matches training notebook exactly):
  1. Strip URLs (`http://`, `https://`, `www.*`)
  2. Strip email addresses
  3. Strip phone numbers
  4. Remove non-alphanumeric characters
  5. Remove underscores
  6. Remove digit sequences
  7. Collapse whitespace
  8. NLTK tokenization → lemmatization → stop-word removal → length filter (`> 1`)

### Phishing URL Detection
- **Model**: XGBoost classifier saved via `joblib.dump`.
- **Features** (18 hand-crafted, matching training notebook):
  `url_length`, `domain_length`, `path_length`, `query_length`, `fragment_length`,
  `num_dots`, `num_hyphens`, `num_underscores`, `num_slashes`, `num_question_marks`,
  `num_equal`, `num_digits`, `num_special_chars`, `num_subdomains`, `https`,
  `has_ip`, `entropy` (Shannon), `suspicious_keyword_count`.

## Usage

```python
from agents.scam_comm_agent import predict_sms, predict_url, build_sms_verdict, build_url_verdict

# SMS
result = predict_sms("URGENT: Your account has been blocked. Click here.", case_id="c-001")
verdict = build_sms_verdict(result, case_id="c-001")

# URL
result = predict_url("http://192.168.0.1/login?user=admin", case_id="c-001")
verdict = build_url_verdict(result, case_id="c-001")
```

## Required Model Files

| Path | Description |
|------|-------------|
| `models/sms/sms_model.pkl` | Trained SMS classifier (joblib) |
| `models/sms/tfidf_vectorizer.pkl` | Fitted TF-IDF vectorizer (joblib) |
| `models/phishing/phishing_model.joblib` | Trained phishing URL classifier (joblib) |

## Configuration

All paths are configurable via environment variables (prefix: `SCAM_COMM_`):

| Variable | Default |
|----------|---------|
| `SCAM_COMM_SMS_MODEL_PATH` | `models/sms/sms_model.pkl` |
| `SCAM_COMM_TFIDF_PATH` | `models/sms/tfidf_vectorizer.pkl` |
| `SCAM_COMM_PHISHING_MODEL_PATH` | `models/phishing/phishing_model.joblib` |
| `SCAM_COMM_SMS_CONFIDENCE_THRESHOLD` | `0.70` |
| `SCAM_COMM_URL_CONFIDENCE_THRESHOLD` | `0.70` |
| `SCAM_COMM_LOG_LEVEL` | `INFO` |

## Dependencies

- `scikit-learn` — LinearSVC, CalibratedClassifierCV, TfidfVectorizer
- `xgboost` — XGBoost classifier
- `joblib` — model serialization/deserialization
- `nltk` — tokenization, lemmatization, stop words (punkt_tab, wordnet, omw-1.4, stopwords)
- `pydantic` / `pydantic-settings` — schema validation and configuration
- `numpy` — feature vector construction
