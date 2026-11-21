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

  // Main Render Loop
  function render() {
    simulatePhysics();

    const width = viewport.clientWidth;
    const height = viewport.clientHeight;

    ctx.clearRect(0, 0, width, height);
    ctx.save();

    // Apply Camera Transform
    ctx.translate(camera.x, camera.y);
    ctx.scale(camera.zoom, camera.zoom);

    // 1. Draw Links
    for (const link of links) {
      const isConnectedToActive = activeNode && (link.source === activeNode || link.target === activeNode);
      ctx.beginPath();
      ctx.moveTo(link.source.x, link.source.y);
      ctx.lineTo(link.target.x, link.target.y);
      ctx.strokeStyle = isConnectedToActive ? "rgba(129, 140, 248, 0.75)" : "rgba(148, 163, 184, 0.18)";
      ctx.lineWidth = isConnectedToActive ? 2.2 : 1.0;
      ctx.stroke();
    }

    // 2. Draw Nodes
    for (const node of nodes) {
      const isSelected = node === activeNode;
      const isHovered = node === hoveredNode;

      // Glow halo
      if (isSelected || isHovered) {
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius + 8, 0, Math.PI * 2);
        ctx.fillStyle = isSelected ? "rgba(99, 102, 241, 0.28)" : "rgba(255, 255, 255, 0.12)";
        ctx.fill();
      }

      // Outer circle
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
      ctx.fillStyle = node.color || "#64748b";
      ctx.fill();
      ctx.lineWidth = isSelected ? 2.5 : 1.2;
      ctx.strokeStyle = isSelected ? "#fff" : "rgba(255, 255, 255, 0.3)";
      ctx.stroke();

      // Node label
      ctx.font = `${isSelected ? "bold " : ""}11px -apple-system, sans-serif`;
      ctx.fillStyle = isSelected ? "#fff" : "#cbd5e1";
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
      drawerBacklinks.innerHTML = "";
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
        drawerBacklinks.innerHTML = "<span style='font-size:11px;color:var(--text-dim)'>gelen bağlantı yok</span>";
      }

      // Outlinks
      drawerOutlinks.innerHTML = "";
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
        drawerOutlinks.innerHTML = "<span style='font-size:11px;color:var(--text-dim)'>giden bağlantı yok</span>";
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
      searchOverlay.innerHTML = "";
      return;
    }

    searchTimeout = setTimeout(async () => {
      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const results = await res.json();
        
        searchOverlay.innerHTML = "";
        if (results.length === 0) {
          searchOverlay.innerHTML = "<div style='padding:12px;font-size:12px;color:var(--text-dim)'>sonuç bulunamadı.</div>";
        } else {
          results.forEach(r => {
            const item = document.createElement("div");
            item.className = "search-item";
            item.innerHTML = `
              <div class="search-item-title">
                <span>⚡ [[${r.node_id}]] ${r.title}</span>
                <span class="search-item-score">skor: ${r.score}</span>
              </div>
              <div class="search-item-snippet">${r.snippet || ""}</div>
            `;
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
