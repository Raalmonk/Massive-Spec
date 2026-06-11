"""Curated FF14 boss timeline markers.

These markers are intentionally sparse. They are for mitigation review, not a
full encounter guide. Multi-phase Ultimate markers carry phase anchors so the
frontend can place them relative to the real FF Logs phase transition for each
pull instead of assuming every previous phase lasted until enrage.
"""

from __future__ import annotations

from typing import Optional

from lorgs.boss_timeline import BossTimelineEvent

from .arcadion_heavyweight import (
    LINDWURM,
    LINDWURM_II,
    RED_HOT_AND_DEEP_BLUE,
    THE_TYRANT,
    VAMP_FATALE,
)
from .futures_rewritten import FUTURES_REWRITTEN
from .legacy_ultimates import (
    DRAGONSONGS_REPRISE,
    THE_EPIC_OF_ALEXANDER,
    THE_OMEGA_PROTOCOL,
    THE_UNENDING_COIL_OF_BAHAMUT,
    THE_WEAPONS_REFRAIN,
)


# Localized action names are from game data Action sheets:
# Chinese: thewakingsands/ffxiv-datamining-cn
# Japanese: xivapi/ffxiv-datamining
# Korean: Ra-Workspace/ffxiv-datamining-ko
ACTION_NAMES: dict[int, dict[str, str]] = {
    9897: {"zh": "死刑", "ja": "デスセンテンス", "ko": "사형 선고"},
    9898: {"zh": "旋风", "ja": "ツイスター", "ko": "회오리"},
    9901: {"zh": "液体地狱", "ja": "ヘルリキッド", "ko": "지옥의 늪"},
    9910: {"zh": "凶鸟尖喙", "ja": "レイヴェンズビーク", "ko": "흉조의 부리"},
    9912: {"zh": "天崩地裂", "ja": "天地崩壊", "ko": "천지붕괴"},
    9914: {"zh": "百万核爆", "ja": "メガフレア", "ko": "메가플레어"},
    9942: {"zh": "十亿核爆", "ja": "ギガフレア", "ko": "기가플레어"},
    9961: {"zh": "万亿核爆", "ja": "テラフレア", "ko": "테라플레어"},
    9962: {"zh": "死亡轮回", "ja": "アク・モーン", "ko": "아크 몬"},
    9964: {"zh": "无尽顿悟", "ja": "モーン・アファー", "ko": "몬 아파"},
    9958: {"zh": "连击的三重奏", "ja": "連撃の三重奏", "ko": "연격의 3중주"},
    9959: {"zh": "群龙的八重奏", "ja": "群竜の八重奏", "ko": "용들의 8중주"},
    11074: {"zh": "寒风之歌", "ja": "ミストラルソング", "ko": "삭풍의 노래"},
    11092: {"zh": "寒风之啸", "ja": "ミストラルシュリーク", "ko": "삭풍의 비명"},
    11095: {"zh": "火神爆裂", "ja": "バルカンバースト", "ko": "폭렬 난사"},
    11103: {"zh": "深红旋风", "ja": "クリムゾンサイクロン", "ko": "진홍 회오리"},
    11126: {"zh": "追击之究极幻想", "ja": "追撃の究極幻想", "ko": "궁극의 추격 환상"},
    11144: {"zh": "以太波动", "ja": "エーテル波動", "ko": "에테르 파동"},
    11288: {"zh": "怒震", "ja": "激震", "ko": "격진"},
    11517: {"zh": "大地粉碎", "ja": "ジオクラッシュ", "ko": "대지 붕괴"},
    11596: {"zh": "爆击之究极幻想", "ja": "爆撃の究極幻想", "ko": "궁극의 폭격 환상"},
    11597: {"zh": "乱击之究极幻想", "ja": "乱撃の究極幻想", "ko": "궁극의 난격 환상"},
    18470: {"zh": "倾泻", "ja": "カスケード", "ko": "폭포수"},
    18471: {"zh": "排水", "ja": "ドレナージ", "ko": "하수로"},
    18483: {"zh": "限制器减档", "ja": "リミッターカット", "ko": "리미터 해제"},
    18494: {"zh": "非最终审判", "ja": "ジャッジメントナイサイ", "ko": "임시처분"},
    18516: {"zh": "正义飞踢", "ja": "ジャスティスキック", "ko": "정의의 발차기"},
    18522: {"zh": "时间停止", "ja": "時間停止", "ko": "시간 정지"},
    18542: {"zh": "次元断绝阵列", "ja": "次元断絶のマーチ", "ko": "차원 단절 대형"},
    18543: {"zh": "时空潜行阵列", "ja": "時空潜行のマーチ", "ko": "시공 잠행 대형"},
    18550: {"zh": "正义风暴", "ja": "ジャスティスストーム", "ko": "정의의 폭풍"},
    18554: {"zh": "神圣审判", "ja": "聖なる審判", "ko": "신성한 심판"},
    18557: {"zh": "终审判决", "ja": "確定判決", "ko": "확정 판결"},
    18574: {"zh": "神圣大审判", "ja": "聖なる大審判", "ko": "성스러운 대심판"},
    18578: {"zh": "加重诛罚", "ja": "加重誅罰", "ko": "가중 처벌"},
    25300: {"zh": "至圣", "ja": "ホリエストホーリー", "ko": "지고한 신성"},
    25298: {"zh": "圣光剑舞", "ja": "ホーリーブレードダンス", "ko": "신성한 검무"},
    25310: {"zh": "天火", "ja": "ヘヴンフレイム", "ko": "천상의 불꽃"},
    25534: {"zh": "万物终结", "ja": "アルティメットエンド", "ko": "궁극의 종말"},
    25555: {"zh": "苍穹之阵：雷枪", "ja": "蒼天の陣：雷槍", "ko": "창천의 진: 번개창"},
    25569: {"zh": "苍穹之阵：圣杖", "ja": "蒼天の陣：聖杖", "ko": "창천의 진: 지팡이"},
    26381: {"zh": "堕天龙炎冲", "ja": "堕天のドラゴンダイブ", "ko": "타락한 천룡 강타"},
    27538: {"zh": "至天之阵：死刻", "ja": "至天の陣：死刻", "ko": "지천의 진: 죽음"},
    27973: {"zh": "邪念之炎", "ja": "邪念の炎", "ko": "사념의 불꽃"},
    27974: {"zh": "死亡轮回", "ja": "アク・モーン", "ko": "아크 몬"},
    28058: {"zh": "十亿核爆剑", "ja": "騎竜剣ギガフレア", "ko": "기룡검 기가플레어"},
    28060: {"zh": "百京核爆剑", "ja": "騎竜剣エクサフレア", "ko": "기룡검 엑사플레어"},
    28208: {"zh": "无尽顿悟剑", "ja": "騎竜剣モーン・アファー", "ko": "기룡검 몬 아파"},
    31491: {"zh": "循环程序", "ja": "サークルプログラム", "ko": "순환 프로그램"},
    31499: {"zh": "全能之主", "ja": "パントクラトル", "ko": "전지전능"},
    31522: {"zh": "宇宙记忆", "ja": "コスモメモリー", "ko": "세계의 기억"},
    31544: {"zh": "协作程序LB", "ja": "連携プログラムLB", "ko": "연계 프로그램[리미트]"},
    31550: {"zh": "协作程序PT", "ja": "連携プログラムPT", "ko": "연계 프로그램[파티]"},
    31573: {"zh": "你好，世界", "ja": "ハロー・ワールド", "ko": "헬로 월드"},
    31588: {"zh": "严重错误", "ja": "クリティカルエラー", "ko": "치명적인 오류"},
    31624: {"zh": "代码：＊能＊（德尔塔）", "ja": "コード：＊＊＊ミ＊【デルタ】", "ko": "코드: ＊＊미＊[델타]"},
    31660: {"zh": "波动炮：限制解除", "ja": "波動砲：リミッターカット", "ko": "파동포: 리미터 해제"},
    31664: {"zh": "宇宙流星", "ja": "コスモメテオ", "ko": "세계의 메테오"},
    31670: {"zh": "魔数", "ja": "マジックナンバー", "ko": "매직 넘버"},
    32362: {"zh": "太阳射线", "ja": "ソーラレイ", "ko": "태양 광선"},
    32788: {"zh": "代码：＊能＊（西格玛）", "ja": "コード：＊＊＊ミ＊【シグマ】", "ko": "코드: ＊＊미＊[시그마]"},
    32789: {"zh": "代码：＊能＊（欧米茄）", "ja": "コード：＊＊＊ミ＊【オメガ】", "ko": "코드: ＊＊미＊[오메가]"},
    40145: {"zh": "暴风破", "ja": "サイクロニックブレイク", "ko": "풍속 파괴"},
    40168: {"zh": "连锁爆印铭刻", "ja": "連鎖爆印刻", "ko": "연쇄 폭인각"},
    40197: {"zh": "钻石星尘", "ja": "ダイアモンドダスト", "ko": "다이아몬드 더스트"},
    40208: {"zh": "罪神圣", "ja": "シンホーリー", "ko": "죄의 홀리"},
    40212: {"zh": "光之失控", "ja": "光の暴走", "ko": "빛의 폭주"},
    40235: {"zh": "罪熔毁", "ja": "シンメルトン", "ko": "죄의 멜튼"},
    40239: {"zh": "光与暗的龙诗", "ja": "光と闇の竜詩", "ko": "빛과 어둠의 용시"},
    40240: {"zh": "时间结晶", "ja": "時間結晶", "ko": "시간의 결정체"},
    40266: {"zh": "时间压缩·绝", "ja": "時間圧縮・絶", "ko": "시간 압축: 절"},
    40302: {"zh": "死亡轮回", "ja": "アク・モーン", "ko": "아크 몬"},
    40304: {"zh": "无尽顿悟", "ja": "モーン・アファー", "ko": "몬 아파"},
    40306: {"zh": "光尘之剑", "ja": "光塵の剣", "ko": "빛먼지 검"},
    40310: {"zh": "死亡轮回", "ja": "アク・モーン", "ko": "아크 몬"},
    40319: {"zh": "复乐园", "ja": "パラダイスリゲインド", "ko": "복낙원"},
    40326: {"zh": "潘多拉魔盒", "ja": "パンドラの櫃", "ko": "판도라의 상자"},
    40328: {"zh": "失乐园", "ja": "パラダイスロスト", "ko": "실낙원"},
    45926: {"zh": "施虐的尖啸", "ja": "サディスティック・スクリーチ", "ko": "가학적인 웃음"},
    45933: {"zh": "全场杀伤", "ja": "クラウドキリング", "ko": "생명력 갈취"},
    45936: {"zh": "致命的闭幕曲", "ja": "フィナーレ・ファターレ", "ko": "파멸적 최후"},
    45938: {"zh": "贪欲无厌", "ja": "インセーシャブル・サースト", "ko": "채워지지 않는 갈증"},
    45939: {"zh": "碎烂脉冲", "ja": "パルピングパルス", "ko": "분쇄 파동"},
    45940: {"zh": "血魅的靴踏音", "ja": "ヴァンプストンプ", "ko": "요염한 짓밟기"},
    45941: {"zh": "共振波", "ja": "共振波", "ko": "공진파"},
    45951: {"zh": "硬核之声", "ja": "ハードコア", "ko": "과격성"},
    45955: {"zh": "粗暴之雨", "ja": "ブルータルレイン", "ko": "잔혹한 비"},
    45956: {"zh": "魅亡之音", "ja": "キラーボイス", "ko": "뇌쇄적인 목소리"},
    45963: {"zh": "掉落", "ja": "落下", "ko": "낙하"},
    45969: {"zh": "以太流失", "ja": "エーテルレッティング", "ko": "에테르 해방"},
    45973: {"zh": "笼中地狱", "ja": "ヘル・イン・ア・セル", "ko": "헬 인 어 셀"},
    45982: {"zh": "音速流散", "ja": "スプレッドソニック", "ko": "확산 음파"},
    46086: {"zh": "天顶的主宰", "ja": "キング・オブ・アルカディア", "ko": "아르카디아의 제왕"},
    46091: {"zh": "铸兵轰击", "ja": "ウェポンバスター", "ko": "무기 맹격"},
    46098: {"zh": "彗星雨", "ja": "コメットレイン", "ko": "혜성우"},
    46103: {"zh": "铸兵突袭", "ja": "ウェポンアサルト", "ko": "무기 공습"},
    46122: {"zh": "举世无双的霸王", "ja": "ワン・アンド・オンリー", "ko": "유일무이"},
    46123: {"zh": "火焰流", "ja": "ファイアストリーム", "ko": "화염 기류"},
    46127: {"zh": "兽焰连尾击", "ja": "ファイア・アンド・テイル", "ko": "화염과 꼬리"},
    46140: {"zh": "三重霸王坠击", "ja": "トライスターズ・タイラントフォール", "ko": "폭군 강하: 삼형제별"},
    46144: {"zh": "王者陨石", "ja": "チャンピオンズ・メテオ", "ko": "챔피언 메테오"},
    46152: {"zh": "重陨石", "ja": "ヘビーメテオ", "ko": "거대 메테오"},
    46154: {"zh": "登天碎地", "ja": "アルカディア・クラッシュ", "ko": "아르카디아 파괴"},
    46162: {"zh": "陨石狂奔", "ja": "メテオスタンピード", "ko": "메테오 쇄도"},
    46230: {"zh": "致命灾变", "ja": "リーサルスカージ", "ko": "죽음의 재앙"},
    46244: {"zh": "震场", "ja": "ブリングダウン・ハウス", "ko": "장내를 흔드는 갈채"},
    46247: {"zh": "分裂灾变", "ja": "スプリットスカージ", "ko": "분열된 재앙"},
    46264: {"zh": "残暴拘束", "ja": "クルエルコイル", "ko": "잔혹한 똬리"},
    46268: {"zh": "蜕鳞", "ja": "スキンスプリッター", "ko": "뱀껍질 균열"},
    46294: {"zh": "脏腑爆裂", "ja": "ヴィセラルバースト", "ko": "내장 파열"},
    46295: {"zh": "补天之手", "ja": "フィクサー・オブ・アルカディア", "ko": "아르카디아의 배후자"},
    46296: {"zh": "自我复制", "ja": "レプリケーション", "ko": "자가 복제"},
    46308: {"zh": "落火飞溅", "ja": "ファイアフォール・スプラッシュ", "ko": "불꽃 하강"},
    46322: {"zh": "林德布鲁姆陨石", "ja": "リンドブルム・メテオ", "ko": "린드블룸 메테오"},
    46345: {"zh": "境中奇梦", "ja": "アルカディアン・ドリーム", "ko": "아르카디아의 꿈"},
    46368: {"zh": "双重飞踢", "ja": "ダブルソバット", "ko": "연속 후려차기"},
    46374: {"zh": "魔力连击", "ja": "マナコンビネーション", "ko": "마나 연격"},
    46376: {"zh": "境中奇焰", "ja": "アルカディアン・フレイム", "ko": "아르카디아의 화염"},
    46377: {"zh": "境中奇奥", "ja": "アルカディアン・アルケイナム", "ko": "아르카디아의 신비"},
    46387: {"zh": "境中奇狱", "ja": "アルカディアン・ヘル", "ko": "아르카디아의 지옥"},
    46392: {"zh": "过愈过伤", "ja": "オーバーキュア・オーバーキル", "ko": "과잉치료, 과잉치사"},
    46458: {"zh": "兄弟同心", "ja": "ブラザーフッド", "ko": "형제애"},
    46518: {"zh": "炽焰冲击", "ja": "ホットインパクト", "ko": "핫 임팩트"},
    46519: {"zh": "深海冲击", "ja": "ディープインパクト", "ko": "딥 임팩트"},
    46520: {"zh": "斗志昂扬", "ja": "ファイティングスピリット", "ko": "끓어오르는 투지"},
    46530: {"zh": "旋绕巨火", "ja": "パイロローテーション", "ko": "화염 회전"},
    46532: {"zh": "腾火踏浪", "ja": "フレイムエアリアル", "ko": "불꽃 공중회전"},
    46541: {"zh": "破势乘浪", "ja": "シック・テイクオフ", "ko": "끝내주는 파도오름"},
    46553: {"zh": "极限炫技", "ja": "エクストリーム・スペクタクル", "ko": "익스트림 스펙터클"},
    47249: {"zh": "浪尖转体", "ja": "ハイドロバリエル", "ko": "물결 보드 꺾기"},
    47255: {"zh": "狂浪腾空", "ja": "インセインエアー", "ko": "광란의 공중 기술"},
    44489: {"zh": "喋血", "ja": "スローターシェッド", "ko": "살육의 허물"},
    47556: {"zh": "溅血", "ja": "スプラッターシェッド", "ko": "유혈의 허물"},
}


