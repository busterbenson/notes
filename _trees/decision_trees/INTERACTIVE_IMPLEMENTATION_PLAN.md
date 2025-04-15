# Interactive Tree Guide Implementation Plan

This document outlines a plan for converting the markdown-based California Tree Identification Guide into an interactive web experience while maintaining the markdown files as the single source of truth.

## Overview

The implementation will:
- Use existing markdown files directly
- Parse ASCII tree structures into interactive elements
- Preserve all connections between paths and reference materials
- Provide a kid-friendly interface appropriate for ages 8-10
- Require minimal maintenance beyond the existing markdown

## Technical Components

### 1. Jekyll Plugin for Markdown Parsing

Create a Jekyll plugin (`_plugins/tree_parser.rb`) that:
- Loads markdown content from decision tree files
- Makes content available to JavaScript for client-side parsing
- Preserves links to reference materials

```ruby
module Jekyll
  class TreeMarkdownTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super
      @path = text.strip
    end

    def render(context)
      site = context.registers[:site]
      # Find the markdown file that corresponds to the path
      page_path = site.pages.find { |p| p.path.include?(@path) }&.path
      
      if page_path
        content = File.read(page_path)
        # Escape content for JavaScript use
        content_json = content.to_json
        
        # Return JavaScript that will make this content available to the browser
        return "<script>window.treeContent = #{content_json};</script>"
      else
        return "<script>console.error('Could not find tree file: #{@path}');</script>"
      end
    end
  end
end

Liquid::Template.register_tag('tree_markdown', Jekyll::TreeMarkdownTag)
```

### 2. Tree Layout Template

Create an HTML layout template for interactive tree pages (`_layouts/interactive_tree.html`):

```html
---
layout: default
---
<div class="tree-app">
  <div class="tree-navigation">
    <div id="breadcrumb-trail"></div>
    <div id="back-button" class="hidden">Back</div>
    <div id="path-selector">
      <select id="tree-path-select">
        <option value="leaf-needle-path">Leaf/Needle Path</option>
        <option value="bark-path">Bark Path</option>
        <option value="winter-detective-path">Winter Detective Path</option>
        <!-- Add other paths as needed -->
      </select>
    </div>
  </div>
  
  <div class="tree-content">
    <div id="current-node"></div>
  </div>
  
  <div class="tree-sidebar">
    <div id="help-resources"></div>
  </div>
</div>

<!-- Include the markdown content from selected path -->
{% tree_markdown leaf-needle-path.md %}

<script src="{{ '/assets/js/tree-parser.js' | relative_url }}"></script>
<script src="{{ '/assets/js/tree-navigation.js' | relative_url }}"></script>
```

### 3. JavaScript Parser

Create a client-side parser (`/assets/js/tree-parser.js`) that:
- Parses ASCII tree structure into a navigable JavaScript object
- Extracts questions, options, and endpoints
- Preserves links to resources and other paths

