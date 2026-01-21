# lorrgs_api/routes/api_fight_analysis.py
from flask import Blueprint, jsonify, request
from lorgs.models.warcraftlogs_report import Report

api = Blueprint("api_fight_analysis", __name__)

@api.route("/fight_analysis/<string:report_id>/<int:fight_id>")
async def get_fight_analysis(report_id, fight_id):
    """获取指定战斗的详细施法时间轴数据"""
    
    # 1. 获取可选的过滤参数 (比如只看特定职业)
    # 用法: /api/fight_analysis/xyz/5?spec=Pictomancer
    target_spec = request.args.get("spec") 

    # 2. 初始化报告
    report = Report(report_id=report_id)
    await report.load() # 加载元数据
    
    # 3. 获取战斗
    fight = report.get_fight(fight_id=fight_id)
    if not fight:
        return jsonify({"error": "Fight not found"}), 404
        
    # 4. 加载玩家列表 (Summary)
    await fight.load() 
    
    # 5. 确定要加载哪些玩家
    # 如果指定了 spec 参数，就只加载那个职业，否则加载所有玩家(可能会慢)
    players_to_load = fight.players
    if target_spec:
        players_to_load = [p for p in fight.players if p.spec_slug == target_spec]
        
    if not players_to_load:
        return jsonify({"error": f"No players found for spec: {target_spec}"}), 404

    # 6. 并行加载选定玩家的施法数据
    # 这里利用了 fight.load_many 或直接遍历 load (lorgs 的设计支持 await 列表)
    for player in players_to_load:
        # 只有当 casts 为空时才去加载，避免重复
        if not player.casts:
            await player.load()

    # 7. 返回数据
    # 利用 fight.as_dict()，它会自动包含 players 和里面的 casts
    # 我们只返回加载了数据的玩家 ID
    loaded_player_ids = [p.source_id for p in players_to_load]
    return jsonify(fight.as_dict(player_ids=loaded_player_ids))