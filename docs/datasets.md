# SentinelAI Dataset Reference

This document lists the datasets required for Sprint 01.

---

# 1. Fraud Detection

## Credit Card Fraud Detection (ULB)

Purpose:
Fraud transaction classification.

Source:
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

License:
Open Database (Kaggle)

Status:
Pending Download

Store in:

datasets/transactions/

Filename:

creditcard.csv

---

## IEEE-CIS Fraud Detection

Purpose:
Large-scale fraud detection dataset.

Source:
https://www.kaggle.com/competitions/ieee-fraud-detection

License:
Kaggle Competition Terms

Status:
Pending Download

Store in:

datasets/transactions/

---

# 2. Scam SMS

## SMS Spam Collection

Purpose:
SMS spam classification.

Source:
https://archive.ics.uci.edu/dataset/228/sms+spam+collection

License:
UCI Dataset License

Status:
Pending Download

Store in:

datasets/sms/

---

## India-specific Scam SMS

Purpose:
Improve detection of Indian cyber fraud messages.

Examples:

- Digital Arrest
- Fake KYC
- Fake Bank Alert
- Lottery Scam
- Courier Scam
- Electricity Bill Scam

Source:
Self-collected and manually labeled.

Status:
Pending Collection

Store in:

datasets/sms/

---

# 3. Phishing URLs

## UCI Phishing Website Dataset

Purpose:
Website phishing detection.

Source:
https://archive.ics.uci.edu/dataset/327/phishing+websites

License:
UCI Dataset License

Status:
Pending Download

Store in:

datasets/phishing/

---

## PhishTank

Purpose:
Latest phishing URLs.

Source:
https://phishtank.org/

License:
PhishTank Terms of Use

Status:
Pending Download

Store in:

datasets/phishing/

---

# Notes

- Keep original downloaded files unchanged.
- Store only raw datasets during Sprint 01.
- Cleaning and preprocessing will be handled by `scripts/prepare_data.py`.
- Validation will be handled by `scripts/validate_datasets.py`.