```javascript
class TreeParser {
  constructor(markdownContent) {
    this.markdown = markdownContent;
    this.lines = this.markdown.split('\n');
    this.treeStartIndex = this.findTreeStart();
    this.treeEndIndex = this.findTreeEnd(this.treeStartIndex);
  }

  findTreeStart() {
    // Find where the tree structure begins (usually after a ```tree or ```)
    for (let i = 0; i < this.lines.length; i++) {
      if (this.lines[i].trim().startsWith('```') && 
          !this.lines[i].includes('```tree')) {
        return i + 1;
      }
    }
    return 0;
  }
  
  findTreeEnd(startIndex) {
    // Find where the tree structure ends
    for (let i = startIndex; i < this.lines.length; i++) {
      if (this.lines[i].trim() === '```') {
        return i;
      }
    }
    return this.lines.length;
  }

  parseTree() {
    const treeLines = this.lines.slice(this.treeStartIndex, this.treeEndIndex);
    const tree = { nodes: {} };
    let currentPath = [];
    let lastIndentLevel = 0;
    
    // Root node is special
    tree.nodes.root = {
      id: 'root',
      question: 'What catches my eye about this tree?',
      options: []
    };
    
    let currentNodeId = 'root';
    
    treeLines.forEach(line => {
      // Skip empty lines
      if (!line.trim()) return;
      
      // Calculate indent level based on │, ├, └ symbols
      const indentMatch = line.match(/^([\s│├└]+)/);
      const indentLevel = indentMatch ? indentMatch[0].length : 0;
      
      // Parse line content
      let content = line.trim();
      
      // Handle node lines
      if (line.includes('├──') || line.includes('└──')) {
        content = line.replace(/├──|└──/, '').trim();
        
        // Adjust the path based on indent level
        if (indentLevel > lastIndentLevel) {
          // Going deeper
          currentPath.push(currentNodeId);
        } else if (indentLevel < lastIndentLevel) {
          // Going back up
          const stepsBack = (lastIndentLevel - indentLevel) / 2; // Assuming 2 chars per level
          currentPath = currentPath.slice(0, -stepsBack);
        }
        
        const nodeId = `node_${Object.keys(tree.nodes).length}`;
        const parentId = currentPath.length > 0 ? currentPath[currentPath.length - 1] : 'root';
        
        // Is this node a question or an endpoint?
        const isQuestion = content.includes('?') || content.endsWith(':');
        
        if (isQuestion) {
          // It's a decision node
          tree.nodes[nodeId] = {
            id: nodeId,
            question: content,
            options: []
          };
          
          // Add as option to parent
          if (tree.nodes[parentId]) {
            tree.nodes[parentId].options.push({
              text: content,
              next: nodeId
            });
          }
          
          currentNodeId = nodeId;
        } else {
          // Check if it's a link to another path or resource
          const linkMatch = content.match(/\[([^\]]+)\]\(([^)]+)\)/);
          
          if (linkMatch) {
            // It's a link
            const text = linkMatch[1];
            const href = linkMatch[2];
            
            if (href.includes('reference')) {
              // It's a reference resource
              if (!tree.resources) tree.resources = {};
              const resourceId = href.split('/').pop().replace('.md', '');
              tree.resources[resourceId] = {
                title: text,
                path: href.replace('.md', '.html')
              };
              
              // Add resource to parent node
              if (tree.nodes[parentId] && !tree.nodes[parentId].resources) {
                tree.nodes[parentId].resources = [];
              }
              if (tree.nodes[parentId]) {
                tree.nodes[parentId].resources.push(resourceId);
              }
            } else {
              // It's a path redirect
              tree.nodes[parentId].options.push({
                text: content,
                redirect: href.replace('.md', '.html')
              });
            }
          } else {
            // It's a terminal node or option
            tree.nodes[parentId].options.push({
              text: content,
              isEndpoint: true,
              details: this.extractDetails(content)
            });
          }
        }
        
        lastIndentLevel = indentLevel;
      }
    });
    
    return tree;
  }
  
  extractDetails(content) {
    // Extract species details if this is a terminal node
    // For example: "Pacific Dogwood: Slender branches with small button-like buds"
    const parts = content.split(':');
    if (parts.length >= 2) {
      return {
        species: parts[0].trim(),
        description: parts.slice(1).join(':').trim()
      };
    }
    return { description: content };
  }
  
  extractResources() {
    // Find reference links in the markdown content
    const resources = {};
    const resourceRegex = /\[([^\]]+)\]\(references\/([^)]+)\)/g;
    let match;
    
    while ((match = resourceRegex.exec(this.markdown)) !== null) {
      const title = match[1];
      const path = `references/${match[2]}`;
      const id = path.split('/').pop().replace('.md', '');
      
      resources[id] = {
        title: title,
        path: path.replace('.md', '.html')
      };
    }
    
    return resources;
  }
}

