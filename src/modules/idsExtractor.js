export const idsExtractor = {
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
};