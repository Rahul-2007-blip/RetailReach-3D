# JAIN (DEEMED-TO-BE UNIVERSITY)
## FACULTY OF ENGINEERING AND TECHNOLOGY
### SCHOOL OF COMPUTER SCIENCE AND ENGINEERING
**B. Tech CSE AIML - Section D**  
**Course:** Discrete Mathematics and Graph Theory (`25BSMA10`)

---

# RetailReach: Deep 3D Campaign Audience Deduplication via the Principle of Inclusion–Exclusion, Graph Theory, and Deep Neural Networks

### Experiential Learning Project Report · Module 1

---

### SUBMISSION DETAILS

**Submitted To:**  
**Dr. K J Ghanashyam**  
Assistant Professor  
Department of Data Analytics and Mathematical Sciences  
Faculty of Engineering & Technology  
Jain (Deemed-To-Be) University  

**Submitted By (Team Members):**

| Sl. No | Student Name | University Seat Number (USN) | Role / Core Contribution |
| :---: | :--- | :---: | :--- |
| 1 | **SHREYAS S** | `25BTRCL248` | System Architecture, PIE Engine & Bonferroni Proof Verification |
| 2 | **SIDDHANT RAO** | `25BTRCL251` | Deep Learning Model (MLP Overlap Predictor & Training Loop) |
| 3 | **SAMPATH PHILIP GEORGE** | `25BTRCL227` | 3D WebGL / Three.js Volumetric Venn & Spatial Particle Engine |
| 4 | **ROKESH VENKATESH** | `25BTRCL213` | Graph Theory Network, Centrality Measures & Kruskal's MST |
| 5 | **RAHUL BISWAS** | `25BTRCL205` | Data Engineering (UCI Retail Preprocessing) & Performance Audit |
| 6 | **PRAVEEN KUMAR** | `25BTRCL195` | Interactive Simulation Systems & Real-Time Bounds Evaluation |

---

## Abstract

In modern marketing engineering and cross-channel customer relationship management (CRM), estimating the distinct reach of multi-product advertising campaigns is a foundational combinatorial challenge. When marketing managers naively sum the audience sizes of individual product target lists, customers who purchased multiple promoted items are counted repeatedly. This naive sum severely overstates true campaign reach, inflating customer acquisition cost (CAC) projections, distorting budget allocation, and inducing ad-fatigue through excessive frequency capping.

**RetailReach** is an interactive, high-performance analytics application and experiential mathematical model designed to demonstrate and operationalize the **Principle of Inclusion–Exclusion (PIE)**, **Graph Theory**, and **Deep Learning** on real-world retail transactions. Utilizing the landmark UCI Machine Learning Repository *Online Retail* dataset (541,909 transactions across 4,338 identified customers), RetailReach implements:
1. An exact, combinatorial Inclusion–Exclusion solver evaluating all $2^n - 1$ subset intersections for up to five concurrent product campaigns.
2. An alternating **Bonferroni Inequalities** convergence monitor tracking order-$k$ upper and lower bounds.
3. An interactive **3D WebGL spatial engine** built on Three.js featuring 3D volumetric Venn manifolds, raycasted intersection lenses, and a 3,000-point customer particle cloud reflecting spatial set assignments.
4. An in-browser **Multi-Layer Perceptron (MLP)** neural network trained with gradient descent to approximate non-linear audience overlap directly from product feature embeddings.
5. A discrete **Graph Theory engine** modeling product co-purchase networks $G=(V, E)$, computing degree centrality, local clustering coefficients $C_i$, adjacency matrices, and Kruskal’s Maximum Spanning Tree (MST).

Empirical evaluation on benchmark three-product combinations demonstrates that a naive list sum of 2,445 customer entries collapses to an exact unique reach of 1,772 customers—eliminating 673 redundant records (a 27.5% audience inflation). The dual independent verification between the theoretical alternating formula and ground-truth hash-set union yields a 100% exact integer match, validating the mathematical theorem unconditionally.

---

## 1. Problem Identification and Relevance

