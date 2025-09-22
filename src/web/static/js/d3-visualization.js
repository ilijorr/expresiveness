/**
 * D3.js Graph Visualization for ExpresiVeNess
 */

class GraphVisualization {
    constructor(svgSelector) {
        this.svg = d3.select(svgSelector);
        this.width = 800;
        this.height = 600;
        this.nodes = [];
        this.links = [];

        this.svg
            .attr('width', this.width)
            .attr('height', this.height);

        // Initialize simulation
        this.simulation = d3.forceSimulation()
            .force('link', d3.forceLink().id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(this.width / 2, this.height / 2));

        // Create arrow marker
        this.svg.append('defs').append('marker')
            .attr('id', 'arrowhead')
            .attr('viewBox', '-0 -5 10 10')
            .attr('refX', 15)
            .attr('refY', 0)
            .attr('orient', 'auto')
            .attr('markerWidth', 13)
            .attr('markerHeight', 13)
            .attr('xoverflow', 'visible')
            .append('path')
            .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
            .attr('fill', '#999')
            .style('stroke', 'none');

        // Create containers
        this.linkContainer = this.svg.append('g').attr('class', 'links');
        this.nodeContainer = this.svg.append('g').attr('class', 'nodes');

        // Add zoom and pan behavior
        this.zoom = d3.zoom()
            .scaleExtent([0.1, 10])
            .on('zoom', (event) => {
                this.currentTransform = event.transform;
                this.nodeContainer.attr('transform', event.transform);
                this.linkContainer.attr('transform', event.transform);
                this.updateViewportRect();
            });

        this.svg.call(this.zoom);

        // Store current transform
        this.currentTransform = d3.zoomIdentity;

        // Initialize minimap
        this.initializeMinimap();
    }

    initializeMinimap() {
        this.minimapSvg = d3.select('#minimap-svg');
        this.minimapWidth = 200;
        this.minimapHeight = 150;

        // Create minimap containers
        this.minimapLinkContainer = this.minimapSvg.append('g').attr('class', 'minimap-links');
        this.minimapNodeContainer = this.minimapSvg.append('g').attr('class', 'minimap-nodes');

        // Viewport rectangle
        this.viewportRect = d3.select('#viewport-rect');

        // Make minimap clickable for navigation
        this.minimapSvg.on('click', (event) => {
            const [x, y] = d3.pointer(event);
            this.navigateToMinimapClick(x, y);
        });
    }

    updateGraph(graphData) {
        this.nodes = graphData.nodes || [];
        this.links = graphData.edges || [];

        this.updateLinks();
        this.updateNodes();

        // Restart simulation
        this.simulation.nodes(this.nodes);
        this.simulation.force('link').links(this.links);
        this.simulation.alpha(1).restart();

        // Update minimap
        this.updateMinimap();
    }

    updateLinks() {
        const linkSelection = this.linkContainer
            .selectAll('.link')
            .data(this.links, d => `${d.source.id || d.source}-${d.target.id || d.target}`);

        linkSelection.exit().remove();

        const linkEnter = linkSelection
            .enter()
            .append('line')
            .attr('class', 'link');

        this.linkElements = linkEnter.merge(linkSelection);
    }

