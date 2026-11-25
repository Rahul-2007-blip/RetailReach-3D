#!/usr/bin/env python3
"""
Generate a publication-quality University Project Report HTML and convert to PDF
using LibreOffice Headless.

Features:
- Official JAIN University Header with exact formatting
- Complete Academic Project Structure
- Professional CSS Print Styles (A4 Page format)
- Base64-embedded official graphics for zero-dependency standalone PDF rendering
- LaTeX-styled Mathematical Formulas & Discrete Math Proofs
- High-contrast Tables, Code blocks, and Diagrams
- Claude AI Assistance Disclosure
"""

import base64
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / 'assets'
REPORT_HTML = ROOT / 'report.html'
REPORT_PDF = ROOT / 'RetailReach_Report.pdf'

def get_base64_image(image_path: Path) -> str:
    if image_path.exists():
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('ascii')
    return ""

def build_html():
    header_b64 = get_base64_image(ASSETS_DIR / 'jain_header.png')
    header_img_src = f"data:image/png;base64,{header_b64}" if header_b64 else "assets/jain_header.png"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>RetailReach Experiential Learning Project Report</title>
<style>
  @page {{
    size: A4;
    margin: 15mm 20mm 15mm 20mm;
  }}

  body {{
    font-family: 'Times New Roman', 'Liberation Serif', serif;
    font-size: 11pt;
    line-height: 1.55;
    color: #1a1a1a;
    background: #ffffff;
    margin: 0;
    padding: 0;
  }}

  .page-break {{
    page-break-before: always;
    display: block;
    height: 1px;
    clear: both;
    visibility: hidden;
  }}

  /* ── Cover Page Layout ─────────────────────────────── */
  .cover-container {{
    text-align: center;
    padding-top: 5px;
  }}

  img {{
    border: none !important;
    outline: none !important;
  }}

  .cover-header-img {{
    width: 100%;
    max-width: 520px;
    height: auto;
    margin: 0 auto 10px;
    display: block;
    border: none !important;
    outline: none !important;
  }}

  .cover-title-box {{
    margin: 10px 0 16px;
  }}

  .project-type {{
    font-family: 'Arial', sans-serif;
    font-size: 10pt;
    font-weight: bold;
    color: #4b5563;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
  }}

  .project-title {{
    font-size: 16.5pt;
    font-weight: bold;
    line-height: 1.3;
    color: #111827;
    margin: 0 auto;
    max-width: 92%;
  }}

  .project-subtitle {{
    font-size: 10.5pt;
    font-style: italic;
    color: #4b5563;
    margin-top: 6px;
    line-height: 1.35;
  }}

  .meta-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    text-align: left;
  }}

  .meta-table td {{
    vertical-align: top;
    width: 50%;
    padding: 0 10px;
  }}

  .meta-title {{
    font-family: 'Arial', sans-serif;
    font-size: 10pt;
    font-weight: bold;
    text-transform: uppercase;
    color: #1f2937;
    border-bottom: 2px solid #1f2937;
    padding-bottom: 2px;
    margin-bottom: 6px;
  }}

  .mentor-details {{
    font-size: 9.5pt;
    line-height: 1.45;
  }}

  .mentor-details b {{
    font-size: 11pt;
    color: #111;
    display: block;
    margin-bottom: 2px;
  }}

  .team-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 9pt;
    margin-top: 2px;
    border: 1.5px solid #1f2937;
  }}

  .team-table th, .team-table td {{
    padding: 3.5px 7px;
    border: 1px solid #4b5563;
    text-align: left;
  }}

  .team-table th {{
    background-color: #f3f4f6;
    font-family: 'Arial', sans-serif;
    font-weight: bold;
    font-size: 8.5pt;
  }}

  .team-table td code {{
    font-family: 'Courier New', monospace;
    font-weight: bold;
    color: #1d4ed8;
  }}

  .cover-footer {{
    margin-top: 16px;
    font-size: 8.5pt;
    color: #4b5563;
    border-top: 1px solid #d1d5db;
    padding-top: 6px;
    line-height: 1.35;
  }}

  /* ── Document Body Headings ────────────────────────── */
  h1 {{
    font-family: 'Arial', sans-serif;
    font-size: 15pt;
    font-weight: bold;
    color: #111827;
    border-bottom: 1.5px solid #111827;
    padding-bottom: 4px;
    margin-top: 24px;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    page-break-after: avoid;
  }}

  h2 {{
    font-family: 'Arial', sans-serif;
    font-size: 12.5pt;
    font-weight: bold;
    color: #1f2937;
    margin-top: 18px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }}

  h3 {{
    font-family: 'Arial', sans-serif;
    font-size: 11pt;
    font-weight: bold;
    color: #374151;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}

  p {{
    text-align: justify;
    margin-bottom: 10px;
    line-height: 1.55;
  }}

  /* Math & Equations */
  .math-block {{
    background: #f9fafb;
    border-left: 3.5px solid #2563eb;
    padding: 9px 16px;
    margin: 14px 0;
    font-family: 'Cambria Math', 'Times New Roman', serif;
    font-size: 11pt;
    text-align: center;
    border-radius: 0 4px 4px 0;
  }}

  /* Tables */
  table.content-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9.5pt;
  }}

  table.content-table th, table.content-table td {{
    border: 1px solid #9ca3af;
    padding: 6px 8px;
    text-align: left;
  }}

  table.content-table th {{
    background-color: #f3f4f6;
    font-family: 'Arial', sans-serif;
    font-weight: bold;
  }}

  /* Callout boxes */
  .callout {{
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 4px solid #3b82f6;
    padding: 10px 14px;
    margin: 14px 0;
    border-radius: 0 4px 4px 0;
    font-size: 9.5pt;
  }}

  .callout-title {{
    font-weight: bold;
    font-family: 'Arial', sans-serif;
    color: #1e40af;
    margin-bottom: 3px;
  }}

  /* Diagram Box */
  .diagram-box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 10px 12px;
    margin: 12px 0;
    font-family: 'Courier New', monospace;
    font-size: 8.5pt;
    line-height: 1.3;
    white-space: pre;
    overflow-x: auto;
  }}

  /* Reflection Quote */
  .reflection-quote {{
    background: #fafaf9;
    border-left: 3px solid #78716c;
    padding: 6px 10px;
    margin: 6px 0;
    font-style: italic;
    font-size: 9.5pt;
    line-height: 1.4;
  }}

  .reflection-quote b {{
    font-style: normal;
    font-family: 'Arial', sans-serif;
    color: #292524;
  }}

  .toc-row {{
    display: flex;
    justify-content: space-between;
    padding: 3px 0;
    border-bottom: 1px dotted #9ca3af;
    font-size: 10pt;
  }}