def _event(
    event_id: str,
    name: str,
    time: float,
    duration: float = 1,
    event_type: str = "mech",
    *,
    action_id: Optional[int] = None,
    phase_index: Optional[int] = None,
    phase_time: Optional[float] = None,
    phase_name: str = "",
) -> BossTimelineEvent:
    return BossTimelineEvent(
        id=event_id,
        name=name,
        time=time,
        duration=duration,
        type=event_type,
        action_id=action_id,
        phase_index=phase_index,
        phase_time=phase_time,
        phase_name=phase_name,
        name_i18n=ACTION_NAMES.get(action_id, {}),
    )


def _attach(boss, events: list[BossTimelineEvent]) -> None:
    object.__setattr__(boss, "boss_timeline", events)


_attach(
    VAMP_FATALE,
    [
        _event("m9s-killer-voice-1", "Killer Voice", 5, 5, "aoe", action_id=45956),
        _event("m9s-hardcore-1", "Hardcore", 15, 5, "tb", action_id=45951),
        _event("m9s-vamp-stomp-1", "Vamp Stomp", 25, 5, "mech", action_id=45940),
        _event("m9s-blast-beat-1", "Blast Beat", 34, 8, "mech", action_id=45941),
        _event("m9s-brutal-rain-1", "Brutal Rain", 42, 4, "aoe", action_id=45955),
        _event("m9s-crowd-kill-1", "Crowd Kill", 147, 6, "mech", action_id=45933),
        _event("m9s-finale-fatale-1", "Finale Fatale", 166, 5, "aoe", action_id=45936),
        _event("m9s-pulping-pulse-1", "Pulping Pulse", 177, 3, "mech", action_id=45939),
        _event("m9s-aetherletting-1", "Aetherletting", 178, 12, "mech", action_id=45969),
        _event("m9s-brutal-rain-2", "Brutal Rain", 252, 5, "aoe", action_id=45955),
        _event("m9s-insatiable-thirst", "Insatiable Thirst", 265, 6, "mech", action_id=45938),
        _event("m9s-sadistic-screech", "Sadistic Screech", 278, 6, "aoe", action_id=45926),
        _event("m9s-plummet", "Plummet", 296, 5, "tb", action_id=45963),
        _event("m9s-killer-voice-2", "Killer Voice", 300, 5, "aoe", action_id=45956),
        _event("m9s-crowd-kill-2", "Crowd Kill", 365, 6, "mech", action_id=45933),
        _event("m9s-finale-fatale-2", "Finale Fatale", 384, 5, "aoe", action_id=45936),
        _event("m9s-hell-in-a-cell", "Hell in a Cell", 396, 5, "mech", action_id=45973),
        _event("m9s-ultrasonic", "Ultrasonic", 403, 6, "tb", action_id=45982),
        _event("m9s-brutal-rain-3", "Brutal Rain", 494, 5, "aoe", action_id=45955),
        _event("m9s-hardcore-2", "Hardcore", 533, 5, "tb", action_id=45951),
    ],
)


