export const baseDecoder = {
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
};