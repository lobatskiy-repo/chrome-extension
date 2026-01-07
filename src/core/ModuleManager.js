export class ModuleManager {
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
}