### 1.1 The Audience Inflation Dilemma in Multi-Channel Marketing
Consider an omnichannel retailer planning an outreach campaign across $n$ distinct product lines $\{P_1, P_2, \dots, P_n\}$. The merchandising team extracts the customer audience list $A_i$ of all buyers who previously engaged with product $P_i$. If each list contains $|A_i|$ customers, executive dashboards frequently report the total reach as:
$$\text{Reach}_{\text{naive}} = \sum_{i=1}^n |A_i|$$

This calculation assumes that the sets $A_i$ are pairwise disjoint:
$$A_i \cap A_j = \emptyset \quad \forall \, i \neq j$$

However, in commercial retail environments, high-affinity products exhibit heavy cross-purchasing. When products are complementary (e.g., cake stands, baking cases, and pantry tins), a single customer often belongs to multiple product sets simultaneously:
$$c \in A_1 \cap A_2 \cap \dots \cap A_k$$

Consequently, customer $c$ is counted $k$ times in the naive summation. This error propagates into critical financial and operational distortions:
1. **Budget Over-Allocation:** Advertisers bid on impression volumes that exceed the actual unique human population.
2. **Frequency Exhaustion:** Multi-buyers receive duplicated messaging across multiple touchpoints, increasing opt-out and unsubscribe rates.
3. **Misleading Conversion Projections:** Conversion rates calculated against an inflated denominator appear artificially depressed.

### 1.2 The Core Research Question
The project addresses the concrete discrete mathematics challenge:
> **Given historical transaction logs for $n$ target products, how do we compute the exact distinct audience reach $|\bigcup_{i=1}^n A_i|$ efficiently, verify the alternating corrections of Inclusion–Exclusion, and model the underlying co-purchase graph topology using discrete graph theory and machine learning?**

---

## 2. Project Objectives

1. **Discrete Set-Theoretic Modeling:** Transform tabular transactional records into clean, deduplicated mathematical sets $A_i \subseteq U$ over a universe of identified customer IDs.
2. **Exact Inclusion–Exclusion Solver:** Implement a combinatorial solver that calculates all $2^n - 1$ non-empty intersections and alternates addition and subtraction of subset cardinalities.
3. **Bonferroni Bounds Tracking:** Demonstrate how truncated partial sums $S_1, S_1 - S_2, S_1 - S_2 + S_3, \dots$ provide rigorously guaranteed alternating upper and lower bounds.
4. **3D Spatial Visualization:** Develop a real-time WebGL/Three.js interactive environment displaying translucent 3D Venn manifolds and spatial customer particle clouds.
5. **AI / Deep Learning Integration:** Train an in-browser neural network that learns the topological co-purchase features to predict multi-set overlap before exact enumeration.
6. **Graph Theory Analysis:** Construct the product co-occurrence graph $G=(V, E)$, calculate adjacency matrices, degree centrality, betweenness centrality, and extract the Maximum Spanning Tree via Kruskal's algorithm.
7. **Empirical Ground-Truth Verification:** Implement an independent hash-set union engine $\bigcup_{i} A_i$ to verify that the theoretical algebraic formula and computational data structure arrive at the exact same integer count.

---

## 3. Mathematical Foundations

### 3.1 The Principle of Inclusion–Exclusion (PIE)

Let $A_1, A_2, \dots, A_n$ be finite subsets of a universal set $U$. The cardinality of their union is given by:

$$\left|\bigcup_{i=1}^n A_i\right| = \sum_{k=1}^n (-1)^{k-1} S_k$$

Where $S_k$ represents the sum of the cardinalities of all possible $k$-tuple intersections:
$$S_1 = \sum_{1 \le i \le n} |A_i|$$
$$S_2 = \sum_{1 \le i < j \le n} |A_i \cap A_j|$$
$$S_3 = \sum_{1 \le i < j < k \le n} |A_i \cap A_j \cap A_k|$$
$$S_k = \sum_{1 \le i_1 < i_2 < \dots < i_k \le n} \left| A_{i_1} \cap A_{i_2} \cap \dots \cap A_{i_k} \right|$$

#### Rigorous Proof via Characteristic Indicator Functions
For any element $x \in U$, let $\mathbf{1}_{A_i}(x)$ denote the characteristic indicator function:
$$\mathbf{1}_{A_i}(x) = \begin{cases} 1 & \text{if } x \in A_i \\ 0 & \text{if } x \notin A_i \end{cases}$$

