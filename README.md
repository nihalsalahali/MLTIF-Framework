# MLTIF: A Multi-Layer Traffic Inspection Framework for Real-Time Detection and Adaptive Mitigation of Multi-Phase Cyberattacks in Distributed SD-IoT Networks

**MLTIF** is a modular, intelligent, and distributed framework for detecting, classifying, and mitigating multi-phase attacks (reconnaissance, exploitation, disruption) in Software-Defined IoT networks. It integrates programmable data planes (P4) with distributed SDN controllers and an ensemble ML-based threat classifier for real-time response and mitigation.

---

##  Core Modules

### 1️⃣ ITAM (Intelligent Traffic Analysis Module)
- Written in P4_16 for BMv2 and P4 hardware targets.
- Extracts advanced flow and packet features: IPs, flags, payload size, entropy estimates, and timing.
- Exports extracted metadata to the controller for higher-layer inspection.

### 2️⃣ ATDM (Advanced Threat Detection Module)
- Ensemble ML classifier combining Decision Tree, Q-CNN, SNN , and Logistic Regression meta-learner.
- Performs phase-aware multi-stage threat classification using temporal correlation.
- Outputs structured alerts with confidence scores and phase classification.

### 3️⃣ AMCM (Adaptive Mitigation and Controller Collaboration Module)
- Receives alerts and applies mitigation strategies:
  - Quarantine traffic
  - Apply rate limiting
  - Update switch flow tables
- Synchronizes mitigation policies across distributed controllers (Ryu, ONOS, or Java-based).
- Implements resilience via master-controller failover and heartbeat sync.

---

## 📂 MLTIF Repository Structure

```plaintext
mltif-framework/
├── itam/                      # P4 feature extractor
│   └── itam.p4
├── atdm/                      # ML training + inference
│   ├── ensemble_trainer.py
│   ├── online_detector.py
│   └── notebooks/
│       └── train_atdm.ipynb
├── amcm/                      # Mitigation logic
│   ├── mitigation_policy_engine.py
│   ├── controller_sync.py
│   └── actions/
│       ├── rate_limit.py
│       ├── quarantine_flow.py
│       └── update_flow_table.py
├── runtime/                   # Orchestrator & control
│   ├── mltif_controller.py
│   ├── flow_rules.json
│   ├── mltif_alert.json
│   └── metrics_logger.py
├── configs/                   # Policy & control config
│   ├── p4info.txt
│   ├── bmv2.json
│   ├── itam_config.yaml
│   ├── atdm_config.yaml
│   └── amcm_policy.yaml
├── datasets/                  # For ML training data
├── LICENSE
├── Makefile
└── README.md
```

---

## ⚙️ Deployment Instructions

###  1. Build the P4 Pipeline
```bash
make p4-compile
```

###  2. Launch BMv2 Switch with gRPC
```bash
simple_switch_grpc --device-id 0 -i 0@veth0 -i 1@veth1 configs/bmv2.json
```

###  3. Start MLTIF Runtime Controller
```bash
python3 runtime/mltif_controller.py
```

###  4. Train ATDM Models
```bash
python3 atdm/ensemble_trainer.py
# or
jupyter notebook notebooks/train_atdm.ipynb
```

###  5. Run Online Detector
```bash
python3 atdm/online_detector.py
```

###  6. Enable Multi-Controller Sync (Optional)
```bash
python3 amcm/controller_sync.py
```

###  7. Start SDN Controllers
- Python: `ryu-manager mltif_controller.py`
- Java: Deploy into ONOS/Floodlight

###  8. Activate Mitigation Logic
```bash
python3 amcm/mitigation_policy_engine.py
```

---

## 📎 Key Config Files

- `itam_config.yaml` – P4 timing and entropy thresholds  
- `atdm_config.yaml` – ML confidence + model parameters  
- `amcm_policy.yaml` – Mitigation triggers (quarantine, rate-limit)  
- `bmv2.json`, `p4info.txt` – BMv2 pipeline & controller interface  

---

## ⚡ Dependencies

- Python 3.x  
- `p4lang/p4c` (P4 compiler)  
- BMv2 (`simple_switch_grpc`)  
- Python libraries:
  - `scikit-learn`, `xgboost`, `joblib`, `numpy`, `requests`  
  - `grpcio`, `p4runtime_lib`  

---

## 🔐 Secure SD-IoT in Real-Time

MLTIF empowers your SDN-based IoT infrastructure to:
- Detect stealthy, multi-phase intrusions
- React with real-time, distributed mitigation
- Scale with controller clusters and programmable data planes

 Run MLTIF in Mininet or on real P4 hardware today!

---

