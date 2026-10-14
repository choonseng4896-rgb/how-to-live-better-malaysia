import fs from 'node:fs';
import vm from 'node:vm';
const html = fs.readFileSync(new URL('../dist/index.html', import.meta.url), 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
if (scripts.length !== 1) throw new Error('Expected one embedded application script');
new vm.Script(scripts[0][1]);
console.log('Embedded JavaScript syntax is valid');