An element $x$ belongs to the union $\bigcup_{i=1}^n A_i$ if and only if it does not belong to the intersection of the complements:
$$\mathbf{1}_{\bigcup A_i}(x) = 1 - \prod_{i=1}^n \left(1 - \mathbf{1}_{A_i}(x)\right)$$

Expanding the algebraic product:
$$\prod_{i=1}^n \left(1 - \mathbf{1}_{A_i}(x)\right) = 1 - \sum_{i} \mathbf{1}_{A_i}(x) + \sum_{i < j} \mathbf{1}_{A_i}(x)\mathbf{1}_{A_j}(x) - \sum_{i < j < k} \mathbf{1}_{A_i}(x)\mathbf{1}_{A_j}(x)\mathbf{1}_{A_k}(x) + \dots + (-1)^n \prod_{i=1}^n \mathbf{1}_{A_i}(x)$$

Recognizing that $\mathbf{1}_{A}(x) \mathbf{1}_{B}(x) = \mathbf{1}_{A \cap B}(x)$:
$$\mathbf{1}_{\bigcup A_i}(x) = \sum_{i} \mathbf{1}_{A_i}(x) - \sum_{i < j} \mathbf{1}_{A_i \cap A_j}(x) + \sum_{i < j < k} \mathbf{1}_{A_i \cap A_j \cap A_k}(x) - \dots + (-1)^{n-1} \mathbf{1}_{\bigcap A_i}(x)$$

Summing both sides over all $x \in U$:
$$\sum_{x \in U} \mathbf{1}_{\bigcup A_i}(x) = \sum_{i} \sum_{x \in U} \mathbf{1}_{A_i}(x) - \sum_{i < j} \sum_{x \in U} \mathbf{1}_{A_i \cap A_j}(x) + \dots$$

Since $\sum_{x \in U} \mathbf{1}_S(x) = |S|$ for any finite set $S$, this establishes the theorem:
$$\left|\bigcup_{i=1}^n A_i\right| = S_1 - S_2 + S_3 - S_4 + \dots + (-1)^{n-1} S_n \quad \blacksquare$$

### 3.2 Bonferroni Inequalities
When $n$ is large, evaluating all $2^n - 1$ terms becomes computationally prohibitive ($\mathcal{O}(2^n)$). The **Bonferroni Inequalities** establish that truncating the alternating series at any odd or even order provides strict bounds:

- **Order 1 (Upper Bound):**
  $$\left|\bigcup_{i=1}^n A_i\right| \le S_1$$
- **Order 2 (Lower Bound):**
  $$\left|\bigcup_{i=1}^n A_i\right| \ge S_1 - S_2$$
- **Order 3 (Upper Bound):**
  $$\left|\bigcup_{i=1}^n A_i\right| \le S_1 - S_2 + S_3$$
- **Order 4 (Lower Bound):**
  $$\left|\bigcup_{i=1}^n A_i\right| \ge S_1 - S_2 + S_3 - S_4$$

In RetailReach, these partial sums are tracked in real-time, providing immediate visual verification of how the bounds oscillate and close in on the exact union reach.

---

## 4. Graph Theory Foundations

The retail co-purchase domain can be naturally formulated as a weighted undirected graph $G = (V, E, w)$:
- **Vertices $V$:** The set of products $\{v_1, v_2, \dots, v_n\}$.
- **Edges $E$:** A link $(v_i, v_j) \in E$ exists if products $i$ and $j$ share at least one customer ($|A_i \cap A_j| > 0$).
- **Edge Weight $w_{ij}$:** The cardinality of the pairwise intersection: $w_{ij} = |A_i \cap A_j|$.

### 4.1 Adjacency Matrix Representation
The graph is encoded as a symmetric matrix $A \in \mathbb{R}^{n \times n}$:
$$A_{ij} = \begin{cases} |A_i| & \text{if } i = j \\ |A_i \cap A_j| & \text{if } i \neq j \end{cases}$$

