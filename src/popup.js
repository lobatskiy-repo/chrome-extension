import { ModuleManager } from './core/ModuleManager.js';
import { baseDecoder } from './modules/baseDecoder.js';
import { idsExtractor } from './modules/idsExtractor.js';

document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('processBtn');
    const input = document.getElementById('urlInput');
    const output = document.getElementById('outputArea');
    const grabBtn = document.getElementById('grabUrlBtn');

    const manager = new ModuleManager();
    manager.register(baseDecoder);
    manager.register(idsExtractor);

    const processUrl = async () => {
        const url = input.value.trim();
        if (!url) {
            output.innerHTML = '<div style="color:red; padding:10px;">Please enter a URL</div>';
            return;
        }

        output.innerHTML = '<div style="text-align:center; color:#666;">Processing...</div>';
        const results = await manager.runAll(url);
        output.innerHTML = '';
        
        for (const [moduleName, data] of Object.entries(results)) {
            const section = document.createElement('div');
            section.className = 'module-result';
            
            const title = document.createElement('h3');
            title.textContent = moduleName;
            
            const pre = document.createElement('pre');
            pre.textContent = JSON.stringify(data, null, 2);
            
            section.appendChild(title);
            section.appendChild(pre);
            output.appendChild(section);
        }
    };

    btn.addEventListener('click', processUrl);

    grabBtn.addEventListener('click', () => {
        if (chrome.tabs) {
            chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
                if (tabs[0]) {
                    input.value = tabs[0].url;
                    processUrl();
                }
            });
        } else {
             input.value = "Chrome API not available (run as extension)";
        }
    });
});