/**
 * 从静态 JSON 文件加载排名数据
 * 这些文件是由后端的 updater.py 脚本定期生成的。
 */
async function loadRanking(bossSlug, specSlug) {
    // 1. 构建静态文件的路径
    // 路径结构: ./data/spec_ranking_<职业>_<BOSS>.json
    // 例如: ./data/spec_ranking_pictomancer-pictomancer_vamp-fatale.json
    
    // 添加时间戳参数 (?t=...) 以防止浏览器缓存旧数据
    const timestamp = new Date().getTime();
    const fileName = `spec_ranking_${specSlug}_${bossSlug}.json`;
    const url = `./data/${fileName}?t=${timestamp}`;

    console.log(`[M-Spec] Fetching static data from: ${url}`);

    try {
        const response = await fetch(url);

        if (!response.ok) {
            // 如果文件不存在 (404)，通常意味着 updater.py 还没有抓取该职业的数据
            throw new Error(`HTTP error! status: ${response.status} (File not found)`);
        }

        const data = await response.json();
        console.log("[M-Spec] Data received:", data);
        return data;

    } catch (error) {
        console.error("[M-Spec] Failed to fetch ranking data:", error);
        console.warn("提示: 请确认 updater.py 是否已成功运行并生成了对应的 .json 文件");
        return null;
    }
}