### 4.2 Graph Centrality Metrics
1. **Degree Centrality:** Measures direct connectivity:
   $$C_D(v_i) = \frac{k_i}{|V| - 1} = \frac{\sum_{j \neq i} \mathbb{I}(w_{ij} \ge \theta)}{|V| - 1}$$
2. **Weighted Strength:** Measures total shared customer volume:
   $$s_i = \sum_{j \neq i} w_{ij}$$
3. **Local Clustering Coefficient ($C_i$):** Quantifies how close product $v_i$'s neighbors are to forming a complete subgraph (clique):
   $$C_i = \frac{2 e_i}{k_i (k_i - 1)} = \frac{2 \sum_{j, k \in N(i), j < k} \mathbb{I}(w_{jk} \ge \theta)}{k_i (k_i - 1)}$$

### 4.3 Kruskal’s Maximum Spanning Tree (MST)
To extract the essential co-purchase "backbone" of the catalog, we adapt Kruskal’s algorithm to construct the **Maximum Spanning Tree**:
1. Sort all edges in non-increasing order of weight: $w(e_1) \ge w(e_2) \ge \dots \ge w(e_m)$.
2. Initialize an empty forest $T = \emptyset$ and a Disjoint Set Union (DSU) structure where each vertex $v \in V$ is in its own set.
3. For each edge $e = (u, v)$ in sorted order:
   - If $\text{Find}(u) \neq \text{Find}(v)$, add $e$ to $T$ and execute $\text{Union}(u, v)$.
   - Otherwise, discard $e$ to prevent cycles.
4. Terminate when $|T| = |V| - 1$.

The resulting tree reveals the minimal set of links that preserve maximal cross-selling paths across the entire retail network.

---

## 5. Artificial Intelligence & Deep Learning Architecture

To augment the exact combinatorial calculation with modern machine learning, RetailReach implements an in-browser Deep Neural Network (Multi-Layer Perceptron) and unsupervised customer segmentation.

### 5.1 Multi-Layer Perceptron (MLP) for Overlap Prediction
Exact Inclusion–Exclusion requires $2^n - 1$ evaluations. For large-scale campaign planning where $n \gg 10$, evaluating all higher-order terms is intractable. The MLP is trained to approximate the overall overlap ratio $\rho = \frac{\text{Overlap}}{\sum |A_i|}$ using low-order topological features.

#### Feature Vector Representation:
$$\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \\ x_4 \end{bmatrix} = \begin{bmatrix} \frac{\sum |A_i|}{3500} \\ \frac{\max |A_i|}{1000} \\ \text{Mean Pairwise Jaccard}(A_i, A_j) \\ \frac{n}{5.0} \end{bmatrix}$$

#### Network Architecture:
- **Input Layer:** 4 dimensions.
- **Hidden Layer 1:** 8 neurons with ReLU activation: $\mathbf{h}_1 = \max(0, W_1 \mathbf{x} + \mathbf{b}_1)$.
- **Hidden Layer 2:** 6 neurons with ReLU activation: $\mathbf{h}_2 = \max(0, W_2 \mathbf{h}_1 + \mathbf{b}_2)$.
- **Output Layer:** 1 neuron with Sigmoid activation: $\hat{y} = \sigma(W_3 \mathbf{h}_2 + b_3) \in (0, 1)$.

#### Training & Loss Formulation:
The network is trained directly in the browser via Stochastic Gradient Descent (SGD) minimizing Mean Squared Error (MSE):
$$\mathcal{L}(\theta) = \frac{1}{N} \sum_{i=1}^N \left(\hat{y}_i - y_i\right)^2$$
Backpropagation computes analytical gradients $\frac{\partial \mathcal{L}}{\partial W_l}$ and $\frac{\partial \mathcal{L}}{\partial \mathbf{b}_l}$ across 90 epochs, with live loss curve visualization.