// Initialize parser when page loads
document.addEventListener('DOMContentLoaded', () => {
  // Use the markdown content injected by the Jekyll plugin
  if (window.treeContent) {
    const parser = new TreeParser(window.treeContent);
    window.treeData = parser.parseTree();
    window.treeResources = parser.extractResources();
    
    // Initialize the tree navigation
    if (typeof initializeTree === 'function') {
      initializeTree();
    }
  }
  
  // Handle tree path selection changes
  document.getElementById('tree-path-select').addEventListener('change', (e) => {
    const path = e.target.value;
    window.location.href = `/trees/decision_trees/paths/${path}.html?interactive=true`;
  });
});
```

### 4. Tree Navigation JavaScript

Create the interactive elements controller (`/assets/js/tree-navigation.js`):

```javascript
let currentNodeId = 'root';
let visitedNodes = new Set(['root']);
let history = [];

function initializeTree() {
  renderNode(currentNodeId);
  document.getElementById('back-button').addEventListener('click', goBack);
}

function renderNode(nodeId) {
  const node = window.treeData.nodes[nodeId];
  if (!node) return;
  
  // Mark this node as visited
  visitedNodes.add(nodeId);
  
  const contentElement = document.getElementById('current-node');
  
  // Create HTML for the current node
  let html = `<div class="node-content">`;
  
  // Add the question
  if (node.question) {
    html += `<h2 class="node-question">${node.question}</h2>`;
  }
  
  // Add options
  if (node.options && node.options.length > 0) {
    html += `<div class="node-options">`;
    node.options.forEach((option, index) => {
      const optionClass = option.isEndpoint ? 'option-endpoint' : 'option-branch';
      
      html += `<div class="tree-option ${optionClass}" data-index="${index}">
                <div class="option-text">${option.text}</div>
              </div>`;
    });
    html += `</div>`;
  }
  
  html += `</div>`;
  contentElement.innerHTML = html;
  
  // Add click event listeners to options
  document.querySelectorAll('.tree-option').forEach((element, index) => {
    element.addEventListener('click', () => {
      const option = node.options[index];
      
      if (option.redirect) {
        // External redirect
        window.location.href = option.redirect;
      } else if (option.next) {
        // Navigate to next node
        history.push(currentNodeId);
        currentNodeId = option.next;
        renderNode(currentNodeId);
      } else if (option.isEndpoint) {
        // Show endpoint details
        showEndpointDetails(option);
      }
    });
  });
  
  // Update resources sidebar
  if (node.resources) {
    updateResourcesSidebar(node.resources);
  }
  
  // Update breadcrumb
  updateBreadcrumb();
  
  // Show/hide back button
  document.getElementById('back-button').classList.toggle('hidden', history.length === 0);
  
  // Animate new content
  animateElement(contentElement, 'fade-in');
}

function showEndpointDetails(option) {
  const contentElement = document.getElementById('current-node');
  
  let html = `<div class="endpoint-details">
                <h2>${option.details.species || 'Tree Identified!'}</h2>
                <p>${option.details.description}</p>
                <button id="continue-button">Continue Exploring</button>
              </div>`;
              
  contentElement.innerHTML = html;
  
  document.getElementById('continue-button').addEventListener('click', () => {
    renderNode(currentNodeId);
  });
}

function updateResourcesSidebar(resourceIds) {
  const resourcesElement = document.getElementById('help-resources');
  
  let html = `<h3>Helpful Resources</h3><ul>`;
  
  resourceIds.forEach(id => {
    const resource = window.treeResources[id];
    if (resource) {
      html += `<li><a href="${resource.path}" target="_blank">${resource.title}</a></li>`;
    }
  });
  
  html += `</ul>`;
  resourcesElement.innerHTML = html;
}

