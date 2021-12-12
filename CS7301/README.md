# AGE-GNN: Adversarial Generator using Graph Neural Network for ML Evasion

## Resource

- Paper:

- Dataset for training/testing/validation:

- Code: See [Doc2Vec](Doc2Vec), [AutoEncoder](AutoEncoder), [LOF](LOF), [Gadget](Gadget)

- Pre-trained Model:

## INTRODUCTION

Signature-based and network-based fail miserable against stealthy attacks such as **zero-day vulnerability**, **malware mutants** and **advanced persistent threats (APTs) attacks**. Simple machine Learning based detectors such as SVM, PCA, ensemble methods such as bagging/boosting and **local outlier factor(LOF)** have been used to detect these advanced threats but they have also been defeated by specifically crafted APTs. Current and on-going work has been using two prominent ML technique called **Variational Auto Encoders(VAE)** and Graph Neural Network(GNN) based anomaly detection.

We propose AGE-GNN, a systematic approach that re-examines the current practices of ML-based security by considering **advanced active adversaries** who focus on exploiting the weaknesses of ML based security  through evasive attacks. In particular, we assume an adversary who seeks to extend the **APT-style attack campaign** by integrating a series of **advanced attack vectors** into a single attack scenario to avoid being detected by the ML-based security model. The
adversary uses system data to replace the attack vectors with attack constructs which we name as **APT-gadget** (or in short *gadget*). In this sense, the APT-gadget defines a structure that carries **malicious semantics** when executed in reference to the APT-attack but is naturally deemed **benign within the context** of the target system. We evaluated AGE-GNN with a **realistic APT scenario** to confirm our research insight.

### ML BASED DETECTION FRAMEWORK
<img src="./assets/ml-detection-workflow.png" alt=": Detection workflow of ML based detector"   width="700"/>

The Machine Learning framework for different models have different specifics but the overall framework is same. They first train a model with **benign system** activity and then uses it to classify system activities with the goal that system or user process that have been *hijacked* by malware(e.g., attacker) will show *abnormal system activity* that can be identified. It is clear that for attackers to cause harm or do their bidding, they will have to interact with system entities like files, network sockets and processes. These **interaction or behavior** would be **different** than the benign program’s normal behavior and this insights has motivated the latest ML based detection models.

## MOTIVATIONAL APT ATTACK STUDY
<img src="./assets/apt.png" alt="Provenance graph for APT attack vs APT with gadget"   width="500"/>

## APPROACH

### GADGET FINIDING & RANKING
<img src="./assets/gadget-rank.png" alt="APT attack stages using gadget chain and their regularity score"   width="800"/>

### GADGET APT ATTACK CREATION
<img src="./assets/gadget-find.png" alt="Regularity Score calculation for causal paths for APT attack vs APT attack with gadgets"   width="500"/>

## DATASET

### Benign Dataset

We selected 30 system programs from our event database that are commonly used in APT campaigns also mentioned in previous studies such as ProvDetector. The provenance graphs generated from the benign system programs consisted of 4735.30 causal paths, 37.51 vertices and 45.78 edges on average (Table 3). The provenance graph generated from the benign user application consisted of 11779.36 causal paths, 90.36 vertices and 112.38 edges on average (Table 3).

<img src="./assets/benign-data.png" alt="Number of vertex and edges used to create benign profile for system programs"   width="500"/>

### Malicious Dataset
The anomaly dataset contains two datasets: APT attack campaign and APT attack campaign with gadget. The APT attack campaign with gadget consists of the APT attack that was conducted using the gadget mentioned in column events in APT Stages using Gadget Chain 1 Table 2.We used a malicious testbed to collect labeled datasets necessary for prediction tasks by running five different kinds of APT attack stages with and without gadgets. 

The provenance graphs for APT Kill Chain Scenario contains an average of 493.92 causal paths, 94.78 vertices and 97.48 edges. The provenance graphs for APT Kill Chain Scenario with Gadget has an average of 175.93 causal paths, 30.39 vertices and 29.50 edges.

<img src="./assets/mal-data.png" alt="Number of vertex and edges used to create malicious APT and gadget APT profile"   width="500"/>

## EVALUATION

### Detection Accuracy
<img src="./assets/result-1.png" alt=": ML-based behavior models’ (LOF and autoencoder) detection results for APT attack and APT attack with gadget"   width="400"/>

### Degree of Evasiveness for APT Stages
<img src="./assets/result-2.png" alt="F1 score for APT attack stage with gadget detection"   width="400"/>

# Citation

```
@Inproceedings{kunal2021,
author = {Mukherjee, Kunal},
title = {AGE-GNN: Adversarial Generator using Graph Neural Network for ML Evasion},
year = {2021},
isbn = {},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {},
doi = {},
booktitle = {Proceedings of the ACM/IEEE 43nd International Conference on Software Engineering},
pages = {},
numpages = {13},
keywords = {System Security, Variational AutoEncoders, Graph Neural Network,
Adversarial Example},
location = {},
series = {CCS '21}
}
```
