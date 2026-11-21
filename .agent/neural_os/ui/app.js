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

  // Physics Simulation Constants
  const REPULSION = 2800;
  const SPRING_LENGTH = 140;
  const SPRING_STRENGTH = 0.045;
  const DAMPING = 0.88;
  const CENTER_GRAVITY = 0.015;

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

  // Force-directed Physics Step
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

        if (dist < 450) {
          const force = REPULSION / distSq;
          const fx = (dx / dist) * force;
          const fy = (dy / dist) * force;
          na.vx -= fx;
          na.vy -= fy;
          nb.vx += fx;
          nb.vy += fy;
        }
      }
    }

    // 2. Spring force along links
    for (const link of links) {
      const dx = link.target.x - link.source.x;
      const dy = link.target.y - link.source.y;
      const dist = Math.sqrt(dx * dx + dy * dy) + 0.1;
      const displacement = dist - SPRING_LENGTH;
      const force = displacement * SPRING_STRENGTH;
      const fx = (dx / dist) * force;
      const fy = (dy / dist) * force;

      link.source.vx += fx;
      link.source.vy += fy;
      link.target.vx -= fx;
      link.target.vy -= fy;
    }

    // 3. Gravity towards center & velocity damping
    for (const node of nodes) {
      if (node === draggedNode) continue;

      node.vx += (cx - node.x) * CENTER_GRAVITY;
      node.vy += (cy - node.y) * CENTER_GRAVITY;

      node.vx *= DAMPING;
      node.vy *= DAMPING;

      node.x += node.vx;
      node.y += node.vy;
    }
  }

  // Draw Cyber Grid & Starfield
  function drawCyberBackground(width, height) {
    // 1. Perspective Cyber Grid
    const gridSize = 48 * camera.zoom;
    const offsetX = (camera.x % gridSize);
    const offsetY = (camera.y % gridSize);

    ctx.save();
    ctx.strokeStyle = "rgba(99, 102, 241, 0.05)";
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

    // 2. Stars
    for (const s of stars) {
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(165, 180, 252, ${s.alpha})`;
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

    // 1. Draw Links & Animated Energy Pulses
    pulseOffset = (pulseOffset + 0.007) % 1.0;

    for (const link of links) {
      const isConnectedToActive = activeNode && (link.source === activeNode || link.target === activeNode);
      ctx.beginPath();
      ctx.moveTo(link.source.x, link.source.y);
      ctx.lineTo(link.target.x, link.target.y);
      ctx.strokeStyle = isConnectedToActive ? "rgba(129, 140, 248, 0.85)" : "rgba(148, 163, 184, 0.16)";
      ctx.lineWidth = isConnectedToActive ? 2.5 : 1.2;
      ctx.stroke();

      // Energy packet animation (flowing photon)
      const dx = link.target.x - link.source.x;
      const dy = link.target.y - link.source.y;
      const px = link.source.x + dx * pulseOffset;
      const py = link.source.y + dy * pulseOffset;

      ctx.beginPath();
      ctx.arc(px, py, isConnectedToActive ? 3.0 : 1.8, 0, Math.PI * 2);
      ctx.fillStyle = isConnectedToActive ? "#38bdf8" : "rgba(129, 140, 248, 0.65)";
      ctx.shadowColor = "#38bdf8";
      ctx.shadowBlur = 6;
      ctx.fill();
      ctx.shadowBlur = 0; // reset
    }

    // 2. Draw Nodes
    const now = Date.now() * 0.003;
    const typeIcons = {
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

    for (const node of nodes) {
      const isSelected = node === activeNode;
      const isHovered = node === hoveredNode;
      const isHub = (node.pagerank || 0) > 18;

      // Holographic Pulsing Outer Rings for Hub / High PageRank nodes
      if (isHub || isSelected) {
        const pulseSize = Math.sin(now + node.radius) * 4;
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius + 10 + pulseSize, 0, Math.PI * 2);
        ctx.strokeStyle = isSelected ? "rgba(56, 189, 248, 0.7)" : `${node.color}55`;
        ctx.lineWidth = 1.2;
        ctx.setLineDash([4, 4]);
        ctx.stroke();
        ctx.setLineDash([]); // reset dash
      }

      // Glow halo
      if (isSelected || isHovered || isHub) {
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius + (isSelected ? 10 : 6), 0, Math.PI * 2);
        ctx.fillStyle = isSelected ? "rgba(56, 189, 248, 0.3)" : `${node.color}25`;
        ctx.shadowColor = node.color || "#8b5cf6";
        ctx.shadowBlur = isSelected ? 16 : 8;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // Outer circle (Glass node container)
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
      ctx.fillStyle = node.color || "#64748b";
      ctx.fill();
      ctx.lineWidth = isSelected ? 2.5 : (isHub ? 2.0 : 1.2);
      ctx.strokeStyle = isSelected ? "#38bdf8" : "rgba(255, 255, 255, 0.6)";
      ctx.stroke();

      // Node Icon (Type symbol)
      const icon = typeIcons[node.type?.toLowerCase()] || "🔹";
      ctx.font = `${Math.max(10, node.radius * 0.9)}px sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(icon, node.x, node.y);

      // Node label
      ctx.font = `${isSelected ? "600 " : ""}11px -apple-system, sans-serif`;
      ctx.fillStyle = isSelected ? "#fff" : "#cbd5e1";
      ctx.textBaseline = "alphabetic";
      ctx.textAlign = "center";
      ctx.fillText(node.title.length > 20 ? node.title.slice(0, 18) + ".." : node.title, node.x, node.y + node.radius + 14);
    }

    ctx.restore();
    requestAnimationFrame(render);
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

  // Open Detailed Drawer for a Node
  async function selectNode(node) {
    activeNode = node;
    try {
      const res = await fetch(`/api/node/${encodeURIComponent(node.id)}`);
      const details = await res.json();

      drawerTitle.textContent = details.title || details.id;
      drawerBadge.textContent = details.type || "concept";
      drawerBadge.style.background = `${node.color}28`;
      drawerBadge.style.color = node.color;

      metricPR.textContent = `${details.pagerank}%`;
      metricIn.textContent = details.in_degree;
      metricOut.textContent = details.out_degree;

      drawerSummary.textContent = details.summary || "özet mevcut değil.";
      drawerContent.textContent = details.content || "";

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
    camera = { x: 0, y: 0, zoom: 1.0 };
  }

  // Pointer & Drag Handlers
  canvas.addEventListener("mousedown", (e) => {
    const rect = canvas.getBoundingClientRect();
    const world = toWorldCoords(e.clientX - rect.left, e.clientY - rect.top);
    const hitNode = findNodeAt(world.x, world.y);

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
      draggedNode.x = world.x;
      draggedNode.y = world.y;
      draggedNode.vx = 0;
      draggedNode.vy = 0;
    } else if (isDragging) {
      camera.x = e.clientX - dragStart.x;
      camera.y = e.clientY - dragStart.y;
    }
  });

  window.addEventListener("mouseup", (e) => {
    if (!isDragging && draggedNode) {
      selectNode(draggedNode);
    }
    isDragging = false;
    draggedNode = null;
  });

  // Zooming
  canvas.addEventListener("wheel", (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
    camera.zoom = Math.max(0.3, Math.min(3.5, camera.zoom * zoomFactor));
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

  // Close search overlay on click outside
  document.addEventListener("click", (e) => {
    if (!searchOverlay.contains(e.target) && e.target !== searchInput) {
      searchOverlay.classList.remove("open");
    }
  });

  // Bootstrap
  resizeCanvas();
  loadGraphData();
  render();
})();
