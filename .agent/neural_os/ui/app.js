/**
 * Antigravity Enterprise Neural-OS: Interactive Force-Directed Canvas Graph.
 * Pure Vanilla JavaScript & HTML5 Canvas - Zero external script dependencies.
 */
(() => {
  // State
  let nodes = [];
  let links = [];
  let activeNode = null;
  let hoveredNode = null;

  // Starfield & Grid Particles
  const STAR_COUNT = 60;
  let stars = [];
  let pulseOffset = 0; // Animating energy packets along links

  // Viewport / Camera Transform
  let camera = { x: 0, y: 0, zoom: 1.0 };
  let isDragging = false;
  let dragStart = { x: 0, y: 0 };
  let draggedNode = null;

  // Canvas elements
  const canvas = document.getElementById("graphCanvas");
  const ctx = canvas.getContext("2d");
  const viewport = document.getElementById("viewport");

  // Radar Minimap elements
  const radarCanvas = document.getElementById("radarCanvas");
  const radarCtx = radarCanvas.getContext("2d");

  // Filtering state (Multi-Select Enabled)
  let activeFilters = new Set(); // Empty means show all

  // UI Drawer elements
  const sideDrawer = document.getElementById("sideDrawer");
  const btnCloseDrawer = document.getElementById("btnCloseDrawer");
  const drawerTitle = document.getElementById("drawerTitle");
  const drawerBadge = document.getElementById("drawerBadge");
  const drawerSummary = document.getElementById("drawerSummary");
  const drawerBacklinks = document.getElementById("drawerBacklinks");
  const drawerOutlinks = document.getElementById("drawerOutlinks");
  const drawerContent = document.getElementById("drawerContent");
  const metricPR = document.getElementById("metricPR");
  const metricIn = document.getElementById("metricIn");
  const metricOut = document.getElementById("metricOut");

  // Search elements
  const searchInput = document.getElementById("searchInput");
  const searchOverlay = document.getElementById("searchOverlay");
  const btnRecenter = document.getElementById("btnRecenter");
  const btnReload = document.getElementById("btnReload");

  // Physics Simulation Dynamic Variables (Obsidian Grade)
  let repulsion = 2200;
  let springLength = 130;
  const SPRING_STRENGTH = 0.005; // Gentle, numerically stable spring force
  const MAX_VELOCITY = 14;       // Prevents physics explosion / infinite drift
  const DAMPING = 0.84;
  let centerGravity = 0.016;

  function resizeCanvas() {
    canvas.width = viewport.clientWidth * window.devicePixelRatio;
    canvas.height = viewport.clientHeight * window.devicePixelRatio;
    canvas.style.width = `${viewport.clientWidth}px`;
    canvas.style.height = `${viewport.clientHeight}px`;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    initStars();
  }

  function initStars() {
    stars = [];
    const w = viewport.clientWidth;
    const h = viewport.clientHeight;
    for (let i = 0; i < STAR_COUNT; i++) {
      stars.push({
        x: Math.random() * w,
        y: Math.random() * h,
        radius: Math.random() * 1.4 + 0.4,
        alpha: Math.random() * 0.5 + 0.2,
        speed: Math.random() * 0.15 + 0.05
      });
    }
  }

  window.addEventListener("resize", resizeCanvas);

  // Initialize Data
  async function loadGraphData() {
    try {
      const res = await fetch("/api/graph");
      const data = await res.json();
      
      const nodeMap = new Map();
      const width = viewport.clientWidth;
      const height = viewport.clientHeight;

      // Layout nodes in a circle initially
      const count = data.nodes.length;
      nodes = data.nodes.map((n, i) => {
        const angle = (i / count) * 2 * Math.PI;
        const radius = Math.min(width, height) * 0.28;
        const nodeObj = {
          ...n,
          x: width / 2 + radius * Math.cos(angle) + (Math.random() - 0.5) * 40,
          y: height / 2 + radius * Math.sin(angle) + (Math.random() - 0.5) * 40,
          vx: 0,
          vy: 0,
          radius: Math.max(9, Math.min(26, n.val || 12))
        };
        nodeMap.set(n.id, nodeObj);
        return nodeObj;
      });

      links = data.links.map(l => ({
        source: nodeMap.get(l.source) || l.source,
        target: nodeMap.get(l.target) || l.target,
        type: l.type
      })).filter(l => typeof l.source === "object" && typeof l.target === "object");

      recenter();
    } catch (err) {
      console.error("Grafik verisi yuklenemedi:", err);
    }
  }

  // Force-directed Physics Step (Adaptive Damping & Pin Support)
  function simulatePhysics() {
    const width = viewport.clientWidth;
    const height = viewport.clientHeight;
    const cx = width / 2;
    const cy = height / 2;

    // 1. Repulsion between all node pairs
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const na = nodes[i];
        const nb = nodes[j];
        const dx = nb.x - na.x;
        const dy = nb.y - na.y;
        const distSq = dx * dx + dy * dy + 1;
        const dist = Math.sqrt(distSq);

        if (dist < (springLength * 2.3)) {
          const force = (repulsion * 0.8) / distSq;
          const fx = (dx / dist) * force;
          const fy = (dy / dist) * force;
          if (!na.pinned) { na.vx -= fx; na.vy -= fy; }
          if (!nb.pinned) { nb.vx += fx; nb.vy += fy; }
        }
      }
    }

    // 2. Spring force along links
    for (const link of links) {
      const dx = link.target.x - link.source.x;
      const dy = link.target.y - link.source.y;
      const dist = Math.sqrt(dx * dx + dy * dy) + 0.1;
      const displacement = dist - springLength;
      const force = displacement * SPRING_STRENGTH;
      const fx = (dx / dist) * force;
      const fy = (dy / dist) * force;

      if (!link.source.pinned) { link.source.vx += fx; link.source.vy += fy; }
      if (!link.target.pinned) { link.target.vx -= fx; link.target.vy -= fy; }
    }

    // 3. Gravity towards center & velocity damping
    for (const node of nodes) {
      if (node === draggedNode || node.pinned) continue;

      // Velocity Clamping to prevent numerical explosion
      const speed = Math.sqrt(node.vx * node.vx + node.vy * node.vy);
      if (speed > MAX_VELOCITY) {
        node.vx = (node.vx / speed) * MAX_VELOCITY;
        node.vy = (node.vy / speed) * MAX_VELOCITY;
      }

      node.vx += (cx - node.x) * centerGravity;
      node.vy += (cy - node.y) * centerGravity;

      node.vx *= DAMPING;
      node.vy *= DAMPING;

      // Velocity threshold: if movement is tiny, lock into rest
      if (Math.abs(node.vx) < 0.04) node.vx = 0;
      if (Math.abs(node.vy) < 0.04) node.vy = 0;

      node.x += node.vx;
      node.y += node.vy;
    }
  }

  // Draw Cyber Grid & Starfield (Strict Monochrome)
  function drawCyberBackground(width, height) {
    // 1. Monochromatic Grid (Dark Gray lines on Black)
    const gridSize = 48 * camera.zoom;
    const offsetX = (camera.x % gridSize);
    const offsetY = (camera.y % gridSize);

    ctx.save();
    ctx.strokeStyle = "rgba(255, 255, 255, 0.04)";
    ctx.lineWidth = 1;

    // Vertical lines
    for (let x = offsetX; x < width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    // Horizontal lines
    for (let y = offsetY; y < height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // 2. Subtle Monochrome Stars (White/Light Gray specs)
    for (const s of stars) {
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${s.alpha * 0.4})`;
      ctx.fill();
      s.y -= s.speed;
      if (s.y < 0) s.y = height;
    }
    ctx.restore();
  }

  // Main Render Loop
  function render() {
    simulatePhysics();

    const width = viewport.clientWidth;
    const height = viewport.clientHeight;

    ctx.clearRect(0, 0, width, height);

    // Render cyber grid & starfield in screen space
    drawCyberBackground(width, height);

    ctx.save();

    // Apply Camera Transform
    ctx.translate(camera.x, camera.y);
    ctx.scale(camera.zoom, camera.zoom);

    // 1. Draw Links & Animated Energy Pulses (Monochrome)
    pulseOffset = (pulseOffset + 0.007) % 1.0;

    for (const link of links) {
      const isConnectedToActive = activeNode && (link.source === activeNode || link.target === activeNode);
      ctx.beginPath();
      ctx.moveTo(link.source.x, link.source.y);
      ctx.lineTo(link.target.x, link.target.y);
      ctx.strokeStyle = isConnectedToActive ? "rgba(255, 255, 255, 0.70)" : "rgba(255, 255, 255, 0.12)";
      ctx.lineWidth = isConnectedToActive ? 2.0 : 1.0;
      ctx.stroke();

      // Energy packet animation (flowing white/light gray photon)
      const dx = link.target.x - link.source.x;
      const dy = link.target.y - link.source.y;
      const px = link.source.x + dx * pulseOffset;
      const py = link.source.y + dy * pulseOffset;

      ctx.beginPath();
      ctx.arc(px, py, isConnectedToActive ? 2.5 : 1.5, 0, Math.PI * 2);
      ctx.fillStyle = isConnectedToActive ? "#ffffff" : "rgba(200, 200, 200, 0.55)";
      ctx.shadowColor = "#ffffff";
      ctx.shadowBlur = isConnectedToActive ? 5 : 2;
      ctx.fill();
      ctx.shadowBlur = 0; // reset
    }

    // 2. Draw Nodes (Living Digital Twin Icons)
    const now = Date.now() * 0.003;
    const typeIcons = {
      "agent": "🤖",
      "skill": "⚡",
      "rule": "📜",
      "moc": "🧠",
      "root": "🧠",
      "concept": "🧬",
      "concepts": "🧬",
      "decision": "⚖️",
      "decisions": "⚖️",
      "playbook": "📖",
      "playbooks": "📖",
      "episode": "📜",
      "episodes": "📜"
    };

    // Identify neighbors if hovering or active
    const focusedNode = hoveredNode || activeNode;
    const neighborIds = new Set();
    if (focusedNode) {
      neighborIds.add(focusedNode.id);
      for (const link of links) {
        if (link.source.id === focusedNode.id) neighborIds.add(link.target.id);
        if (link.target.id === focusedNode.id) neighborIds.add(link.source.id);
      }
    }

    for (const node of nodes) {
      if (node.filtered) continue;
      const isSelected = node === activeNode;
      const isHovered = node === hoveredNode;
      const isHub = (node.pagerank || 0) > 18;
      const isNeighbor = focusedNode ? neighborIds.has(node.id) : true;
      const opacity = isNeighbor ? 1.0 : 0.25;

      ctx.globalAlpha = opacity;

      // Holographic Pulsing Outer Rings for Hub / High PageRank nodes
      if (isHub || isSelected) {
        const pulseSize = Math.sin(now + node.radius) * 3;
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius + 8 + pulseSize, 0, Math.PI * 2);
        ctx.strokeStyle = isSelected ? "#ffffff" : `${node.color}88`;
        ctx.lineWidth = isSelected ? 1.8 : 1.0;
        ctx.setLineDash([3, 3]);
        ctx.stroke();
        ctx.setLineDash([]); // reset dash
      }

      // Glow halo
      if (isSelected || isHovered || isHub) {
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius + (isSelected ? 8 : 4), 0, Math.PI * 2);
        ctx.fillStyle = isSelected ? "rgba(255, 255, 255, 0.25)" : `${node.color}33`;
        ctx.shadowColor = node.color || "#ffffff";
        ctx.shadowBlur = isSelected ? 16 : 8;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // Outer circle (High-contrast colored container)
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
      ctx.fillStyle = node.color || "#38bdf8";
      ctx.fill();
      ctx.lineWidth = isSelected ? 2.5 : (isHub ? 2.0 : 1.2);
      ctx.strokeStyle = isSelected ? "#ffffff" : "rgba(255, 255, 255, 0.85)";
      ctx.stroke();

      // Node Icon (Type symbol with drop shadow for extreme contrast)
      const icon = typeIcons[node.type?.toLowerCase()] || "🔹";
      ctx.font = `${Math.max(10, node.radius * 0.9)}px sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(icon, node.x, node.y);

      // Node label (Obsidian-Grade Zoom-Dependent Culling)
      // If zoomed out, only show hub / high authority or focused nodes
      const shouldShowLabel = camera.zoom > 1.1 || isHub || isSelected || isHovered || (camera.zoom > 0.7 && (node.type === "agent" || node.type === "MOC" || node.type === "rule"));
      
      if (shouldShowLabel) {
        ctx.font = `${isSelected ? "700 " : "500 "}11.5px -apple-system, BlinkMacSystemFont, sans-serif`;
        ctx.fillStyle = isSelected ? "#ffffff" : (isHub ? "#f8fafc" : "#cbd5e1");
        ctx.textBaseline = "alphabetic";
        ctx.textAlign = "center";
        // Shadow behind text for readability over links
        ctx.shadowColor = "rgba(0,0,0,0.95)";
        ctx.shadowBlur = 4;
        ctx.fillText(node.title.length > 22 ? node.title.slice(0, 20) + ".." : node.title, node.x, node.y + node.radius + 15);
        ctx.shadowBlur = 0;
      }
      ctx.globalAlpha = 1.0;
    }

    ctx.restore();

    // Render Radar Minimap
    drawRadarMinimap();

    requestAnimationFrame(render);
  }

  // Draw Cyber Radar Minimap
  function drawRadarMinimap() {
    const rw = radarCanvas.width;
    const rh = radarCanvas.height;
    radarCtx.clearRect(0, 0, rw, rh);

    if (nodes.length === 0) return;

    // Calculate bounding box of all nodes
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    for (const n of nodes) {
      if (n.x < minX) minX = n.x;
      if (n.x > maxX) maxX = n.x;
      if (n.y < minY) minY = n.y;
      if (n.y > maxY) maxY = n.y;
    }

    const pad = 80;
    minX -= pad; maxX += pad; minY -= pad; maxY += pad;
    const boxW = Math.max(10, maxX - minX);
    const boxH = Math.max(10, maxY - minY);
    const scale = Math.min((rw - 12) / boxW, (rh - 12) / boxH);

    const toRadarX = (wx) => 6 + (wx - minX) * scale;
    const toRadarY = (wy) => 6 + (wy - minY) * scale;

    // Draw minimap nodes (Monochrome)
    for (const n of nodes) {
      const rx = toRadarX(n.x);
      const ry = toRadarY(n.y);
      radarCtx.beginPath();
      radarCtx.arc(rx, ry, n === activeNode ? 3.0 : 1.8, 0, Math.PI * 2);
      radarCtx.fillStyle = n === activeNode ? "#ffffff" : "#525252";
      radarCtx.fill();
    }

    // Draw camera viewport box on radar
    const camWorldTopLeft = toWorldCoords(0, 0);
    const camWorldBottomRight = toWorldCoords(viewport.clientWidth, viewport.clientHeight);
    const rvx = toRadarX(camWorldTopLeft.x);
    const rvy = toRadarY(camWorldTopLeft.y);
    const rvw = (camWorldBottomRight.x - camWorldTopLeft.x) * scale;
    const rvh = (camWorldBottomRight.y - camWorldTopLeft.y) * scale;

    radarCtx.strokeStyle = "rgba(255, 255, 255, 0.50)";
    radarCtx.lineWidth = 1;
    radarCtx.strokeRect(rvx, rvy, rvw, rvh);
  }

  // Coordinate Conversion
  function toWorldCoords(screenX, screenY) {
    return {
      x: (screenX - camera.x) / camera.zoom,
      y: (screenY - camera.y) / camera.zoom
    };
  }

  function findNodeAt(worldX, worldY) {
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      const dx = worldX - n.x;
      const dy = worldY - n.y;
      if (dx * dx + dy * dy <= (n.radius + 4) * (n.radius + 4)) {
        return n;
      }
    }
    return null;
  }

  // Parse and render clean markdown without raw frontmatter
  function renderCleanMarkdown(container, rawText) {
    container.replaceChildren();
    if (!rawText) return;

    // Strip Frontmatter
    let text = rawText;
    if (text.startsWith("---")) {
      const secondIndex = text.indexOf("---", 3);
      if (secondIndex !== -1) {
        text = text.substring(secondIndex + 3).trim();
      }
    }

    const lines = text.split("\n");
    let currentList = null;
    let inRelatedSection = false;

    lines.forEach(line => {
      const trimmed = line.trim();
      if (!trimmed) {
        currentList = null;
        return;
      }

      // Hide repetitive related links block at the end (already rendered as pills)
      if (trimmed.includes("ilgili bağlantılar") || trimmed.includes("İlgili Bağlantılar")) {
        inRelatedSection = true;
        return;
      }
      if (inRelatedSection) {
        if (trimmed.startsWith("#")) {
          inRelatedSection = false;
        } else {
          return; // Skip duplicate link lines
        }
      }

      if (trimmed.startsWith("### ")) {
        currentList = null;
        const h3 = document.createElement("h3");
        h3.textContent = trimmed.substring(4);
        container.appendChild(h3);
      } else if (trimmed.startsWith("## ")) {
        currentList = null;
        const h2 = document.createElement("h2");
        h2.textContent = trimmed.substring(3);
        container.appendChild(h2);
      } else if (trimmed.startsWith("# ")) {
        currentList = null;
        const h1 = document.createElement("h1");
        h1.textContent = trimmed.substring(2);
        container.appendChild(h1);
      } else if (trimmed.startsWith("- ")) {
        if (!currentList) {
          currentList = document.createElement("ul");
          container.appendChild(currentList);
        }
        const li = document.createElement("li");
        li.textContent = trimmed.substring(2);
        currentList.appendChild(li);
      } else {
        currentList = null;
        const p = document.createElement("p");
        p.textContent = trimmed;
        container.appendChild(p);
      }
    });
  }

  // Open Detailed Drawer for a Node
  async function selectNode(node) {
    activeNode = node;
    try {
      const res = await fetch(`/api/node/${encodeURIComponent(node.id)}`);
      const details = await res.json();

      drawerTitle.textContent = details.title || details.id;
      drawerBadge.textContent = details.type || "concept";
      
      // High-contrast, crystal clear badge styling
      const typeColor = node.color || "#38bdf8";
      drawerBadge.style.background = `${typeColor}22`;
      drawerBadge.style.color = typeColor;
      drawerBadge.style.border = `1px solid ${typeColor}55`;

      metricPR.textContent = `${details.pagerank}%`;
      metricIn.textContent = details.in_degree;
      metricOut.textContent = details.out_degree;

      // Render clean, beautiful markdown
      renderCleanMarkdown(drawerContent, details.content || "");

      // Backlinks
      drawerBacklinks.replaceChildren();
      if (details.backlinks && details.backlinks.length > 0) {
        details.backlinks.forEach(bid => {
          const pill = document.createElement("a");
          pill.className = "link-pill";
          pill.textContent = `← [[${bid}]]`;
          pill.onclick = (e) => {
            e.preventDefault();
            const targetNode = nodes.find(n => n.id === bid);
            if (targetNode) selectNode(targetNode);
          };
          drawerBacklinks.appendChild(pill);
        });
      } else {
        const emptyMsg = document.createElement("span");
        emptyMsg.style.cssText = "font-size:11px;color:var(--text-dim)";
        emptyMsg.textContent = "gelen bağlantı yok";
        drawerBacklinks.appendChild(emptyMsg);
      }

      // Outlinks
      drawerOutlinks.replaceChildren();
      if (details.outlinks && details.outlinks.length > 0) {
        details.outlinks.forEach(oid => {
          const pill = document.createElement("a");
          pill.className = "link-pill";
          pill.textContent = `→ [[${oid}]]`;
          pill.onclick = (e) => {
            e.preventDefault();
            const targetNode = nodes.find(n => n.id === oid);
            if (targetNode) selectNode(targetNode);
          };
          drawerOutlinks.appendChild(pill);
        });
      } else {
        const emptyMsg = document.createElement("span");
        emptyMsg.style.cssText = "font-size:11px;color:var(--text-dim)";
        emptyMsg.textContent = "giden bağlantı yok";
        drawerOutlinks.appendChild(emptyMsg);
      }

      sideDrawer.classList.add("open");
    } catch (err) {
      console.error("Düğüm detayları alınamadı:", err);
    }
  }

  function recenter() {
    if (nodes.length === 0) {
      camera = { x: 0, y: 0, zoom: 1.0 };
      return;
    }

    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    for (const n of nodes) {
      if (n.x < minX) minX = n.x;
      if (n.x > maxX) maxX = n.x;
      if (n.y < minY) minY = n.y;
      if (n.y > maxY) maxY = n.y;
    }

    const graphCenterX = (minX + maxX) / 2;
    const graphCenterY = (minY + maxY) / 2;
    const graphW = Math.max(200, maxX - minX + 160);
    const graphH = Math.max(200, maxY - minY + 160);

    const vpW = viewport.clientWidth;
    const vpH = viewport.clientHeight;

    const fitZoom = Math.min(1.2, Math.min(vpW / graphW, vpH / graphH));
    camera.zoom = Math.max(0.4, fitZoom);

    camera.x = vpW / 2 - graphCenterX * camera.zoom;
    camera.y = vpH / 2 - graphCenterY * camera.zoom;
  }

  // Pointer & Drag Handlers
  let nodeDragMoved = false;

  canvas.addEventListener("mousedown", (e) => {
    const rect = canvas.getBoundingClientRect();
    const world = toWorldCoords(e.clientX - rect.left, e.clientY - rect.top);
    const hitNode = findNodeAt(world.x, world.y);

    nodeDragMoved = false;
    if (hitNode) {
      draggedNode = hitNode;
    } else {
      isDragging = true;
      dragStart = { x: e.clientX - camera.x, y: e.clientY - camera.y };
    }
  });

  window.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    const world = toWorldCoords(e.clientX - rect.left, e.clientY - rect.top);

    hoveredNode = findNodeAt(world.x, world.y);
    canvas.style.cursor = hoveredNode ? "pointer" : (isDragging ? "grabbing" : "grab");

    if (draggedNode) {
      nodeDragMoved = true;
      draggedNode.x = world.x;
      draggedNode.y = world.y;
      draggedNode.vx = 0;
      draggedNode.vy = 0;
      draggedNode.pinned = true; // Obsidian-Style Pinning on drag!
    } else if (isDragging) {
      camera.x = e.clientX - dragStart.x;
      camera.y = e.clientY - dragStart.y;
    }
  });

  window.addEventListener("mouseup", (e) => {
    if (!isDragging && draggedNode) {
      if (!nodeDragMoved) {
        selectNode(draggedNode);
      }
    }
    isDragging = false;
    draggedNode = null;
  });

  // Zooming around cursor
  canvas.addEventListener("wheel", (e) => {
    e.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const zoomFactor = e.deltaY < 0 ? 1.12 : 0.88;
    const newZoom = Math.max(0.2, Math.min(4.0, camera.zoom * zoomFactor));

    // Keep world coordinate under mouse fixed while zooming
    camera.x = mouseX - (mouseX - camera.x) * (newZoom / camera.zoom);
    camera.y = mouseY - (mouseY - camera.y) * (newZoom / camera.zoom);
    camera.zoom = newZoom;
  }, { passive: false });

  // Drawer Close
  btnCloseDrawer.addEventListener("click", () => {
    sideDrawer.classList.remove("open");
    activeNode = null;
  });

  btnRecenter.addEventListener("click", recenter);
  btnReload.addEventListener("click", loadGraphData);

  // Search Input Handler (Debounced)
  let searchTimeout = null;
  searchInput.addEventListener("input", (e) => {
    const query = e.target.value.trim();
    clearTimeout(searchTimeout);
    if (!query) {
      searchOverlay.classList.remove("open");
      searchOverlay.replaceChildren();
      return;
    }

    searchTimeout = setTimeout(async () => {
      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const results = await res.json();
        
        searchOverlay.replaceChildren();
        if (results.length === 0) {
          const noRes = document.createElement("div");
          noRes.style.cssText = "padding:12px;font-size:12px;color:var(--text-dim)";
          noRes.textContent = "sonuç bulunamadı.";
          searchOverlay.appendChild(noRes);
        } else {
          results.forEach(r => {
            const item = document.createElement("div");
            item.className = "search-item";
            
            const titleRow = document.createElement("div");
            titleRow.className = "search-item-title";
            
            const titleSpan = document.createElement("span");
            titleSpan.textContent = `⚡ [[${r.node_id}]] ${r.title}`;
            
            const scoreSpan = document.createElement("span");
            scoreSpan.className = "search-item-score";
            scoreSpan.textContent = `skor: ${r.score}`;
            
            titleRow.appendChild(titleSpan);
            titleRow.appendChild(scoreSpan);
            
            const snippetDiv = document.createElement("div");
            snippetDiv.className = "search-item-snippet";
            snippetDiv.textContent = r.snippet || "";
            
            item.appendChild(titleRow);
            item.appendChild(snippetDiv);

            item.onclick = () => {
              searchOverlay.classList.remove("open");
              searchInput.value = "";
              const target = nodes.find(n => n.id === r.node_id);
              if (target) {
                selectNode(target);
                // Pan camera to target node
                camera.x = viewport.clientWidth / 2 - target.x * camera.zoom;
                camera.y = viewport.clientHeight / 2 - target.y * camera.zoom;
              }
            };
            searchOverlay.appendChild(item);
          });
        }
        searchOverlay.classList.add("open");
      } catch (err) {
        console.error("Arama hatası:", err);
      }
    }, 180);
  });

  // Filter Button Listeners (Multi-Select Enabled)
  const btnAll = document.querySelector('.filter-btn[data-type="all"]');
  const typeButtons = document.querySelectorAll('.filter-btn:not([data-type="all"])');

  function updateNodeFiltering() {
    if (activeFilters.size === 0) {
      if (btnAll) btnAll.classList.add("active");
      typeButtons.forEach(b => b.classList.remove("active"));
      nodes.forEach(n => { n.filtered = false; });
    } else {
      if (btnAll) btnAll.classList.remove("active");
      typeButtons.forEach(b => {
        const type = b.getAttribute("data-type");
        if (activeFilters.has(type)) {
          b.classList.add("active");
        } else {
          b.classList.remove("active");
        }
      });
      nodes.forEach(n => {
        const nType = (n.type || "").toLowerCase();
        // Check if node matches any active filter
        let matched = false;
        for (const f of activeFilters) {
          if (nType.includes(f)) {
            matched = true;
            break;
          }
        }
        n.filtered = !matched;
      });
    }
  }

  document.querySelectorAll(".filter-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const type = btn.getAttribute("data-type");

      if (type === "all") {
        activeFilters.clear();
      } else {
        if (activeFilters.has(type)) {
          activeFilters.delete(type);
        } else {
          activeFilters.add(type);
        }
      }
      updateNodeFiltering();
    });
  });

  // Close search overlay on click outside
  document.addEventListener("click", (e) => {
    if (!searchOverlay.contains(e.target) && e.target !== searchInput) {
      searchOverlay.classList.remove("open");
    }
  });

  // Physics Control HUD Wiring (Obsidian Grade)
  const physicsPanel = document.getElementById("physicsPanel");
  const btnTogglePhysics = document.getElementById("btnTogglePhysics");
  const physicsHeader = document.getElementById("physicsHeader");
  const sliderRepulsion = document.getElementById("sliderRepulsion");
  const sliderDistance = document.getElementById("sliderDistance");
  const sliderGravity = document.getElementById("sliderGravity");
  const valRepulsion = document.getElementById("valRepulsion");
  const valDistance = document.getElementById("valDistance");
  const valGravity = document.getElementById("valGravity");
  const btnResetPhysics = document.getElementById("btnResetPhysics");

  function wakeUpSimulation() {
    nodes.forEach(n => {
      if (!n.pinned) {
        n.vx += (Math.random() - 0.5) * 0.8;
        n.vy += (Math.random() - 0.5) * 0.8;
      }
    });
  }

  if (btnTogglePhysics && physicsPanel) {
    const togglePanel = () => {
      physicsPanel.classList.toggle("collapsed");
      btnTogglePhysics.textContent = physicsPanel.classList.contains("collapsed") ? "+" : "−";
    };
    btnTogglePhysics.addEventListener("click", (e) => {
      e.stopPropagation();
      togglePanel();
    });
    physicsHeader.addEventListener("click", togglePanel);
  }

  if (sliderRepulsion && valRepulsion) {
    sliderRepulsion.addEventListener("input", (e) => {
      repulsion = parseFloat(e.target.value);
      valRepulsion.textContent = repulsion;
      wakeUpSimulation();
    });
  }

  if (sliderDistance && valDistance) {
    sliderDistance.addEventListener("input", (e) => {
      springLength = parseFloat(e.target.value);
      valDistance.textContent = springLength;
      wakeUpSimulation();
    });
  }

  if (sliderGravity && valGravity) {
    sliderGravity.addEventListener("input", (e) => {
      centerGravity = parseFloat(e.target.value);
      valGravity.textContent = centerGravity.toFixed(3);
      wakeUpSimulation();
    });
  }

  if (btnResetPhysics) {
    btnResetPhysics.addEventListener("click", () => {
      repulsion = 2800;
      springLength = 140;
      centerGravity = 0.015;

      if (sliderRepulsion) sliderRepulsion.value = 2800;
      if (valRepulsion) valRepulsion.textContent = "2800";
      if (sliderDistance) sliderDistance.value = 140;
      if (valDistance) valDistance.textContent = "140";
      if (sliderGravity) sliderGravity.value = 0.015;
      if (valGravity) valGravity.textContent = "0.015";

      wakeUpSimulation();
    });
  }

  // Fullscreen & Keyboard Shortcuts (Obsidian Grade)
  const btnToggleFullscreen = document.getElementById("btnToggleFullscreen");
  if (btnToggleFullscreen) {
    btnToggleFullscreen.addEventListener("click", () => {
      document.body.classList.toggle("fullscreen-mode");
      resizeCanvas();
    });
  }

  document.addEventListener("keydown", (e) => {
    // ESC closes search, drawer or exits fullscreen
    if (e.key === "Escape") {
      if (document.body.classList.contains("fullscreen-mode")) {
        document.body.classList.remove("fullscreen-mode");
        resizeCanvas();
        return;
      }
      if (searchOverlay.classList.contains("open")) {
        searchOverlay.classList.remove("open");
        return;
      }
      if (sideDrawer.classList.contains("open")) {
        sideDrawer.classList.remove("open");
        activeNode = null;
        return;
      }
    }
    // F key toggles clean full screen
    if ((e.key === "f" || e.key === "F") && document.activeElement !== searchInput) {
      document.body.classList.toggle("fullscreen-mode");
      resizeCanvas();
    }
  });

  // Bootstrap
  resizeCanvas();
  loadGraphData();
  render();
})();