    updateNodes() {
        const nodeSelection = this.nodeContainer
            .selectAll('.node-group')
            .data(this.nodes, d => d.id);

        nodeSelection.exit().remove();

        const nodeEnter = nodeSelection
            .enter()
            .append('g')
            .attr('class', 'node-group')
            .call(this.drag());

        // Add circles
        nodeEnter
            .append('circle')
            .attr('class', 'node')
            .attr('r', 20)
            .attr('fill', d => this.getNodeColor(d.group || 1))
            .on('click', (event, d) => {
                event.stopPropagation();
                this.selectNode(d);
            });

        // Add labels
        nodeEnter
            .append('text')
            .attr('class', 'node-label')
            .attr('dy', '.35em')
            .text(d => d.label || d.id);

        this.nodeElements = nodeEnter.merge(nodeSelection);

        // Update simulation tick
        this.simulation.on('tick', () => {
            this.linkElements
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);

            this.nodeElements
                .attr('transform', d => `translate(${d.x},${d.y})`);

            // Update minimap during simulation
            if (this.simulation.alpha() < 0.1) {
                this.updateMinimap();
            }
        });
    }

    getNodeColor(group) {
        const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'];
        return colors[group % colors.length];
    }

    drag() {
        return d3.drag()
            .on('start', (event, d) => {
                if (!event.active) this.simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            })
            .on('drag', (event, d) => {
                d.fx = event.x;
                d.fy = event.y;
            })
            .on('end', (event, d) => {
                if (!event.active) this.simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            });
    }

    clearGraph() {
        this.linkContainer.selectAll('.link').remove();
        this.nodeContainer.selectAll('.node-group').remove();
        this.nodes = [];
        this.links = [];
        this.simulation.nodes([]);
        this.simulation.force('link').links([]);
    }

    // Pan operations
    panLeft(amount = 50) {
        const newTransform = this.currentTransform.translate(amount, 0);
        this.svg.transition().duration(300).call(this.zoom.transform, newTransform);
    }

    panRight(amount = 50) {
        const newTransform = this.currentTransform.translate(-amount, 0);
        this.svg.transition().duration(300).call(this.zoom.transform, newTransform);
    }

    panUp(amount = 50) {
        const newTransform = this.currentTransform.translate(0, amount);
        this.svg.transition().duration(300).call(this.zoom.transform, newTransform);
    }

    panDown(amount = 50) {
        const newTransform = this.currentTransform.translate(0, -amount);
        this.svg.transition().duration(300).call(this.zoom.transform, newTransform);
    }

    // Zoom operations
    zoomIn(factor = 1.2) {
        const newTransform = this.currentTransform.scale(factor);
        this.svg.transition().duration(300).call(this.zoom.transform, newTransform);
    }

    zoomOut(factor = 0.8) {
        const newTransform = this.currentTransform.scale(factor);
        this.svg.transition().duration(300).call(this.zoom.transform, newTransform);
    }

    resetView() {
        this.svg.transition().duration(500).call(this.zoom.transform, d3.zoomIdentity);
    }

    centerOnGraph() {
        if (this.nodes.length === 0) return;

        // Calculate bounding box of all nodes
        const xExtent = d3.extent(this.nodes, d => d.x);
        const yExtent = d3.extent(this.nodes, d => d.y);

        const centerX = (xExtent[0] + xExtent[1]) / 2;
        const centerY = (yExtent[0] + yExtent[1]) / 2;

        const width = xExtent[1] - xExtent[0];
        const height = yExtent[1] - yExtent[0];

        const scale = Math.min(this.width / width, this.height / height) * 0.8;

        const transform = d3.zoomIdentity
            .translate(this.width / 2 - centerX * scale, this.height / 2 - centerY * scale)
            .scale(scale);

        this.svg.transition().duration(500).call(this.zoom.transform, transform);
    }

    updateMinimap() {
        if (!this.minimapSvg || this.nodes.length === 0) return;

        // Calculate bounding box
        const xExtent = d3.extent(this.nodes, d => d.x || 0);
        const yExtent = d3.extent(this.nodes, d => d.y || 0);

        const graphWidth = xExtent[1] - xExtent[0] || 100;
        const graphHeight = yExtent[1] - yExtent[0] || 100;

        // Calculate scale to fit minimap
        this.minimapScale = Math.min(
            this.minimapWidth / graphWidth,
            this.minimapHeight / graphHeight
        ) * 0.8;

        // Calculate offset to center graph in minimap
        this.minimapOffsetX = (this.minimapWidth - graphWidth * this.minimapScale) / 2 - xExtent[0] * this.minimapScale;
        this.minimapOffsetY = (this.minimapHeight - graphHeight * this.minimapScale) / 2 - yExtent[0] * this.minimapScale;

        // Update minimap links
        const minimapLinks = this.minimapLinkContainer
            .selectAll('.minimap-link')
            .data(this.links);

        minimapLinks.exit().remove();

        minimapLinks.enter()
            .append('line')
            .attr('class', 'minimap-link')
            .attr('stroke', '#999')
            .attr('stroke-width', 1)
            .merge(minimapLinks)
            .attr('x1', d => (d.source.x || 0) * this.minimapScale + this.minimapOffsetX)
            .attr('y1', d => (d.source.y || 0) * this.minimapScale + this.minimapOffsetY)
            .attr('x2', d => (d.target.x || 0) * this.minimapScale + this.minimapOffsetX)
            .attr('y2', d => (d.target.y || 0) * this.minimapScale + this.minimapOffsetY);

        // Update minimap nodes
        const minimapNodes = this.minimapNodeContainer
            .selectAll('.minimap-node')
            .data(this.nodes);

        minimapNodes.exit().remove();

        minimapNodes.enter()
            .append('circle')
            .attr('class', 'minimap-node')
            .attr('r', 3)
            .attr('fill', d => this.getNodeColor(d.group || 1))
            .attr('stroke', '#fff')
            .attr('stroke-width', 1)
            .merge(minimapNodes)
            .attr('cx', d => (d.x || 0) * this.minimapScale + this.minimapOffsetX)
            .attr('cy', d => (d.y || 0) * this.minimapScale + this.minimapOffsetY);

        // Update viewport rectangle
        this.updateViewportRect();
    }

    updateViewportRect() {
        if (!this.viewportRect || !this.currentTransform) return;

        // Calculate viewport bounds in graph coordinates
        const viewportWidth = this.width / this.currentTransform.k;
        const viewportHeight = this.height / this.currentTransform.k;
        const viewportX = -this.currentTransform.x / this.currentTransform.k;
        const viewportY = -this.currentTransform.y / this.currentTransform.k;

        // Convert to minimap coordinates
        const rectX = viewportX * this.minimapScale + this.minimapOffsetX;
        const rectY = viewportY * this.minimapScale + this.minimapOffsetY;
        const rectWidth = viewportWidth * this.minimapScale;
        const rectHeight = viewportHeight * this.minimapScale;

        this.viewportRect
            .style('left', Math.max(0, Math.min(this.minimapWidth - rectWidth, rectX)) + 'px')
            .style('top', Math.max(0, Math.min(this.minimapHeight - rectHeight, rectY)) + 'px')
            .style('width', Math.min(this.minimapWidth, rectWidth) + 'px')
            .style('height', Math.min(this.minimapHeight, rectHeight) + 'px');
    }

    navigateToMinimapClick(x, y) {
        // Convert minimap coordinates to graph coordinates
        const graphX = (x - this.minimapOffsetX) / this.minimapScale;
        const graphY = (y - this.minimapOffsetY) / this.minimapScale;

        // Center the main view on the clicked point
        const transform = d3.zoomIdentity
            .translate(this.width / 2 - graphX * this.currentTransform.k,
                      this.height / 2 - graphY * this.currentTransform.k)
            .scale(this.currentTransform.k);

        this.svg.transition().duration(300).call(this.zoom.transform, transform);
    }

    selectNode(node) {
        // Clear previous selections
        this.nodeContainer.selectAll('.node')
            .classed('selected', false)
            .attr('stroke', '#fff')
            .attr('stroke-width', 2);

        // Select the clicked node
        this.nodeContainer.selectAll('.node-group')
            .filter(d => d.id === node.id)
            .select('.node')
            .classed('selected', true)
            .attr('stroke', '#ff6b35')
            .attr('stroke-width', 4);

        // Trigger external node selection handler
        if (window.onNodeSelected) {
            window.onNodeSelected(node);
        }
    }
}