/**
 * 从静态 JSON 文件加载排名数据
 * 这些文件是由后端的 updater.py 脚本定期生成的。
 */
async function loadRanking(bossSlug, specSlug) {
    // 1. 构建静态文件的路径
    // 路径结构: ./data/spec_ranking_<职业>_<BOSS>.json
    // 例如: ./data/spec_ranking_pictomancer-pictomancer_vamp-fatale.json
    //
    // 注意: 不再拼 ?t=时间戳 强制绕过缓存。服务器对 /data 返回
    // Cache-Control: no-cache + ETag，浏览器每次都会回源校验，
    // 数据没变时直接拿 304（不重新下载），数据更新后立刻生效。
    const fileName = `spec_ranking_${specSlug}_${bossSlug}.json`;
    const url = `./data/${fileName}`;

    console.log(`[M-Spec] Fetching static data from: ${url}`);

    try {
        const response = await fetch(url);

        if (!response.ok) {
            // 如果文件不存在 (404)，通常意味着 updater.py 还没有抓取该职业的数据
            throw new Error(`HTTP error! status: ${response.status} (File not found)`);
        }

        const data = await response.json();
        return data;

    } catch (error) {
        console.error("[M-Spec] Failed to fetch ranking data:", error);
        console.warn("提示: 请确认 updater.py 是否已成功运行并生成了对应的 .json 文件");
        return null;
    }
}
