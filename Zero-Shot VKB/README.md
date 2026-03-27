# A Visual Knowledge Base Framework for Interpretable Zero-Shot Scene Classification

> **Author**: Pavan Kolasani  
> **Institution**: Technological University Dublin  
> **Degree**: M.Sc. in Computer Science (Data Science)  
> **Date**: September 2025  

An interpretable, end-to-end computer vision pipeline that performs zero-shot scene classification by intelligently mapping local object detections to global scene definitions using robust statistics and YOLOv8 architectures.

## Overview
This repository contains the official codebase and evaluation framework for the dissertation **"A Visual Knowledge Base Framework for Interpretable Zero-Shot Scene Classification"**. 

Traditional deep convolutional models (like ResNet or ViT) achieve high accuracy on large-scale datasets such as ImageNet and Places365, but they require extensive labelled training data and lack interpretability. This project introduces an alternative **Visual Knowledge Base (VKB)** paradigm. By automatically detecting objects in an image and weighting them against this VKB, the system successfully classifies complex scenes **without direct training on scene labels**, providing transparent and accountable predictions.

## Dataset Specification
Evaluated on a curated, balanced subset of the **Places365 dataset**:
- **8 Categories**: Bedroom, Kitchen, Office, Supermarket, Bus Station, Train Station, Highway, and Living Room.
- **Scale**: 4,400 images total (resized to 640x640 pixels).
- **Split**: 500 images per class for VKB construction (4,000 total) and 50 images per class for zero-shot testing (400 total).

---

## Technical Architecture

The methodology operates in two primary stages:

### Stage 1: VKB Construction (Training Phase)
We extract a semantic understanding of scenes by scanning the training split:
- **Object Detection:** Executes `YOLOv8-Large` (`yolov8l.pt`) to generate bounding boxes. Only the maximum-confidence instance per object class is retained to avoid duplicate-box inflation.
- **Robust Aggregation:** Groups images by scene and calculates detection frequency alongside **trimmed-mean confidence** (trimming at $t_s = \min(0.10, 10/N_s)$ per tail) to mitigate outliers.
- **TF-IDF Weighting:** Computes distinctiveness using an Inverse Document Frequency (IDF) mechanism to down-weight ubiquitous objects (e.g., "person") and highly reward diagnostic cues. 
  - $idf(o) = \log((S+1)/(df(o)+1)) + 1$
- **VKB Compilation:** Retains the smallest ranked set of key objects covering **90%** of the scene's cumulative evidence. This is followed by $\ell_1$ Normalisation to ensure fair cross-scene comparability.

### Stage 2: Zero-Shot Classification
When classifying an unseen test image:
- YOLO extracts the semantic objects present in the frame.
- The pipeline scores the image against all VKB scene profiles using an L1-normalized intersection score:
  - $S(I, s) = \sum conf(o) \times w(o, s)$
- **Abstention (Reject Option):** The class with the highest score is declared via `argmax`. However, if no detected object overlaps with any VKB profile (score = 0), the system outputs **"unknown"** rather than forcing a low-confidence guess.

---

## Evaluation & Results

The framework was rigorously evaluated against the 400 held-out test images. All outputs were saved in JSON format for explicit, object-grounded audit trails.

| Metric | Result |
|--------|--------|
| **Top-1 Accuracy** (strict; unknown counted as wrong) | **68.50%** |
| **Valid Predictions Accuracy** (excluding abstentions) | **77.00%** |
| **Top-2 Containment** | **80.25%** |
| **Abstention Rate** | **10.75%** |

**Empirical Insights:**
- **Distinctive Anchors:** Classes with unique objects (Bedroom, Bus Station) reached near-ceiling F1 scores (0.95).
- **Ambiguous Environments:** Object lists struggle without spatial layout context. Dense offices were routinely confused for supermarkets, and kitchens overlapped with living rooms due to shared indoor furniture.
- **Ablation Studies:** Demonstrated that disabling IDF weighting, replacing weights with a uniform distribution (dropped Top-1 to 50%), or removing the abstain rule severely degraded reliability and accuracy, proving the robust statistical design.

---

## Repository Structure & Usage

This project is built to execute inside **Google Colab** to utilize `cuda` memory for YOLO. 

### Prerequisites
```bash
pip install -r requirements.txt
```

### Execution Steps
1. Upload the analysis `.ipynb` notebook into Google Colab.
2. Mount your Google Drive where your Places365 subset resides.
3. Update `DATA_ROOT` and `CLEAN_VKB_PATH` to point to your image folders.
4. Execute the cells sequentially. 
5. Outputs will include VKB JSON dictionaries, ablation results, and structured prediction logs detailing the exact mathematical justification for every classification.

---
## 🔒 Version Control
This repository utilizes a strict `.gitignore` to prevent massive Machine Learning weights (`*.pt`), raw image datasets, and generated cache dictionaries from ballooning the Git history. The `.ipynb` file safely retains its cell outputs for immediate review.