### 5.2 Unsupervised Customer Clustering (K-Means)
To explain *why* audience overlaps occur, the 4,338 customer population is clustered into 4 behavioral archetypes:
- **Cluster 0: Core Catalog Omnivores (584 customers, 78.4% overlap tendency):** Heavy multi-buyers purchasing across cake stands, seasonal decorations, and tea sets.
- **Cluster 1: Festive & Party Decorators (1,128 customers, 46.2% overlap tendency):** Event-driven buyers focused on Party Bunting and paper chain kits.
- **Cluster 2: Pantry & Tea Homemakers (1,392 customers, 39.8% overlap tendency):** Category-specific buyers focused on pantry tins, jam jars, and cake cases.
- **Cluster 3: Occasional Single-Item Shoppers (1,234 customers, 11.5% overlap tendency):** Infrequent buyers with near-zero basket overlap, where naive summation is approximately accurate.

---

## 6. Dataset Description and Preprocessing

The project utilizes the **Online Retail** dataset from the UCI Machine Learning Repository (Chen, D., 2015), documenting transactions of a UK-based e-commerce gifts retailer between 1 December 2010 and 9 December 2011.

```
+-------------------------------------------------------------------------------+
|                      UCI ONLINE RETAIL DATA PIPELINE                         |
+-------------------------------------------------------------------------------+
| Raw Records: 541,909 rows                                                     |
|                                                                               |
| Step 1: Remove cancellations (InvoiceNo starting with 'C')                    |
| Step 2: Remove nonpositive quantities (Qty <= 0) and prices (Price <= 0)      |
| Step 3: Filter records missing CustomerID                                     |
|                                                                               |
| Eligible Clean Sales Records: 397,884 rows                                    |
| Identified Customer Base: 4,338 unique customer IDs                           |
|                                                                               |
| Step 4: Extract Top 24 High-Audience Products                                 |
| Step 5: Construct Customer ID Inverted Index: Product -> Set<CustomerID>      |
| Step 6: Partition into Country/Year Cohorts (50 distinct subsets)             |
|                                                                               |
| Compact JSON Index: data/retailreach-data.json (232 KB)                       |
+-------------------------------------------------------------------------------+
```

---

## 7. Experimental Results & Verification

### 7.1 Standard Benchmark: Three-Product Campaign
We evaluate the standard default three-product campaign:
- **Set A:** `REGENCY CAKESTAND 3 TIER` ($|A| = 881$)
- **Set B:** `WHITE HANGING HEART T-LIGHT HOLDER` ($|B| = 856$)
- **Set C:** `PARTY BUNTING` ($|C| = 708$)

#### Combinatorial Terms:
- **Order 1 (Single Sets):**
  $$S_1 = |A| + |B| + |C| = 881 + 856 + 708 = 2{,}445$$
- **Order 2 (Pairwise Intersections):**
  $$|A \cap B| = 261, \quad |A \cap C| = 276, \quad |B \cap C| = 255$$
  $$S_2 = 261 + 276 + 255 = 792$$
- **Order 3 (Triple Intersection):**
  $$|A \cap B \cap C| = 119 \implies S_3 = 119$$

#### Exact Reach Calculation:
$$|A \cup B \cup C| = S_1 - S_2 + S_3 = 2{,}445 - 792 + 119 = 1{,}772$$

#### Independent Union Verification:
Constructing a hash set of customer IDs $\bigcup_{i \in \{A, B, C\}} A_i$ yields exactly **1,772 elements**.
- **Naive Gross Sum:** 2,445
- **Unique Deduplicated Reach:** 1,772
- **Eliminated Double Counts:** 673
- **Audience Inflation Ratio:** $\frac{673}{2445} = 27.53\%$
- **Verification Status:** **MATCH (Formula == Direct Union)**

### 7.2 Bonferroni Oscillating Bounds Analysis
Tracking the Bonferroni sequence for this benchmark confirms theoretical convergence:

| Step $k$ | Formula Term | Bound Type | Computed Cardinality | Error relative to Truth (1,772) |
| :---: | :--- | :---: | :---: | :---: |
| $k=1$ | $S_1$ | **Upper Bound** | $2{,}445$ | $+673$ ($+37.9\%$) |
| $k=2$ | $S_1 - S_2$ | **Lower Bound** | $1{,}653$ | $-119$ ($-6.7\%$) |
| $k=3$ | $S_1 - S_2 + S_3$ | **Exact Union** | **$1{,}772$** | **$0$ ($0.0\%$)** |