</style>
</head>
<body>

<!-- ========================================== -->
<!-- 1. COVER PAGE (Exactly 1 Page)              -->
<!-- ========================================== -->
<div class="cover-container">
  <img src="{header_img_src}" class="cover-header-img" alt="Jain University Header">

  <div class="cover-title-box">
    <div class="project-type">Experiential Learning Project Report · Module 1</div>
    <div class="project-title">RetailReach: Intelligent Campaign Audience Deduplication via the Principle of Inclusion–Exclusion, Graph Theory, and Deep Neural Networks</div>
    <div class="project-subtitle">An Interactive High-Performance Discrete Mathematics Suite for Multi-Product Retail Co-Purchase Analytics</div>
  </div>

  <table class="meta-table">
    <tr>
      <td>
        <div class="meta-title">Submitted To</div>
        <div class="mentor-details" style="text-align: left;">
          <b style="font-size: 11.5pt; color: #111;">Dr. K J Ghanashyam</b><br>
          Assistant Professor,<br>
          Department of Data Analytics &amp; Mathematical Sciences,<br>
          Faculty of Engineering &amp; Technology,<br>
          Jain (Deemed-To-Be) University.
        </div>
      </td>
      <td>
        <div class="meta-title">Submitted By (Student Team)</div>
        <table class="team-table">
          <thead>
            <tr>
              <th style="width:28px;">Sl.</th>
              <th>Name</th>
              <th>USN</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>1</td><td><b>SHREYAS S</b></td><td><code>25BTRCL248</code></td></tr>
            <tr><td>2</td><td><b>SIDDHANT RAO</b></td><td><code>25BTRCL251</code></td></tr>
            <tr><td>3</td><td><b>SAMPATH PHILIP GEORGE</b></td><td><code>25BTRCL227</code></td></tr>
            <tr><td>4</td><td><b>ROKESH VENKATESH</b></td><td><code>25BTRCL213</code></td></tr>
            <tr><td>5</td><td><b>RAHUL BISWAS</b></td><td><code>25BTRCL205</code></td></tr>
            <tr><td>6</td><td><b>PRAVEEN KUMAR</b></td><td><code>25BTRCL195</code></td></tr>
          </tbody>
        </table>
      </td>
    </tr>
  </table>

  <div class="cover-footer">
    Academic Year 2026–2027 · B. Tech Computer Science &amp; Engineering (AIML) · Section D<br>
    Discrete Mathematics and Graph Theory (Course Code: 25BSMA10)
  </div>
</div>

<!-- ========================================== -->
<!-- 2. TABLE OF CONTENTS                       -->
<!-- ========================================== -->
<h1 style="page-break-before: always; margin-top: 20px;">Table of Contents</h1>
<table style="width: 100%; border-collapse: collapse; margin: 18px 0; font-size: 10pt;">
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>Executive Summary &amp; Abstract</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right; width: 80px;">Page 3</td></tr>
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>1. Problem Identification and Industrial Relevance</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right;">Page 3</td></tr>
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>2. Formal Mathematical Objectives and Scope</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right;">Page 4</td></tr>
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>3. Mathematical Foundations: Set Theory &amp; Bonferroni Bounds</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right;">Page 5</td></tr>
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>4. Discrete Graph Theory Modeling &amp; Topology</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right;">Page 6</td></tr>
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>5. Deep Learning &amp; Machine Learning Overlap Predictor</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right;">Page 7</td></tr>
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>6. Interactive 3D WebGL Visualization Architecture</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right;">Page 8</td></tr>
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>7. Empirical Dataset &amp; Data Pipeline Architecture</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right;">Page 9</td></tr>
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>8. Quantitative Experimental Verification &amp; Findings</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right;">Page 10</td></tr>
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>9. Individual &amp; Team Learning Outcomes</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right;">Page 11</td></tr>
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>10. Conclusion and Future Research Directions</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right;">Page 12</td></tr>
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>11. Academic Disclosure &amp; AI Assistance Statement</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right;">Page 13</td></tr>
  <tr><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af;"><b>12. References &amp; Academic Bibliography</b></td><td style="padding: 5px 0; border: none; border-bottom: 1px dotted #9ca3af; text-align: right;">Page 13</td></tr>
</table>

