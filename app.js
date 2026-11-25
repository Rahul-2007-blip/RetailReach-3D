/**
 * RetailReach Core Orchestrator
 * Integrates:
 *  - Discrete Mathematics Inclusion-Exclusion Engine (up to 5 sets)
 *  - Bonferroni Alternating Bounds Evaluator
 *  - ThreeViz (3D WebGL Spatial Lab)
 *  - MLEngine (Deep Neural Network Overlap Predictor & Customer Segmentation)
 *  - GraphViz (Discrete Graph Theory & Kruskal's MST Analyzer)
 */

const DATA_URL = './data/retailreach-data.json';
const MAX_PRODUCTS = 5;
const fmt = new Intl.NumberFormat('en-US');

let data = null;
let selected = [0, 1, 2]; // Default to top 3 products
let currentTab = '3d-studio';
let current3DMode = 'venn';
let showMSTOnly = false;

const $ = (id) => document.getElementById(id);

function pretty(n) { return fmt.format(n || 0); }

function combinations(values, size) {
  const result = [];
  function walk(start, chosen) {
    if (chosen.length === size) { result.push(chosen.slice()); return; }
    for (let i = start; i <= values.length - (size - chosen.length); i++) {
      chosen.push(values[i]); walk(i + 1, chosen); chosen.pop();
    }
  }
  walk(0, []); return result;
}

// Current cohort buyer sets
function currentSets() {
  const country = $('countryFilter') ? $('countryFilter').value : 'all';
  const year = $('yearFilter') ? $('yearFilter').value : 'all';

  if (!data) return [];
  if (country === 'all' && year === 'all') {
    return data.products.map(p => new Set(p.buyers));
  }

  const sets = data.products.map(() => new Set());
  for (const cohort of data.cohorts) {
    if (country !== 'all' && cohort.country !== country) continue;
    if (year !== 'all' && cohort.year !== year) continue;
    for (const [idx, ids] of Object.entries(cohort.sets)) {
      const target = sets[Number(idx)];
      for (const id of ids) target.add(id);
    }
  }
  return sets;
}

function intersectionCount(indices, sets) {
  if (!indices.length) return 0;
  const ordered = indices.map(i => sets[i]).sort((a, b) => a.size - b.size);
  let count = 0;
  for (const value of ordered[0]) {
    let found = true;
    for (let i = 1; i < ordered.length; i++) {
      if (!ordered[i].has(value)) { found = false; break; }
    }
    if (found) count++;
  }
  return count;
}

// Full Inclusion-Exclusion & Bonferroni Bounds Calculation
function calculateInclusionExclusion(sets) {
  const chosen = selected.slice();
  const terms = [];
  let formula = 0;

  // S_k sums for Bonferroni bounds
  const S = new Array(chosen.length + 1).fill(0);

  for (let size = 1; size <= chosen.length; size++) {
    for (const indices of combinations(chosen, size)) {
      const count = intersectionCount(indices, sets);
      const sign = size % 2 ? 1 : -1;
      formula += sign * count;
      S[size] += count;
      terms.push({ indices, count, sign, size });
    }
  }

  // Direct Ground-Truth Union
  const union = new Set();
  let naiveSum = 0;
  for (const i of chosen) {
    naiveSum += sets[i].size;
    for (const id of sets[i]) union.add(id);
  }

  const overlap = naiveSum - union.size;
  const intersections = terms.filter(t => t.size > 1 && t.count > 0).sort((a, b) => b.count - a.count);

  // Bonferroni partial sums:
  // B_1 = S_1 (Upper bound)
  // B_2 = S_1 - S_2 (Lower bound)
  // B_3 = S_1 - S_2 + S_3 (Upper bound)
  // B_4 = S_1 - S_2 + S_3 - S_4 (Lower bound)
  // B_5 = S_1 - S_2 + S_3 - S_4 + S_5 (Exact)
  const bonferroni = [];
  let running = 0;
  for (let k = 1; k <= chosen.length; k++) {
    const sign = k % 2 ? 1 : -1;
    running += sign * S[k];
    bonferroni.push({
      k: k,
      name: `Order ${k} (${k % 2 ? 'Upper Bound' : 'Lower Bound'})`,
      sk: S[k],
      value: running,
      isUpper: k % 2 !== 0
    });
  }

  return {
    terms,
    formula,
    direct: union.size,
    naiveSum,
    overlap,
    intersections,
    bonferroni,
    S
  };
}