_attach(
    RED_HOT_AND_DEEP_BLUE,
    [
        _event("m10s-hot-impact-1", "Hot Impact", 9, 5, "tb", action_id=46518),
        _event("m10s-pyrotation-1", "Pyrotation", 64, 5, "aoe", action_id=46530),
        _event("m10s-divers-dare-1", "Divers' Dare", 78, 5, "aoe", action_id=46520),
        _event("m10s-deep-impact-1", "Deep Impact", 132, 5, "tb", action_id=46519),
        _event("m10s-xtreme-spectacular", "Xtreme Spectacular", 157, 17, "aoe", action_id=46553),
        _event("m10s-epic-brotherhood-1", "Epic Brotherhood", 179, 5, "aoe", action_id=46458),
        _event("m10s-insane-air-1", "Insane Air", 189, 31, "mech", action_id=47255),
        _event("m10s-deep-varial", "Deep Varial", 270, 7, "mech", action_id=47249),
        _event("m10s-hot-aerial", "Hot Aerial", 284, 7, "tb", action_id=46532),
        _event("m10s-watery-grave", "Watery Grave", 338, 5, "mech"),
        _event("m10s-sickest-takeoff", "Sickest Take-off", 434, 4, "mech", action_id=46541),
        _event("m10s-divers-dare-2", "Divers' Dare", 524, 5, "aoe", action_id=46520),
    ],
)


