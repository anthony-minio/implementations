// Load the review page in headless Chromium and report errors and counts.
//   node tools/check.mjs output/<slug>.html [screenshot.png]
import { createRequire } from 'module';
import { execSync } from 'child_process';
import path from 'path';
const require = createRequire(execSync('npm root -g').toString().trim() + '/');
const { chromium } = require('playwright');
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1100, height: 1400 } });
const errs = [];
p.on('pageerror', e => errs.push(e.message));
p.on('console', m => m.type() === 'error' && errs.push(m.text()));
await p.goto('file://' + path.resolve(process.argv[2]));
if (process.argv[3]) await p.screenshot({ path: process.argv[3] });
console.log('errors:', errs, 'tables:', await p.locator('table').count(),
  'copy buttons:', await p.locator('button.copy').count(), 'TBC:', await p.locator('.tbc').count());
await b.close();