// Product Selector UI
function renderProductList(sets) {
  const listEl = $('productList');
  if (!listEl || !data) return;

  const query = $('productSearch') ? $('productSearch').value.trim().toLowerCase() : '';
  const filtered = data.products.map((p, i) => ({ p, i })).filter(({ p }) =>
    p.name.toLowerCase().includes(query) || p.id.toLowerCase().includes(query)
  );

  if (!filtered.length) {
    listEl.innerHTML = '<div class="loading-state">No matching products found.</div>';
    return;
  }

  listEl.innerHTML = filtered.map(({ p, i }) => {
    const isSelected = selected.includes(i);
    const setIndex = selected.indexOf(i);
    const letter = isSelected ? String.fromCharCode(65 + setIndex) : '';
    const disabled = !isSelected && selected.length >= MAX_PRODUCTS;

    return `
      <div class="product-item ${isSelected ? 'active' : ''} ${disabled ? 'disabled' : ''}" data-index="${i}">
        <div class="prod-badge ${isSelected ? 'badge-set' : ''}">${isSelected ? letter : (i + 1)}</div>
        <div class="prod-details">
          <div class="prod-title" title="${escapeHtml(p.name)}">${escapeHtml(p.name)}</div>
          <div class="prod-code">Stock Code: <b>${escapeHtml(p.id)}</b></div>
        </div>
        <div class="prod-reach-num">${pretty(sets[i].size)} <small>buyers</small></div>
      </div>
    `;
  }).join('');

  listEl.querySelectorAll('.product-item').forEach(el => {
    el.addEventListener('click', () => {
      const idx = Number(el.dataset.index);
      if (selected.includes(idx)) {
        selected = selected.filter(x => x !== idx);
      } else if (selected.length < MAX_PRODUCTS) {
        selected.push(idx);
      }
      renderAll();
    });
  });

  if ($('selectionCount')) $('selectionCount').textContent = `${selected.length} / ${MAX_PRODUCTS}`;
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

// Update Top KPI Cards
function updateKPICards(result) {
  const hasSelection = selected.length > 0;
  if ($('kpiUniqueReach')) $('kpiUniqueReach').textContent = hasSelection ? pretty(result.direct) : '—';
  if ($('kpiDuplicates')) $('kpiDuplicates').textContent = hasSelection ? pretty(result.overlap) : '—';
  if ($('kpiNaiveSum')) $('kpiNaiveSum').textContent = hasSelection ? pretty(result.naiveSum) : '—';

  const overlapPct = result.naiveSum ? Math.round((result.overlap / result.naiveSum) * 100) : 0;
  if ($('kpiOverlapPct')) $('kpiOverlapPct').textContent = hasSelection ? `${overlapPct}%` : '—';
  if ($('kpiSetCount')) $('kpiSetCount').textContent = selected.length;

  // Comparison bar
  if ($('barNaive')) $('barNaive').style.width = '100%';
  if ($('barUnique')) {
    const pct = result.naiveSum ? Math.max(5, (result.direct / result.naiveSum) * 100) : 0;
    $('barUnique').style.width = `${pct}%`;
  }
}

// Render Inclusion-Exclusion Math Proof
function renderProofSection(result) {
  if ($('formulaResultVal')) $('formulaResultVal').textContent = pretty(result.formula);
  if ($('directResultVal')) $('directResultVal').textContent = pretty(result.direct);

  const isMatch = result.formula === result.direct;
  const matchEl = $('mathVerifyStatus');
  if (matchEl) {
    matchEl.textContent = isMatch ? '✓ EXACT PROOF VERIFIED' : 'MISMATCH';
    matchEl.className = isMatch ? 'verify-pill verified' : 'verify-pill error';
  }

  // Formula Expression
  const exprEl = $('formulaExpressionStr');
  if (exprEl) {
    if (selected.length === 0) {
      exprEl.textContent = 'Select at least 1 product to inspect the Inclusion-Exclusion theorem.';
    } else {
      const setLetters = selected.map((_, i) => String.fromCharCode(65 + i));
      const unionLHS = `|${setLetters.join(' ∪ ')}| = `;
      const singleTerms = setLetters.map(l => `|${l}|`).join(' + ');
      const higherOrder = selected.length > 1 ? ' − Pairwise Intersections + Triple Intersections − ...' : '';
      exprEl.textContent = unionLHS + singleTerms + higherOrder;
    }
  }

  // Term Chips
  const termsEl = $('formulaTermsContainer');
  if (termsEl) {
    if (!result.terms.length) {
      termsEl.innerHTML = '<span class="text-muted">No terms to display.</span>';
    } else {
      termsEl.innerHTML = result.terms.map(t => {
        const letters = t.indices.map(i => String.fromCharCode(65 + selected.indexOf(i))).join('∩');
        const signStr = t.sign > 0 ? '+' : '−';
        const chipClass = t.sign > 0 ? 'chip-plus' : 'chip-minus';
        return `
          <div class="term-tag ${chipClass}">
            <span class="sign">${signStr}</span>
            <span class="set-label">|${letters}|</span>
            <span class="count">${pretty(t.count)}</span>
          </div>
        `;
      }).join('');
    }
  }

  // Bonferroni Bounds Timeline
  const bonfEl = $('bonferroniContainer');
  if (bonfEl) {
    bonfEl.innerHTML = result.bonferroni.map((b, idx) => {
      const isFinal = idx === result.bonferroni.length - 1;
      return `
        <div class="bonf-step ${isFinal ? 'bonf-final' : ''}">
          <div class="bonf-header">
            <span class="bonf-order">k = ${b.k}</span>
            <span class="bonf-name">${b.name}</span>
            <span class="bonf-val">${pretty(b.value)}</span>
          </div>
          <div class="bonf-bar-track">
            <div class="bonf-bar-fill ${b.isUpper ? 'upper' : 'lower'}" style="width:${Math.min(100, Math.max(5, (b.value / (result.naiveSum || 1)) * 100))}%"></div>
          </div>
        </div>
      `;
    }).join('');
  }

  // Intersection Ledger Table
  const ledgerEl = $('intersectionLedger');
  if (ledgerEl) {
    if (!result.intersections.length) {
      ledgerEl.innerHTML = '<div class="p-3 text-muted">No overlapping customer segments found for selected scope.</div>';
    } else {
      const maxCount = Math.max(1, result.intersections[0].count);
      ledgerEl.innerHTML = result.intersections.map(t => {
        const prodNames = t.indices.map(i => data.products[i].name).join(' ∩ ');
        const pctOfUnion = Math.round((t.count / (result.direct || 1)) * 100);
        return `
          <div class="ledger-row">
            <div class="ledger-name" title="${escapeHtml(prodNames)}">${escapeHtml(prodNames)}</div>
            <div class="ledger-bar-col">
              <div class="ledger-bar" style="width:${Math.max(3, (t.count / maxCount) * 100)}%"></div>
            </div>
            <div class="ledger-count"><b>${pretty(t.count)}</b> <small>(${pctOfUnion}%)</small></div>
          </div>
        `;
      }).join('');
    }
  }
}

// Render AI / Machine Learning Section
function renderMLSection(sets) {
  if (!selected.length) return;

  const prediction = window.MLEngine.predictOverlap(selected, data, sets);

  if ($('mlPredReach')) $('mlPredReach').textContent = pretty(prediction.predictedReach);
  if ($('mlPredOverlap')) $('mlPredOverlap').textContent = pretty(prediction.predictedOverlap);
  if ($('mlPredOverlapPct')) $('mlPredOverlapPct').textContent = `${prediction.overlapPct}%`;

  const statusEl = $('mlModelStatusBadge');
  if (statusEl) {
    statusEl.textContent = prediction.isTrained ? 'TRAINED (120 Epochs)' : 'INITIALIZED (Random Weights)';
    statusEl.className = prediction.isTrained ? 'status-pill pill-trained' : 'status-pill pill-untrained';
  }

  // Comparison with exact calculation
  const exactResult = calculateInclusionExclusion(sets);
  const delta = Math.abs(prediction.predictedReach - exactResult.direct);
  const errorPct = exactResult.direct > 0 ? ((delta / exactResult.direct) * 100).toFixed(1) : 0;

  if ($('mlExactReach')) $('mlExactReach').textContent = pretty(exactResult.direct);
  if ($('mlDeltaError')) $('mlDeltaError').textContent = `Δ ${pretty(delta)} (${errorPct}% err)`;

  // Render SVG Architecture
  window.MLEngine.renderNetworkSVG('neuralNetSvg');

  // Render Customer Segmentation cards
  const segContainer = $('customerSegmentsGrid');
  if (segContainer) {
    const segments = window.MLEngine.runCustomerSegmentation(data, sets);
    segContainer.innerHTML = segments.map(s => `
      <div class="segment-card" style="border-top:3px solid ${s.color}">
        <div class="segment-title" style="color:${s.color}">${s.name}</div>
        <div class="segment-stat"><b>${pretty(s.count)}</b> <small>customers</small></div>
        <div class="segment-desc">${s.description}</div>
        <div class="segment-tags">
          ${s.traits.map(t => `<span class="trait-tag">${t}</span>`).join('')}
        </div>
      </div>
    `).join('');
  }
}

// Render Graph Theory Section
function renderGraphSection(sets) {
  window.GraphViz.buildGraph(data, sets, 120);
  window.GraphViz.renderCanvasGraph('graphCanvas', selected, showMSTOnly);
  window.GraphViz.renderAdjacencyMatrix('adjMatrixContainer', selected);
  window.GraphViz.renderCentralityTable('centralityTableBody');
}

// Main Render Function
function renderAll() {
  const sets = currentSets();
  if (!sets.length) return;

  renderProductList(sets);

  if (selected.length > 0) {
    const result = calculateInclusionExclusion(sets);
    updateKPICards(result);
    renderProofSection(result);
    renderMLSection(sets);
    renderGraphSection(sets);

    // Update 3D Viewport
    if (window.ThreeViz) {
      window.ThreeViz.setMode(current3DMode, selected, data, sets);
    }
  } else {
    // Clear displays when nothing selected
    updateKPICards({ direct: 0, overlap: 0, naiveSum: 0 });
    renderProofSection({ terms: [], formula: 0, direct: 0, bonferroni: [], intersections: [], naiveSum: 0 });
  }
}

// Setup Event Listeners
function setupEvents() {
  // Filters
  if ($('countryFilter')) $('countryFilter').addEventListener('change', renderAll);
  if ($('yearFilter')) $('yearFilter').addEventListener('change', renderAll);
  if ($('productSearch')) $('productSearch').addEventListener('input', () => renderProductList(currentSets()));

  if ($('clearSelectionBtn')) {
    $('clearSelectionBtn').addEventListener('click', () => {
      selected = [];
      renderAll();
    });
  }

  if ($('resetFiltersBtn')) {
    $('resetFiltersBtn').addEventListener('click', () => {
      if ($('countryFilter')) $('countryFilter').value = 'all';
      if ($('yearFilter')) $('yearFilter').value = 'all';
      selected = [0, 1, 2];
      renderAll();
    });
  }

  // 3D Viewport Controls (Venn, Particle Cloud, 3D Graph)
  document.querySelectorAll('.three-mode-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.three-mode-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      current3DMode = btn.dataset.mode;
      if (window.ThreeViz) {
        window.ThreeViz.setMode(current3DMode, selected, data, currentSets());
      }
    });
  });

  // Main Workspace Tabs
  document.querySelectorAll('.workspace-tab').forEach(tab => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      document.querySelectorAll('.workspace-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const targetId = tab.dataset.target;
      document.querySelectorAll('.tab-view').forEach(view => view.classList.add('hidden'));
      const targetView = $(targetId);
      if (targetView) targetView.classList.remove('hidden');

      // Re-trigger layout if graph or canvas opened
      if (targetId === 'view-graph') {
        setTimeout(() => {
          window.GraphViz.renderCanvasGraph('graphCanvas', selected, showMSTOnly);
        }, 50);
      }
      // Re-init 3D viewport size when tab switches back
      if (targetId === 'view-3d' && window.ThreeViz) {
        setTimeout(() => {
          window.ThreeViz.resize();
          window.ThreeViz.setMode(current3DMode, selected, data, currentSets());
        }, 50);
      }
      // Re-draw AI loss canvas and neural SVG when switching to AI tab
      if (targetId === 'view-ai' && window.MLEngine) {
        setTimeout(() => {
          window.MLEngine.renderLossCanvas('lossCanvas', window.MLEngine.getLossHistory());
          window.MLEngine.renderNetworkSVG('neuralNetSvg');
        }, 50);
      }
    });
  });

  // MST Toggle in Graph Theory Tab
  if ($('toggleMstBtn')) {
    $('toggleMstBtn').addEventListener('click', () => {
      showMSTOnly = !showMSTOnly;
      $('toggleMstBtn').textContent = showMSTOnly ? 'Show Full Network' : 'Show Kruskal MST Only';
      $('toggleMstBtn').classList.toggle('active', showMSTOnly);
      window.GraphViz.renderCanvasGraph('graphCanvas', selected, showMSTOnly);
    });
  }

  // Train Neural Network Button
  if ($('trainModelBtn')) {
    $('trainModelBtn').addEventListener('click', () => {
      const btn = $('trainModelBtn');
      btn.disabled = true;
      btn.textContent = 'Training in Browser...';

      window.MLEngine.trainModel(
        data,
        currentSets(),
        (progress) => {
          if ($('mlEpochCounter')) $('mlEpochCounter').textContent = `Epoch: ${progress.epoch} / ${progress.totalEpochs}`;
          if ($('mlLossVal')) $('mlLossVal').textContent = `MSE Loss: ${progress.loss.toFixed(6)}`;
          window.MLEngine.renderLossCanvas('lossCanvas', progress.history);
          // Update SVG every 10 epochs to avoid flicker
          if (progress.epoch % 10 === 0 || progress.epoch === progress.totalEpochs) {
            window.MLEngine.renderNetworkSVG('neuralNetSvg');
          }
        },
        (res) => {
          btn.disabled = false;
          btn.textContent = 'Re-Train Neural Network';
          renderMLSection(currentSets());
        }
      );
    });
  }

  // CSV Calculation Audit Exporter
  if ($('exportCsvBtn')) {
    $('exportCsvBtn').addEventListener('click', () => {
      if (!data || !selected.length) return;
      const sets = currentSets();
      const result = calculateInclusionExclusion(sets);
      const rows = [
        ['RetailReach Inclusion-Exclusion Audit'],
        ['Dataset', 'UCI Online Retail (CC BY 4.0)'],
        ['Course', 'Discrete Mathematics and Graph Theory (25BSMA10)'],
        ['Institution', 'Jain (Deemed-to-be University) - School of CSE (AIML-D)'],
        ['Submitted By', 'Shreyas S, Siddhant Rao, Sampath Philip George, Rokesh Venkatesh, Rahul Biswas'],
        ['Submitted To', 'Dr. K J Ghanashyam'],
        ['Selected Products', selected.map(i => data.products[i].name).join(' | ')],
        [''],
        ['Intersection Term', 'Sign', 'Intersection Size (Shared Customers)'],
      ];

      result.terms.forEach(t => {
        const label = t.indices.map(i => data.products[i].name).join(' ∩ ');
        rows.push([label, t.sign > 0 ? '+' : '−', t.count]);
      });

      rows.push(['']);
      rows.push(['Naive Sum of Individual Lists', '', result.naiveSum]);
      rows.push(['Inclusion-Exclusion Exact Reach', '', result.formula]);
      rows.push(['Direct Union (Ground Truth)', '', result.direct]);
      rows.push(['Double-counted entries removed', '', result.overlap]);
      rows.push(['Mathematical Proof Match', '', result.formula === result.direct ? 'YES' : 'NO']);

      const csvContent = rows.map(r => r.map(cell => `"${String(cell || '').replace(/"/g, '""')}"`).join(',')).join('\r\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'RetailReach-IE-Audit.csv';
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  // Download PDF Report Button
  if ($('downloadPdfBtn')) {
    $('downloadPdfBtn').addEventListener('click', () => {
      const a = document.createElement('a');
      a.href = 'RetailReach_Report.pdf';
      a.download = 'RetailReach_Report.pdf';
      a.click();
    });
  }
}

// Initialization
async function initApp() {
  try {
    const res = await fetch(DATA_URL);
    if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
    data = await res.json();

    // Populate country filter
    const countryEl = $('countryFilter');
    if (countryEl) {
      const countries = [...new Set(data.cohorts.map(c => c.country))].sort();
      countryEl.innerHTML = '<option value="all">All Global Markets</option>' +
        countries.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('');
    }

    // Initialize 3D WebGL viewport
    if (window.ThreeViz) {
      window.ThreeViz.init('threeContainer');
    }

    setupEvents();
    renderAll();

    // Render loss canvas placeholder on load
    window.MLEngine.renderLossCanvas('lossCanvas', []);
  } catch (err) {
    console.error('App init failed:', err);
    const container = $('productList');
    if (container) {
      container.innerHTML = `<div class="p-4 text-danger">Failed to load dataset: ${escapeHtml(err.message)}</div>`;
    }
  }
}

window.addEventListener('DOMContentLoaded', initApp);