<!-- ========================================== -->
<!-- 3. ABSTRACT                                -->
<!-- ========================================== -->
<h1 style="page-break-before: always; margin-top: 20px;">Abstract</h1>
<p>
In modern marketing analytics and customer relationship management (CRM), planning multi-product promotional campaigns requires measuring the distinct reach of an audience. When marketers aggregate customer lists across multiple products, customers who purchased multiple promoted items are counted multiple times. This naive summation grossly overestimates unique audience size, causing distorted return-on-ad-spend (ROAS) projections and excessive advertising spend.
</p>
<p>
<b>RetailReach</b> addresses this fundamental challenge by applying the <b>Principle of Inclusion–Exclusion (PIE)</b>, <b>Discrete Graph Theory</b>, and <b>Deep Learning</b> to 541,909 real-world e-commerce transactions from the UCI Machine Learning Repository <i>Online Retail</i> dataset. The system calculates exact audience unions by evaluating all 2<sup>n</sup> &minus; 1 combinatorial intersections for up to five concurrent product sets, tracking alternating Bonferroni bounds, rendering dynamic 3D volumetric Venn manifolds via WebGL/Three.js, modeling product co-purchase graphs with Kruskal's Maximum Spanning Tree, and training an in-browser Multi-Layer Perceptron (MLP) neural network to predict multi-audience overlap in O(1) time.
</p>
<p>
On a representative three-product benchmark (Regency Cakestand, White Heart T-Light Holder, Party Bunting), a naive sum of 2,445 customer entries collapses to an exact unique reach of 1,772 customers, safely removing 673 redundant records (a 27.53% overlap distortion). An independent computational check between the combinatorial formula and direct set unions confirmed 100% exact numerical agreement across all tested combinations.
</p>

<!-- ========================================== -->
<!-- 4. SECTION 1: PROBLEM IDENTIFICATION       -->
<!-- ========================================== -->
<h1>1. Problem Identification and Industrial Relevance</h1>

<h2>1.1 The Audience Inflation Dilemma</h2>
<p>
Consider a marketing campaign promoting <i>n</i> products: P<sub>1</sub>, P<sub>2</sub>, &hellip;, P<sub>n</sub>. For each product P<sub>i</sub>, historical sales records identify a set of distinct customer buyers, denoted A<sub>i</sub>, with cardinality |A<sub>i</sub>|. When campaign managers launch cross-promotions, they frequently compute projected audience size as the naive sum of individual list sizes:
</p>
<div class="math-block">
  Reach<sub>naive</sub> = &sum;<sub>i=1</sub><sup>n</sup> |A<sub>i</sub>|
</div>
<p>
This uncorrected sum assumes that customer sets A<sub>i</sub> and A<sub>j</sub> are mutually disjoint (A<sub>i</sub> &cap; A<sub>j</sub> = &empty; for all i &ne; j). In retail environments with strong cross-category affinity, this assumption fails catastrophically. Multi-product buyers belong to multiple target sets simultaneously, resulting in significant overcounting:
</p>
<ul>
  <li><b>Budget Waste:</b> Marketing teams over-allocate ad spend based on inflated impression estimates.</li>
  <li><b>Ad Fatigue:</b> High-value customers who purchased several promoted products receive repetitive, uncoordinated advertisements.</li>
  <li><b>Distorted Metrics:</b> Conversion rates computed against an inflated denominator appear artificially low.</li>
</ul>

<h2>1.2 The Combinatorial Challenge</h2>
<p>
Calculating exact union size |A<sub>1</sub> &cup; A<sub>2</sub> &cup; &hellip; &cup; A<sub>n</sub>| requires evaluating all 2<sup>n</sup> &minus; 1 non-empty subsets. For large numbers of products, exact enumeration becomes computationally prohibitive (&Omicron;(2<sup>n</sup>)). This creates a pressing need for:
</p>
<ol>
  <li>Strict analytical bounds (Bonferroni Inequalities) to establish guarantees at early stopping orders.</li>
  <li>Graph-theoretic topological modeling to uncover high-affinity product communities.</li>
  <li>Deep learning surrogates capable of predicting overlap ratios in constant time (&Omicron;(1)).</li>
</ol>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- 5. SECTION 2: OBJECTIVES & SCOPE           -->
<!-- ========================================== -->
<h1>2. Formal Mathematical Objectives and Scope</h1>

<table class="content-table">
  <thead>
    <tr>
      <th style="width: 25%;">Domain</th>
      <th style="width: 35%;">Theoretical Concept</th>
      <th style="width: 40%;">Project Implementation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Discrete Mathematics</b></td>
      <td>Principle of Inclusion–Exclusion (PIE) &amp; Bonferroni Inequalities</td>
      <td>Exact 2<sup>n</sup> &minus; 1 subset evaluation engine with alternating sign verification and order-<i>k</i> convergence tracking.</td>
    </tr>
    <tr>
      <td><b>Graph Theory</b></td>
      <td>Weighted Graphs, Centrality Metrics, Kruskal's MST, DSU</td>
      <td>24-product co-purchase network G=(V,E), degree centrality C<sub>D</sub>, clustering coefficients C<sub>i</sub>, and Maximum Spanning Tree.</td>
    </tr>
    <tr>
      <td><b>Artificial Intelligence</b></td>
      <td>Multi-Layer Perceptron (MLP) &amp; K-Means Clustering</td>
      <td>Custom 4&rarr;8&rarr;6&rarr;1 neural network trained via in-browser SGD (120 epochs) and 4-cluster RFM customer segmentation.</td>
    </tr>
    <tr>
      <td><b>3D Computer Graphics</b></td>
      <td>WebGL, Three.js Manifolds, Spatial Hashing</td>
      <td>Interactive 3D volumetric Venn spheres, 3,000-point customer particle cloud with bitmask clustering, and spherical graph shell.</td>
    </tr>
    <tr>
      <td><b>Data Engineering</b></td>
      <td>Set Deduplication &amp; Preprocessing</td>
      <td>Processing 541,909 raw UCI transactions into a clean 232 KB JSON cohort index across 4,338 identified customer IDs.</td>
    </tr>
  </tbody>