_attach(
    THE_TYRANT,
    [
        _event("m11s-crown-1", "Crown of Arcadia", 5, 5, "aoe", action_id=46086),
        _event("m11s-raw-steel-1", "Raw Steel", 25, 5, "tb", action_id=46091),
        _event("m11s-assault-evolved-1", "Assault Evolved", 41, 20, "mech", action_id=46103),
        _event("m11s-void-stardust", "Void Stardust", 75, 14, "mech", action_id=46098),
        _event("m11s-crown-2", "Crown of Arcadia", 117, 5, "aoe", action_id=46086),
        _event("m11s-one-and-only", "One and Only", 232, 9, "aoe", action_id=46122),
        _event("m11s-great-wall", "Great Wall of Fire", 248, 5, "tb", action_id=46123),
        _event("m11s-fire-and-fury", "Fire and Fury", 271, 5, "mech", action_id=46127),
        _event("m11s-triple-tyrannihilation", "Triple Tyrannihilation", 336, 7, "aoe", action_id=46140),
        _event("m11s-majestic-meteor", "Majestic Meteor", 372, 5, "mech", action_id=46144),
        _event("m11s-massive-meteor", "Massive Meteor", 441, 6, "aoe", action_id=46152),
        _event("m11s-arcadian-avalanche", "Arcadian Avalanche", 455, 16, "mech", action_id=46154),
        _event("m11s-ecliptic-stampede", "Ecliptic Stampede", 531, 5, "aoe", action_id=46162),
    ],
)