function updateBreadcrumb() {
  const breadcrumbElement = document.getElementById('breadcrumb-trail');
  
  let html = `<div class="breadcrumb">`;
  
  // Add root
  html += `<span class="breadcrumb-item ${currentNodeId === 'root' ? 'active' : ''}" 
            data-node-id="root">Start</span>`;
  
  // Add history items
  history.forEach((nodeId, index) => {
    const node = window.treeData.nodes[nodeId];
    if (!node) return;
    
    const label = node.question ? 
      (node.question.length > 20 ? node.question.substring(0, 20) + '...' : node.question) : 
      `Step ${index + 1}`;
    
    html += `<span class="breadcrumb-separator">›</span>
             <span class="breadcrumb-item" data-node-id="${nodeId}">${label}</span>`;
  });
  
  // Add current if not root
  if (currentNodeId !== 'root' && currentNodeId !== history[history.length - 1]) {
    const node = window.treeData.nodes[currentNodeId];
    if (node) {
      const label = node.question ? 
        (node.question.length > 20 ? node.question.substring(0, 20) + '...' : node.question) : 
        'Current';
      
      html += `<span class="breadcrumb-separator">›</span>
               <span class="breadcrumb-item active">${label}</span>`;
    }
  }
  
  html += `</div>`;
  breadcrumbElement.innerHTML = html;
  
  // Add click events to breadcrumb items
  document.querySelectorAll('.breadcrumb-item').forEach(item => {
    item.addEventListener('click', () => {
      const nodeId = item.getAttribute('data-node-id');
      if (nodeId && visitedNodes.has(nodeId)) {
        // If going backward, adjust history
        if (history.includes(nodeId)) {
          const index = history.indexOf(nodeId);
          history = history.slice(0, index);
        } else {
          // Going back to root
          history = [];
        }
        currentNodeId = nodeId;
        renderNode(currentNodeId);
      }
    });
  });
}

function goBack() {
  if (history.length > 0) {
    currentNodeId = history.pop();
    renderNode(currentNodeId);
  }
}

function animateElement(element, animationClass) {
  element.classList.add(animationClass);
  setTimeout(() => {
    element.classList.remove(animationClass);
  }, 500);
}
```

### 5. CSS Styling for Kid-Friendly Interface

Create styles for the interactive elements (`/assets/css/tree-app.css`):

```css
/* Base Styles */
.tree-app {
  font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

/* Tree Options */
.tree-option {
  background-color: #f8f9fa;
  border: 3px solid #4CAF50;
  border-radius: 15px;
  padding: 15px;
  margin: 10px 0;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1.2rem;
  position: relative;
}

.tree-option:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  background-color: #e8f5e9;
}

.option-endpoint {
  border-color: #2196F3;
  background-color: #e3f2fd;
}

/* Breadcrumb navigation */
.breadcrumb {
  display: flex;
  flex-wrap: wrap;
  padding: 8px 0;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.breadcrumb-item {
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
}

.breadcrumb-item:hover {
  background-color: #e3f2fd;
}

.breadcrumb-item.active {
  font-weight: bold;
  background-color: #e3f2fd;
}

.breadcrumb-separator {
  padding: 4px;
  color: #757575;
}

/* Back button */
#back-button {
  display: inline-block;
  padding: 8px 16px;
  background-color: #f5f5f5;
  border-radius: 20px;
  cursor: pointer;
  margin-bottom: 1rem;
}

#back-button:hover {
  background-color: #e0e0e0;
}

#back-button.hidden {
  display: none;
}

/* Path selector */
#path-selector {
  margin: 1rem 0;
}

#tree-path-select {
  padding: 8px;
  font-size: 1rem;
  border-radius: 8px;
  border: 2px solid #4CAF50;
}

/* Resources sidebar */
#help-resources {
  background-color: #f1f8e9;
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
}

#help-resources h3 {
  margin-top: 0;
  border-bottom: 1px solid #4CAF50;
  padding-bottom: 8px;
}

#help-resources ul {
  padding-left: 20px;
}

#help-resources a {
  color: #2196F3;
  text-decoration: none;
}

#help-resources a:hover {
  text-decoration: underline;
}

