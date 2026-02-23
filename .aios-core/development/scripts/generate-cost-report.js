#!/usr/bin/env node

/**
 * @module GenerateCostReport
 * @description Reads routing-log.jsonl and generates a cost analysis report
 * @version 1.0.0
 *
 * Usage:
 *   node generate-cost-report.js [--period=today|week|month|all] [--group-by=model|task|agent]
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ─── Config ──────────────────────────────────────────────────────────────────

const DEFAULT_LOG_PATH = path.resolve(__dirname, '../../../.aios/routing-log.jsonl');
const PERIODS = ['today', 'week', 'month', 'all'];
const GROUP_BY_OPTIONS = ['model', 'task', 'agent'];

// ─── Argument Parsing ────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = { period: 'all', groupBy: 'model', logPath: DEFAULT_LOG_PATH };

  for (const arg of argv.slice(2)) {
    if (arg.startsWith('--period=')) {
      const val = arg.split('=')[1];
      if (PERIODS.includes(val)) args.period = val;
    } else if (arg.startsWith('--group-by=')) {
      const val = arg.split('=')[1];
      if (GROUP_BY_OPTIONS.includes(val)) args.groupBy = val;
    } else if (arg.startsWith('--log=')) {
      args.logPath = path.resolve(arg.split('=')[1]);
    }
  }

  return args;
}

// ─── Data Loading ────────────────────────────────────────────────────────────

function loadEntries(logPath) {
  if (!fs.existsSync(logPath)) {
    return [];
  }

  const content = fs.readFileSync(logPath, 'utf-8').trim();
  if (!content) return [];

  return content
    .split('\n')
    .map((line) => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    })
    .filter(Boolean);
}

// ─── Filtering ───────────────────────────────────────────────────────────────

function filterByPeriod(entries, period) {
  if (period === 'all') return entries;

  const now = new Date();
  let cutoff;

  switch (period) {
    case 'today':
      cutoff = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      break;
    case 'week':
      cutoff = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
      break;
    case 'month':
      cutoff = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
      break;
    default:
      return entries;
  }

  return entries.filter((e) => new Date(e.timestamp) >= cutoff);
}

// ─── Aggregation ─────────────────────────────────────────────────────────────

function parseDollar(str) {
  if (!str) return 0;
  const match = String(str).match(/\$?([\d.]+)/);
  return match ? parseFloat(match[1]) : 0;
}

function aggregate(entries, groupBy) {
  const groups = {};

  for (const entry of entries) {
    let key;
    switch (groupBy) {
      case 'model':
        key = entry.model || 'unknown';
        break;
      case 'task':
        key = (entry.context && entry.context.taskName) || 'unknown';
        break;
      case 'agent':
        key = (entry.context && entry.context.agentId) || 'unknown';
        break;
      default:
        key = entry.model || 'unknown';
    }

    if (!groups[key]) {
      groups[key] = { count: 0, estimatedCost: 0, baselineCost: 0 };
    }

    groups[key].count++;
    groups[key].estimatedCost += parseDollar(entry.estimatedCost);

    // Calculate baseline from savings string: "$X.XXXX (YY.Y%)"
    const estimated = parseDollar(entry.estimatedCost);
    const savingsMatch = entry.savings ? String(entry.savings).match(/\$?([\d.]+)/) : null;
    const savingsVal = savingsMatch ? parseFloat(savingsMatch[1]) : 0;
    groups[key].baselineCost += estimated + savingsVal;
  }

  return groups;
}

// ─── Formatting ──────────────────────────────────────────────────────────────

function padRight(str, len) {
  return String(str).padEnd(len);
}

function padLeft(str, len) {
  return String(str).padStart(len);
}

function formatReport(groups, groupBy, period, totalEntries) {
  const lines = [];

  lines.push('');
  lines.push('\uD83D\uDCB0 Model Routing Cost Report');
  lines.push('\u2501'.repeat(40));
  lines.push('');
  lines.push(`Period: ${period} (${totalEntries} routing decisions)`);
  lines.push('');

  const header = padRight(groupBy.charAt(0).toUpperCase() + groupBy.slice(1), 20);
  lines.push(`\uD83D\uDCCA By ${groupBy}:`);
  lines.push(
    `  ${padRight(header, 20)} ${padLeft('Count', 6)} ${padLeft('Est.Cost', 10)} ${padLeft('Baseline', 10)} ${padLeft('Savings', 10)} ${padLeft('%', 7)}`
  );
  lines.push(`  ${'─'.repeat(20)} ${'─'.repeat(6)} ${'─'.repeat(10)} ${'─'.repeat(10)} ${'─'.repeat(10)} ${'─'.repeat(7)}`);

  let totalCount = 0;
  let totalEstimated = 0;
  let totalBaseline = 0;

  const sortedKeys = Object.keys(groups).sort((a, b) => groups[b].count - groups[a].count);

  for (const key of sortedKeys) {
    const g = groups[key];
    const savings = g.baselineCost - g.estimatedCost;
    const pct = g.baselineCost > 0 ? ((savings / g.baselineCost) * 100).toFixed(1) : '0.0';

    lines.push(
      `  ${padRight(key, 20)} ${padLeft(g.count, 6)} ${padLeft('$' + g.estimatedCost.toFixed(4), 10)} ${padLeft('$' + g.baselineCost.toFixed(4), 10)} ${padLeft('$' + savings.toFixed(4), 10)} ${padLeft(pct + '%', 7)}`
    );

    totalCount += g.count;
    totalEstimated += g.estimatedCost;
    totalBaseline += g.baselineCost;
  }

  const totalSavings = totalBaseline - totalEstimated;
  const totalPct = totalBaseline > 0 ? ((totalSavings / totalBaseline) * 100).toFixed(1) : '0.0';

  lines.push(`  ${'─'.repeat(20)} ${'─'.repeat(6)} ${'─'.repeat(10)} ${'─'.repeat(10)} ${'─'.repeat(10)} ${'─'.repeat(7)}`);
  lines.push(
    `  ${padRight('TOTAL', 20)} ${padLeft(totalCount, 6)} ${padLeft('$' + totalEstimated.toFixed(4), 10)} ${padLeft('$' + totalBaseline.toFixed(4), 10)} ${padLeft('$' + totalSavings.toFixed(4), 10)} ${padLeft(totalPct + '%', 7)}`
  );

  lines.push('');
  lines.push(`\uD83D\uDCA1 Summary: Saved $${totalSavings.toFixed(4)} (${totalPct}%) vs running everything on Opus.`);
  lines.push('');

  return lines.join('\n');
}

// ─── Main ────────────────────────────────────────────────────────────────────

function main() {
  const args = parseArgs(process.argv);

  const allEntries = loadEntries(args.logPath);

  if (allEntries.length === 0) {
    console.log('\nNo routing data yet.');
    console.log('Run workflows with model routing enabled to collect data.\n');
    process.exit(0);
  }

  const filtered = filterByPeriod(allEntries, args.period);

  if (filtered.length === 0) {
    console.log(`\nNo routing data for period: ${args.period}\n`);
    process.exit(0);
  }

  const groups = aggregate(filtered, args.groupBy);
  const report = formatReport(groups, args.groupBy, args.period, filtered.length);

  console.log(report);
}

main();