_attach(
    LINDWURM,
    [
        _event("m12s1-fixer-1", "The Fixer", 10, 5, "aoe", action_id=46295),
        _event("m12s1-mortal-slayer", "Mortal Slayer", 29, 12, "mech", action_id=46230),
        _event("m12s1-visceral-burst", "Visceral Burst", 97, 5, "tb", action_id=46294),
        _event("m12s1-cruel-coil", "Cruel Coil", 132, 3, "mech", action_id=46264),
        _event("m12s1-skinsplitter", "Skinsplitter", 141, 5, "mech", action_id=46268),
        _event("m12s1-splattershed-1", "Splattershed", 183, 5, "aoe", action_id=47556),
        _event("m12s1-bring-down-house", "Bring Down the House", 216, 5, "mech", action_id=46244),
        _event("m12s1-split-scourge", "Split Scourge", 229, 5, "tb", action_id=46247),
        _event("m12s1-splattershed-2", "Splattershed", 284, 6, "aoe", action_id=47556),
        _event("m12s1-slaughtershed", "Slaughtershed", 337, 3, "aoe", action_id=44489),
        _event("m12s1-refreshing-overkill", "Refreshing Overkill", 428, 10, "aoe", action_id=46392),
    ],
)


_attach(
    LINDWURM_II,
    [
        _event("m12s2-arcadian-aflame", "Arcadian Aflame", 10, 5, "aoe", action_id=46376),
        _event("m12s2-replication", "Replication I", 25, 3, "mech", action_id=46296),
        _event("m12s2-double-sobat-1", "Double Sobat", 64, 6, "tb", action_id=46368),
        _event("m12s2-esoteric-1", "Esoteric Finisher", 77, 5, "tb", action_id=46374),
        _event("m12s2-firefall", "Firefall Splash", 122, 6, "mech", action_id=46308),
        _event("m12s2-idyllic-dream", "Idyllic Dream", 265, 5, "aoe", action_id=46345),
        _event("m12s2-lindwurm-meteor", "Lindwurm's Meteor", 344, 5, "aoe", action_id=46322),
        _event("m12s2-arcadian-arcanum", "Arcadian Arcanum", 353, 4, "mech", action_id=46377),
        _event("m12s2-esoteric-2", "Esoteric Finisher", 488, 5, "tb", action_id=46374),
        _event("m12s2-arcadian-hell", "Arcadian Hell", 510, 5, "aoe", action_id=46387),
    ],
)


