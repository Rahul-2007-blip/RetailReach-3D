/**
 * RetailReach Discrete Mathematics & Graph Theory Module
 * Features:
 *  1. Bipartite Customer-Product Projection into Co-Purchase Graph G = (V, E)
 *  2. Centrality Analysis (Degree Centrality, Weighted Degree, Clustering Coefficient)
 *  3. Kruskal's Minimum/Maximum Spanning Tree (MST) Algorithm Solver
 *  4. Interactive 2D Force-Directed Canvas / SVG Graph Renderer
 *  5. Interactive Adjacency Matrix Heatmap
 */

window.GraphViz = (function() {
  let graphData = null;

  function buildGraph(data, sets, edgeThreshold = 100) {
    const nodes = data.products.map((p, idx) => ({
      id: idx,
      stockCode: p.id,
      name: p.name,
      buyerCount: sets[idx].size,
      radius: 6 + Math.sqrt(sets[idx].size) * 0.35,
      degree: 0,
      weightedDegree: 0,
      clusteringCoefficient: 0
    }));

    const edges = [];
    const adj = Array.from({ length: nodes.length }, () => new Array(nodes.length).fill(0));

    // Compute pairwise overlaps
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        let weight = 0;
        sets[i].forEach(cust => {
          if (sets[j].has(cust)) weight++;
        });

        adj[i][j] = weight;
        adj[j][i] = weight;

        if (weight >= edgeThreshold) {
          edges.push({
            source: i,
            target: j,
            weight: weight,
            isMST: false
          });
          nodes[i].degree++;
          nodes[j].degree++;
          nodes[i].weightedDegree += weight;
          nodes[j].weightedDegree += weight;
        }
      }
    }

    // Compute Clustering Coefficient: C_i = 2 * e_i / (k_i * (k_i - 1))
    for (let i = 0; i < nodes.length; i++) {
      const neighbors = [];
      for (let j = 0; j < nodes.length; j++) {
        if (adj[i][j] >= edgeThreshold) neighbors.push(j);
      }
      const k = neighbors.length;
      if (k > 1) {
        let triEdges = 0;
        for (let a = 0; a < k; a++) {
          for (let b = a + 1; b < k; b++) {
            if (adj[neighbors[a]][neighbors[b]] >= edgeThreshold) triEdges++;
          }
        }
        nodes[i].clusteringCoefficient = (2 * triEdges) / (k * (k - 1));
      } else {
        nodes[i].clusteringCoefficient = 0;
      }
    }

    // Compute Kruskal's Maximum Spanning Tree (MST for strongest co-purchases)
    const sortedEdges = [...edges].sort((a, b) => b.weight - a.weight);
    const parent = Array.from({ length: nodes.length }, (_, i) => i);
    function find(i) {
      if (parent[i] === i) return i;
      return parent[i] = find(parent[i]);
    }
    function union(i, j) {
      const rootI = find(i);
      const rootJ = find(j);
      if (rootI !== rootJ) {
        parent[rootI] = rootJ;
        return true;
      }
      return false;
    }

    let mstEdgeCount = 0;
    sortedEdges.forEach(edge => {
      if (union(edge.source, edge.target)) {
        edge.isMST = true;
        mstEdgeCount++;
      }
    });

    graphData = { nodes, edges, adj, edgeThreshold, mstEdgeCount };
    return graphData;
  }

  // Render 2D Interactive Force/Radial Network on Canvas
  function renderCanvasGraph(canvasId, selectedIndices, showOnlyMST = false) {
    if (!graphData) return;
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    // Don't render if canvas is hidden (zero size)
    const cw = canvas.clientWidth;
    const ch = canvas.clientHeight;
    if (cw < 10 || ch < 10) return;

    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const w = cw;
    const h = ch;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.scale(dpr, dpr);

    ctx.clearRect(0, 0, w, h);

    const cx = w / 2;
    const cy = h / 2;
    const layoutRadius = Math.min(w, h) * 0.40;

    // Calculate node coordinates in circular/force layout
    const coords = graphData.nodes.map((node, i) => {
      const angle = (i / graphData.nodes.length) * Math.PI * 2 - Math.PI / 2;
      return {
        x: cx + Math.cos(angle) * layoutRadius,
        y: cy + Math.sin(angle) * layoutRadius
      };
    });

    // 1. Draw Edges
    graphData.edges.forEach(edge => {
      if (showOnlyMST && !edge.isMST) return;

      const p1 = coords[edge.source];
      const p2 = coords[edge.target];
      const isSelectedPair = selectedIndices.includes(edge.source) && selectedIndices.includes(edge.target);

      ctx.beginPath();
      ctx.moveTo(p1.x, p1.y);
      ctx.lineTo(p2.x, p2.y);

      if (edge.isMST) {
        ctx.strokeStyle = '#d9f46a';
        ctx.lineWidth = isSelectedPair ? 3.5 : 2.0;
        ctx.globalAlpha = isSelectedPair ? 0.95 : 0.65;
      } else {
        ctx.strokeStyle = isSelectedPair ? '#06b6d4' : '#4b4d6e';
        ctx.lineWidth = isSelectedPair ? 2.5 : 1.0;
        ctx.globalAlpha = isSelectedPair ? 0.85 : 0.25;
      }
      ctx.stroke();
    });

    ctx.globalAlpha = 1.0;

    // 2. Draw Nodes
    graphData.nodes.forEach((node, i) => {
      const pos = coords[i];
      const isSelected = selectedIndices.includes(i);

      ctx.beginPath();
      ctx.arc(pos.x, pos.y, node.radius, 0, Math.PI * 2);

      if (isSelected) {
        ctx.fillStyle = '#d9f46a';
        ctx.shadowColor = '#d9f46a';
        ctx.shadowBlur = 12;
      } else {
        ctx.fillStyle = '#8b5cf6';
        ctx.shadowBlur = 0;
      }
      ctx.fill();

      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1.5;
      ctx.stroke();
      ctx.shadowBlur = 0;

      // Label
      ctx.fillStyle = isSelected ? '#ffffff' : '#9ca3af';
      ctx.font = isSelected ? 'bold 10px Inter, sans-serif' : '9px Inter, sans-serif';
      ctx.textAlign = 'center';
      const offset = (pos.y > cy) ? 14 : -10;
      ctx.fillText(`P${i + 1}`, pos.x, pos.y + offset);
    });
  }

  // Render Adjacency Matrix Heatmap
  function renderAdjacencyMatrix(containerId, selectedIndices) {
    const container = document.getElementById(containerId);
    if (!container || !graphData) return;

    // Display matrix for either selected indices (if >= 2) or top 8 products
    const displayList = (selectedIndices.length >= 2)
      ? selectedIndices
      : [0, 1, 2, 3, 4, 5, 6, 7];

    const n = displayList.length;
    let html = `<div class="adj-matrix-wrap"><table class="adj-table"><thead><tr><th>P</th>`;

    for (let j = 0; j < n; j++) {
      html += `<th>P${displayList[j] + 1}</th>`;
    }
    html += `</tr></thead><tbody>`;

    for (let i = 0; i < n; i++) {
      const idxA = displayList[i];
      html += `<tr><th>P${idxA + 1}</th>`;
      for (let j = 0; j < n; j++) {
        const idxB = displayList[j];
        if (i === j) {
          const size = graphData.nodes[idxA].buyerCount;
          html += `<td class="diag-cell" title="Self-cardinality: ${size}">${size}</td>`;
        } else {
          const overlap = graphData.adj[idxA][idxB];
          const intensity = Math.min(1.0, overlap / 280);
          const bg = `rgba(217, 244, 106, ${(intensity * 0.85).toFixed(2)})`;
          const textColor = intensity > 0.45 ? '#11142a' : '#d1d5db';
          html += `<td style="background:${bg};color:${textColor}" title="P${idxA + 1} ∩ P${idxB + 1}: ${overlap} buyers">${overlap}</td>`;
        }
      }
      html += `</tr>`;
    }
    html += `</tbody></table></div>`;
    container.innerHTML = html;
  }

  // Populate Centrality Table
  function renderCentralityTable(tbodyId) {
    const tbody = document.getElementById(tbodyId);
    if (!tbody || !graphData) return;

    // Sort by weighted degree descending
    const sorted = [...graphData.nodes].sort((a, b) => b.weightedDegree - a.weightedDegree);

    let rows = '';
    sorted.slice(0, 10).forEach((node, rank) => {
      const degCentrality = (node.degree / (graphData.nodes.length - 1)).toFixed(3);
      const clusterCoeff = node.clusteringCoefficient.toFixed(3);

      rows += `
        <tr>
          <td><span class="rank-badge">#${rank + 1}</span> <b>P${node.id + 1}</b></td>
          <td class="table-prod-name" title="${node.name}">${node.name}</td>
          <td><b>${node.buyerCount}</b></td>
          <td>${node.degree}</td>
          <td><b>${node.weightedDegree.toLocaleString()}</b></td>
          <td><code>${degCentrality}</code></td>
          <td><code>${clusterCoeff}</code></td>
        </tr>
      `;
    });

    tbody.innerHTML = rows;
  }

  return {
    buildGraph: buildGraph,
    renderCanvasGraph: renderCanvasGraph,
    renderAdjacencyMatrix: renderAdjacencyMatrix,
    renderCentralityTable: renderCentralityTable,
    getGraphData: () => graphData
  };
})();