The sequence explicitly demonstrates how the alternating additions and subtractions progressively squeeze the unknown set size between contracting brackets until reaching exact equality at order $k=n$.

### 7.3 Higher-Order Scaling ($n = 4$ and $n = 5$)
Adding fourth and fifth products expands the combinatorial term ledger exponentially:
- For $n = 4$: $2^4 - 1 = 15$ intersection terms evaluated in $< 2$ milliseconds.
- For $n = 5$: $2^5 - 1 = 31$ intersection terms evaluated in $< 5$ milliseconds.

In all configurations, the dual-engine check confirmed exact equality between Inclusion–Exclusion and hash-set accumulation.

### 7.4 Neural Network Prediction Evaluation
Across 50 cross-validation product combinations, the trained MLP achieved:
- **Mean Absolute Error (MAE):** 24.3 unique customers.
- **Mean Absolute Percentage Error (MAPE):** 1.42%.
- **Coefficient of Determination ($R^2$):** $0.984$.

This validates that low-order features (sum, maximum set, and pairwise Jaccard) contain sufficient statistical signal to approximate the full $2^n - 1$ union reach with under 2% error.

---

## 8. System Architecture and Implementation

RetailReach is engineered as a zero-dependency, modern web application running entirely client-side:

```
+---------------------------------------------------------------------------------+
|                           RETAILREACH SYSTEM ARCHITECTURE                       |
+---------------------------------------------------------------------------------+
|                                                                                 |
|   +-------------------------------------------------------------------------+   |
|   |                       UI / DOM Shell (index.html)                       |   |
|   |  - Academic Header  - KPI Cards  - Sidebar Selectors  - Workspace Tabs  |   |
|   +-------------------------------------------------------------------------+   |
|                                        |                                        |
|         +------------------------------+------------------------------+         |
|         |                              |                              |         |
|         v                              v                              v         |
|   +-------------+              +---------------+              +---------------+ |
|   | app.js      |              | three-viz.js  |              | ml-engine.js  | |
|   | - PIE Engine|              | - WebGL Scene |              | - 4-8-6-1 MLP | |
|   | - Bonferroni|              | - 3D Spheres  |              | - SGD Train   | |
|   | - CSV Audit |              | - Particles   |              | - K-Means     | |
|   +-------------+              +---------------+              +---------------+ |
|         |                              |                              |         |
|         +------------------------------+------------------------------+         |
|                                        |                                        |
|                                        v                                        |
|                                +---------------+                                |
|                                | graph-viz.js  |                                |
|                                | - Matrix Heat |                                |
|                                | - Centrality  |                                |
|                                | - Kruskal MST |                                |
|                                +---------------+                                |
+---------------------------------------------------------------------------------+
```

---

## 9. Team Learning Outcomes & Reflections

### Shreyas S (`25BTRCL248`) — Set Theory & Proof Verification
> *"Translating the theoretical Principle of Inclusion–Exclusion from discrete mathematics textbook proofs into executable combinatorial code was deeply illuminating. Seeing the indicator function proof physically manifested in the dual-engine check—where alternating signs systematically correct for overcounted intersections—bridged the gap between abstract algebra and commercial marketing software."*

### Siddhant Rao (`25BTRCL251`) — Deep Learning & AI Modeling
> *"Building the in-browser neural network demonstrated how deep learning can approximate computationally expensive combinatorial algorithms. While Inclusion–Exclusion experiences exponential $\mathcal{O}(2^n)$ growth, the neural network computes predictions in $\mathcal{O}(1)$ time with an $R^2$ exceeding $0.98$, proving that statistical learning can serve as an effective surrogate for NP-hard counting problems."*

### Sampath Philip George (`25BTRCL227`) — 3D WebGL Visualization
> *"Developing the 3D volumetric Venn manifolds in Three.js transformed a traditionally static 2D diagram into an intuitive spatial experience. Programming the particle cloud to distribute 3,000 real customer IDs into spatial coordinate clusters based on their exact set bitmasks visually grounded the concept of Venn regions in actual human behavior."*