_attach(
    FUTURES_REWRITTEN,
    [
        _event("fru-cyclonic-break-1", "Cyclonic Break", 14.6, 7, "mech", action_id=40145, phase_index=0, phase_time=14.6),
        _event("fru-powder-mark-1", "Powder Mark Trail", 24.4, 5, "tb", action_id=40168, phase_index=0, phase_time=24.4),
        _event("fru-powder-mark-2", "Powder Mark Trail", 129.9, 5, "tb", action_id=40168, phase_index=0, phase_time=129.9),
        _event("fru-diamond-dust", "Diamond Dust", 235.9, 5, "mech", action_id=40197, phase_index=1, phase_time=35.9),
        _event("fru-sinbound-holy", "Sinbound Holy", 254.6, 6, "aoe", action_id=40208, phase_index=1, phase_time=54.6),
        _event("fru-light-rampant", "Light Rampant", 332.7, 8, "mech", action_id=40212, phase_index=1, phase_time=132.7),
        _event("fru-ultimate-relativity", "Ultimate Relativity", 532.4, 8, "mech", action_id=40266, phase_index=2, phase_time=32.4),
        _event("fru-sinbound-meltdown", "Sinbound Meltdown", 549.4, 30, "aoe", action_id=40235, phase_index=2, phase_time=49.4),
        _event("fru-darklit-dragonsong", "Darklit Dragonsong", 714.9, 8, "mech", action_id=40239, phase_index=3, phase_time=34.1),
        _event("fru-akh-morn-1", "Akh Morn", 750.7, 5, "tb", action_id=40302, phase_index=3, phase_time=69.9),
        _event("fru-morn-afah-1", "Morn Afah", 760.8, 4, "aoe", action_id=40304, phase_index=3, phase_time=80.0),
        _event("fru-crystallize-time", "Crystallize Time", 776.3, 8, "mech", action_id=40240, phase_index=3, phase_time=95.5),
        _event("fru-fulgent-blade-1", "Fulgent Blade", 1040.8, 5, "mech", action_id=40306, phase_index=4, phase_time=11.2),
        _event("fru-akh-morn-2", "Akh Morn", 1067.8, 5, "tb", action_id=40310, phase_index=4, phase_time=38.2),
        _event("fru-paradise-regained-1", "Paradise Regained", 1076.0, 5, "mech", action_id=40319, phase_index=4, phase_time=46.4),
        _event("fru-pandoras-box", "Pandora's Box", 1141.7, 5, "aoe", action_id=40326, phase_index=4, phase_time=112.1),
        _event("fru-fulgent-blade-2", "Fulgent Blade", 1153.8, 5, "mech", action_id=40306, phase_index=4, phase_time=124.2),
        _event("fru-paradise-lost", "Paradise Lost", 1301.3, 8, "aoe", action_id=40328, phase_index=4, phase_time=271.7),
    ],
)


