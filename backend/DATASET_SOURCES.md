# 🛡️ Real-Life Dataset Sources for Anti-Lust Guardian

To make the AI "the strongest," you need high-quality, diverse datasets. Here are the best sources for real-world data to train the models.

## 1. NSFW Image Datasets (Computer Vision)
These datasets are used to train the `NSFWDetector` (ResNet/EfficientNet/CLIP).

*   **NudeNet Dataset:** A massive collection of labeled NSFW images.
    *   **Source:** [GitHub - NudeNet](https://github.com/notAI-tech/NudeNet) (Check releases/links)
    *   **Usage:** Use for training the object detection and classification heads.
*   **NSFW Data Scraper:** A collection of scripts to scrape Reddit/Imgur for labeled NSFW content.
    *   **Source:** [GitHub - ebony72/nsfw_data_scraper](https://github.com/ebony72/nsfw_data_scraper)
    *   **Warning:** Requires careful cleaning.
*   **Kaggle NSFW Detection:** Various community datasets.
    *   **Source:** [Kaggle - NSFW Detection](https://www.kaggle.com/search?q=nsfw+detection)

## 2. Toxic Text Datasets (NLP)
These datasets are used to train the `TextClassifier` (BERT/RoBERTa).

*   **Jigsaw Toxic Comment Classification Challenge:** The gold standard for toxicity detection.
    *   **Source:** [Kaggle - Jigsaw Toxic Comment](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data)
    *   **Content:** Wikipedia comments labeled as toxic, severe_toxic, obscene, threat, insult, identity_hate.
*   **Hate Speech and Offensive Language:**
    *   **Source:** [HuggingFace - tweet_eval](https://huggingface.co/datasets/tweet_eval)
    *   **Content:** Tweets labeled for hate speech and offensive language.
*   **Civil Comments:**
    *   **Source:** [TensorFlow Datasets](https://www.tensorflow.org/datasets/catalog/civil_comments)

## 3. Malicious URL Datasets
These datasets are used to train the `URLAnalyzer`.

*   **URLHaus:** A project from abuse.ch with massive lists of malware URLs.
    *   **Source:** [URLHaus Database](https://urlhaus.abuse.ch/browse/)
*   **PhishTank:** A collaborative clearing house for data and information about phishing on the Internet.
    *   **Source:** [PhishTank Developer Info](https://www.phishtank.com/developer_info.php)
*   **Shallalist:** A huge blacklist of domains divided by category (porn, gamble, etc.).
    *   **Source:** [Shallalist](http://www.shallalist.de/)

## 🚀 How to Use
1.  **Download** the dataset (e.g., `toxic_comments.csv`).
2.  **Place** it in `backend/data/`.
3.  **Run** the training command (I have added a new feature for this):
    ```bash
    # Example
    POST /api/ml/train-file
    {
      "file_path": "backend/data/toxic_comments.csv",
      "type": "text"
    }
    ```
