/**
 * RetailReach 3D Spatial Visualization Engine
 * Powered by Three.js & WebGL
 * Features:
 *  - Mode 1: 3D Volumetric Venn Manifold (translucent intersecting spheres with custom shader glow & raycasting)
 *  - Mode 2: 3D Customer Particle Cloud (actual customer IDs mapped to 3D spatial coordinate clusters)
 *  - Mode 3: 3D Product Graph Topology (force-directed product network with laser-tube edges)
 */

window.ThreeViz = (function() {
  let container, scene, camera, renderer, controls;
  let currentMode = 'venn'; // 'venn' | 'particles' | 'graph'
  let activeObjects = [];
  let animFrameId = null;
  let raycaster, mouse;
  let hoveredInfo = null;
  let isInitialized = false;

  // Color palette for sets A, B, C, D, E
  const SET_COLORS = [
    0x8b5cf6, // A: Electric Violet
    0x06b6d4, // B: Cyber Cyan
    0xf43f5e, // C: Neon Rose
    0xd9f46a, // D: Acid Lime
    0xf59e0b  // E: Amber Glow
  ];

  const SET_NAMES = ['A', 'B', 'C', 'D', 'E'];

  function init(containerId) {
    container = document.getElementById(containerId);
    if (!container) return;

    const width = container.clientWidth || 600;
    const height = container.clientHeight || 420;

    // 1. Scene
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0c0e18, 0.002);

    // 2. Camera
    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 2000);
    camera.position.set(0, 45, 120);

    // 3. Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    // 4. Controls (using OrbitControls if loaded, or custom mouse fallback)
    if (typeof THREE.OrbitControls !== 'undefined') {
      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.maxDistance = 400;
      controls.minDistance = 20;
    } else {
      setupManualMouseControls();
    }

    // 5. Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0xd9f46a, 0.9);
    dirLight1.position.set(60, 100, 80);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x8b5cf6, 0.8);
    dirLight2.position.set(-60, -50, -60);
    scene.add(dirLight2);

    const pointLight = new THREE.PointLight(0x06b6d4, 1.2, 300);
    pointLight.position.set(0, 0, 0);
    scene.add(pointLight);

    // Raycasting for interactive tooltips
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    renderer.domElement.addEventListener('mousemove', onMouseMove, false);
    window.addEventListener('resize', onWindowResize, false);

    isInitialized = true;
    animate();
  }

  function setupManualMouseControls() {
    let isDragging = false;
    let prevMousePos = { x: 0, y: 0 };

    renderer.domElement.addEventListener('mousedown', (e) => {
      isDragging = true;
      prevMousePos = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('mouseup', () => { isDragging = false; });

    renderer.domElement.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      const deltaX = e.clientX - prevMousePos.x;
      const deltaY = e.clientY - prevMousePos.y;

      const rotSpeed = 0.005;
      camera.position.x = camera.position.x * Math.cos(deltaX * rotSpeed) + camera.position.z * Math.sin(deltaX * rotSpeed);
      camera.position.z = camera.position.z * Math.cos(deltaX * rotSpeed) - camera.position.x * Math.sin(deltaX * rotSpeed);
      camera.position.y += deltaY * 0.2;
      camera.lookAt(0, 0, 0);

      prevMousePos = { x: e.clientX, y: e.clientY };
    });

    renderer.domElement.addEventListener('wheel', (e) => {
      e.preventDefault();
      const zoomFactor = e.deltaY * 0.05;
      camera.position.z = Math.max(30, Math.min(300, camera.position.z + zoomFactor));
    });
  }

  function onMouseMove(event) {
    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(activeObjects, true);

    const tooltip = document.getElementById('threeTooltip');
    if (intersects.length > 0 && intersects[0].object.userData && intersects[0].object.userData.label) {
      const ud = intersects[0].object.userData;
      if (tooltip) {
        tooltip.innerHTML = `<strong>${ud.label}</strong><br><span>${ud.value}</span>`;
        tooltip.style.display = 'block';
        // Position relative to the viewport-box container
        const containerRect = container.parentElement.getBoundingClientRect();
        tooltip.style.left = (event.clientX - containerRect.left + 14) + 'px';
        tooltip.style.top = (event.clientY - containerRect.top + 14) + 'px';
      }
    } else {
      if (tooltip) tooltip.style.display = 'none';
    }
  }

  function onWindowResize() {
    if (!container || !renderer || !camera) return;
    const width = container.clientWidth;
    const height = container.clientHeight;
    if (width < 20 || height < 20) return; // Do not resize if container is hidden in background tab
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  }

  function clearActiveObjects() {
    activeObjects.forEach(obj => {
      scene.remove(obj);
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) {
        if (Array.isArray(obj.material)) obj.material.forEach(m => m.dispose());
        else obj.material.dispose();
      }
    });
    activeObjects = [];
  }

  // ==========================================
  // MODE 1: 3D VOLUMETRIC VENN MANIFOLD
  // ==========================================
  function renderVenn3D(selectedIndices, data, sets) {
    if (!isInitialized) return;
    clearActiveObjects();
    currentMode = 'venn';

    const count = selectedIndices.length;
    if (count === 0) return;

    // Define positions in 3D for up to 5 sets
    const positions = [
      new THREE.Vector3(-18, 10, 0),   // Set A
      new THREE.Vector3(18, 10, 0),    // Set B
      new THREE.Vector3(0, -16, 12),   // Set C
      new THREE.Vector3(-14, -14, -14),// Set D
      new THREE.Vector3(14, -14, -14)  // Set E
    ];

    const group = new THREE.Group();

    // 1. Render primary translucent spheres for each set
    selectedIndices.forEach((prodIdx, i) => {
      const p = data.products[prodIdx];
      const buyerCount = sets[prodIdx].size;
      const radius = 22 + Math.min(12, Math.sqrt(buyerCount) * 0.45);
      const pos = positions[i] || new THREE.Vector3(0, 0, 0);

      // Sphere geometry
      const geom = new THREE.SphereGeometry(radius, 40, 40);
      const color = SET_COLORS[i % SET_COLORS.length];

      // Physical glass-like translucent material
      const mat = new THREE.MeshPhysicalMaterial({
        color: color,
        emissive: color,
        emissiveIntensity: 0.15,
        roughness: 0.1,
        transmission: 0.85,
        thickness: 1.8,
        transparent: true,
        opacity: 0.38,
        wireframe: false,
        depthWrite: false
      });

      const sphere = new THREE.Mesh(geom, mat);
      sphere.position.copy(pos);
      sphere.userData = {
        label: `Set ${SET_NAMES[i]}: ${p.name}`,
        value: `${buyerCount.toLocaleString()} identified buyers (${p.id})`
      };
      group.add(sphere);
      activeObjects.push(sphere);

      // Wireframe overlay for geometric aesthetic
      const wireMat = new THREE.MeshBasicMaterial({
        color: color,
        wireframe: true,
        transparent: true,
        opacity: 0.18
      });
      const wireSphere = new THREE.Mesh(geom, wireMat);
      wireSphere.position.copy(pos);
      group.add(wireSphere);

      // Floating 3D Text Billboard / Marker for Set Label
      const markerGeom = new THREE.SphereGeometry(2.2, 16, 16);
      const markerMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
      const marker = new THREE.Mesh(markerGeom, markerMat);
      marker.position.set(pos.x * 1.5, pos.y * 1.5 + radius * 0.8, pos.z * 1.5);
      marker.userData = {
        label: `Set ${SET_NAMES[i]} Anchor`,
        value: p.name
      };
      group.add(marker);
      activeObjects.push(marker);
    });

    // 2. Glowing Core Intersections (Center of Mass of overlapping sets)
    if (count >= 2) {
      // Pairwise glowing connecting beams
      for (let i = 0; i < count; i++) {
        for (let j = i + 1; j < count; j++) {
          const idxA = selectedIndices[i];
          const idxB = selectedIndices[j];
          let sharedCount = 0;
          sets[idxA].forEach(id => { if (sets[idxB].has(id)) sharedCount++; });

          if (sharedCount > 0) {
            const posA = positions[i];
            const posB = positions[j];
            const midPoint = new THREE.Vector3().addVectors(posA, posB).multiplyScalar(0.5);

            // Glowing lens at midpoint
            const lensGeom = new THREE.SphereGeometry(5 + Math.min(8, Math.sqrt(sharedCount) * 0.35), 24, 24);
            const lensMat = new THREE.MeshStandardMaterial({
              color: 0xd9f46a,
              emissive: 0xd9f46a,
              emissiveIntensity: 0.5,
              transparent: true,
              opacity: 0.55,
              roughness: 0.2
            });
            const lens = new THREE.Mesh(lensGeom, lensMat);
            lens.position.copy(midPoint);
            lens.userData = {
              label: `${SET_NAMES[i]} ∩ ${SET_NAMES[j]} Overlap`,
              value: `${sharedCount.toLocaleString()} shared customers`
            };
            group.add(lens);
            activeObjects.push(lens);

            // Connective laser line
            const lineGeom = new THREE.BufferGeometry().setFromPoints([posA, posB]);
            const lineMat = new THREE.LineBasicMaterial({
              color: 0xd9f46a,
              transparent: true,
              opacity: 0.45,
              linewidth: 2
            });
            const line = new THREE.Line(lineGeom, lineMat);
            group.add(line);
          }
        }
      }
    }

    // 3. Central Triple Intersection Core
    if (count >= 3) {
      const idx0 = selectedIndices[0], idx1 = selectedIndices[1], idx2 = selectedIndices[2];
      let tripleCount = 0;
      sets[idx0].forEach(id => {
        if (sets[idx1].has(id) && sets[idx2].has(id)) tripleCount++;
      });

      if (tripleCount > 0) {
        const corePos = new THREE.Vector3(0, 0, 4);
        const coreGeom = new THREE.IcosahedronGeometry(7, 3);
        const coreMat = new THREE.MeshStandardMaterial({
          color: 0xffffff,
          emissive: 0xd9f46a,
          emissiveIntensity: 0.9,
          roughness: 0.1,
          metalness: 0.8,
          wireframe: true
        });
        const core = new THREE.Mesh(coreGeom, coreMat);
        core.position.copy(corePos);
        core.userData = {
          label: `Universal Core: A ∩ B ∩ C`,
          value: `${tripleCount.toLocaleString()} triple-overlap buyers`
        };
        group.add(core);
        activeObjects.push(core);
      }
    }

    // Ambient orbital ring
    const ringGeom = new THREE.RingGeometry(55, 56, 64);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0x3b3a58,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.35
    });
    const ring = new THREE.Mesh(ringGeom, ringMat);
    ring.rotation.x = Math.PI / 2;
    group.add(ring);

    scene.add(group);
    activeObjects.push(group);
  }

  // ==========================================
  // MODE 2: 3D CUSTOMER PARTICLE CLOUD
  // ==========================================
  function renderParticleCloud(selectedIndices, data, sets) {
    if (!isInitialized) return;
    clearActiveObjects();
    currentMode = 'particles';

    if (selectedIndices.length === 0) return;

    // Gather all unique customers in union
    const customerSetMap = new Map(); // customerId -> bitmask
    selectedIndices.forEach((prodIdx, bitIndex) => {
      sets[prodIdx].forEach(cust => {
        const mask = customerSetMap.get(cust) || 0;
        customerSetMap.set(cust, mask | (1 << bitIndex));
      });
    });

    const totalCustomers = customerSetMap.size;
    const particleCount = Math.min(totalCustomers, 3000);
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    // Anchor positions for bitmasks
    const anchorMap = {};
    const n = selectedIndices.length;
    for (let mask = 1; mask < (1 << n); mask++) {
      let x = 0, y = 0, z = 0, bits = 0;
      for (let i = 0; i < n; i++) {
        if (mask & (1 << i)) {
          const angle = (i / n) * Math.PI * 2;
          x += Math.cos(angle) * 35;
          y += Math.sin(angle) * 35;
          z += ((i % 2 === 0) ? 1 : -1) * 12;
          bits++;
        }
      }
      anchorMap[mask] = new THREE.Vector3(x / bits, y / bits, z / bits);
    }

    let i = 0;
    const sampleFactor = Math.max(1, Math.floor(totalCustomers / particleCount));
    let sampleIdx = 0;

    customerSetMap.forEach((mask, custId) => {
      if (i >= particleCount) return;
      if (sampleIdx++ % sampleFactor !== 0) return;

      const anchor = anchorMap[mask] || new THREE.Vector3(0, 0, 0);
      // Gaussian scatter around anchor
      const scatter = 9.0;
      positions[i * 3]     = anchor.x + (Math.random() - 0.5) * scatter;
      positions[i * 3 + 1] = anchor.y + (Math.random() - 0.5) * scatter;
      positions[i * 3 + 2] = anchor.z + (Math.random() - 0.5) * scatter;

      // Color coding: Multi-set customers glow electric lime; single-set have assigned hue
      let c = new THREE.Color();
      const bitCount = (mask.toString(2).match(/1/g) || []).length;
      if (bitCount > 1) {
        c.setHex(0xd9f46a); // Golden lime intersection
      } else {
        const firstBit = Math.log2(mask);
        c.setHex(SET_COLORS[firstBit % SET_COLORS.length]);
      }

      colors[i * 3]     = c.r;
      colors[i * 3 + 1] = c.g;
      colors[i * 3 + 2] = c.b;
      i++;
    });

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    // Particle Material with additive glow
    const pMaterial = new THREE.PointsMaterial({
      size: 2.8,
      vertexColors: true,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending
    });

    const particleSystem = new THREE.Points(geometry, pMaterial);
    scene.add(particleSystem);
    activeObjects.push(particleSystem);

    // Add coordinate reference grid
    const gridHelper = new THREE.GridHelper(100, 20, 0xd9f46a, 0x1f2237);
    gridHelper.position.y = -35;
    scene.add(gridHelper);
    activeObjects.push(gridHelper);
  }

  // ==========================================
  // MODE 3: 3D GRAPH THEORY PRODUCT TOPOLOGY
  // ==========================================
  function renderGraphTopology(data, sets) {
    if (!isInitialized) return;
    clearActiveObjects();
    currentMode = 'graph';

    const group = new THREE.Group();
    const productCount = data.products.length;
    const nodes = [];

    // Arrange 24 products on a dynamic 3D sphere shell
    const radius = 45;
    for (let i = 0; i < productCount; i++) {
      const phi = Math.acos(-1 + (2 * i) / productCount);
      const theta = Math.sqrt(productCount * Math.PI) * phi;

      const pos = new THREE.Vector3(
        radius * Math.cos(theta) * Math.sin(phi),
        radius * Math.sin(theta) * Math.sin(phi),
        radius * Math.cos(phi)
      );

      const p = data.products[i];
      const buyerSize = sets[i].size;
      const nodeSize = 1.8 + Math.sqrt(buyerSize) * 0.18;

      const nodeGeom = new THREE.SphereGeometry(nodeSize, 20, 20);
      const nodeMat = new THREE.MeshStandardMaterial({
        color: 0x8b5cf6,
        emissive: 0x4c1d95,
        roughness: 0.3,
        metalness: 0.7
      });
      const nodeMesh = new THREE.Mesh(nodeGeom, nodeMat);
      nodeMesh.position.copy(pos);
      nodeMesh.userData = {
        label: `Product #${i + 1}: ${p.name}`,
        value: `${buyerSize} unique buyers | Stock: ${p.id}`
      };
      group.add(nodeMesh);
      activeObjects.push(nodeMesh);

      nodes.push({ id: i, pos: pos, buyers: sets[i], name: p.name });
    }

    // Connect top co-purchase edges
    for (let i = 0; i < productCount; i++) {
      for (let j = i + 1; j < productCount; j++) {
        let overlap = 0;
        nodes[i].buyers.forEach(c => { if (nodes[j].buyers.has(c)) overlap++; });

        // Only draw significant edges (threshold >= 140 shared buyers)
        if (overlap >= 140) {
          const lineGeom = new THREE.BufferGeometry().setFromPoints([nodes[i].pos, nodes[j].pos]);
          const intensity = Math.min(1.0, overlap / 280);
          const lineMat = new THREE.LineBasicMaterial({
            color: (overlap > 220) ? 0xd9f46a : 0x06b6d4,
            transparent: true,
            opacity: 0.2 + intensity * 0.6,
            linewidth: 1 + Math.floor(intensity * 2)
          });
          const line = new THREE.Line(lineGeom, lineMat);
          group.add(line);
        }
      }
    }

    scene.add(group);
    activeObjects.push(group);
  }

  // Animation Loop
  function animate() {
    animFrameId = requestAnimationFrame(animate);

    if (controls && controls.update) {
      controls.update();
    }

    // Subtle gentle auto-rotation for 3D presence
    if (activeObjects.length > 0) {
      activeObjects.forEach(obj => {
        if (obj.isGroup || obj.isPoints) {
          obj.rotation.y += 0.0018;
        }
      });
    }

    if (renderer && scene && camera) {
      renderer.render(scene, camera);
    }
  }

  function setMode(mode, selectedIndices, data, sets) {
    onWindowResize();
    if (mode === 'venn') renderVenn3D(selectedIndices, data, sets);
    else if (mode === 'particles') renderParticleCloud(selectedIndices, data, sets);
    else if (mode === 'graph') renderGraphTopology(data, sets);
  }

  return {
    init: init,
    resize: onWindowResize,
    renderVenn3D: renderVenn3D,
    renderParticleCloud: renderParticleCloud,
    renderGraphTopology: renderGraphTopology,
    setMode: setMode,
    getMode: () => currentMode
  };
})();