_attach(
    THE_UNENDING_COIL_OF_BAHAMUT,
    [
        _event("ucob-twister-1", "Twister", 12.6, 1, "mech", action_id=9898, phase_index=0, phase_time=12.6),
        _event("ucob-death-sentence-1", "Death Sentence", 23.9, 3, "tb", action_id=9897, phase_index=0, phase_time=23.9),
        _event("ucob-liquid-hell", "Liquid Hell", 108.5, 5, "mech", action_id=9901, phase_index=0, phase_time=108.5),
        _event("ucob-death-sentence-2", "Death Sentence", 132.3, 3, "tb", action_id=9897, phase_index=0, phase_time=132.3),
        _event("ucob-heavensfall", "Heavensfall", 407.5, 5, "mech", action_id=9912, phase_index=1, phase_time=0),
        _event("ucob-ravensbeak", "Ravensbeak", 532.4, 4, "tb", action_id=9910, phase_index=1, phase_time=124.9),
        _event("ucob-megaflare", "Megaflare", 1086.5, 6, "mech", action_id=9914, phase_index=2, phase_time=81.2),
        _event("ucob-gigaflare-1", "Gigaflare", 1102.8, 5, "aoe", action_id=9942, phase_index=2, phase_time=97.5),
        _event("ucob-tenstrike", "Tenstrike Trio", 1242.3, 8, "mech", action_id=9958, phase_index=2, phase_time=237.0),
        _event("ucob-grand-octet", "Grand Octet", 1298.5, 8, "mech", action_id=9959, phase_index=2, phase_time=293.2),
        _event("ucob-teraflare", "Teraflare", 2316.2, 8, "aoe", action_id=9961, phase_index=4, phase_time=0),
        _event("ucob-morn-afah", "Morn Afah", 2367.2, 5, "aoe", action_id=9964, phase_index=4, phase_time=51.0),
        _event("ucob-akh-morn-1", "Akh Morn", 2373.3, 5, "tb", action_id=9962, phase_index=4, phase_time=57.1),
    ],
)


_attach(
    THE_WEAPONS_REFRAIN,
    [
        _event("uwu-mistral-song", "Mistral Song", 11.4, 3, "tb", action_id=11074, phase_index=0, phase_time=11.4),
        _event("uwu-mistral-shriek", "Mistral Shriek", 42.2, 4, "aoe", action_id=11092, phase_index=0, phase_time=42.2),
        _event("uwu-crimson-cyclone", "Crimson Cyclone", 303.0, 5, "mech", action_id=11103, phase_index=1, phase_time=3.0),
        _event("uwu-vulcan-burst", "Vulcan Burst", 318.3, 3, "mech", action_id=11095, phase_index=1, phase_time=18.3),
        _event("uwu-geocrush-1", "Geocrush", 603.0, 5, "mech", action_id=11517, phase_index=2, phase_time=3.0),
        _event("uwu-tumult", "Tumult", 654.2, 8, "aoe", action_id=11288, phase_index=2, phase_time=54.2),
        _event("uwu-ultimate-predation", "Ultimate Predation", 1023.5, 8, "mech", action_id=11126, phase_index=4, phase_time=63.2),
        _event("uwu-ultimate-annihilation", "Ultimate Annihilation", 1101.8, 8, "mech", action_id=11596, phase_index=4, phase_time=141.5),
        _event("uwu-ultimate-suppression", "Ultimate Suppression", 1195.0, 8, "mech", action_id=11597, phase_index=4, phase_time=234.7),
        _event("uwu-aetheric-boom", "Aetheric Boom", 1254.7, 5, "aoe", action_id=11144, phase_index=4, phase_time=294.4),
    ],
)


_attach(
    THE_EPIC_OF_ALEXANDER,
    [
        _event("tea-cascade-1", "Cascade", 19.5, 4, "aoe", action_id=18470, phase_index=0, phase_time=19.5),
        _event("tea-drainage", "Drainage", 86.6, 4, "tb", action_id=18471, phase_index=0, phase_time=86.6),
        _event("tea-j-kick", "J Kick", 226.1, 4, "aoe", action_id=18516, phase_index=2, phase_time=56.0),
        _event("tea-judgment-nisi", "Judgment Nisi", 241.3, 6, "mech", action_id=18494, phase_index=2, phase_time=71.2),
        _event("tea-limit-cut", "Limit Cut", 313.5, 6, "mech", action_id=18483, phase_index=2, phase_time=143.4),
        _event("tea-temporal-stasis", "Temporal Stasis", 500.0, 6, "mech", action_id=18522, phase_index=4, phase_time=116.0),
        _event("tea-inception", "Inception Formation", 537.9, 6, "mech", action_id=18543, phase_index=4, phase_time=153.9),
        _event("tea-wormhole", "Wormhole Formation", 629.3, 6, "mech", action_id=18542, phase_index=4, phase_time=245.3),
        _event("tea-j-storm", "J Storm", 705.7, 50, "aoe", action_id=18550, phase_index=4, phase_time=321.7),
        _event("tea-divine-judgment", "Divine Judgment", 787.3, 5, "aoe", action_id=18554, phase_index=5, phase_time=64.8),
        _event("tea-final-word", "The Final Word", 909.1, 6, "mech", action_id=18557, phase_index=5, phase_time=186.6),
        _event("tea-capital-punishment", "Ordained Capital Punishment", 1008.0, 5, "tb", action_id=18578, phase_index=5, phase_time=285.5),
        _event("tea-almighty-judgment", "Almighty Judgment", 1126.2, 8, "aoe", action_id=18574, phase_index=5, phase_time=403.7),
    ],
)