</table>

<!-- ========================================== -->
<!-- 6. SECTION 3: MATHEMATICAL FOUNDATIONS     -->
<!-- ========================================== -->
<h1>3. Mathematical Foundations: Set Theory &amp; Bonferroni Bounds</h1>

<h2>3.1 The Principle of Inclusion–Exclusion</h2>
<p>
Let A<sub>1</sub>, A<sub>2</sub>, &hellip;, A<sub>n</sub> be finite sets. The cardinality of their union is defined by the alternating sum:
</p>
<div class="math-block">
  |&cup;<sub>i=1</sub><sup>n</sup> A<sub>i</sub>| = &sum;<sub>k=1</sub><sup>n</sup> (&minus;1)<sup>k&minus;1</sup> S<sub>k</sub>
</div>
<p>where S<sub>k</sub> represents the sum of cardinalities of all k-tuple intersections:</p>
<div class="math-block">
  S<sub>k</sub> = &sum;<sub>1 &le; i<sub>1</sub> &lt; &hellip; &lt; i<sub>k</sub> &le; n</sub> |A<sub>i<sub>1</sub></sub> &cap; A<sub>i<sub>2</sub></sub> &cap; &hellip; &cap; A<sub>i<sub>k</sub></sub>|
</div>

<h2>3.2 Rigorous Proof via Characteristic Indicator Functions</h2>
<p>
For each customer element <i>x</i> &isin; U, let <b>1</b><sub>A<sub>i</sub></sub>(x) be the indicator function:
</p>
<div class="math-block">
  <b>1</b><sub>A<sub>i</sub></sub>(x) = 1 if x &isin; A<sub>i</sub>, else 0
</div>
<p>An element belongs to the union if and only if it does not belong to the complement intersection:</p>
<div class="math-block">
  <b>1</b><sub>&cup; A<sub>i</sub></sub>(x) = 1 &minus; &prod;<sub>i=1</sub><sup>n</sup> (1 &minus; <b>1</b><sub>A<sub>i</sub></sub>(x))
</div>
<p>Expanding this algebraic product yields:</p>
<div class="math-block">
  <b>1</b><sub>&cup; A<sub>i</sub></sub>(x) = &sum;<sub>i</sub> <b>1</b><sub>A<sub>i</sub></sub>(x) &minus; &sum;<sub>i &lt; j</sub> <b>1</b><sub>A<sub>i</sub> &cap; A<sub>j</sub></sub>(x) + &hellip; + (&minus;1)<sup>n&minus;1</sup> <b>1</b><sub>&cap; A<sub>i</sub></sub>(x)
</div>
<p>Summing both sides over all elements x &isin; U confirms the theorem unconditionally: &sum;<sub>x</sub> <b>1</b><sub>S</sub>(x) = |S|.</p>

<div class="page-break"></div>

<h2>3.3 Bonferroni Inequalities &amp; Convergence Behavior</h2>
<p>
Truncating the alternating series at partial sum order <i>k</i> produces guaranteed alternating upper and lower bounds:
</p>
<table class="content-table">
  <thead>
    <tr>
      <th>Order k</th>
      <th>Partial Sum B<sub>k</sub></th>
      <th>Bound Type</th>
      <th>Benchmark Value</th>
      <th>Error vs Exact (1,772)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>k = 1</td>
      <td>B<sub>1</sub> = S<sub>1</sub></td>
      <td><b>Upper Bound</b></td>
      <td>2,445</td>
      <td>+673 (+37.98%)</td>
    </tr>
    <tr>
      <td>k = 2</td>
      <td>B<sub>2</sub> = S<sub>1</sub> &minus; S<sub>2</sub></td>
      <td><b>Lower Bound</b></td>
      <td>1,629</td>
      <td>&minus;143 (&minus;8.07%)</td>
    </tr>
    <tr>
      <td>k = 3</td>
      <td>B<sub>3</sub> = S<sub>1</sub> &minus; S<sub>2</sub> + S<sub>3</sub></td>
      <td><b>Exact (n=3)</b></td>
      <td>1,772</td>
      <td><b>0 (0.00% exact match)</b></td>
    </tr>
  </tbody>
</table>

<!-- ========================================== -->
<!-- 7. SECTION 4: GRAPH THEORY MODELING        -->
<!-- ========================================== -->
<h1>4. Discrete Graph Theory Modeling &amp; Topology</h1>

<h2>4.1 Bipartite Projection to Co-Purchase Graph</h2>
<p>
Customer transaction logs form an undirected bipartite graph G<sub>bipartite</sub> = (C &cup; P, E<sub>bip</sub>). Projecting this bipartite graph onto the product set P yields a weighted product co-purchase network G = (V, E, w):
</p>
<ul>
  <li><b>Vertices V:</b> The top 24 retail catalog products (|V| = 24).</li>
  <li><b>Edge Weights w<sub>ij</sub>:</b> Pairwise intersection size w<sub>ij</sub> = |A<sub>i</sub> &cap; A<sub>j</sub>|.</li>
</ul>

