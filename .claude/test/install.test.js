'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const PACKAGE_ROOT = path.resolve(__dirname, '..');
const REPO_ROOT = path.resolve(PACKAGE_ROOT, '..');
const FEATURE = 'testflow';
// Each skill is independent; fordec is one of them, not a parent of the rest.
const SKILLS = [
  { name: 'before-startup', relPath: 'before-startup' },
  { name: 'cruising', relPath: 'cruising' },
  { name: 'landing', relPath: 'landing' },
  { name: 'fordec', relPath: 'emergency/fordec' },
];
const SKILL_NAMES = SKILLS.map(({ name }) => name);

function makeTempDir(t) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'testflow-'));
  t.after(() => fs.rmSync(directory, { force: true, recursive: true }));
  return directory;
}

test('plugin manifest exposes all four independent testflow skills', () => {
  const manifest = JSON.parse(
    fs.readFileSync(path.join(REPO_ROOT, '.claude-plugin', 'plugin.json'), 'utf8'),
  );
  const packageJson = JSON.parse(
    fs.readFileSync(path.join(REPO_ROOT, 'package.json'), 'utf8'),
  );

  assert.equal(manifest.name, 'testflow');
  assert.equal(manifest.version, packageJson.version);
  for (const { relPath } of SKILLS) {
    assert.ok(
      fs.existsSync(path.join(PACKAGE_ROOT, 'skills', FEATURE, relPath, 'SKILL.md')),
    );
  }
});

test('installer copies every skill into a project Claude directory', (t) => {
  const { installSkills } = require('../bin/checklist.js');
  const projectRoot = makeTempDir(t);

  const result = installSkills({ projectRoot });

  assert.deepEqual(result.installed, SKILL_NAMES);
  assert.equal(result.target, path.join(projectRoot, '.claude', 'skills', FEATURE));
  for (const { name, relPath } of SKILLS) {
    const installed = fs.readFileSync(
      path.join(result.target, name, 'SKILL.md'),
      'utf8',
    );
    const source = fs.readFileSync(
      path.join(PACKAGE_ROOT, 'skills', FEATURE, relPath, 'SKILL.md'),
      'utf8',
    );
    assert.equal(installed, source);
  }
});

test('installer refuses to overwrite a changed skill without --force', (t) => {
  const { installSkills } = require('../bin/checklist.js');
  const projectRoot = makeTempDir(t);
  const existing = path.join(
    projectRoot,
    '.claude',
    'skills',
    FEATURE,
    'cruising',
    'SKILL.md',
  );
  fs.mkdirSync(path.dirname(existing), { recursive: true });
  fs.writeFileSync(existing, 'local customization\n');

  assert.throws(
    () => installSkills({ projectRoot }),
    /Refusing to overwrite existing skill: cruising/,
  );
  assert.equal(fs.readFileSync(existing, 'utf8'), 'local customization\n');
  assert.equal(
    fs.existsSync(path.join(projectRoot, '.claude', 'skills', FEATURE, 'before-startup')),
    false,
  );
});

test('installer overwrites changed skills when force is enabled', (t) => {
  const { installSkills } = require('../bin/checklist.js');
  const projectRoot = makeTempDir(t);
  const existing = path.join(
    projectRoot,
    '.claude',
    'skills',
    FEATURE,
    'landing',
    'SKILL.md',
  );
  fs.mkdirSync(path.dirname(existing), { recursive: true });
  fs.writeFileSync(existing, 'old version\n');

  installSkills({ projectRoot, force: true });

  assert.equal(
    fs.readFileSync(existing, 'utf8'),
    fs.readFileSync(path.join(PACKAGE_ROOT, 'skills', FEATURE, 'landing', 'SKILL.md'), 'utf8'),
  );
});