/* Animations */
.fade-in {
  animation: fadeIn 0.5s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Responsive layout */
@media (min-width: 768px) {
  .tree-app {
    display: grid;
    grid-template-columns: 3fr 1fr;
    grid-template-areas:
      "navigation navigation"
      "content sidebar";
    gap: 1rem;
  }
  
  .tree-navigation { grid-area: navigation; }
  .tree-content { grid-area: content; }
  .tree-sidebar { grid-area: sidebar; }
}

/* Kid-friendly enhancements */
.node-question {
  font-size: 1.4rem;
  color: #2E7D32;
  background-color: #f1f8e9;
  padding: 12px;
  border-radius: 10px;
  border-left: 5px solid #4CAF50;
}

.endpoint-details {
  background-color: #e8f5e9;
  border-radius: 10px;
  padding: 15px;
  margin-top: 20px;
  border: 2px solid #4CAF50;
}

.endpoint-details h2 {
  color: #2E7D32;
  margin-top: 0;
}

#continue-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 15px;
  font-family: inherit;
}

#continue-button:hover {
  background-color: #388E3C;
}
```

## Implementation Steps

1. **Directory Setup**

Create these directories if they don't exist:
```
/assets/js/
/assets/css/
/_plugins/
/_layouts/
```

2. **Implementation Files**

Create these key files:
- `/_plugins/tree_parser.rb` - Ruby plugin for Jekyll
- `/assets/js/tree-parser.js` - JavaScript tree parser
- `/assets/js/tree-navigation.js` - Navigation controller
- `/assets/css/tree-app.css` - Styling for interactive elements
- `/_layouts/interactive_tree.html` - Layout template

3. **Interactive Pages**

Create a page file for each tree path:

```yaml
---
layout: interactive_tree
title: Interactive Leaf/Needle Path
permalink: /trees/interactive/leaf-needle/
tree_path: leaf-needle-path.md
---
```

Create a main entry point:

```yaml
---
layout: interactive_tree
title: Interactive Tree Guide
permalink: /trees/interactive/
---
Welcome to the Interactive California Tree Identification Guide! 

This guide helps you identify trees by what catches your eye first. Select a starting path below:
```

4. **Testing and Debugging**

- Verify Jekyll plugin loads markdown files correctly
- Test tree parsing with sample markdown files
- Ensure navigation through tree works as expected
- Verify resources load correctly
- Test on different screen sizes

## Advantages of This Approach

1. **No Content Duplication** - Uses markdown files as the single source of truth
2. **Automatic Updates** - Changes to markdown files immediately reflected in interactive version
3. **Maintains Original Format** - No need to change existing markdown structure
4. **Kid-Friendly Interface** - Designed specifically for elementary-age children
5. **Resource Integration** - Seamlessly incorporates reference guides

## Potential Extensions

1. **Progress Tracking**
   - Store user's progress in localStorage
   - Allow resuming identification sessions
   - Track which trees have been identified

2. **Visual Enhancements**
   - Add image support for tree features
   - Include simple animations for selections
   - Add sound effects for different actions

3. **Gamification Elements**
   - Award badges for identified trees
   - Create a "tree detective journal" to record findings
   - Implement achievement system for completed paths

4. **Accessibility Enhancements**
   - Add text-to-speech support for younger readers
   - Implement high-contrast mode for outdoor use
   - Add keyboard navigation options

## Maintenance Considerations

- When adding new markdown files, no additional work is needed - they'll automatically work with the interactive version
- If ASCII tree structure format changes, the parser will need updating
- CSS and JavaScript files can be minified for production using Jekyll's asset pipeline
- Consider browser compatibility testing, especially for school environments

---

This plan provides a comprehensive approach to creating an interactive web interface for the California Tree Identification Guide while maintaining your markdown files as the single source of truth. When you're ready to implement, you can follow the steps outlined above to create a kid-friendly, engaging tree identification experience.