_attach(
    DRAGONSONGS_REPRISE,
    [
        _event("dsr-holiest-1", "Holiest of Holy", 10.0, 4, "aoe", action_id=25300, phase_index=0, phase_time=10.0),
        _event("dsr-holy-bladedance", "Holy Bladedance", 25.3, 3, "tb", action_id=25298, phase_index=0, phase_time=25.3),
        _event("dsr-heavensflame", "Heavensflame", 88.2, 5, "mech", action_id=25310, phase_index=0, phase_time=88.2),
        _event("dsr-strength", "Strength of the Ward", 570.4, 8, "mech", action_id=25555, phase_index=1, phase_time=17.4),
        _event("dsr-sanctity", "Sanctity of the Ward", 638.7, 8, "mech", action_id=25569, phase_index=1, phase_time=85.7),
        _event("dsr-ultimate-end", "Ultimate End", 706.1, 5, "aoe", action_id=25534, phase_index=1, phase_time=153.1),
        _event("dsr-dive-from-grace", "Dive from Grace", 1020.5, 8, "mech", action_id=26381, phase_index=2, phase_time=20.5),
        _event("dsr-death-heavens", "Death of the Heavens", 3085.2, 8, "mech", action_id=27538, phase_index=5, phase_time=85.2),
        _event("dsr-wroth-flames", "Wroth Flames", 3582.4, 8, "mech", action_id=27973, phase_index=6, phase_time=82.4),
        _event("dsr-akh-morn", "Akh Morn", 3593.2, 8, "tb", action_id=27974, phase_index=6, phase_time=93.2),
        _event("dsr-exaflares", "Exaflare's Edge", 4036.0, 9, "mech", action_id=28060, phase_index=7, phase_time=36.0),
        _event("dsr-gigaflare", "Gigaflare's Edge", 4083.9, 8, "aoe", action_id=28058, phase_index=7, phase_time=83.9),
        _event("dsr-morn-afah", "Morn Afah's Edge", 4249.5, 5, "aoe", action_id=28208, phase_index=7, phase_time=249.5),
    ],
)


_attach(
    THE_OMEGA_PROTOCOL,
    [
        _event("top-program-loop", "Program Loop", 15.0, 6, "mech", action_id=31491, phase_index=0, phase_time=15.0),
        _event("top-pantokrator", "Pantokrator", 69.2, 8, "mech", action_id=31499, phase_index=0, phase_time=69.2),
        _event("top-solar-ray-1", "Solar Ray", 214.5, 5, "tb", action_id=32362, phase_index=1, phase_time=14.5),
        _event("top-party-synergy", "Party Synergy", 230.9, 8, "mech", action_id=31550, phase_index=1, phase_time=30.9),
        _event("top-limitless-synergy", "Limitless Synergy", 282.4, 8, "mech", action_id=31544, phase_index=1, phase_time=82.4),
        _event("top-cosmo-memory-1", "Cosmo Memory", 318.8, 5, "aoe", action_id=31522, phase_index=1, phase_time=118.8),
        _event("top-hello-world", "Hello, World", 441.3, 8, "mech", action_id=31573, phase_index=2, phase_time=41.3),
        _event("top-critical-error", "Critical Error", 550.1, 5, "aoe", action_id=31588, phase_index=2, phase_time=150.1),
        _event("top-run-delta", "Run: ****mi* (Delta)", 740.0, 8, "mech", action_id=31624, phase_index=4, phase_time=40.0),
        _event("top-run-sigma", "Run: ****mi* (Sigma)", 821.7, 8, "mech", action_id=32788, phase_index=4, phase_time=121.7),
        _event("top-run-omega", "Run: ****mi* (Omega)", 910.7, 8, "mech", action_id=32789, phase_index=4, phase_time=210.7),
        _event("top-solar-ray-2", "Solar Ray", 976.8, 5, "tb", action_id=32362, phase_index=4, phase_time=276.8),
        _event("top-cosmo-memory-2", "Cosmo Memory", 1167.8, 5, "aoe", action_id=31522, phase_index=5, phase_time=67.8),
        _event("top-wave-cannon", "Unlimited Wave Cannon", 1215.4, 8, "tb", action_id=31660, phase_index=5, phase_time=115.4),
        _event("top-cosmo-meteor", "Cosmo Meteor", 1331.6, 8, "mech", action_id=31664, phase_index=5, phase_time=231.6),
        _event("top-magic-number", "Magic Number", 1366.7, 5, "aoe", action_id=31670, phase_index=5, phase_time=266.7),
    ],
)
