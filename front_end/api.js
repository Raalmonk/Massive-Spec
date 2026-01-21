
async function loadFightData(reportId, fightId, specSlug = 'redmage-redmage') {
    // URL structure: http://127.0.0.1:5000/api/fight_analysis/<ReportID>/<FightID>
    const url = `http://127.0.0.1:5000/api/fight_analysis/${reportId}/${fightId}?spec=${specSlug}`;

    console.log(`[FFLorrgs] Fetching data from: ${url}`);

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        console.log("[FFLorrgs] Data received:", data);

        // Call the render function if it exists
        if (typeof renderCanvas === 'function') {
            renderCanvas(data, specSlug);
        } else {
            console.error("renderCanvas function is not defined!");
        }

    } catch (error) {
        console.error("[FFLorrgs] Failed to fetch fight data:", error);
    }
}

async function loadSpellData(specSlug) {
    const url = `http://127.0.0.1:5000/api/specs/${specSlug}/spells`;
    console.log(`[FFLorrgs] Fetching spell data from: ${url}`);

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("[FFLorrgs] Failed to fetch spell data:", error);
        return {};
    }
}
