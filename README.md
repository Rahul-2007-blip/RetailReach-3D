# RetailReach 3D · AI & Discrete Mathematics Campaign Overlap Lab

**Experiential Learning Project · Module 1: Principle of Inclusion–Exclusion & Graph Theory**  
**Institution:** JAIN (Deemed-to-be University) · Faculty of Engineering and Technology  
**Department:** School of Computer Science and Engineering · **Section:** B. Tech CSE AIML - D  
**Course Code:** Discrete Mathematics and Graph Theory (`25BSMA10`)

---

### Academic Submission Details

- **Submitted To:**  
  **Dr. K J Ghanashyam**, Assistant Professor  
  Department of Data Analytics and Mathematical Sciences, Faculty of Engineering & Technology, Jain (Deemed-To-Be) University.

- **Submitted By (Student Team):**
  1. **SHREYAS S** — USN: `25BTRCL248` (System Architecture & Inclusion-Exclusion Engine)
  2. **SIDDHANT RAO** — USN: `25BTRCL251` (Deep Learning Overlap Predictor & Training Loop)
  3. **SAMPATH PHILIP GEORGE** — USN: `25BTRCL227` (3D Three.js Volumetric Venn & Particle Engine)
  4. **ROKESH VENKATESH** — USN: `25BTRCL213` (Graph Theory Topology, Centrality & Kruskal's MST)
  5. **RAHUL BISWAS** — USN: `25BTRCL205` (UCI Retail Data Engineering & Experimental Validation)
  6. **PRAVEEN KUMAR** — USN: `25BTRCL195` (Interactive Simulation Systems & Real-Time Bounds Evaluation)

---

## Overview

RetailReach is an interactive analytics suite and dynamic experiential learning application designed to demonstrate and operationalize the **Principle of Inclusion–Exclusion (PIE)**, **Discrete Graph Theory**, and **Deep Neural Networks** using real retail transaction data (541,909 transactions from the UCI *Online Retail* dataset).

### Core Features

1. **3D WebGL Spatial Lab (Three.js):**
   - **Mode 1: 3D Volumetric Venn Manifold:** Translucent glass-like intersecting spheres with glowing intersection lenses and raycasting tooltips.
   - **Mode 2: 3D Customer Particle Cloud:** 3,000 unique customer IDs mapped to spatial coordinate clusters based on set bitmasks.
   - **Mode 3: 3D Product Graph Topology:** Spherical 3D lattice of 24 products linked by volumetric laser beams representing shared customer volume.
2. **AI & Deep Learning Module (MLP & K-Means):**
   - In-browser Multi-Layer Perceptron (4-8-6-1) trained via Stochastic Gradient Descent to approximate audience overlap in $\mathcal{O}(1)$ time.
   - Interactive live loss curve updating on HTML5 Canvas across 90 training epochs.
   - Synaptic architecture SVG showing forward-pass activations.
   - Customer behavioral segmentation (K-Means into 4 distinct clusters).
3. **Discrete Graph Theory & Kruskal's MST:**
   - Product Co-purchase network $G=(V, E)$ with interactive canvas renderer.
   - Kruskal’s Maximum Spanning Tree (MST) algorithm to extract the core cross-selling catalog backbone.
   - Interactive $24 \times 24$ Adjacency Matrix Heatmap ($A[i][j] = |A_i \cap A_j|$).
   - Graph Centrality Metrics table (Degree Centrality, Weighted Degree, and Local Clustering Coefficient $C_i$).
4. **Exact Inclusion–Exclusion Solver:**
   - Evaluates all $2^n - 1$ combinatorial terms for up to 5 concurrent product sets ($A$ through $E$).
   - Dual-engine verification against an independent direct hash-set union.
   - Bonferroni Alternating Bounds convergence ladder ($S_1, S_1 - S_2, S_1 - S_2 + S_3, \dots$).
5. **Formal Academic Project Report:**
   - Complete 12-page PDF project report: [`RetailReach_Report.pdf`](RetailReach_Report.pdf).
   - Generated with official university headers, formatting, student USN tables, and IEEE references.

---

## Quickstart: How to Run

The application is completely self-contained and runs with any static web server:

```bash
# Navigate to project directory
cd "/home/requiem/Archimedes/Maths exp"

# Start local web server
python3 -m http.server 8000
```

Open your browser to: **<http://localhost:8000>**

To regenerate the PDF report at any time:
```bash
python3 scripts/generate_pdf_report.py
```

---

## Project Structure

```
├── index.html                   # Main interactive web application shell
├── styles.css                   # Cyber-academic dark design system
├── app.js                       # Core application state & PIE engine
├── three-viz.js                 # Three.js 3D WebGL spatial visualization engine
├── ml-engine.js                 # Deep neural network overlap predictor & clustering
├── graph-viz.js                 # Graph theory network, Kruskal MST & centrality
├── data/
│   └── retailreach-data.json    # 232 KB clean inverted index (24 products, 50 cohorts)
├── assets/
│   ├── jain_header.png          # Official Jain University header image
│   └── submitted_to.png         # Submitted To Dr. K J Ghanashyam image
├── scripts/
│   ├── prepare_data.py          # UCI Excel preprocessor
│   └── generate_pdf_report.py   # Publication-quality HTML to PDF generator
├── EXPERIENTIAL_REPORT.md       # Full detailed academic report markdown
├── report.html                  # Styled HTML report with print CSS
└── RetailReach_Report.pdf       # 12-page formal project PDF report
```
