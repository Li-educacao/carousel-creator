#!/usr/bin/env node
'use strict';

/**
 * LOCAL MEMORY BRIDGE — Pattern Learning & Suggestion Engine
 * Learns from user command patterns and suggests next actions
 * No external dependencies — pure Node.js JSON storage
 */

const fs = require('fs');
const path = require('path');

class LocalMemoryBridge {
  constructor(dataDir = '.synapse') {
    this.dataDir = dataDir;
    this.patternsFile = path.join(dataDir, 'learned-patterns.json');
    this.sessionsDir = path.join(dataDir, 'sessions');
    this.patterns = this.loadPatterns();
    this.ensureDirectories();
  }

  /**
   * Ensure necessary directories exist
   */
  ensureDirectories() {
    if (!fs.existsSync(this.dataDir)) {
      fs.mkdirSync(this.dataDir, { recursive: true });
    }
    if (!fs.existsSync(this.sessionsDir)) {
      fs.mkdirSync(this.sessionsDir, { recursive: true });
    }
  }

  /**
   * Load existing patterns from disk
   */
  loadPatterns() {
    try {
      if (fs.existsSync(this.patternsFile)) {
        const data = fs.readFileSync(this.patternsFile, 'utf8');
        return JSON.parse(data);
      }
    } catch (err) {
      console.error('[memory-bridge] Failed to load patterns:', err.message);
    }
    return {
      commands: {},
      workflows: {},
      agents: {},
      timestamp: new Date().toISOString(),
    };
  }

  /**
   * Save patterns to disk
   */
  savePatterns() {
    try {
      fs.writeFileSync(
        this.patternsFile,
        JSON.stringify(this.patterns, null, 2),
        'utf8'
      );
    } catch (err) {
      console.error('[memory-bridge] Failed to save patterns:', err.message);
    }
  }

  /**
   * Record a command execution
   * @param {string} command - Command executed (e.g., '*create-story')
   * @param {string} agent - Agent used (e.g., '@dev')
   * @param {object} context - Additional context
   */
  recordCommand(command, agent = 'none', context = {}) {
    const key = `${agent}:${command}`;

    if (!this.patterns.commands[key]) {
      this.patterns.commands[key] = {
        count: 0,
        lastUsed: null,
        nextCommands: {},
        contexts: [],
      };
    }

    const record = this.patterns.commands[key];
    record.count += 1;
    record.lastUsed = new Date().toISOString();
    if (!record.contexts.includes(JSON.stringify(context))) {
      record.contexts.push(JSON.stringify(context));
    }

    this.patterns.timestamp = new Date().toISOString();
    this.savePatterns();

    return record;
  }

  /**
   * Record a sequence of commands (workflow)
   * @param {array} commands - Sequence of commands
   * @param {string} agent - Agent
   */
  recordWorkflow(commands, agent = 'none') {
    if (commands.length < 2) return;

    for (let i = 0; i < commands.length - 1; i++) {
      const current = `${agent}:${commands[i]}`;
      const next = commands[i + 1];

      if (!this.patterns.commands[current]) {
        this.patterns.commands[current] = {
          count: 0,
          lastUsed: null,
          nextCommands: {},
          contexts: [],
        };
      }

      if (!this.patterns.commands[current].nextCommands[next]) {
        this.patterns.commands[current].nextCommands[next] = 0;
      }

      this.patterns.commands[current].nextCommands[next] += 1;
    }

    this.savePatterns();
  }

  /**
   * Suggest next command based on current context
   * @param {string} currentCommand - Current command
   * @param {string} agent - Current agent
   * @returns {array} Suggested commands with confidence scores
   */
  suggestNext(currentCommand, agent = 'none') {
    const key = `${agent}:${currentCommand}`;
    const record = this.patterns.commands[key];

    if (!record || Object.keys(record.nextCommands).length === 0) {
      return [];
    }

    const suggestions = Object.entries(record.nextCommands)
      .map(([cmd, count]) => ({
        command: cmd,
        confidence: Math.min((count / record.count) * 100, 100),
      }))
      .sort((a, b) => b.confidence - a.confidence)
      .slice(0, 3); // Top 3 suggestions

    return suggestions;
  }

  /**
   * Get most used commands
   * @param {number} limit - Number of results
   * @returns {array} Top commands
   */
  getMostUsedCommands(limit = 5) {
    return Object.entries(this.patterns.commands)
      .map(([key, record]) => ({
        command: key,
        count: record.count,
        lastUsed: record.lastUsed,
      }))
      .sort((a, b) => b.count - a.count)
      .slice(0, limit);
  }

  /**
   * Get command frequency by agent
   * @returns {object} Commands grouped by agent
   */
  getFrequencyByAgent() {
    const byAgent = {};

    Object.entries(this.patterns.commands).forEach(([key, record]) => {
      const [agent, cmd] = key.split(':');
      if (!byAgent[agent]) {
        byAgent[agent] = [];
      }
      byAgent[agent].push({
        command: cmd,
        count: record.count,
      });
    });

    Object.keys(byAgent).forEach((agent) => {
      byAgent[agent].sort((a, b) => b.count - a.count);
    });

    return byAgent;
  }

  /**
   * Export summary for Synapse context injection
   * @returns {object} Context-ready summary
   */
  exportContext() {
    return {
      totalCommands: Object.keys(this.patterns.commands).length,
      totalExecutions: Object.values(this.patterns.commands).reduce(
        (sum, cmd) => sum + cmd.count,
        0
      ),
      mostUsed: this.getMostUsedCommands(3),
      byAgent: this.getFrequencyByAgent(),
      lastUpdated: this.patterns.timestamp,
    };
  }

  /**
   * Clear old patterns (older than 30 days)
   */
  cleanup() {
    const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);

    Object.entries(this.patterns.commands).forEach(([key, record]) => {
      if (new Date(record.lastUsed) < thirtyDaysAgo) {
        delete this.patterns.commands[key];
      }
    });

    this.savePatterns();
  }
}

module.exports = LocalMemoryBridge;

// CLI usage
if (require.main === module) {
  const bridge = new LocalMemoryBridge();
  const cmd = process.argv[2];

  if (cmd === 'export') {
    console.log(JSON.stringify(bridge.exportContext(), null, 2));
  } else if (cmd === 'suggest') {
    const current = process.argv[3] || '*help';
    const agent = process.argv[4] || '@dev';
    const suggestions = bridge.suggestNext(current, agent);
    console.log(JSON.stringify(suggestions, null, 2));
  } else if (cmd === 'most-used') {
    const used = bridge.getMostUsedCommands();
    console.log(JSON.stringify(used, null, 2));
  } else if (cmd === 'stats') {
    console.log(JSON.stringify(bridge.getFrequencyByAgent(), null, 2));
  } else if (cmd === 'cleanup') {
    bridge.cleanup();
    console.log('Old patterns cleaned up');
  } else {
    console.log(`
LocalMemoryBridge CLI

Usage:
  node local-memory-bridge.js export       - Export context for Synapse
  node local-memory-bridge.js suggest <cmd> [agent] - Suggest next commands
  node local-memory-bridge.js most-used    - Show top 5 commands
  node local-memory-bridge.js stats        - Show frequency by agent
  node local-memory-bridge.js cleanup      - Remove patterns > 30 days old
    `);
  }
}