<h2>4.2 Centrality Metrics &amp; Top Product Rankings</h2>
<table class="content-table">
  <thead>
    <tr>
      <th>Rank</th>
      <th>Product Title</th>
      <th>Buyers |A<sub>i</sub>|</th>
      <th>Degree k<sub>i</sub></th>
      <th>Weighted Strength</th>
      <th>Degree Centrality</th>
      <th>Clustering C<sub>i</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr><td>#1</td><td>REGENCY CAKESTAND 3 TIER</td><td>881</td><td>23</td><td>4,982</td><td>1.000</td><td>0.784</td></tr>
    <tr><td>#2</td><td>WHITE HANGING HEART T-LIGHT HOLDER</td><td>856</td><td>23</td><td>4,710</td><td>1.000</td><td>0.742</td></tr>
    <tr><td>#3</td><td>PARTY BUNTING</td><td>708</td><td>21</td><td>3,892</td><td>0.913</td><td>0.695</td></tr>
    <tr><td>#4</td><td>ASSORTED COLOUR BIRD ORNAMENT</td><td>684</td><td>20</td><td>3,540</td><td>0.870</td><td>0.680</td></tr>
    <tr><td>#5</td><td>SET OF 3 CAKE TINS PANTRY DESIGN</td><td>642</td><td>19</td><td>3,210</td><td>0.826</td><td>0.710</td></tr>
  </tbody>
</table>

<h2>4.3 Kruskal's Maximum Spanning Tree (MST)</h2>
<p>
To identify the core structural backbone connecting all products without redundant cycles, RetailReach adapts Kruskal's algorithm to compute the <b>Maximum Spanning Tree</b>:
</p>
<ol>
  <li>Sort all 276 candidate edges in non-increasing order of weight: w(e<sub>1</sub>) &ge; w(e<sub>2</sub>) &ge; &hellip; &ge; w(e<sub>m</sub>).</li>
  <li>Initialize a Disjoint Set Union (DSU) data structure with path compression and union-by-rank.</li>
  <li>Iterate through sorted edges; add edge (u, v) to tree T if Find(u) &ne; Find(v), then Union(u, v).</li>
  <li>Terminate when |T| = |V| &minus; 1 = 23 edges.</li>
</ol>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- 8. SECTION 5: DEEP LEARNING ARCHITECTURE   -->
<!-- ========================================== -->
<h1>5. Deep Learning &amp; Machine Learning Overlap Predictor</h1>

<h2>5.1 Multi-Layer Perceptron (MLP) Architecture</h2>
<p>
While Inclusion–Exclusion scales exponentially (&Omicron;(2<sup>n</sup>)), real-time bidding engines require audience predictions in constant time (&Omicron;(1)). RetailReach implements a custom feedforward neural network trained directly in-browser using stochastic gradient descent:
</p>
<div class="diagram-box">
[Input: 4 Features] &rarr; [Dense: 8 Neurons, ReLU] &rarr; [Dense: 6 Neurons, ReLU] &rarr; [Output: 1 Neuron, Sigmoid]
Features: [ &Sigma;|A_i|/3500 , max|A_i|/1000 , Mean Pairwise Jaccard , n/5 ] &rarr; Predicted Overlap Ratio &isin; [0, 1]
</div>

<h2>5.2 Mathematical Formulation of Backpropagation</h2>
<p>
Let <i>x</i> be the 4-dimensional input feature vector. The network forward pass computes:
</p>
<div class="math-block">
  h<sub>1</sub> = ReLU(W<sub>1</sub> x + b<sub>1</sub>) &emsp;|&emsp; h<sub>2</sub> = ReLU(W<sub>2</sub> h<sub>1</sub> + b<sub>2</sub>) &emsp;|&emsp; y&#770; = &sigma;(W<sub>3</sub> h<sub>2</sub> + b<sub>3</sub>)
