import os

# Назва кореневої папки
root_dir = "threekit-parser-extension"

# Структура папок
dirs = [
    f"{root_dir}/src/core",
    f"{root_dir}/src/modules"
]

# Створення папок
for d in dirs:
    os.makedirs(d, exist_ok=True)

# --- ВМІСТ ФАЙЛІВ ---

manifest_json = """{
  "manifest_version": 3,
  "name": "ThreeKit Modular Parser",
  "version": "1.0",
  "description": "Modular parser for ThreeKit URLs.",
  "action": {
    "default_popup": "popup.html",
    "default_title": "TK Parser"
  },
  "permissions": ["activeTab"]
}"""

popup_html = """<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>TK Parser</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h2>ThreeKit URL Parser</h2>
        <div class="input-group">
            <button id="grabUrlBtn" class="secondary">📥 Взяти URL з поточної вкладки</button>
        </div>
        <textarea id="urlInput" placeholder="Вставте URL сюди..."></textarea>
        <button id="processBtn" class="primary">🚀 Розпарсити</button>
        <div id="outputArea"></div>
    </div>
    <script type="module" src="src/popup.js"></script>
</body>
</html>"""

style_css = """body { width: 400px; font-family: 'Segoe UI', Tahoma, sans-serif; padding: 15px; background: #f4f6f8; color: #333; }
h2 { margin-top: 0; font-size: 18px; color: #2c3e50; }
textarea { width: 100%; height: 80px; margin: 10px 0; border: 1px solid #ddd; border-radius: 6px; padding: 8px; box-sizing: border-box; font-family: monospace; font-size: 12px; resize: vertical; }
button { width: 100%; padding: 10px; cursor: pointer; border: none; border-radius: 6px; margin-bottom: 8px; font-weight: 600; transition: background 0.2s; }
.primary { background: #3498db; color: white; }
.primary:hover { background: #2980b9; }
.secondary { background: #ecf0f1; color: #2c3e50; border: 1px solid #bdc3c7; }
.secondary:hover { background: #dfe6e9; }
.module-result { background: white; border: 1px solid #e1e1e1; border-radius: 6px; padding: 12px; margin-bottom: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
.module-result h3 { margin-top: 0; color: #e67e22; border-bottom: 1px solid #eee; padding-bottom: 8px; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; }
pre { white-space: pre-wrap; word-wrap: break-word; font-size: 11px; color: #2c3e50; background: #f8f9fa; padding: 8px; border-radius: 4px; border: 1px solid #eee; }
"""

module_manager_js = """export class ModuleManager {
    constructor() {
        this.modules = [];
    }
    register(module) {
        if (!module.name || !module.run) {
            console.error("Module must have 'name' and 'run' function");
            return;
        }
        this.modules.push(module);
    }
    async runAll(urlString) {
        const results = {};
        let urlObject;
        try {
            urlObject = new URL(urlString);
        } catch (e) {
            return { "Error": "Invalid URL provided" };
        }

        for (const module of this.modules) {
            try {
                results[module.name] = await module.run(urlString, urlObject);
            } catch (error) {
                results[module.name] = { error: error.message };
            }
        }
        return results;
    }
}"""

base_decoder_js = """export const baseDecoder = {
    name: "Full JSON Decode",
    description: "Decodes URL parameters and nested JSON",
    run: (urlString, urlObject) => {
        const queryParams = {};
        for (const [key, value] of urlObject.searchParams.entries()) {
            try {
                queryParams[key] = JSON.parse(value);
            } catch (e) {
                if (!isNaN(value) && value.trim() !== '') {
                    queryParams[key] = Number(value);
                } else {
                    queryParams[key] = value;
                }
            }
        }
        return {
            host: urlObject.host,
            path: urlObject.pathname,
            params: queryParams
        };
    }
};"""

ids_extractor_js = """export const idsExtractor = {
    name: "Asset IDs List",
    description: "Extracts purely asset IDs from configuration",
    run: (urlString, urlObject) => {
        const ids = {};
        const configStr = urlObject.searchParams.get('configuration');
        
        if (configStr) {
            try {
                const config = JSON.parse(configStr);
                for (const key in config) {
                    if (config[key].assetId) {
                        ids[key] = config[key].assetId;
                    }
                }
            } catch (e) {
                return "Error parsing configuration JSON";
            }
        }
        
        const stageConfigStr = urlObject.searchParams.get('stageConfiguration');
        if(stageConfigStr) {
             try {
                const sConf = JSON.parse(stageConfigStr);
                ids['Stage Config'] = sConf;
             } catch(e){}
        }

        return Object.keys(ids).length > 0 ? ids : "No Asset IDs found in configuration";
    }
};"""

popup_js = """import { ModuleManager } from './core/ModuleManager.js';
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
});"""

# Словник файлів і шляхів
files = {
    f"{root_dir}/manifest.json": manifest_json,
    f"{root_dir}/popup.html": popup_html,
    f"{root_dir}/style.css": style_css,
    f"{root_dir}/src/popup.js": popup_js,
    f"{root_dir}/src/core/ModuleManager.js": module_manager_js,
    f"{root_dir}/src/modules/baseDecoder.js": base_decoder_js,
    f"{root_dir}/src/modules/idsExtractor.js": ids_extractor_js,
}

# Запис файлів
print("Створення файлів...")
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Створено: {path}")

print(f"\\nГотово! Папка '{root_dir}' створена і готова до встановлення.")