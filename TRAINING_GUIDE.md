# 🥋 Master Training Guide: Creating the Unbeatable AI

To build the strongest "Anti-Lust" AI that no other app can beat, you need **Massive Scale** and **High Quality** data. Follow these exact steps.

## 📁 Step 1: Prepare Your Data Bunker
I have already created this folder for you. This is where all your raw intelligence goes.
`E:\Anti-Lust app\backend\data\`

---

## 🖼️ Step 2: The Vision System (NSFW Images)
**Goal:** The AI must see *everything* to block *everything*.
**Target Quantity:** 50,000+ Images.

### 1. Download "NudeNet Classifier Dataset"
This is the industry standard.
1.  **Go to:** [https://github.com/notAI-tech/NudeNet/releases](https://github.com/notAI-tech/NudeNet/releases)
2.  **Look for:** `classifier_data.zip` or similar large data links in the latest release notes.
3.  **Alternative (Kaggle):** Go to [Kaggle NudeNet Dataset](https://www.kaggle.com/datasets/dwdkills/nudenet-classifier-dataset)
4.  **Action:** Click **Download** (approx 2-3 GB).
5.  **Extract:** Unzip contents into `backend/data/nudenet/`.
    *   You should see folders like `/safe` and `/unsafe`.

### 2. Download "Raw SFW/NSFW"
1.  **Go to:** [https://www.kaggle.com/datasets/dvd758/nsfw-and-sfw-images-dataset](https://www.kaggle.com/datasets/dvd758/nsfw-and-sfw-images-dataset)
2.  **Action:** Click **Download**.
3.  **Extract:** Unzip to `backend/data/raw_images/`.

---

## 💬 Step 3: The Language Brain (Toxic Text)
**Goal:** Detect manipulation, aggression, and sexual grooming text.
**Target Quantity:** 100,000+ Comments.

### 1. Download "Jigsaw Toxic Comment History"
1.  **Go to:** [https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data)
2.  **Action:** Download `train.csv.zip`.
3.  **Extract:** Unzip `train.csv` to `backend/data/`.

### 2. Download "Civil Comments"
1.  **Go to:** [https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/data](https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/data)
2.  **Action:** Download `train.csv`.
3.  **Rename:** Rename to `civil_comments.csv` and place in `backend/data/`.

---

## 🔗 Step 4: The Web Guardian (Malicious URLs)
**Goal:** Block porn sites before they even load.
**Target Quantity:** 1 Million+ URLs.

### 1. Download "URLHaus Database"
1.  **Go to:** [https://urlhaus.abuse.ch/api/](https://urlhaus.abuse.ch/api/)
2.  **Find:** "Download CSV" (usually `csv.txt.zip`).
3.  **Direct Link:** [https://urlhaus.abuse.ch/downloads/csv_recent/](https://urlhaus.abuse.ch/downloads/csv_recent/)
4.  **Action:** Download and unzip to `backend/data/urlhaus.csv`.

### 2. Download "Shallalist" (The Old Guard)
1.  **Go to:** [http://www.shallalist.de/Downloads/shallalist.tar.gz](http://www.shallalist.de/Downloads/shallalist.tar.gz)
2.  **Action:** Download.
3.  **Extract:** Look for the `porn` and `gamble` folders. Copy the `domains` files to `backend/data/blacklists/`.

---

## 🏋️ Step 5: Train the Beast
Now that you have the data, you must feed it to the AI.

**Open your terminal (in `backend/` folder) and run:**

### Train Vision (Images)
```bash
# This will take hours. Do this overnight.
curl -X POST "http://localhost:8000/api/ml/train-file" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_secret_key" \
     -d '{"file_path": "backend/data/nudenet/", "data_type": "nsfw"}'
```

### Train Language (Text)
```bash
curl -X POST "http://localhost:8000/api/ml/train-file" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_secret_key" \
     -d '{"file_path": "backend/data/train.csv", "data_type": "text"}'
```

### Train Web (URLs)
```bash
curl -X POST "http://localhost:8000/api/ml/train-file" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_secret_key" \
     -d '{"file_path": "backend/data/urlhaus.csv", "data_type": "url"}'
```

## 🏆 The "Unbeatable" Standard
To be truly unbeatable, you need to reach these metrics (The AI will tell you this after training):
*   **Accuracy:** > 98.5%
*   **False Positives:** < 0.1% (Crucial! Don't block innocent stuff)
*   **Inference Time:** < 50ms

**Go now. The data awaits.**