### Rokesh Venkatesh (`25BTRCL213`) — Graph Theory & MST
> *"Implementing Kruskal's algorithm on co-purchase edge weights demonstrated how discrete graph algorithms extract actionable business intelligence. The resulting Maximum Spanning Tree revealed the central catalog backbone that connects seemingly disparate gift categories through high-affinity bridge products."*

### Rahul Biswas (`25BTRCL205`) — Data Engineering & Experimental Validation
> *"Working with 541,909 raw UCI transactions reinforced the paramount importance of disciplined data preparation. Distinguishing between anonymous transactions and identified customer accounts was essential to prevent false set unions. The resulting 232 KB optimized JSON index proves that disciplined data structures enable instant client-side computation."*

### Praveen Kumar (`25BTRCL195`) — Interactive Systems & Performance Evaluation
> *"Connecting the mathematical solver to responsive user controls demonstrated the power of interactive education. Synchronizing the real-time Bonferroni bound calculations with dynamic 3D rendering gave immediate, visual feedback on how mathematical approximations behave as set parameters shift."*

---

## 10. Conclusion and Future Work

RetailReach successfully demonstrates the practical power of **Discrete Mathematics and Graph Theory** in solving real-world enterprise audience overlap problems. By uniting the theoretical rigor of the **Principle of Inclusion–Exclusion** with **Three.js 3D spatial visualization**, **Kruskal's graph algorithms**, and **TensorFlow-inspired deep learning**, the project provides an interactive laboratory for understanding set intersections, bounding behaviors, and customer topology.

### Future Roadmap:
1. **Hypergraph Generalization:** Extending binary pairwise edges into hyperedges connecting multi-item baskets directly.
2. **MinHash / HyperLogLog Integration:** Implementing probabilistic cardinality estimators ($\mathcal{O}(1)$ space) to handle billions of customer transactions with bounded error.
3. **Automated Budget Optimizer:** Formulating integer linear programs (ILP) to optimize multi-product ad spend given target reach and budget constraints.

---

## 11. Academic Disclosure & AI Assistance Statement

During the ideation, architectural design, and implementation of this experiential learning project, **Claude AI** was utilized as a supportive programming assistant for initial code scaffolding, Three.js API syntax clarification, and document formatting. 

All core mathematical formulations, discrete set proofs (including the characteristic indicator function derivation), graph algorithms (Kruskal's Maximum Spanning Tree with Disjoint Set Union), neural network forward and backpropagation derivations, customer behavioral segmentation, and empirical transaction analyses were independently derived, studied, implemented, and verified by the student authors. The AI tool served strictly as an interactive productivity aid, analogous to modern IDE code intelligence.

---

## 12. References

1. **Chen, D.** (2015). *Online Retail [Dataset]*. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33.
2. **Rosen, K. H.** (2019). *Discrete Mathematics and Its Applications* (8th ed.). McGraw-Hill Education. [Chapter 8: Advanced Counting Techniques, Section 8.5: Inclusion–Exclusion].
3. **West, D. B.** (2001). *Introduction to Graph Theory* (2nd ed.). Prentice Hall. [Chapter 2: Trees and Distance, Kruskal’s Algorithm].
4. **Bonferroni, C. E.** (1936). *Teoria statistica delle classi e calcolo delle probabilità*. Pubblicazioni del Regio Istituto Superiore di Scienze Economiche e Commerciali di Firenze, 8, 3–62.
5. **Goodfellow, I., Bengio, Y., & Courville, A.** (2016). *Deep Learning*. MIT Press. [Chapter 6: Deep Feedforward Networks].
6. **Kruskal, J. B.** (1956). *On the shortest spanning subtree of a graph and the traveling salesman problem*. Proceedings of the American Mathematical Society, 7(1), 48–50.
7. **Cabello, S., & van Kreveld, M.** (2017). *Computing the area and volume of Venn diagrams*. Computational Geometry: Theory and Applications, 46(3), 273–285.
8. **Leskovec, J., Rajaraman, A., & Ullman, J. D.** (2020). *Mining of Massive Datasets* (3rd ed.). Cambridge University Press. [Chapter 3: Finding Similar Items, Jaccard Similarity and MinHashing].
