#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const PACKAGE_ROOT = path.resolve(__dirname, '..');
const FEATURE = 'testflow';
// Each skill is independent; FORDEC is only one of them (the emergency skill).
// `relPath` is where the skill lives under skills/testflow/ in this repo;
// it installs flat as skills/testflow/<name> regardless of source nesting.
const SKILLS = [
  { name: 'before-startup', relPath: 'before-startup' },
  { name: 'cruising', relPath: 'cruising' },
  { name: 'landing', relPath: 'landing' },
  { name: 'fordec', relPath: 'emergency/fordec' },
];

function filesMatch(left, right) {
  return (
    fs.existsSync(left) &&
    fs.existsSync(right) &&
    fs.readFileSync(left).equals(fs.readFileSync(right))
  );
}

function installSkills({ projectRoot = process.cwd(), global = false, force = false } = {}) {
  const target = global
    ? path.join(os.homedir(), '.claude', 'skills', FEATURE)
    : path.join(path.resolve(projectRoot), '.claude', 'skills', FEATURE);
  const unchanged = [];
  const pending = [];

  for (const { name: skill, relPath } of SKILLS) {
    const source = path.join(PACKAGE_ROOT, 'skills', FEATURE, relPath);
    const destination = path.join(target, skill);
    const sourceSkill = path.join(source, 'SKILL.md');
    const destinationSkill = path.join(destination, 'SKILL.md');

    if (!fs.existsSync(destination)) {
      pending.push({ destination, source, skill });
      continue;
    }

    if (filesMatch(sourceSkill, destinationSkill)) {
      unchanged.push(skill);
      continue;
    }

    if (!force) {
      throw new Error(
        `Refusing to overwrite existing skill: ${skill}. Re-run with --force to replace it.`,
      );
    }

    pending.push({ destination, source, skill });
  }

  fs.mkdirSync(target, { recursive: true });
  for (const { destination, source } of pending) {
    fs.rmSync(destination, { force: true, recursive: true });
    fs.cpSync(source, destination, { recursive: true });
  }

  return {
    installed: pending.map(({ skill }) => skill),
    target,
    unchanged,
  };
}

function printHelp() {
  process.stdout.write(`Testflow installer (independent FORDEC-style skills; fordec is one of several, not the whole set)\n\nUsage:\n  fordec-checklist [--global] [--force]\n\nOptions:\n  --global   Install into ~/.claude/skills/testflow instead of ./.claude/skills/testflow\n  --force    Replace skills with local modifications\n  --help     Show this help\n  --version  Show the package version\n`);
}

function run(argv = process.argv.slice(2)) {
  const known = new Set(['--force', '--global', '--help', '-h', '--version', '-v']);
  const unknown = argv.find((argument) => !known.has(argument));
  if (unknown) {
    throw new Error(`Unknown option: ${unknown}`);
  }

  if (argv.includes('--help') || argv.includes('-h')) {
    printHelp();
    return;
  }

  if (argv.includes('--version') || argv.includes('-v')) {
    const { version } = require('../../package.json');
    process.stdout.write(`${version}\n`);
    return;
  }

  const result = installSkills({
    force: argv.includes('--force'),
    global: argv.includes('--global'),
  });
  const installed = result.installed.length
    ? `Installed: ${result.installed.join(', ')}`
    : 'All skills already match this package.';
  process.stdout.write(`${installed}\nClaude Code skills directory: ${result.target}\n`);
}

if (require.main === module) {
  try {
    run();
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}

module.exports = { installSkills, run };