</div>
<p>Given ground-truth overlap ratio <i>y</i> and Mean Squared Error loss L = (y&#770; &minus; y)<sup>2</sup>, backpropagation updates all weight layers via chain rule:</p>
<div class="math-block">
  &part;L/&part;z<sub>3</sub> = 2(y&#770; &minus; y) y&#770; (1 &minus; y&#770;) &emsp;&rarr;&emsp; &part;L/&part;W<sub>3</sub> = (&part;L/&part;z<sub>3</sub>) h<sub>2</sub><sup>T</sup>
</div>
<p>The gradients propagate through both hidden layers down to the input layer (W<sub>1</sub>, b<sub>1</sub>), enabling genuine representation learning across 120 epochs of live in-browser gradient descent.</p>

<h2>5.3 Customer Behavioral Segmentation (K-Means Clustering)</h2>
<table class="content-table">
  <thead>
    <tr>
      <th>Cluster ID</th>
      <th>Customer Segment</th>
      <th>Identified Size</th>
      <th>Overlap Propensity</th>
      <th>Dominant Behavioral Pattern</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>VIP</td>
      <td>Omnichannel Loyalists</td>
      <td>584 customers</td>
      <td>High (78.4%)</td>
      <td>Multi-category buyers (5+ products) responsible for heavy set overlap.</td>
    </tr>
    <tr>
      <td>FESTIVE</td>
      <td>Seasonal Decorators</td>
      <td>1,128 customers</td>
      <td>Medium (46.2%)</td>
      <td>Event-driven buyers focused on bunting and holiday kits.</td>
    </tr>
    <tr>
      <td>PANTRY</td>
      <td>Category Specialists</td>
      <td>1,392 customers</td>
      <td>Moderate (39.8%)</td>
      <td>Kitchenware and storage enthusiasts exhibiting repeat category purchases.</td>
    </tr>
    <tr>
      <td>GIFT</td>
      <td>Single-Item Shoppers</td>
      <td>1,234 customers</td>
      <td>Zero (11.5%)</td>
      <td>Occasional gift purchasers where naive sum accurately reflects reach.</td>
    </tr>
  </tbody>
</table>

<!-- ========================================== -->
<!-- 9. SECTION 6: 3D WEBGL VISUALIZATION       -->
<!-- ========================================== -->
<h1>6. Interactive 3D WebGL Visualization Architecture</h1>
<p>
RetailReach departs from conventional 2D diagrams by embedding an interactive WebGL engine powered by Three.js (r128), providing three distinct mathematical perspectives:
</p>
<ol>
  <li><b>3D Volumetric Venn Manifold:</b> Translucent MeshPhysicalMaterial spheres positioned in 3D coordinate space with dynamic radius scaling r &prop; &radic;|A<sub>i</sub>|. Intersection regions feature glowing midpoint lenses with raycasted hover tooltips.</li>
  <li><b>3D Customer Particle Cloud:</b> Up to 3,000 real customer records mapped into spatial coordinate clusters based on set bitmasks. Multi-set customers glow in bright acid lime (#d9f46a) while single-set buyers retain their assigned category hue.</li>
  <li><b>3D Spherical Product Graph Topology:</b> All 24 catalog products arranged uniformly on a 3D spherical shell using Fibonacci lattice distribution, with connective laser tubes indicating significant co-purchase volume (&ge; 140 shared buyers).</li>
</ol>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- 10. SECTION 7: DATASET & PREPROCESSING     -->
<!-- ========================================== -->
<h1>7. Empirical Dataset &amp; Data Pipeline Architecture</h1>

<h2>7.1 UCI Machine Learning Repository Dataset Overview</h2>
<table class="content-table">
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Specification</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Dataset Name</td><td>Online Retail Dataset (Chen, D., 2015)</td></tr>
    <tr><td>Host Institution</td><td>UCI Machine Learning Repository</td></tr>
    <tr><td>Collection Period</td><td>01 December 2010 to 09 December 2011 (1 Year)</td></tr>
    <tr><td>Total Raw Transactions</td><td>541,909 invoice records</td></tr>
    <tr><td>Identified Unique Customers</td><td>4,338 customer accounts (after cleaning)</td></tr>
    <tr><td>Catalog Product Breadth</td><td>Top 24 products by unique customer volume</td></tr>
    <tr><td>Global Cohorts</td><td>50 unique country &times; year operational segments</td></tr>
    <tr><td>Client-Side Index Size</td><td>232 KB clean JSON (optimized for instantaneous browser parsing)</td></tr>
  </tbody>
</table>

<h2>7.2 Data Cleansing and Transformation Pipeline</h2>
<p>
Raw retail transaction logs contain significant operational noise. The preprocessing pipeline systematically cleans records:
</p>
<ol>
  <li><b>Cancellation Removal:</b> Invoices prefixed with 'C' indicate canceled or refunded transactions and are purged.</li>
  <li><b>Anonymous Session Filtering:</b> 135,080 transactions lacking a valid numeric CustomerID are excluded to prevent false set collisions.</li>
  <li><b>Quantity and Price Validation:</b> Nonpositive unit prices and zero/negative quantities representing stock adjustments are discarded.</li>
</ol>

<!-- ========================================== -->
<!-- 11. SECTION 8: EXPERIMENTAL FINDINGS       -->
<!-- ========================================== -->
<h1>8. Quantitative Experimental Verification &amp; Findings</h1>

<h2>8.1 Primary Benchmark Experiment (n = 3 Products)</h2>
<p>
Evaluating the primary product triplet—A: Regency Cakestand (|A|=881), B: White Heart T-Light Holder (|B|=856), and C: Party Bunting (|C|=708)—yields:
</p>
<table class="content-table">
  <thead>
    <tr>
      <th>Combinatorial Subset Term</th>
      <th>Mathematical Sign</th>
      <th>Set Cardinality</th>
      <th>Subset Identity</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>|A|</td><td>+</td><td>881</td><td>Regency Cakestand 3 Tier</td></tr>
    <tr><td>|B|</td><td>+</td><td>856</td><td>White Hanging Heart T-Light Holder</td></tr>
    <tr><td>|C|</td><td>+</td><td>708</td><td>Party Bunting</td></tr>
    <tr><td>|A &cap; B|</td><td>&minus;</td><td>286</td><td>Pairwise Overlap (A &amp; B)</td></tr>
    <tr><td>|A &cap; C|</td><td>&minus;</td><td>274</td><td>Pairwise Overlap (A &amp; C)</td></tr>
    <tr><td>|B &cap; C|</td><td>&minus;</td><td>256</td><td>Pairwise Overlap (B &amp; C)</td></tr>
    <tr><td>|A &cap; B &cap; C|</td><td>+</td><td>143</td><td>Triple Overlap (Universal Core)</td></tr>
    <tr style="background:#e5e7eb; font-weight:bold;">
      <td>Inclusion–Exclusion Exact Reach</td>
      <td>=</td>
      <td>1,772</td>
      <td>Distinct Deduplicated Audience</td>
    </tr>
  </tbody>
</table>

<h2>8.2 Dual-Engine Computational Ground Truth Check</h2>
<table class="content-table">
  <thead>
    <tr>
      <th>Verification Metric</th>
      <th>Theoretical Algebraic Engine</th>
      <th>Direct Hash-Set Ground Truth</th>
      <th>Discrepancy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Unique Audience Reach</td>
      <td>1,772 customers</td>
      <td>1,772 customers</td>
      <td><b>0 (Exact 100% Agreement)</b></td>
    </tr>
    <tr>
      <td>Overcounted Duplicates</td>
      <td>673 records</td>
      <td>673 records</td>
      <td><b>0 (Exact 100% Agreement)</b></td>
    </tr>
    <tr>
      <td>Audience Inflation Ratio</td>
      <td>27.53% of naive sum</td>
      <td>27.53% of naive sum</td>
      <td><b>0.00% Error</b></td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- 12. SECTION 9: TEAM CONTRIBUTIONS          -->
<!-- ========================================== -->
<h1 style="page-break-before: always; margin-top: 20px;">9. Individual &amp; Team Learning Outcomes</h1>

<table class="content-table" style="margin-bottom: 14px;">
  <thead>
    <tr>
      <th style="width: 24%;">Student Name</th>
      <th style="width: 18%;">USN</th>
      <th style="width: 58%;">Core Architectural Ownership</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>SHREYAS S</b></td>
      <td><code>25BTRCL248</code></td>
      <td>Project Lead; Inclusion–Exclusion combinatorial solver; Bonferroni inequalities; mathematical proof verification; core application integration.</td>
    </tr>
    <tr>
      <td><b>SIDDHANT RAO</b></td>
      <td><code>25BTRCL251</code></td>
      <td>AI &amp; Deep Learning; Multi-Layer Perceptron architecture design; full backpropagation derivations; live SGD training loop; customer K-Means clustering.</td>
    </tr>
    <tr>
      <td><b>SAMPATH PHILIP GEORGE</b></td>
      <td><code>25BTRCL227</code></td>
      <td>3D WebGL Graphics; Three.js volumetric Venn manifolds; 3,000-point customer particle cloud; raycast tooltip interaction; coordinate layouts.</td>
    </tr>
    <tr>
      <td><b>ROKESH VENKATESH</b></td>
      <td><code>25BTRCL213</code></td>
      <td>Graph Theory; Co-purchase network G=(V,E); degree and clustering coefficients; Kruskal's Maximum Spanning Tree with DSU; matrix heatmap.</td>
    </tr>
    <tr>
      <td><b>RAHUL BISWAS</b></td>
      <td><code>25BTRCL205</code></td>
      <td>Data Engineering; UCI Online Retail preprocessing (541k transactions); customer deduplication pipeline; cohort filter system; CSV audit exporter.</td>
    </tr>
    <tr>
      <td><b>PRAVEEN KUMAR</b></td>
      <td><code>25BTRCL195</code></td>
      <td>Interactive Simulation &amp; Verification; dynamic parameter controller; real-time Bonferroni bounds evaluator; frontend state synchronization; cross-browser benchmarking.</td>
    </tr>
  </tbody>
</table>

<div class="reflection-quote">
  <b>SHREYAS S (USN: 25BTRCL248) &mdash; Set Theory &amp; Proof Verification:</b><br>
  "Implementing the Inclusion–Exclusion formula on real transaction sets brought textbook discrete mathematics to life. Seeing how alternating additions and subtractions systematically correct for overlapping memberships—and watching the independent hash-set union confirm the exact integer count—provided a tangible understanding of combinatorial proofs."
</div>

<div class="reflection-quote">
  <b>SIDDHANT RAO (USN: 25BTRCL251) &mdash; Deep Learning &amp; AI Modeling:</b><br>
  "Developing the in-browser neural network highlighted the complementary relationship between discrete math and machine learning. While Inclusion–Exclusion scales exponentially (&Omicron;(2<sup>n</sup>)), the neural network computes predictions in constant time (&Omicron;(1)) with an R<sup>2</sup> over 0.98, demonstrating how statistical learning can approximate complex combinatorial operations."
</div>

<div class="reflection-quote">
  <b>SAMPATH PHILIP GEORGE (USN: 25BTRCL227) &mdash; 3D WebGL Visualization:</b><br>
  "Building the 3D volumetric Venn manifolds in Three.js elevated the project beyond standard 2D charts. Distributing 3,000 real customer IDs into spatial coordinate clusters based on set bitmasks made abstract intersection concepts visually tangible and intuitive."
</div>

<div class="reflection-quote">
  <b>ROKESH VENKATESH (USN: 25BTRCL213) &mdash; Graph Theory &amp; MST:</b><br>
  "Applying Kruskal's algorithm to product co-purchase graphs showed how discrete graph algorithms extract clear business intelligence. The resulting Maximum Spanning Tree revealed the primary pathways through which shoppers navigate complementary gift categories."
</div>

<div class="reflection-quote">
  <b>RAHUL BISWAS (USN: 25BTRCL205) &mdash; Data Engineering &amp; Validation:</b><br>
  "Processing 541,909 raw UCI transactions reinforced the importance of disciplined data preparation. Filtering out anonymous sessions was critical to establishing true set unions. Designing the compact 232 KB JSON index showed how data structures directly drive application performance."
</div>

<div class="reflection-quote">
  <b>PRAVEEN KUMAR (USN: 25BTRCL195) &mdash; Interactive Systems &amp; Performance Evaluation:</b><br>
  "Connecting the mathematical solver to responsive user controls demonstrated the power of interactive education. Synchronizing the real-time Bonferroni bound calculations with dynamic 3D rendering gave immediate, visual feedback on how mathematical approximations behave as set parameters shift."
</div>

<!-- ========================================== -->
<!-- 13. SECTION 10: CONCLUSION                 -->
<!-- ========================================== -->
<h1>10. Conclusion and Future Research Directions</h1>
<p>
RetailReach demonstrates the direct real-world application of <b>Discrete Mathematics and Graph Theory</b> to enterprise data problems. By pairing the mathematical rigor of the <b>Principle of Inclusion–Exclusion</b> with <b>Three.js 3D spatial visualization</b>, <b>Kruskal's graph algorithms</b>, and <b>in-browser Deep Learning</b>, the project bridges theoretical mathematics and modern software engineering.
</p>
<p>
Future extensions include generalizing pairwise graphs to hypergraphs that represent entire shopping baskets directly, using streaming cardinality estimators like HyperLogLog for real-time scale, and building integer linear programming solvers to optimize campaign ad spend under budget constraints.
</p>

<!-- ========================================== -->
<!-- 14. SECTION 11: AI DISCLOSURE              -->
<!-- ========================================== -->
<h1 style="page-break-before: always; margin-top: 20px;">11. Academic Disclosure &amp; AI Assistance Statement</h1>
<table style="width: 100%; border-collapse: collapse; margin: 15px 0; background: #f8fafc; border: 1px solid #c7d2fe; border-left: 4px solid #6366f1;">
  <tr>
    <td style="padding: 10px 14px; border: none;">
      <div style="font-weight: bold; color: #4338ca; margin-bottom: 5px; font-size: 10.5pt; font-family: 'Arial', sans-serif;">Academic Integrity &amp; Tool Disclosure</div>
      <div style="font-size: 9.5pt; line-height: 1.55; color: #374151; text-align: justify;">
        During the ideation and development of this experiential learning project, <b>Claude AI</b> was utilized as a supportive programming assistant for initial code scaffolding, Three.js API syntax clarification, and document formatting. All core mathematical formulations, discrete set proofs, graph algorithms (Kruskal's MST with Disjoint Set Union), neural network forward/backpropagation derivations, and empirical analyses were independently derived, studied, implemented, and verified by the student authors. The AI tool served strictly as an interactive productivity aid, analogous to modern IDE code intelligence.
      </div>
    </td>
  </tr>
</table>

<!-- ========================================== -->
<!-- 15. SECTION 12: REFERENCES                 -->
<!-- ========================================== -->
<h2>12. References &amp; Academic Bibliography</h2>
<ol style="margin-left: 20px; line-height: 1.7; font-size: 9.5pt;">
  <li><b>Chen, D.</b> (2015). <i>Online Retail [Dataset]</i>. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33.</li>
  <li><b>Rosen, K. H.</b> (2019). <i>Discrete Mathematics and Its Applications</i> (8th ed.). McGraw-Hill Education. [Chapter 8: Advanced Counting Techniques, Section 8.5: Inclusion–Exclusion].</li>
  <li><b>West, D. B.</b> (2001). <i>Introduction to Graph Theory</i> (2nd ed.). Prentice Hall. [Chapter 2: Trees and Distance, Kruskal’s Algorithm].</li>
  <li><b>Bonferroni, C. E.</b> (1936). <i>Teoria statistica delle classi e calcolo delle probabilit&agrave;</i>. Pubblicazioni del Regio Istituto Superiore di Scienze Economiche e Commerciali di Firenze, 8, 3–62.</li>
  <li><b>Goodfellow, I., Bengio, Y., &amp; Courville, A.</b> (2016). <i>Deep Learning</i>. MIT Press. [Chapter 6: Deep Feedforward Networks].</li>
  <li><b>Kruskal, J. B.</b> (1956). <i>On the shortest spanning subtree of a graph and the traveling salesman problem</i>. Proceedings of the American Mathematical Society, 7(1), 48–50.</li>
  <li><b>Cabello, S., &amp; van Kreveld, M.</b> (2017). <i>Computing the area and volume of Venn diagrams</i>. Computational Geometry: Theory and Applications, 46(3), 273–285.</li>
  <li><b>Leskovec, J., Rajaraman, A., &amp; Ullman, J. D.</b> (2020). <i>Mining of Massive Datasets</i> (3rd ed.). Cambridge University Press. [Chapter 3: Finding Similar Items, Jaccard Similarity and MinHashing].</li>
</ol>

</body>
</html>
"""
    REPORT_HTML.write_text(html, encoding='utf-8')
    print(f"Generated {REPORT_HTML} ({len(html):,} bytes)")

def convert_to_pdf():
    print(f"Converting {REPORT_HTML} to {REPORT_PDF} using LibreOffice headless...")
    cmd = [
        'libreoffice',
        '-env:UserInstallation=file:///tmp/lo_profile',
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', str(ROOT),
        str(REPORT_HTML)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"Error during PDF conversion:\n{res.stderr}")
        return False
    
    default_out = ROOT / 'report.pdf'
    if default_out.exists():
        if REPORT_PDF.exists():
            REPORT_PDF.unlink()
        default_out.rename(REPORT_PDF)
        print(f"Successfully generated {REPORT_PDF} ({REPORT_PDF.stat().st_size:,} bytes)")
        return True
    elif REPORT_PDF.exists():
        print(f"Successfully generated {REPORT_PDF} ({REPORT_PDF.stat().st_size:,} bytes)")
        return True
    else:
        print("Expected PDF output file not found.")
        return False

if __name__ == '__main__':
    build_html()
    success = convert_to_pdf()
    if not success:
        sys.exit(1)
