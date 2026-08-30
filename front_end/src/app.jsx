        import React, { useState, useRef, useEffect, useMemo, useCallback } from 'react';
        import { createRoot } from 'react-dom/client';
        import { ZoomIn, ZoomOut, Shield, ShieldAlert, Zap, Swords, MoreHorizontal, Layers, Minimize2, Maximize2, ChevronDown, ExternalLink, Flag, Timer, MousePointer2, CheckCircle2, XCircle, SlidersHorizontal } from 'lucide-react';

        // --- Configuration ---
        const THEME_COLOR = '#00FF96';
        const SELECTION_COLOR_BLUE = '#3B82F6'; // Blue for Curation Mode
        const JOB_COLOR_RDM = '#E87B7B';
        const FIGHT_DURATION = 1200; // Increased to 10 minutes (600s) to fix the "7 minute" overflow issue
        const API_BASE = '';
        const LEFT_PANEL_WIDTH = 260;
        const LEFT_PANEL_COLLAPSED_WIDTH = 46;
        const DRAG_THRESHOLD = 6;
        // --- 横向虚拟化 (拖动卡顿的根治) ---
        // 一整场战斗的所有 cast 全渲染出来是几万个 DOM 节点, 浏览器拖动时
        // 光栅化/命中测试都在这棵大树上跑, 必然掉帧。改为只渲染视口附近的
        // cast: 每滚过 CHUNK 像素才触发一次低优先级重渲染重算可见窗口。
        const SCROLL_CULL_CHUNK_PX = 1200;    // 滚动多少像素触发一次窗口重算
        const SCROLL_CULL_MARGIN_PX = 2000;   // 视口两侧预渲染余量 (必须 > CHUNK)
        const MIN_VISIBLE_MINUTES = 0.25;
        const MAX_VISIBLE_MINUTES = 21;
        const DEFAULT_VISIBLE_MINUTES = 6;
        const LIMIT_BREAK_ICON = './images/spells/Limit_Break.png';

        // Palette for Duration Bars (Sequential assignment)
        const DURATION_PALETTE = [
            '#F87171', '#FB923C', '#FACC15', '#A3E635',
            '#34D399', '#22D3EE', '#60A5FA', '#818CF8',
            '#A78BFA', '#E879F9', '#FB7185', '#F472B6'
        ];

        // ==================== Canvas 渲染层 ====================
        // 时间轴的 cast 层默认用一块视口大小的 canvas 绘制, 替代原来
        // 每场战斗数万个 DOM 节点 (拖动/缩放卡顿的根源)。
        // ?render=dom 可切回 DOM 渲染路径作为兜底。
        const RENDER_MODE = (() => {
            try {
                return new URLSearchParams(window.location.search).get('render') === 'dom' ? 'dom' : 'canvas';
            } catch (e) {
                return 'canvas';
            }
        })();
        const RULER_HEIGHT_PX = 32; // sticky 时间标尺高度 (h-8), 命中测试时排除这块
        // canvas 放在滚动内容内部, 随内容被合成器原生滚动 (与 DOM 刻度像素级同步,
        // 拖动零延迟)。画布只覆盖 "视口 + 余量" 的区域, 滚近边缘时才重画一次。
        const CANVAS_MARGIN_X = 1000;   // 水平预绘余量 (px)
        const CANVAS_MARGIN_Y = 400;    // 垂直预绘余量 (px)
        const CANVAS_REDRAW_SLACK = 150; // 距离已绘区边缘多近时触发重画

        // 图标位图缓存: url -> {img, loaded}; 圆角+底色合成缓存: `url|尺寸px` -> offscreen canvas
        const castIconImages = new Map();
        const castIconComposites = new Map();
        // 图标异步加载完成后通知当前挂载的 App 重画 (由 effect 注入)
        let castCanvasRedrawHook = null;

        const traceRoundedRect = (ctx, x, y, w, h, r) => {
            const radius = Math.min(r, w / 2, h / 2);
            ctx.beginPath();
            ctx.moveTo(x + radius, y);
            ctx.arcTo(x + w, y, x + w, y + h, radius);
            ctx.arcTo(x + w, y + h, x, y + h, radius);
            ctx.arcTo(x, y + h, x, y, radius);
            ctx.arcTo(x, y, x + w, y, radius);
            ctx.closePath();
        };

        const fillRoundedRect = (ctx, x, y, w, h, r) => {
            traceRoundedRect(ctx, x, y, w, h, r);
            ctx.fill();
        };

        // 图标合成: 黑底 50% + 圆角裁剪 + object-cover 铺满, 结果缓存为 offscreen canvas
        const getIconComposite = (url, px) => {
            if (!url || px <= 0) return null;
            const key = `${url}|${px}`;
            const cached = castIconComposites.get(key);
            if (cached) return cached;

            let rec = castIconImages.get(url);
            if (!rec) {
                const img = new Image();
                rec = { img, loaded: false, failed: false };
                img.onload = () => {
                    rec.loaded = true;
                    if (castCanvasRedrawHook) castCanvasRedrawHook();
                };
                img.onerror = () => { rec.failed = true; };
                img.src = url;
                castIconImages.set(url, rec);
            }
            if (!rec.loaded || rec.failed) return null;

            const comp = document.createElement('canvas');
            comp.width = px;
            comp.height = px;
            const ictx = comp.getContext('2d');
            traceRoundedRect(ictx, 0, 0, px, px, 2);
            ictx.clip();
            ictx.fillStyle = 'rgba(0,0,0,0.5)';
            ictx.fillRect(0, 0, px, px);
            const iw = rec.img.naturalWidth || px;
            const ih = rec.img.naturalHeight || px;
            const scale = Math.max(px / iw, px / ih); // object-cover
            ictx.drawImage(rec.img, (px - iw * scale) / 2, (px - ih * scale) / 2, iw * scale, ih * scale);
            castIconComposites.set(key, comp);
            return comp;
        };

        // 画一行的所有 cast (视觉规格与 DOM 渲染路径逐项对齐:
        // CD 条 / 持续条 / 图标 / 时间文字 / 聚焦高亮与压暗)
        // 坐标系: 内容坐标 (ctx 已由调用方平移), cullX0/cullX1 为需要绘制的内容 x 范围
        const drawRowCasts = (ctx, params, rowY, state, cullX0, cullX1) => {
            const { casts, totalHeight, trackHeight, rowPhases, killTimeSeconds, durOpacity, fontFactor, textAlpha } = params;
            const { zoom, showCooldown, showDuration, showSkillTimes, isCollapsed, focusedSpellId, isFocusedSpellId, getPhaseOffset, leftPanelWidth, formatTime } = state;
            const phaseOffset = getPhaseOffset(rowPhases);
            const focusActive = !!focusedSpellId;

            // 两遍绘制模拟 DOM 的 zIndex 规则 (聚焦的 cast 永远盖在未聚焦之上)
            for (let pass = 0; pass < (focusActive ? 2 : 1); pass++) {
                for (let i = 0; i < casts.length; i++) {
                    const cast = casts[i];
                    const isFocused = focusActive && isFocusedSpellId(cast.spellId);
                    if (focusActive && ((pass === 1) !== isFocused)) continue;

                    const timeUntilKill = killTimeSeconds ? (killTimeSeconds - cast.timestamp) : 99999;
                    if (timeUntilKill <= 0) continue;

                    const spell = cast.spell;
                    const alignedT = Number(cast.timestamp || 0) - phaseOffset;
                    const x = leftPanelWidth + alignedT * zoom;
                    const maxVisibleWidth = timeUntilKill * zoom;
                    const durationWidth = Math.max(0, Math.min((cast.duration || 0) * zoom, maxVisibleWidth));
                    const cdWidth = Math.max(0, Math.min((spell.cd || 0) * zoom, maxVisibleWidth));

                    const currentTrackHeight = isCollapsed ? totalHeight : trackHeight;
                    const iconHeight = currentTrackHeight * 0.9;
                    // 只画已绘区内的 cast (内容坐标)
                    if (x > cullX1 || x + Math.max(durationWidth, cdWidth, iconHeight) + iconHeight * fontFactor * 5 < cullX0) continue;

                    const yTop = rowY + (isCollapsed ? 0 : cast.trackIndex * trackHeight);
                    const iconY = yTop + (currentTrackHeight - iconHeight) / 2;
                    const baseAlpha = focusActive && !isFocused ? 0.25 : 1;

                    // 1. CD 条 (垂直居中, 高 1/3, 色带 20% 透明)
                    if (showCooldown && (spell.cd || 0) > 0 && cdWidth > 0) {
                        ctx.globalAlpha = baseAlpha;
                        ctx.fillStyle = hexToRgba(cast.barColor, 0.2);
                        const barH = currentTrackHeight / 3;
                        fillRoundedRect(ctx, x + iconHeight / 2, yTop + (currentTrackHeight - barH) / 2, cdWidth, barH, 2);
                    }

                    // 2. 持续条 (与图标同高)
                    if (showDuration && durationWidth > 0) {
                        ctx.globalAlpha = baseAlpha * durOpacity;
                        ctx.fillStyle = cast.barColor;
                        fillRoundedRect(ctx, x, iconY, durationWidth, iconHeight, 2);
                    }

                    // 3. 图标 (或首字母占位)
                    ctx.globalAlpha = baseAlpha;
                    const iconPx = Math.max(1, Math.round(iconHeight));
                    const iconUrl = spell.image || spell.icon;
                    const composite = iconUrl ? getIconComposite(iconUrl, iconPx) : null;
                    if (composite) {
                        ctx.drawImage(composite, x, iconY, iconHeight, iconHeight);
                    } else {
                        ctx.fillStyle = iconUrl ? 'rgba(0,0,0,0.5)' : '#374151'; // 加载中黑底 / 无图灰底
                        fillRoundedRect(ctx, x, iconY, iconHeight, iconHeight, 2);
                        if (!iconUrl) {
                            const ch = spell.char || (spell.name ? spell.name[0] : '?');
                            ctx.fillStyle = '#f3f4f6';
                            ctx.font = `${Math.max(8, Math.round(iconHeight * 0.5))}px ui-sans-serif, system-ui, sans-serif`;
                            ctx.textAlign = 'center';
                            ctx.textBaseline = 'middle';
                            ctx.fillText(ch, x + iconHeight / 2, iconY + iconHeight / 2);
                            ctx.textAlign = 'left';
                        }
                    }
                    if (isFocused) {
                        // 聚焦描边 (对应 DOM 的 inset ring + 两侧 2px 光边)
                        ctx.strokeStyle = '#00FF96';
                        ctx.lineWidth = 2;
                        ctx.strokeRect(x - 1, iconY, iconHeight + 2, iconHeight);
                    }

                    // 4. 时间文字
                    if (showSkillTimes) {
                        ctx.globalAlpha = baseAlpha * textAlpha;
                        ctx.fillStyle = '#ffffff';
                        ctx.font = `bold ${Math.max(7, Math.round(iconHeight * fontFactor))}px ui-sans-serif, system-ui, sans-serif`;
                        ctx.textBaseline = 'middle';
                        ctx.shadowColor = 'rgba(0,0,0,0.8)';
                        ctx.shadowBlur = 2;
                        ctx.shadowOffsetY = 1;
                        ctx.fillText(formatTime(cast.timestamp), x + iconHeight + 4, yTop + currentTrackHeight / 2);
                        ctx.shadowColor = 'transparent';
                        ctx.shadowBlur = 0;
                        ctx.shadowOffsetY = 0;
                    }
                }
            }
            ctx.globalAlpha = 1;
        };
        // ================== Canvas 渲染层 (结束) ==================

        const LIMIT_BREAK_SPELLS = {
            197: "Shield Wall",
            198: "Stronghold",
            199: "Last Bastion",
            200: "Braver",
            201: "Bladedance",
            202: "Final Heaven",
            203: "Skyshard",
            204: "Starstorm",
            205: "Meteor",
            206: "Healing Wind",
            207: "Breath of the Earth",
            208: "Pulse of Life",
            4238: "Big Shot",
            4239: "Desperado",
            4240: "Land Waker",
            4241: "Dark Force",
            4242: "Dragonsong Dive",
            4243: "Chimatsuri",
            4244: "Sagittarius Arrow",
            4245: "Satellite Beam",
            4246: "Teraflare",
            4247: "Angel Feathers",
            4248: "Astral Stasis",
            7861: "Doom of the Living",
            7862: "Vermilion Scourge",
            17105: "Gunmetal Soul",
            17106: "Crimson Lotus",
            24858: "The End",
            24859: "Techne Makre",
            34866: "World-swallower",
            34867: "Chromatic Fantasy"
        };
        const LIMIT_BREAK_IDS = new Set(Object.keys(LIMIT_BREAK_SPELLS).map(Number));
        const DANCER_DEVILMENT_ID = 16011;
        const DANCER_TANGO_EARLY_SECONDS = 2;
        const DANCER_TANGO_DURATION_SECONDS = 20;
        const RAID_BUFF_FOCUS_IDS = new Set([
            118, 2248, 2258, 3557, 7396, 7436, 7520,
            15998, 16004, 16552, 24405, 25785, 25801,
            34675, 36957, 36958
        ]);
        const isLimitBreakSpellId = (spellId) => LIMIT_BREAK_IDS.has(Number(spellId));
        const getLimitBreakSpell = (spellId) => ({
            id: Number(spellId),
            name: LIMIT_BREAK_SPELLS[Number(spellId)] || `Limit Break ${spellId}`,
            image: LIMIT_BREAK_ICON,
            cd: 0,
            duration: 0,
            color: '#f59e0b',
            category: 'LIMIT_BREAK',
            show: true
        });

        const BOSS_TIMELINE_TYPES = {
            mech: { label: 'Mech', color: '#facc15' },
            tb: { label: 'TB', color: '#60a5fa' },
            aoe: { label: 'AOE', color: '#fb923c' }
        };
        const normalizeBossTimelineType = (type) => {
            const normalized = String(type || 'mech').toLowerCase();
            return normalized === 'mechanic' ? 'mech' : normalized;
        };
        const getBossTimelineColor = (type, color) => color || BOSS_TIMELINE_TYPES[type]?.color || BOSS_TIMELINE_TYPES.mech.color;

        const UI_LANGUAGE_STORAGE_KEY = 'm-spec:ui-language';
        const ZOOM_VISIBLE_MINUTES_STORAGE_KEY = 'm-spec:visible-minutes';
        const ZOOM_VISIBLE_MINUTES_MIGRATION_KEY = 'm-spec:visible-minutes-migration';
        const ZOOM_VISIBLE_MINUTES_MIGRATION = 'default-6m-2026-06-08';
        const USER_FFLOGS_CLIENT_ID_STORAGE_KEY = 'm-spec:fflogs-client-id';
        const USER_FFLOGS_CLIENT_SECRET_STORAGE_KEY = 'm-spec:fflogs-client-secret';
        const UI_LANGUAGES = [
            { id: 'en', label: 'EN' },
            { id: 'zh', label: '中文' },
            { id: 'ja', label: '日本語' },
            { id: 'ko', label: '한국어' }
        ];
        const I18N = {
            en: {
                language: 'Language',
                loading: 'Loading...',
                boss: 'Boss',
                bossGroup_current: 'Current Content',
                bossGroup_legacyUltimates: 'Legacy Ultimates',
                spec: 'Spec',
                region: 'Region',
                with: 'Comp Filter',
                killTime: 'Kill Time',
                importLog: 'Import Log',
                select: 'Curate',
                selected: 'Selected',
                confirm: 'Confirm',
                cancel: 'Cancel',
                curated: 'Curated',
                close: 'Close',
                importPull: 'Import FF Logs Pull',
                loadPlayers: 'Load Players',
                display: 'Display',
                controls: 'Controls',
                all: 'ALL',
                showAllSpells: 'Show all spells',
                hideAllSpells: 'Hide all spells',
                duration: 'Duration',
                cooldown: 'Cooldown',
                skillTimeLabels: 'Skill time labels',
                phases: 'Phases',
                alignPhase: 'Align rows to this phase',
                clearPhaseAlignment: 'Clear phase alignment',
                collapseLeftPanel: 'Collapse left panel',
                expandLeftPanel: 'Expand left panel',
                showBossRow: 'Toggle Boss Row',
                category_cd: 'CD',
                category_single_mit: 'Single Mit',
                category_group_mit: 'Group Mit',
                category_utility: 'Utility',
                category_others: 'Others',
                limitBreak: 'Limit Break',
                showLimitBreak: 'Show limit break casts',
                party: 'Party',
                buddy: 'Buddy',
                showBuddy: 'Show buddy tank/healer cooldowns',
                technicalTangoWindow: 'TG',
                zoomTechnicalTangoWindow: 'Only show buddy casts from 2s before Devilment until Devilment ends',
                bossTimeline: 'Boss Timeline',
                mech: 'Mech',
                tb: 'TB',
                aoe: 'AOE',
                rank: 'Rank',
                rdps: 'RDPS',
                reg: 'Reg',
                pair: 'Pair',
                buffs: 'Buffs',
                importedLog: 'Loaded Log',
                removeImportedLog: 'Remove imported log',
                shown: 'shown',
                filterKillTime: 'Filter Kill Time (Min : Sec)',
                min: 'Min',
                max: 'Max',
                reset: 'Reset',
                apply: 'Apply',
                openFFLogs: 'Open in FF Logs',
                enterCuration: 'Enter Curation Mode',
                exitCuration: 'Exit Curated Mode',
                showBossTimelineType: 'Show',
                selectAtLeastOneRow: 'Please select at least one row.',
                expandRows: 'Expand Rows (Split lines)',
                collapseRows: 'Collapse Rows',
                apiSettings: 'API Settings',
                publicImportActive: 'Using the shared import quota. If it is full, you can use your own FF Logs API client.',
                userApiActive: 'Personal FF Logs API client enabled. This import will not use the shared quota.',
                apiLimitTitle: 'Shared Import Quota Is Full',
                apiLimitSubtitle: 'You can wait for the shared quota to refresh at the next hour, or use your own FF Logs v2 API client now.',
                apiDisclosure: 'Your FF Logs client ID and client secret will be sent to the M-Spec server so the server can request FF Logs on your behalf. The M-Spec server will not store them locally, write them to a database, or intentionally log them. They are saved in your own browser and used automatically for future imports. Keep the secret private.',
                apiTokenInstructionsTitle: 'Create Your Own FF Logs v2 API Client',
                apiTokenInstructionsBody: 'Open the FF Logs client page and click Create a Client. Fill the form exactly like this, then copy the client ID and client secret shown after creation. The secret will never be shown again.',
                apiClientPageLabel: 'FF Logs clients page',
                apiClientNameLabel: 'Application name',
                apiRedirectUrlLabel: 'Redirect URL',
                apiPublicClientLabel: 'Public Client checkbox',
                apiPublicClientValue: 'Leave unchecked. M-Spec needs the client secret.',
                copy: 'Copy',
                copied: 'Copied',
                apiTokenInputLabel: 'FF Logs Client ID / Client Secret',
                apiClientIdPlaceholder: 'Client ID',
                apiClientSecretPlaceholder: 'Client Secret',
                save: 'Save',
                savedUserApiNotice: 'This browser has a personal FF Logs API client saved. Imports will prefer it.',
                clear: 'Clear',
                missingFflogsToken: 'Please enter both FF Logs client ID and client secret.',
                invalidFflogsCredentials: 'Your FF Logs client ID or client secret may be incorrect. Please re-enter them.',
                importUrlHelp: 'Paste a full FF Logs report URL with a numeric fight value, for example fight=9. Do not use fight=last. Open the specific pull in FF Logs first, then copy the URL after the pull number appears.',
                numericFightError: 'The FF Logs URL must include a numeric fight value, such as fight=9. fight=last is not supported. Open that pull in FF Logs first, then copy the URL after it changes to a number.',
                importRateLimitError: 'Too many players are importing right now. Please wait until the next hourly quota refresh, or use your own FF Logs API client.',
                missingReportIdError: 'Could not find a report ID in the URL. Paste the full FF Logs report link starting with https://.',
                reportNotFoundError: 'Report not found. Check that the link is correct and visible to FF Logs.',
                noReportPermissionError: 'M-Spec does not have permission to view this report. Make the report public or use a client that can access it.',
                fightNotFoundError: 'Fight not found in this report. Open the exact pull in FF Logs and copy the URL after fight becomes a number.',
                playerNotFoundError: 'Player not found in this fight. Reload the player list and choose again.',
                importGenericError: 'Import failed. Please try again later.',
                role_Tanks: 'Tanks',
                role_Healers: 'Healers',
                role_Melee: 'Melee',
                role_Physical_Ranged: 'Physical Ranged',
                role_Magical_Ranged: 'Magical Ranged'
            },
            zh: {
                language: '语言',
                loading: '加载中...',
                boss: 'Boss',
                bossGroup_current: '当前副本',
                bossGroup_legacyUltimates: '旧绝本',
                spec: '职业',
                region: '地区',
                with: '阵容筛选',
                killTime: '击杀时间',
                importLog: '导入 Log',
                select: '精选',
                selected: '已选择',
                confirm: '确认',
                cancel: '取消',
                curated: '精选',
                close: '关闭',
                importPull: '导入 FF Logs Pull',
                loadPlayers: '读取玩家',
                display: '显示',
                controls: '控制',
                all: '全部',
                showAllSpells: '显示所有技能',
                hideAllSpells: '隐藏所有技能',
                duration: '持续时间',
                cooldown: 'CD',
                skillTimeLabels: '技能时间',
                phases: '阶段',
                alignPhase: '按此阶段对齐',
                clearPhaseAlignment: '取消阶段对齐',
                collapseLeftPanel: '折叠左栏',
                expandLeftPanel: '展开左栏',
                showBossRow: '切换 Boss 行',
                category_cd: 'CD',
                category_single_mit: '单减',
                category_group_mit: '团减',
                category_utility: '功能',
                category_others: '其他',
                limitBreak: 'Limit Break',
                showLimitBreak: '显示 LB',
                party: '队伍',
                buddy: '搭档',
                showBuddy: '显示另一个同职能技能',
                technicalTangoWindow: 'TG',
                zoomTechnicalTangoWindow: '只显示搭档在进攻之探戈前 2 秒到结束期间的技能',
                bossTimeline: 'Boss 时间轴',
                mech: '机制',
                tb: '死刑',
                aoe: 'AOE',
                rank: '排名',
                rdps: 'RDPS',
                reg: '地区',
                pair: '搭档',
                buffs: '团辅',
                importedLog: 'Log 已装载',
                removeImportedLog: '移除导入 Log',
                shown: '显示',
                filterKillTime: '筛选击杀时间（分 : 秒）',
                min: '最小',
                max: '最大',
                reset: '重置',
                apply: '应用',
                openFFLogs: '打开 FF Logs',
                enterCuration: '进入精选模式',
                exitCuration: '退出精选模式',
                showBossTimelineType: '显示',
                selectAtLeastOneRow: '请至少选择一行。',
                expandRows: '展开行',
                collapseRows: '折叠行',
                apiSettings: 'API 设置',
                publicImportActive: '使用公共额度导入。公共额度满时可以改用自己的 FF Logs API。',
                userApiActive: '已启用个人 FF Logs API client，本次导入不占用公共额度。',
                apiLimitTitle: '公共导入额度已满',
                apiLimitSubtitle: '你可以等到下一个整点公共额度刷新，也可以现在使用自己的 FF Logs v2 API client 继续导入。',
                apiDisclosure: '你的 FF Logs client ID 和 client secret 会上传到 M-Spec 服务器，由服务器代为请求 FF Logs。M-Spec 服务器不会在本地保存它们，也不会写入数据库或日志。它们会保存在你自己的浏览器中，之后导入 Log 时自动使用。请不要把 client secret 分享给别人。',
                apiTokenInstructionsTitle: '创建自己的 FF Logs v2 API Client',
                apiTokenInstructionsBody: '打开 FF Logs client 页面，点击 Create a Client。按下面这样填写表格。创建成功后 FF Logs 会显示 client ID 和 client secret，请立刻复制这两个内容；secret 只会显示一次，丢了就只能删掉 client 重新创建。',
                apiClientPageLabel: 'FF Logs clients 页面',
                apiClientNameLabel: '应用名称',
                apiRedirectUrlLabel: 'Redirect URL',
                apiPublicClientLabel: 'Public Client 选项',
                apiPublicClientValue: '不要勾选。M-Spec 需要 client secret。',
                copy: '复制',
                copied: '已复制',
                apiTokenInputLabel: 'FF Logs Client ID / Client Secret',
                apiClientIdPlaceholder: 'Client ID',
                apiClientSecretPlaceholder: 'Client Secret',
                save: '保存',
                savedUserApiNotice: '当前浏览器已经保存个人 FF Logs API client，导入时会优先使用它。',
                clear: '清除',
                missingFflogsToken: '请同时输入 FF Logs client ID 和 client secret。',
                invalidFflogsCredentials: '你的 FF Logs client ID 或 client secret 可能有问题，请重新输入。',
                importUrlHelp: '请粘贴完整 FF Logs 链接，并且 fight 必须是数字，例如 fight=9。不要用 fight=last。解决办法：先在 FF Logs 里点进这一 pull，再复制地址栏里已经变成数字的链接。',
                numericFightError: 'FF Logs 链接必须包含数字 fight，例如 fight=9。不能使用 fight=last。请先在 FF Logs 里点进这一 pull，再复制地址栏里变成数字后的链接。',
                importRateLimitError: '正在使用导入功能的玩家过多。请等到下一个整点额度刷新，或使用自己的 FF Logs API client。',
                missingReportIdError: '链接里找不到 report ID。请粘贴完整 FF Logs 链接，必须包含前面的 https://。',
                reportNotFoundError: '找不到这份 Log。请检查链接是否正确，以及 FF Logs 上是否可见。',
                noReportPermissionError: 'M-Spec 没有权限读取这份 Log。请把 Log 设为公开，或使用有权限读取它的 client。',
                fightNotFoundError: '这份 Log 里找不到这一 pull。请在 FF Logs 里点进具体 pull，等地址里的 fight 变成数字后再复制。',
                playerNotFoundError: '这一 pull 里找不到这个玩家。请重新加载玩家列表再选择。',
                importGenericError: '导入失败，请稍后再试。',
                role_Tanks: '坦克',
                role_Healers: '治疗',
                role_Melee: '近战',
                role_Physical_Ranged: '远敏',
                role_Magical_Ranged: '法系'
            },
            ja: {
                language: '言語',
                loading: '読み込み中...',
                boss: 'Boss',
                bossGroup_current: '現行コンテンツ',
                bossGroup_legacyUltimates: '過去の絶',
                spec: 'ジョブ',
                region: '地域',
                with: '構成フィルター',
                killTime: '討伐時間',
                importLog: 'Log 取込',
                select: '選抜',
                selected: '選択中',
                confirm: '確定',
                cancel: '取消',
                curated: '選抜',
                close: '閉じる',
                importPull: 'FF Logs Pull 取込',
                loadPlayers: 'プレイヤー読込',
                display: '表示',
                controls: 'コントロール',
                all: '全て',
                showAllSpells: '全スキル表示',
                hideAllSpells: '全スキル非表示',
                duration: '持続',
                cooldown: 'CD',
                skillTimeLabels: 'スキル時刻',
                phases: 'フェーズ',
                alignPhase: 'このフェーズで揃える',
                clearPhaseAlignment: 'フェーズ揃えを解除',
                collapseLeftPanel: '左パネルを折りたたむ',
                expandLeftPanel: '左パネルを展開',
                showBossRow: 'Boss 行を切替',
                category_cd: 'CD',
                category_single_mit: '単体軽減',
                category_group_mit: '全体軽減',
                category_utility: '補助',
                category_others: 'その他',
                limitBreak: 'Limit Break',
                showLimitBreak: 'LB を表示',
                party: 'パーティ',
                buddy: '相方',
                showBuddy: '相方タンク/ヒラのスキルを表示',
                technicalTangoWindow: 'TG',
                zoomTechnicalTangoWindow: '相方のスキルを攻めのタンゴ2秒前から終了までに絞り込み',
                bossTimeline: 'Boss タイムライン',
                mech: 'ギミック',
                tb: 'TB',
                aoe: 'AOE',
                rank: '順位',
                rdps: 'RDPS',
                reg: '地域',
                pair: '相方',
                buffs: 'シナジー',
                importedLog: '読込済み Log',
                removeImportedLog: '取込 Log を削除',
                shown: '表示',
                filterKillTime: '討伐時間フィルター（分 : 秒）',
                min: '最小',
                max: '最大',
                reset: 'リセット',
                apply: '適用',
                openFFLogs: 'FF Logs で開く',
                enterCuration: '選抜モード',
                exitCuration: '選抜モード終了',
                showBossTimelineType: '表示',
                selectAtLeastOneRow: '少なくとも1行を選択してください。',
                expandRows: '行を展開',
                collapseRows: '行を折りたたむ',
                apiSettings: 'API 設定',
                publicImportActive: '共有インポート枠を使用中です。上限に達した場合は自分の FF Logs API client を使用できます。',
                userApiActive: '個人 FF Logs API client が有効です。このインポートは共有枠を使用しません。',
                apiLimitTitle: '共有インポート枠が上限に達しました',
                apiLimitSubtitle: '次の正時に共有枠が更新されるまで待つか、自分の FF Logs v2 API client を使って続行できます。',
                apiDisclosure: 'あなたの FF Logs client ID と client secret は M-Spec サーバーへ送信され、サーバーが代理で FF Logs にリクエストします。M-Spec サーバーはそれらをローカル保存せず、データベースやログにも意図的に書き込みません。それらはあなたのブラウザに保存され、今後のインポートで自動使用されます。client secret を他人に共有しないでください。',
                apiTokenInstructionsTitle: '自分の FF Logs v2 API Client を作成する',
                apiTokenInstructionsBody: 'FF Logs client ページを開き、Create a Client をクリックします。下の内容でフォームを入力してください。作成後、client ID と client secret が表示されます。secret は一度しか表示されないため、必ずその場でコピーしてください。',
                apiClientPageLabel: 'FF Logs clients ページ',
                apiClientNameLabel: 'アプリ名',
                apiRedirectUrlLabel: 'Redirect URL',
                apiPublicClientLabel: 'Public Client チェック',
                apiPublicClientValue: 'チェックしないでください。M-Spec は client secret を使用します。',
                copy: 'コピー',
                copied: 'コピー済み',
                apiTokenInputLabel: 'FF Logs Client ID / Client Secret',
                apiClientIdPlaceholder: 'Client ID',
                apiClientSecretPlaceholder: 'Client Secret',
                save: '保存',
                savedUserApiNotice: 'このブラウザには個人 FF Logs API client が保存されています。インポート時に優先して使用されます。',
                clear: '削除',
                missingFflogsToken: 'FF Logs client ID と client secret の両方を入力してください。',
                invalidFflogsCredentials: 'FF Logs client ID または client secret が間違っている可能性があります。再入力してください。',
                importUrlHelp: '数字の fight を含む完全な FF Logs URL を貼り付けてください。例: fight=9。fight=last は使えません。FF Logs で該当 pull を開き、URL が数字になってからコピーしてください。',
                numericFightError: 'FF Logs URL には fight=9 のような数字の fight が必要です。fight=last は使えません。FF Logs で該当 pull を開き、URL が数字になってからコピーしてください。',
                importRateLimitError: '現在インポート機能の利用者が多すぎます。次の正時に共有枠が更新されるまで待つか、自分の FF Logs API client を使用してください。',
                missingReportIdError: 'URL から report ID を取得できません。https:// から始まる完全な FF Logs レポート URL を貼り付けてください。',
                reportNotFoundError: 'レポートが見つかりません。リンクが正しいか、FF Logs 上で閲覧可能か確認してください。',
                noReportPermissionError: 'M-Spec にはこのレポートを閲覧する権限がありません。レポートを公開するか、閲覧権限のある client を使用してください。',
                fightNotFoundError: 'このレポート内に該当 pull が見つかりません。FF Logs で対象 pull を開き、fight が数字になってから URL をコピーしてください。',
                playerNotFoundError: 'この pull 内に該当プレイヤーが見つかりません。プレイヤー一覧を再読み込みして選び直してください。',
                importGenericError: 'インポートに失敗しました。しばらくしてから再試行してください。',
                role_Tanks: 'タンク',
                role_Healers: 'ヒーラー',
                role_Melee: '近接',
                role_Physical_Ranged: 'レンジ',
                role_Magical_Ranged: 'キャスター'
            },
            ko: {
                language: '언어',
                loading: '불러오는 중...',
                boss: 'Boss',
                bossGroup_current: '현재 콘텐츠',
                bossGroup_legacyUltimates: '이전 절 레이드',
                spec: '직업',
                region: '지역',
                with: '조합 필터',
                killTime: '킬 타임',
                importLog: 'Log 가져오기',
                select: '선별',
                selected: '선택됨',
                confirm: '확인',
                cancel: '취소',
                curated: '선별',
                close: '닫기',
                importPull: 'FF Logs Pull 가져오기',
                loadPlayers: '플레이어 로드',
                display: '표시',
                controls: '컨트롤',
                all: '전체',
                showAllSpells: '모든 스킬 표시',
                hideAllSpells: '모든 스킬 숨김',
                duration: '지속',
                cooldown: 'CD',
                skillTimeLabels: '스킬 시간',
                phases: '페이즈',
                alignPhase: '이 페이즈로 정렬',
                clearPhaseAlignment: '페이즈 정렬 해제',
                collapseLeftPanel: '왼쪽 패널 접기',
                expandLeftPanel: '왼쪽 패널 펼치기',
                showBossRow: 'Boss 행 전환',
                category_cd: 'CD',
                category_single_mit: '단일 생존기',
                category_group_mit: '파티 생존기',
                category_utility: '유틸',
                category_others: '기타',
                limitBreak: 'Limit Break',
                showLimitBreak: 'LB 표시',
                party: '파티',
                buddy: '버디',
                showBuddy: '다른 탱/힐 스킬 표시',
                technicalTangoWindow: 'TG',
                zoomTechnicalTangoWindow: '버디 스킬을 데빌먼트 2초 전부터 종료까지로 필터',
                bossTimeline: 'Boss 타임라인',
                mech: '기믹',
                tb: 'TB',
                aoe: 'AOE',
                rank: '순위',
                rdps: 'RDPS',
                reg: '지역',
                pair: '짝',
                buffs: '시너지',
                importedLog: '로드된 Log',
                removeImportedLog: '가져온 Log 제거',
                shown: '표시',
                filterKillTime: '킬 타임 필터 (분 : 초)',
                min: '최소',
                max: '최대',
                reset: '초기화',
                apply: '적용',
                openFFLogs: 'FF Logs 열기',
                enterCuration: '선별 모드',
                exitCuration: '선별 모드 종료',
                showBossTimelineType: '표시',
                selectAtLeastOneRow: '최소 한 줄을 선택해 주세요.',
                expandRows: '행 펼치기',
                collapseRows: '행 접기',
                apiSettings: 'API 설정',
                publicImportActive: '공용 가져오기 한도를 사용 중입니다. 한도가 찼다면 본인의 FF Logs API client 를 사용할 수 있습니다.',
                userApiActive: '개인 FF Logs API client 가 활성화되었습니다. 이 가져오기는 공용 한도를 사용하지 않습니다.',
                apiLimitTitle: '공용 가져오기 한도가 가득 찼습니다',
                apiLimitSubtitle: '다음 정시에 공용 한도가 갱신될 때까지 기다리거나, 본인의 FF Logs v2 API client 를 사용해 계속 가져올 수 있습니다.',
                apiDisclosure: 'FF Logs client ID 와 client secret 은 M-Spec 서버로 전송되며, 서버가 대신 FF Logs 에 요청합니다. M-Spec 서버는 이를 로컬에 저장하지 않고 데이터베이스나 로그에도 의도적으로 기록하지 않습니다. 이 정보는 사용자의 브라우저에 저장되어 이후 Log 가져오기에 자동으로 사용됩니다. client secret 을 다른 사람에게 공유하지 마세요.',
                apiTokenInstructionsTitle: '본인의 FF Logs v2 API Client 만들기',
                apiTokenInstructionsBody: 'FF Logs client 페이지를 열고 Create a Client 를 클릭하세요. 아래 값으로 폼을 입력하세요. 생성 후 client ID 와 client secret 이 표시됩니다. secret 은 한 번만 표시되므로 반드시 바로 복사하세요.',
                apiClientPageLabel: 'FF Logs clients 페이지',
                apiClientNameLabel: '애플리케이션 이름',
                apiRedirectUrlLabel: 'Redirect URL',
                apiPublicClientLabel: 'Public Client 체크',
                apiPublicClientValue: '체크하지 마세요. M-Spec 은 client secret 이 필요합니다.',
                copy: '복사',
                copied: '복사됨',
                apiTokenInputLabel: 'FF Logs Client ID / Client Secret',
                apiClientIdPlaceholder: 'Client ID',
                apiClientSecretPlaceholder: 'Client Secret',
                save: '저장',
                savedUserApiNotice: '이 브라우저에 개인 FF Logs API client 가 저장되어 있습니다. 가져오기 시 우선 사용됩니다.',
                clear: '삭제',
                missingFflogsToken: 'FF Logs client ID 와 client secret 을 모두 입력해 주세요.',
                invalidFflogsCredentials: 'FF Logs client ID 또는 client secret 이 잘못되었을 수 있습니다. 다시 입력해 주세요.',
                importUrlHelp: '숫자 fight 값이 포함된 전체 FF Logs URL 을 붙여넣으세요. 예: fight=9. fight=last 는 사용할 수 없습니다. FF Logs 에서 해당 pull 을 먼저 연 뒤, URL 이 숫자로 바뀐 후 복사하세요.',
                numericFightError: 'FF Logs URL 에는 fight=9 처럼 숫자 fight 값이 필요합니다. fight=last 는 사용할 수 없습니다. FF Logs 에서 해당 pull 을 먼저 연 뒤, URL 이 숫자로 바뀐 후 복사하세요.',
                importRateLimitError: '현재 가져오기 기능을 사용하는 플레이어가 너무 많습니다. 다음 정시에 공용 한도가 갱신될 때까지 기다리거나 본인의 FF Logs API client 를 사용해 주세요.',
                missingReportIdError: 'URL 에서 report ID 를 찾을 수 없습니다. https:// 로 시작하는 전체 FF Logs 리포트 링크를 붙여넣어 주세요.',
                reportNotFoundError: '리포트를 찾을 수 없습니다. 링크가 올바른지, FF Logs 에서 볼 수 있는지 확인해 주세요.',
                noReportPermissionError: 'M-Spec 에 이 리포트를 볼 권한이 없습니다. 리포트를 공개하거나 접근 권한이 있는 client 를 사용해 주세요.',
                fightNotFoundError: '이 리포트에서 해당 pull 을 찾을 수 없습니다. FF Logs 에서 정확한 pull 을 열고 fight 가 숫자로 바뀐 뒤 URL 을 복사해 주세요.',
                playerNotFoundError: '이 pull 에서 해당 플레이어를 찾을 수 없습니다. 플레이어 목록을 다시 불러온 뒤 선택해 주세요.',
                importGenericError: '가져오기에 실패했습니다. 잠시 후 다시 시도해 주세요.',
                role_Tanks: '탱커',
                role_Healers: '힐러',
                role_Melee: '근접',
                role_Physical_Ranged: '물리 원거리',
                role_Magical_Ranged: '마법 원거리'
            }
        };
        const normalizeUiLanguage = (language) => {
            const normalized = String(language || '').toLowerCase();
            if (normalized.startsWith('zh')) return 'zh';
            if (normalized.startsWith('ja')) return 'ja';
            if (normalized.startsWith('ko')) return 'ko';
            return 'en';
        };
        const getInitialUiLanguage = () => {
            try {
                const stored = localStorage.getItem(UI_LANGUAGE_STORAGE_KEY);
                if (I18N[stored]) return stored;
            } catch (e) {}
            return normalizeUiLanguage(navigator.language || navigator.userLanguage || 'en');
        };
        const getStoredVisibleMinutes = () => {
            try {
                if (localStorage.getItem(ZOOM_VISIBLE_MINUTES_MIGRATION_KEY) !== ZOOM_VISIBLE_MINUTES_MIGRATION) {
                    localStorage.removeItem(ZOOM_VISIBLE_MINUTES_STORAGE_KEY);
                    localStorage.setItem(ZOOM_VISIBLE_MINUTES_MIGRATION_KEY, ZOOM_VISIBLE_MINUTES_MIGRATION);
                    return null;
                }
                const stored = Number(localStorage.getItem(ZOOM_VISIBLE_MINUTES_STORAGE_KEY));
                if (Number.isFinite(stored)) {
                    return Math.max(MIN_VISIBLE_MINUTES, Math.min(MAX_VISIBLE_MINUTES, stored));
                }
            } catch (e) {}
            return null;
        };
        // 窄屏默认少看几分钟: 375px 宽的屏幕上铺 6 分钟等于每秒不到 1 像素,
        // 28px 的技能图标会叠成一团完全看不清; 2 分钟约 2.6px/秒, 密但可读。
        const DEFAULT_VISIBLE_MINUTES_MOBILE = 2;

        const getInitialZoom = () => {
            const storedVisibleMinutes = getStoredVisibleMinutes();
            const narrow = (window.innerWidth || 1280) < 768;
            const fallbackMinutes = narrow ? DEFAULT_VISIBLE_MINUTES_MOBILE : DEFAULT_VISIBLE_MINUTES;
            const visibleMinutes = storedVisibleMinutes !== null ? storedVisibleMinutes : fallbackMinutes;
            // 左面板在窄屏下是收起的, 用实际宽度算才不会低估可视区
            const panelWidth = narrow ? LEFT_PANEL_COLLAPSED_WIDTH : LEFT_PANEL_WIDTH;
            const visibleWidth = Math.max(280, (window.innerWidth || 1280) - panelWidth - 12);
            return visibleWidth / (visibleMinutes * 60);
        };
        const BUDDY_VISIBILITY_STORAGE_KEY = 'm-spec:show-buddy';
        const SPELL_SELECTION_MIGRATIONS = {
            'reaper-reaper': 'rpr-defaults-2026-06-08',
            'viper-viper': 'vpr-defaults-2026-06-08'
        };
        const getSpellSelectionStorageKey = (specSlug) => `m-spec:selected-spells:${specSlug}`;
        const getSpellSelectionSlotStorageKey = (specSlug) => `m-spec:selected-spell-slots:${specSlug}`;
        const getSpellSelectionMigrationKey = (specSlug) => `m-spec:selected-spells-migration:${specSlug}`;
        const applySpellSelectionMigration = (specSlug) => {
            const migration = SPELL_SELECTION_MIGRATIONS[specSlug];
            if (!migration) return false;
            try {
                const migrationKey = getSpellSelectionMigrationKey(specSlug);
                if (localStorage.getItem(migrationKey) === migration) return false;
                localStorage.removeItem(getSpellSelectionStorageKey(specSlug));
                localStorage.setItem(migrationKey, migration);
                return true;
            } catch (e) {}
            return false;
        };
        const parseBooleanParam = (value) => {
            if (value === null || value === undefined) return null;
            const normalized = String(value).trim().toLowerCase();
            if (['1', 'true', 'on', 'yes'].includes(normalized)) return true;
            if (['0', 'false', 'off', 'no'].includes(normalized)) return false;
            return null;
        };
        const getInitialBuddyVisibility = () => {
            const params = new URLSearchParams(window.location.search);
            const fromUrl = parseBooleanParam(params.get('buddy'));
            if (fromUrl !== null) return fromUrl;
            try {
                const stored = parseBooleanParam(localStorage.getItem(BUDDY_VISIBILITY_STORAGE_KEY));
                if (stored !== null) return stored;
            } catch (e) {}
            return false;
        };
        const writeBuddyVisibility = (enabled) => {
            try {
                localStorage.setItem(BUDDY_VISIBILITY_STORAGE_KEY, enabled ? '1' : '0');
            } catch (e) {}
            const url = new URL(window.location.href);
            url.searchParams.set('buddy', enabled ? '1' : '0');
            window.history.replaceState({}, '', url);
        };
        const DEFAULT_CONTENT_LEVEL = 100;
        const BOSS_CONTENT_LEVELS = {
            'vamp-fatale': 100,
            'red-hot-and-deep-blue': 100,
            'the-tyrant': 100,
            'lindwurm': 100,
            'lindwurm-ii': 100,
            'futures-rewritten': 100,
            'dancing-mad': 100,
            'the-unending-coil-of-bahamut': 70,
            'the-weapons-refrain': 70,
            'the-epic-of-alexander': 80,
            'dragonsongs-reprise': 90,
            'the-omega-protocol': 90
        };
        const getBossContentLevel = (bossSlug) => BOSS_CONTENT_LEVELS[bossSlug] || DEFAULT_CONTENT_LEVEL;
        const getSpellDisplaySlot = (spell) => spell.display_slot || `spell:${spell.id || spell.spell_id || spell.name}`;
        const filterSpellListForContentLevel = (spellList, contentLevel) => {
            const bySlot = new Map();
            (spellList || []).forEach((spell, index) => {
                const level = Number(spell.level || 0);
                if (level > contentLevel) return;

                const slot = getSpellDisplaySlot(spell);
                const current = bySlot.get(slot);
                const currentLevel = Number(current?.level || 0);
                const currentOrder = Number(current?.load_order ?? 999999);
                const order = Number(spell.load_order ?? index);

                if (!current || level > currentLevel || (level === currentLevel && order < currentOrder)) {
                    bySlot.set(slot, spell);
                }
            });

            return [...bySlot.values()].sort((a, b) => {
                const orderA = Number(a.load_order ?? 999999);
                const orderB = Number(b.load_order ?? 999999);
                if (orderA !== orderB) return orderA - orderB;
                return Number(a.id || a.spell_id || 0) - Number(b.id || b.spell_id || 0);
            });
        };
        const markSpellRepresentativesForContentLevel = (spellList, contentLevel) => {
            const representatives = new Set(filterSpellListForContentLevel(spellList, contentLevel).map(spell => Number(spell.id || spell.spell_id)));
            return (spellList || [])
                .filter(spell => Number(spell.level || 0) <= contentLevel)
                .map(spell => ({
                    ...spell,
                    is_display_representative: representatives.has(Number(spell.id || spell.spell_id))
                }));
        };
        const translate = (language, key) => I18N[language]?.[key] || I18N.en[key] || key;
        const translateWithValues = (language, key, values = {}) => (
            Object.entries(values).reduce(
                (text, [name, value]) => text.replaceAll(`{${name}}`, value),
                translate(language, key)
            )
        );
        const getCategoryLabel = (category, t) => {
            const key = `category_${String(category.label || '').toLowerCase().replace(/\s+/g, '_')}`;
            const translated = t(key);
            return translated === key ? category.label : translated;
        };
        const getSpecGroupLabel = (groupLabel, t) => {
            const key = `role_${String(groupLabel || '').replace(/\s+/g, '_')}`;
            const translated = t(key);
            return translated === key ? groupLabel : translated;
        };
        const getBossTimelineTypeLabel = (type, t) => {
            const key = type || 'mech';
            const translated = t(key);
            return translated === key ? (BOSS_TIMELINE_TYPES[key]?.label || key) : translated;
        };

        // --- Mock Data Layer ---
        const fetchSpellCategories = async () => ({
            // defaultActive: controls if spells in this category are shown by default
            MAJOR: { label: 'CD', color: '#E87B7B', iconType: 'swords', defaultActive: true },
            SINGLE_MIT: { label: 'Single Mit', color: '#4facfe', iconType: 'shield', defaultActive: false },
            RAID_MIT: { label: 'Group Mit', color: '#8657FF', iconType: 'shieldAlert', defaultActive: true },
            UTILITY: { label: 'Utility', color: '#E6B33D', iconType: 'zap', defaultActive: false },
            OTHER: { label: 'Others', color: '#94A3B8', iconType: 'more', defaultActive: false },
        });

        // 1. fetchSpellData (API)
        const fetchSpellData = async (specSlug = 'redmage-redmage', bossSlug = '') => {
            try {
                // 不再拼 ?t= 时间戳绕缓存: 服务器对 /data 返回 no-cache + ETag,
                // 浏览器每次回源校验, 未变化时 304 复用缓存, 数据更新后立刻生效
                const url = `./data/spells_${specSlug}.json`;

                const res = await fetch(url);
                if (!res.ok) throw new Error("Local spell file not found");
                const data = await res.json();
                
                const spellMap = {};
                const list = Array.isArray(data) ? data : Object.values(data);
                const contentLevel = getBossContentLevel(bossSlug);
                const visibleList = markSpellRepresentativesForContentLevel(list, contentLevel);

                visibleList.forEach((spell) => {
                    spellMap[spell.spell_id] = {
                        id: spell.spell_id,
                        name: spell.name,
                        image: `./images/spells/${spell.icon}`,
                        cd: spell.cooldown || 0,
                        duration: spell.duration || 0,
                        color: spell.color || '#ffcc00',
                        category: spell.category || 'MAJOR', 
                        show: (spell.show !== undefined && spell.show !== null) ? spell.show : true,
                        load_order: (spell.load_order !== undefined) ? spell.load_order : 9999,
                        level: Number(spell.level || 0),
                        display_slot: spell.display_slot || "",
                        is_display_representative: spell.is_display_representative !== false
                    };
                });
                return spellMap;

            } catch (e) {
                console.warn(`[离线模式] 未找到 ${specSlug} 的技能定义文件。`, e);
                return {};
            }
        };
        // Mock Data for Specs - Moved to Global Scope
        const SPECS = [
            { label: 'Tanks', items: [
                {id:'tank-combined', icon:null, n:'Tank Combined', combined: true},
                {id:'paladin-paladin', icon:'paladin.png', n:'Paladin'},
                {id:'warrior-warrior', icon:'warrior.png', n:'Warrior'},
                {id:'darkknight-darkknight', icon:'Dark_Knight.png', n:'Dark Knight'},
                {id:'gunbreaker-gunbreaker', icon:'Gunbreaker.png', n:'Gunbreaker'}
            ]},
            { label: 'Healers', items: [
                {id:'healer-combined', icon:null, n:'Healer Combined', combined: true},
                {id:'whitemage-whitemage', icon:'White_Mage.png', n:'White Mage'},
                {id:'scholar-scholar', icon:'Scholar.png', n:'Scholar'},
                {id:'astrologian-astrologian', icon:'Astrologian.png', n:'Astrologian'},
                {id:'sage-sage', icon:'Sage.png', n:'Sage'}
            ]},
            { label: 'Melee', items: [
                {id:'monk-monk', icon:'monk.png', n:'Monk'},
                {id:'dragoon-dragoon', icon:'Dragoon.png', n:'Dragoon'},
                {id:'ninja-ninja', icon:'Ninja.png', n:'Ninja'},
                {id:'samurai-samurai', icon:'Samurai.png', n:'Samurai'},
                {id:'reaper-reaper', icon:'Reaper.png', n:'Reaper'},
                {id:'viper-viper', icon:'Viper.png', n:'Viper'}
            ]},
            { label: 'Physical Ranged', items: [
                {id:'bard-bard', icon:'Bard.png', n:'Bard'},
                {id:'machinist-machinist', icon:'Machinist.png', n:'Machinist'},
                {id:'dancer-dancer', icon:'Dancer.png', n:'Dancer'}
            ]},
            { label: 'Magical Ranged', items: [
                {id:'blackmage-blackmage', icon:'Black_Mage.png', n:'Black Mage'},
                {id:'summoner-summoner', icon:'Summoner.png', n:'Summoner'},
                {id:'redmage-redmage', icon:'Red_Mage.png', n:'Red Mage'},
                {id:'pictomancer-pictomancer', icon:'Pictomancer.png', n:'Pictomancer'}
            ]},
        ];

        const COMBINED_SPECS = {
            'tank-combined': {
                role: 'tank',
                baseSpec: 'paladin-paladin',
                specs: ['paladin-paladin', 'warrior-warrior', 'darkknight-darkknight', 'gunbreaker-gunbreaker']
            },
            'healer-combined': {
                role: 'healer',
                baseSpec: 'whitemage-whitemage',
                specs: ['whitemage-whitemage', 'scholar-scholar', 'astrologian-astrologian', 'sage-sage']
            }
        };

        const BOSS_GROUPS = [
            {
                labelKey: 'bossGroup_current',
                items: [
                    { id: 'vamp-fatale', label: 'M9S: Vamp Fatale' },
                    { id: 'red-hot-and-deep-blue', label: 'M10S: Red Hot and Deep Blue' },
                    { id: 'the-tyrant', label: 'M11S: The Tyrant' },
                    { id: 'lindwurm', label: 'M12S P1: Lindwurm' },
                    { id: 'lindwurm-ii', label: 'M12S P2: Lindwurm' },
                    { id: 'futures-rewritten', label: 'FRU: Futures Rewritten' },
                    { id: 'dancing-mad', label: 'DMU: Dancing Mad' }
                ]
            },
            {
                labelKey: 'bossGroup_legacyUltimates',
                items: [
                    { id: 'the-unending-coil-of-bahamut', label: 'UCOB: The Unending Coil of Bahamut' },
                    { id: 'the-weapons-refrain', label: "UWU: The Weapon's Refrain" },
                    { id: 'the-epic-of-alexander', label: 'TEA: The Epic of Alexander' },
                    { id: 'dragonsongs-reprise', label: "DSR: Dragonsong's Reprise" },
                    { id: 'the-omega-protocol', label: 'TOP: The Omega Protocol' }
                ]
            }
        ];
        const BOSS_OPTIONS = BOSS_GROUPS.flatMap(group => group.items);

        const SPEC_NAME_TRANSLATIONS = {
            zh: {
                'tank-combined': '双T合计',
                'healer-combined': '双奶合计',
                'paladin-paladin': '骑士',
                'warrior-warrior': '战士',
                'darkknight-darkknight': '暗黑骑士',
                'gunbreaker-gunbreaker': '绝枪战士',
                'whitemage-whitemage': '白魔法师',
                'scholar-scholar': '学者',
                'astrologian-astrologian': '占星术士',
                'sage-sage': '贤者',
                'monk-monk': '武僧',
                'dragoon-dragoon': '龙骑士',
                'ninja-ninja': '忍者',
                'samurai-samurai': '武士',
                'reaper-reaper': '钐镰客',
                'viper-viper': '蝰蛇剑士',
                'bard-bard': '吟游诗人',
                'machinist-machinist': '机工士',
                'dancer-dancer': '舞者',
                'blackmage-blackmage': '黑魔法师',
                'summoner-summoner': '召唤师',
                'redmage-redmage': '赤魔法师',
                'pictomancer-pictomancer': '绘灵法师'
            },
            ja: {
                'tank-combined': 'タンク合算',
                'healer-combined': 'ヒーラー合算',
                'paladin-paladin': 'ナイト',
                'warrior-warrior': '戦士',
                'darkknight-darkknight': '暗黒騎士',
                'gunbreaker-gunbreaker': 'ガンブレイカー',
                'whitemage-whitemage': '白魔道士',
                'scholar-scholar': '学者',
                'astrologian-astrologian': '占星術師',
                'sage-sage': '賢者',
                'monk-monk': 'モンク',
                'dragoon-dragoon': '竜騎士',
                'ninja-ninja': '忍者',
                'samurai-samurai': '侍',
                'reaper-reaper': 'リーパー',
                'viper-viper': 'ヴァイパー',
                'bard-bard': '吟遊詩人',
                'machinist-machinist': '機工士',
                'dancer-dancer': '踊り子',
                'blackmage-blackmage': '黒魔道士',
                'summoner-summoner': '召喚士',
                'redmage-redmage': '赤魔道士',
                'pictomancer-pictomancer': 'ピクトマンサー'
            },
            ko: {
                'tank-combined': '탱커 합산',
                'healer-combined': '힐러 합산',
                'paladin-paladin': '나이트',
                'warrior-warrior': '전사',
                'darkknight-darkknight': '암흑기사',
                'gunbreaker-gunbreaker': '건브레이커',
                'whitemage-whitemage': '백마도사',
                'scholar-scholar': '학자',
                'astrologian-astrologian': '점성술사',
                'sage-sage': '현자',
                'monk-monk': '몽크',
                'dragoon-dragoon': '용기사',
                'ninja-ninja': '닌자',
                'samurai-samurai': '사무라이',
                'reaper-reaper': '리퍼',
                'viper-viper': '바이퍼',
                'bard-bard': '음유시인',
                'machinist-machinist': '기공사',
                'dancer-dancer': '무도가',
                'blackmage-blackmage': '흑마도사',
                'summoner-summoner': '소환사',
                'redmage-redmage': '적마도사',
                'pictomancer-pictomancer': '픽토맨서'
            }
        };

        const BOSS_NAME_TRANSLATIONS = {
            zh: {
                'vamp-fatale': 'M9S：致命美人',
                'red-hot-and-deep-blue': 'M10S：极限温度差兄弟',
                'the-tyrant': 'M11S：霸王',
                'lindwurm': 'M12S P1：亡国大蛇 林德布鲁姆',
                'lindwurm-ii': 'M12S P2：亡国大蛇 林德布鲁姆',
                'futures-rewritten': 'FRU：光暗未来绝境战',
                'dancing-mad': 'DMU：妖星乱舞绝境战',
                'the-unending-coil-of-bahamut': 'UCOB：巴哈姆特绝境战',
                'the-weapons-refrain': 'UWU：究极神兵绝境战',
                'the-epic-of-alexander': 'TEA：亚历山大绝境战',
                'dragonsongs-reprise': 'DSR：幻想龙诗绝境战',
                'the-omega-protocol': 'TOP：欧米茄绝境验证战'
            },
            ja: {
                'vamp-fatale': 'M9S：ヴァンプ・ファタール',
                'red-hot-and-deep-blue': 'M10S：レッドホット／ディープブルー',
                'the-tyrant': 'M11S：ザ・タイラント',
                'lindwurm': 'M12S P1：リンドブルム',
                'lindwurm-ii': 'M12S P2：リンドブルム',
                'futures-rewritten': 'FRU：絶もうひとつの未来',
                'dancing-mad': 'DMU：絶妖星乱舞',
                'the-unending-coil-of-bahamut': 'UCOB：絶バハムート討滅戦',
                'the-weapons-refrain': 'UWU：絶アルテマウェポン破壊作戦',
                'the-epic-of-alexander': 'TEA：絶アレキサンダー討滅戦',
                'dragonsongs-reprise': 'DSR：絶竜詩戦争',
                'the-omega-protocol': 'TOP：絶オメガ検証戦'
            },
            ko: {
                'vamp-fatale': 'M9S: 뱀프 파탈',
                'red-hot-and-deep-blue': 'M10S: 레드 핫과 딥 블루',
                'the-tyrant': 'M11S: 더 타이런트',
                'lindwurm': 'M12S P1: 린드블룸',
                'lindwurm-ii': 'M12S P2: 린드블룸',
                'futures-rewritten': 'FRU: 절 또 하나의 미래',
                'dancing-mad': 'DMU: 절 요성난무',
                'the-unending-coil-of-bahamut': 'UCOB: 절 바하무트 토벌전',
                'the-weapons-refrain': 'UWU: 절 알테마 웨폰 파괴작전',
                'the-epic-of-alexander': 'TEA: 절 알렉산더 토벌전',
                'dragonsongs-reprise': 'DSR: 절 용시전쟁',
                'the-omega-protocol': 'TOP: 절 오메가 검증전'
            }
        };

        const isCombinedSpec = (specSlug) => Boolean(COMBINED_SPECS[specSlug]);
        const getCombinedConfig = (specSlug) => COMBINED_SPECS[specSlug] || null;

        const getIconForSpec = (specSlug) => {
             const item = SPECS.flatMap(g => g.items).find(i => i.id === specSlug);
             return item ? item.icon : null;
        };

        const getSpecInfo = (specSlug) => {
            const item = SPECS.flatMap(g => g.items).find(i => i.id === specSlug);
            if (item) return item;
            return {
                id: specSlug,
                icon: null,
                n: (specSlug || "Unknown").split("-")[0].replace(/\b\w/g, c => c.toUpperCase())
            };
        };

        const getLocalizedSpecName = (specSlug, language) => (
            SPEC_NAME_TRANSLATIONS[language]?.[specSlug] || getSpecInfo(specSlug).n
        );

        const getLocalizedBossName = (bossSlug, language) => (
            BOSS_NAME_TRANSLATIONS[language]?.[bossSlug] || BOSS_OPTIONS.find(boss => boss.id === bossSlug)?.label || bossSlug
        );

        const getLocalizedBossTimelineName = (event, language) => (
            event?.name_i18n?.[language] || event?.name || 'Unknown'
        );

        const CopyValue = ({ value, label, t }) => {
            const [copied, setCopied] = useState(false);
            const handleCopy = async () => {
                try {
                    await navigator.clipboard.writeText(value);
                    setCopied(true);
                    window.setTimeout(() => setCopied(false), 1200);
                } catch (error) {
                    console.warn("[M-Spec] Could not copy value.", error);
                }
            };
            return (
                <div className="rounded border border-gray-800 bg-black/25 p-2">
                    <div className="mb-1 text-[10px] font-black uppercase tracking-wide text-gray-500">{label}</div>
                    <div className="flex items-center gap-2">
                        <code className="min-w-0 flex-1 truncate rounded bg-black/40 px-2 py-1.5 text-xs text-gray-200">{value}</code>
                        <button
                            type="button"
                            onClick={handleCopy}
                            className="shrink-0 rounded border border-gray-700 px-2 py-1 text-xs font-bold text-gray-300 hover:border-[#00FF96] hover:text-white"
                        >
                            {copied ? t("copied") : t("copy")}
                        </button>
                    </div>
                </div>
            );
        };

        const getDisplaySpells = (spellMap) => (
            Object.values(spellMap || {}).filter(spell => spell.is_display_representative !== false)
        );

        const getSpellSlotIds = (spellMap, spellOrSlot) => {
            const slot = typeof spellOrSlot === "string" ? spellOrSlot : getSpellDisplaySlot(spellOrSlot);
            return Object.values(spellMap || {})
                .filter(spell => getSpellDisplaySlot(spell) === slot)
                .map(spell => Number(spell.id));
        };

        const isSpellSlotSelected = (spellMap, selectedIds, spell) => {
            const selectedIdSet = selectedIds instanceof Set ? selectedIds : new Set(selectedIds || []);
            return getSpellSlotIds(spellMap, spell).some(id => selectedIdSet.has(Number(id)));
        };

        const getSelectedDisplaySpellCount = (spellMap, selectedIds, category = null) => (
            getDisplaySpells(spellMap)
                .filter(spell => (!category || spell.category === category) && isSpellSlotSelected(spellMap, selectedIds, spell))
                .length
        );

        const setSpellSlotSelected = (currentIds, spellMap, spell, selected) => {
            const next = new Set(currentIds || []);
            getSpellSlotIds(spellMap, spell).forEach(id => {
                if (selected) next.add(Number(id)); else next.delete(Number(id));
            });
            return next;
        };

        const toggleSpellSlot = (currentIds, spellMap, spell) => (
            setSpellSlotSelected(currentIds, spellMap, spell, !isSpellSlotSelected(spellMap, currentIds, spell))
        );

        const EMPTY_SPELL_ID_SET = new Set();

        const expandSelectedSpellSlots = (selectedIds, spellMap) => {
            let expanded = new Set();
            const selectedIdSet = selectedIds instanceof Set ? selectedIds : new Set(selectedIds || []);
            selectedIdSet.forEach(id => {
                const spell = spellMap?.[id] || spellMap?.[String(id)];
                if (spell) {
                    expanded = setSpellSlotSelected(expanded, spellMap, spell, true);
                } else {
                    expanded.add(Number(id));
                }
            });
            return expanded;
        };

        const getDefaultSelectedSpellIds = (spellMap, categories) => {
            let selectedIds = new Set();
            getDisplaySpells(spellMap)
                .filter(s => {
                    if (s.show !== null && s.show !== undefined) {
                        return s.show;
                    }
                    const cat = categories[s.category];
                    return cat ? cat.defaultActive : true;
                })
                .forEach(spell => {
                    selectedIds = setSpellSlotSelected(selectedIds, spellMap, spell, true);
                });
            return [...selectedIds];
        };

        const getSelectedSpellSlots = (spellMap, selectedIds) => {
            const selectedIdSet = selectedIds instanceof Set ? selectedIds : new Set(selectedIds || []);
            return [...new Set(
                Object.values(spellMap || {})
                    .filter(spell => selectedIdSet.has(Number(spell.id)))
                    .map(getSpellDisplaySlot)
            )];
        };

        const readStoredSpellSelection = (specSlug, spellMap) => {
            try {
                if (applySpellSelectionMigration(specSlug)) return null;
                const rawSlots = localStorage.getItem(getSpellSelectionSlotStorageKey(specSlug));
                if (rawSlots !== null) {
                    const selectedSlots = new Set(JSON.parse(rawSlots).map(String));
                    return new Set(
                        Object.values(spellMap)
                            .filter(spell => selectedSlots.has(getSpellDisplaySlot(spell)))
                            .map(spell => Number(spell.id))
                    );
                }
                const raw = localStorage.getItem(getSpellSelectionStorageKey(specSlug));
                if (raw === null) return null;
                const validIds = new Set(Object.values(spellMap).map(spell => Number(spell.id)));
                return expandSelectedSpellSlots(
                    JSON.parse(raw).map(Number).filter(id => validIds.has(id)),
                    spellMap
                );
            } catch (error) {
                console.warn("[M-Spec] Could not read stored spell selection.", error);
                return null;
            }
        };

        const writeStoredSpellSelection = (specSlug, selectedIds, spellMap = {}) => {
            try {
                localStorage.setItem(getSpellSelectionStorageKey(specSlug), JSON.stringify([...selectedIds].map(Number)));
                localStorage.setItem(
                    getSpellSelectionSlotStorageKey(specSlug),
                    JSON.stringify(getSelectedSpellSlots(spellMap, selectedIds))
                );
            } catch (error) {
                console.warn("[M-Spec] Could not store spell selection.", error);
            }
        };

        const readStoredUserFflogsCredentials = () => {
            try {
                return {
                    clientId: localStorage.getItem(USER_FFLOGS_CLIENT_ID_STORAGE_KEY) || "",
                    clientSecret: localStorage.getItem(USER_FFLOGS_CLIENT_SECRET_STORAGE_KEY) || ""
                };
            } catch (error) {
                return { clientId: "", clientSecret: "" };
            }
        };

        const writeStoredUserFflogsCredentials = (clientId, clientSecret) => {
            try {
                if (clientId && clientSecret) {
                    localStorage.setItem(USER_FFLOGS_CLIENT_ID_STORAGE_KEY, clientId);
                    localStorage.setItem(USER_FFLOGS_CLIENT_SECRET_STORAGE_KEY, clientSecret);
                } else {
                    localStorage.removeItem(USER_FFLOGS_CLIENT_ID_STORAGE_KEY);
                    localStorage.removeItem(USER_FFLOGS_CLIENT_SECRET_STORAGE_KEY);
                }
            } catch (error) {
                console.warn("[M-Spec] Could not store FF Logs credentials.", error);
            }
        };

        const getImportedLogsStorageKey = (bossSlug) => `m-spec:imported-logs:${bossSlug}`;
        const getImportedLogRowId = (reportId, fightId, sourceId) => `import-${reportId}-${fightId}-${sourceId}`;

        const serializeImportedSpellSelections = (selections) => (
            Object.fromEntries(
                Object.entries(selections || {}).map(([rowId, selectedIds]) => [
                    rowId,
                    [...(selectedIds || [])].map(Number)
                ])
            )
        );

        const readStoredImportedLogCache = (bossSlug) => {
            try {
                const raw = localStorage.getItem(getImportedLogsStorageKey(bossSlug));
                if (!raw) return { rows: [], selections: {}, hiddenRowIds: new Set(), fights: {} };
                const parsed = JSON.parse(raw);
                const rows = Array.isArray(parsed.rows) ? parsed.rows : [];
                const rowIds = new Set(rows.map(row => row.id));
                const selections = Object.fromEntries(
                    Object.entries(parsed.selections || {})
                        .filter(([rowId]) => rowIds.has(rowId))
                        .map(([rowId, selectedIds]) => [
                            rowId,
                            new Set((Array.isArray(selectedIds) ? selectedIds : []).map(Number))
                        ])
                );
                return {
                    rows,
                    selections,
                    fights: parsed.fights || {},
                    hiddenRowIds: new Set(
                        (Array.isArray(parsed.hiddenRowIds) ? parsed.hiddenRowIds : []).filter(rowId => rowIds.has(rowId))
                    )
                };
            } catch (error) {
                console.warn("[M-Spec] Could not read stored imported logs.", error);
                return { rows: [], selections: {}, hiddenRowIds: new Set(), fights: {} };
            }
        };

        const readStoredImportedLogs = (bossSlug) => {
            const cache = readStoredImportedLogCache(bossSlug);
            return {
                rows: cache.rows.filter(row => !cache.hiddenRowIds.has(row.id)),
                selections: cache.selections,
                hiddenRowIds: cache.hiddenRowIds
            };
        };

        const parseImportLogUrlForCache = (url) => {
            try {
                const parsedUrl = new URL(url);
                const reportMatch = parsedUrl.pathname.match(/\/reports\/([^/]+)/);
                const fightRaw = parsedUrl.searchParams.get("fight");
                if (!reportMatch || !/^\d+$/.test(String(fightRaw || ""))) return null;
                return { reportId: reportMatch[1], fightId: Number(fightRaw) };
            } catch (error) {
                const reportMatch = String(url || "").match(/\/reports\/([A-Za-z0-9]+)/);
                const fightMatch = String(url || "").match(/[?&]fight=(\d+)/);
                if (!reportMatch || !fightMatch) return null;
                return { reportId: reportMatch[1], fightId: Number(fightMatch[1]) };
            }
        };

        const getImportFightCacheKey = (reportId, fightId) => `${reportId}:${fightId}`;

        const getCachedImportPlayers = (bossSlug, url) => {
            const importKey = parseImportLogUrlForCache(url);
            if (!importKey) return null;
            const cache = readStoredImportedLogCache(bossSlug);
            return cache.fights[getImportFightCacheKey(importKey.reportId, importKey.fightId)] || null;
        };

        const writeStoredImportFightPlayers = (bossSlug, data) => {
            if (!data?.report_id || !data?.fight_id) return;
            try {
                const cache = readStoredImportedLogCache(bossSlug);
                const key = getImportedLogsStorageKey(bossSlug);
                localStorage.setItem(key, JSON.stringify({
                    version: 2,
                    rows: cache.rows,
                    selections: serializeImportedSpellSelections(cache.selections),
                    hiddenRowIds: [...cache.hiddenRowIds],
                    fights: {
                        ...(cache.fights || {}),
                        [getImportFightCacheKey(data.report_id, data.fight_id)]: {
                            ...data,
                            cached: true
                        }
                    }
                }));
            } catch (error) {
                console.warn("[M-Spec] Could not store imported fight players.", error);
            }
        };

        const writeStoredImportedLogs = (bossSlug, rows, selections, options = {}) => {
            try {
                const safeRows = Array.isArray(rows) ? rows : [];
                const cache = readStoredImportedLogCache(bossSlug);
                const rowMap = new Map(cache.rows.map(row => [row.id, row]));
                safeRows.forEach(row => rowMap.set(row.id, row));
                const allRows = [...rowMap.values()];
                const key = getImportedLogsStorageKey(bossSlug);
                if (!allRows.length) {
                    localStorage.removeItem(key);
                    return;
                }
                const hiddenRowIds = new Set(cache.hiddenRowIds);
                (options.hideRowIds || []).forEach(rowId => hiddenRowIds.add(rowId));
                (options.unhideRowIds || []).forEach(rowId => hiddenRowIds.delete(rowId));
                const rowIds = new Set(allRows.map(row => row.id));
                const mergedSelections = { ...cache.selections, ...(selections || {}) };
                const safeSelections = Object.fromEntries(
                    Object.entries(mergedSelections).filter(([rowId]) => rowIds.has(rowId))
                );
                localStorage.setItem(key, JSON.stringify({
                    version: 2,
                    rows: allRows,
                    selections: serializeImportedSpellSelections(safeSelections),
                    hiddenRowIds: [...hiddenRowIds].filter(rowId => rowIds.has(rowId)),
                    fights: cache.fights || {}
                }));
            } catch (error) {
                console.warn("[M-Spec] Could not store imported logs.", error);
            }
        };

        const mergeSpellMaps = (baseSpells, observedSpells) => {
            const merged = { ...baseSpells };
            Object.entries(observedSpells || {}).forEach(([spellId, spell]) => {
                if (isLimitBreakSpellId(spellId)) return;
                const base = merged[spellId] || {};
                merged[spellId] = {
                    ...spell,
                    ...base,
                    id: Number(spell.id || spellId),
                    image: base.image || spell.image || spell.icon || null,
                    icon: base.icon || spell.icon || spell.image || null,
                    name: base.name || spell.name || `ID: ${spellId}`,
                    color: base.color || spell.color || "#666666",
                    category: base.category || spell.category || "MAJOR",
                    load_order: base.load_order !== undefined ? base.load_order : (spell.load_order !== undefined ? spell.load_order : 9999),
                    show: base.show !== undefined ? base.show : spell.show,
                    duration: base.duration !== undefined ? base.duration : (spell.duration || 0),
                    cd: base.cd !== undefined ? base.cd : (spell.cd || 0),
                    level: base.level !== undefined ? base.level : (spell.level || 0),
                    display_slot: base.display_slot || spell.display_slot || "",
                    is_display_representative: base.is_display_representative !== undefined
                        ? base.is_display_representative
                        : spell.is_display_representative !== false
                };
            });
            return merged;
        };

        const markSpellMapRepresentativesForContentLevel = (spellMap, contentLevel) => {
            const marked = markSpellRepresentativesForContentLevel(
                Object.values(spellMap || {}).map(spell => ({
                    ...spell,
                    id: Number(spell.id || spell.spell_id),
                    spell_id: Number(spell.spell_id || spell.id)
                })),
                contentLevel
            );
            return Object.fromEntries(marked.map(spell => {
                const id = Number(spell.id || spell.spell_id);
                return [id, { ...spell, id, spell_id: id }];
            }));
        };

        const hexToRgba = (hex, alpha) => {
            if (!hex) return `rgba(255,255,255,${alpha})`;
            if (hex.startsWith('#')) {
                const r = parseInt(hex.slice(1, 3), 16);
                const g = parseInt(hex.slice(3, 5), 16);
                const b = parseInt(hex.slice(5, 7), 16);
                return `rgba(${r},${g},${b},${alpha})`;
            }
            return hex;
        };

        const getRole = (specSlug) => {
            const combinedConfig = getCombinedConfig(specSlug);
            if (combinedConfig) return combinedConfig.role;
            if (specSlug.includes('paladin') || specSlug.includes('warrior') || specSlug.includes('darkknight') || specSlug.includes('gunbreaker')) return 'tank';
            if (specSlug.includes('whitemage') || specSlug.includes('scholar') || specSlug.includes('astrologian') || specSlug.includes('sage')) return 'healer';
            return 'dps';
        };

        const getDetailedRole = (specSlug) => {
            const combinedConfig = getCombinedConfig(specSlug);
            if (combinedConfig) return combinedConfig.role;
            const group = SPECS.find(g => g.items.some(i => i.id === specSlug));
            if (!group) return 'dps';
            if (group.label === 'Tanks') return 'tank';
            if (group.label === 'Healers') return 'healer';
            if (group.label === 'Melee') return 'melee';
            if (group.label === 'Physical Ranged') return 'phys_ranged';
            if (group.label === 'Magical Ranged') return 'magic_ranged';
            return 'dps';
        };

        const supportsBuddy = (specSlug) => {
            const role = getRole(specSlug);
            return role === 'tank' || role === 'healer' || specSlug === 'dancer-dancer';
        };

        const getAllPlayableSpecs = () => SPECS.flatMap(group => group.items).filter(spec => !spec.combined);

        const getSpecsForDetailedRole = (role) => {
            const groupLabel = role === 'tank' ? 'Tanks' : role === 'healer' ? 'Healers' : '';
            const group = SPECS.find(g => g.label === groupLabel);
            return group ? group.items.filter(spec => !spec.combined) : [];
        };

        const getBuddySpecOptions = (specSlug) => {
            const role = getRole(specSlug);
            if (!supportsBuddy(specSlug)) return [];
            if (specSlug === 'dancer-dancer') return [];
            return getSpecsForDetailedRole(role).filter(spec => spec.id !== specSlug);
        };

        const getCombinedSpecOptions = (specSlug) => {
            const config = getCombinedConfig(specSlug);
            if (!config) return [];
            return config.specs.map(getSpecInfo);
        };

        const findBuddyPlayer = (player, fightPlayers, specSlug) => {
            if (!supportsBuddy(specSlug)) return null;
            if (specSlug === 'dancer-dancer') return null;
            const role = getRole(specSlug);
            const playerSourceId = Number(player.source_id || 0);
            const candidates = (fightPlayers || []).filter(candidate => (
                getRole(candidate.spec_slug) === role
                && Number(candidate.source_id || 0) !== playerSourceId
            ));
            return candidates.find(candidate => candidate.casts && candidate.casts.length) || candidates[0] || null;
        };

        const getFFLogsUrl = (reportId, fightId, region) => {
            const baseUrl = (region === "CN") ? "https://cn.fflogs.com" : "https://www.fflogs.com";
            return `${baseUrl}/reports/${reportId}#fight=${fightId}`;
        };

        // 2. fetchRankings (API with Region & Partner Logic)
        const fetchRankings = async (specSlug, bossSlug, spellMap, regionFilter = 'All') => {

            const BUFF_SPECS = new Set([
                'astrologian-astrologian', 'scholar-scholar',
                'dragoon-dragoon', 'reaper-reaper', 'monk-monk', 'ninja-ninja',
                'dancer-dancer', 'bard-bard', 
                'redmage-redmage', 'summoner-summoner', 'pictomancer-pictomancer'
            ]);

            try {
                const combinedConfig = getCombinedConfig(specSlug);
                const dataSpecSlugs = combinedConfig ? combinedConfig.specs : [specSlug];
                const dataSets = (await Promise.all(dataSpecSlugs.map(async dataSpecSlug => {
                    const fileName = `spec_ranking_${dataSpecSlug}_${bossSlug}.json`;
                    const url = `./data/${fileName}`;
                    const res = await fetch(url);
                    if (!res.ok) {
                        if (combinedConfig) {
                            console.warn(`[M-Spec] Combined source missing: ${url}`);
                            return null;
                        }
                        throw new Error(`Ranking file not found: ${url}`);
                    }
                    return res.json();
                }))).filter(Boolean);

                if (!dataSets.length) throw new Error(`Ranking files not found: ${bossSlug}`);
                
                const allPlayers = [];
                const playersByFight = new Map();
                const addFightPlayers = (fightKey, fightPlayers) => {
                    const existingPlayers = playersByFight.get(fightKey) || [];
                    const playerMap = new Map(existingPlayers.map(player => [
                        `${player.source_id}-${player.spec_slug}-${player.name}`,
                        player
                    ]));
                    fightPlayers.forEach(player => {
                        const key = `${player.source_id}-${player.spec_slug}-${player.name}`;
                        const existing = playerMap.get(key);
                        if (!existing || (player.casts || []).length > (existing.casts || []).length) {
                            playerMap.set(key, player);
                        }
                    });
                    playersByFight.set(fightKey, [...playerMap.values()]);
                };
                dataSets.forEach(data => {
                    if (data.reports) {
                        data.reports.forEach(report => {
                            if (report.fights) {
                                report.fights.forEach(fight => {
                                    const fightKey = `${report.report_id}-${fight.fight_id}`;
                                    const fightPlayers = (fight.players || []).map(player => ({
                                        ...player,
                                        fightDuration: fight.duration,
                                        fightId: fight.fight_id,
                                        reportId: report.report_id,
                                        region: report.region,
                                        composition: fight.composition || [],
                                        phases: fight.phases || [],
                                        fightKey
                                    }));
                                    addFightPlayers(fightKey, fightPlayers);
                                    allPlayers.push(...fightPlayers);
                                });
                            }
                        });
                    }
                });
                const normalizeCasts = (casts, durationSpellMap = {}, ownerSpecSlug = "", ownerName = "") => (casts || []).map(c => ({
                    spellId: c.spell_id,
                    timestamp: c.ts ? c.ts / 1000 : (c.timestamp || 0),
                    duration: c.duration || (durationSpellMap[c.spell_id] ? durationSpellMap[c.spell_id].duration : 0),
                    specSlug: ownerSpecSlug,
                    ownerName,
                    isLimitBreak: isLimitBreakSpellId(c.spell_id)
                }));

                if (combinedConfig) {
                    let combinedRows = [];
                    playersByFight.forEach((fightPlayers, fightKey) => {
                        const rolePlayers = fightPlayers
                            .filter(player => getRole(player.spec_slug) === combinedConfig.role && player.total > 0)
                            .sort((a, b) => b.total - a.total);

                        if (rolePlayers.length < 2) return;
                        const firstPlayer = rolePlayers[0];
                        if (regionFilter && regionFilter !== 'All' && firstPlayer.region !== regionFilter) return;

                        const durationSeconds = firstPlayer.fightDuration / 1000;
                        const m = Math.floor(durationSeconds / 60);
                        const s = Math.floor(durationSeconds % 60).toString().padStart(2, '0');
                        const combinedPlayers = rolePlayers.slice(0, 2);
                        const secondPlayer = combinedPlayers[1];
                        const total = combinedPlayers.reduce((sum, player) => sum + (player.total || 0), 0);
                        const buffCount = (firstPlayer.composition || []).filter(s => BUFF_SPECS.has(s)).length;

                        combinedRows.push({
                            rank: 0,
                            id: `${specSlug}-${fightKey}`,
                            name: combinedPlayers.map(player => player.name).join(' + '),
                            region: firstPlayer.region || '??',
                            reportId: firstPlayer.reportId,
                            fightId: firstPlayer.fightId,
                            partner: null,
                            buffCount,
                            composition: firstPlayer.composition,
                            dps: total,
                            killTime: `${m}:${s}`,
                            killTimeSeconds: durationSeconds,
                            phases: (firstPlayer.phases || []).map(p => ({
                                name: p.name || "Phase",
                                timestamp: p.time !== undefined ? p.time : ((p.ts || 0) / 1000),
                                ts: p.ts || 0,
                                mrt: p.mrt || ""
                            })),
                            casts: normalizeCasts(firstPlayer.casts, {}, firstPlayer.spec_slug, firstPlayer.name),
                            combinedPlayers: combinedPlayers.map(player => ({
                                sourceId: player.source_id,
                                name: player.name,
                                specSlug: player.spec_slug,
                                dps: player.total || 0
                            })),
                            buddy: {
                                sourceId: secondPlayer.source_id,
                                name: secondPlayer.name,
                                classSlug: secondPlayer.class_slug,
                                specSlug: secondPlayer.spec_slug,
                                icon: getIconForSpec(secondPlayer.spec_slug),
                                dps: secondPlayer.total || 0,
                                region: secondPlayer.region || firstPlayer.region || '??',
                                casts: normalizeCasts(secondPlayer.casts, {}, secondPlayer.spec_slug, secondPlayer.name),
                                deaths: secondPlayer.deaths || []
                            },
                            deaths: combinedPlayers.flatMap(player => player.deaths || []),
                            isCombined: true
                        });
                    });

                    combinedRows.sort((a, b) => b.dps - a.dps);
                    return combinedRows.slice(0, 100).map((row, index) => ({ ...row, rank: index + 1 }));
                }

                let filteredPlayers = allPlayers.filter(p => p.spec_slug === specSlug && p.total > 0);
                
                if (regionFilter && regionFilter !== 'All') {
                    filteredPlayers = filteredPlayers.filter(p => p.region === regionFilter);
                }

                filteredPlayers.sort((a, b) => b.total - a.total);

                const rankedPlayers = filteredPlayers.slice(0, 100);

                const rankData = rankedPlayers.map((player, index) => {
                        const id = `${player.reportId}-${player.fightId}-${player.source_id}`;
                        
                        const buffCount = (player.composition || []).filter(s => BUFF_SPECS.has(s)).length;

                        let partnerIcon = null;
                        const myDetailedRole = getDetailedRole(specSlug);
                        const fightPlayers = playersByFight.get(player.fightKey) || [];
                        const buddyPlayer = findBuddyPlayer(player, fightPlayers, specSlug);
                        const makeBuddy = (buddySource, buddyMeta = {}) => ({
                            sourceId: buddySource.source_id,
                            name: buddySource.name,
                            classSlug: buddySource.class_slug,
                            specSlug: buddySource.spec_slug,
                            icon: getIconForSpec(buddySource.spec_slug),
                            dps: buddySource.total || 0,
                            region: player.region || '??',
                            casts: normalizeCasts(buddySource.casts, {}, buddySource.spec_slug, buddySource.name),
                            deaths: buddySource.deaths || [],
                            dancePartner: buddyMeta
                        });
                        const dancePartnerBuddies = specSlug === 'dancer-dancer'
                            ? (player.dance_partners || [])
                                .map(partnerInfo => {
                                    const sourceId = Number(partnerInfo.source_id || 0);
                                    const partner = fightPlayers.find(candidate => Number(candidate.source_id || 0) === sourceId);
                                    return partner ? makeBuddy(partner, partnerInfo) : null;
                                })
                                .filter(Boolean)
                            : [];

                        if (dancePartnerBuddies.length) {
                            const iconName = getIconForSpec(dancePartnerBuddies[0].specSlug);
                            if (iconName) {
                                partnerIcon = `./images/classes/${iconName}`;
                            }
                        } else if (buddyPlayer) {
                            const iconName = getIconForSpec(buddyPlayer.spec_slug);
                            if (iconName) {
                                partnerIcon = `./images/classes/${iconName}`;
                            }
                        } else if (player.composition && Array.isArray(player.composition)) {
                            const roleMates = player.composition.filter(s => getDetailedRole(s) === myDetailedRole);
                            let partnerSpec = roleMates.find(s => s !== specSlug);

                            if (['tank', 'healer'].includes(myDetailedRole)) {
                                if (!partnerSpec && roleMates.length >= 2) {
                                    partnerSpec = specSlug;
                                }
                            }

                            if (partnerSpec) {
                                const iconName = getIconForSpec(partnerSpec);
                                if (iconName) {
                                    partnerIcon = `./images/classes/${iconName}`;
                                }
                            }
                        }

                        const durationSeconds = player.fightDuration / 1000;
                        const m = Math.floor(durationSeconds / 60);
                        const s = Math.floor(durationSeconds % 60).toString().padStart(2, '0');
                        return {
                        rank: index + 1,
                        id: id,
                        name: player.name,
                        region: player.region || '??',
                        reportId: player.reportId,
                        fightId: player.fightId,
                        partner: partnerIcon,
                        buffCount: buffCount,
                        composition: player.composition,
                        dps: player.total,
                        killTime: `${m}:${s}`,
                        killTimeSeconds: durationSeconds,
                        phases: (player.phases || []).map(p => ({
                            name: p.name || "Phase",
                            timestamp: p.time !== undefined ? p.time : ((p.ts || 0) / 1000),
                            ts: p.ts || 0,
                            mrt: p.mrt || ""
                        })),
                        casts: normalizeCasts(player.casts, spellMap),
                        buddy: dancePartnerBuddies[0] || (buddyPlayer ? makeBuddy(buddyPlayer) : null),
                        buddies: dancePartnerBuddies.length ? dancePartnerBuddies : (buddyPlayer ? [makeBuddy(buddyPlayer)] : []),
                        deaths: player.deaths || [] 
                    };
                });
                return rankData;

            } catch (error) {
                console.error('[M-Spec] 读取排名数据失败:', error);
                return [];
            }
        };

        const parseTime = (timeStr) => {
            if (!timeStr) return 0;
            const parts = timeStr.split(':');
            if (parts.length === 2) {
                return parseInt(parts[0]) * 60 + parseInt(parts[1]);
            }
            return parseInt(timeStr);
        };

        const fetchBossMechanics = async (bossSlug) => {
            if (!bossSlug) return [];

            const fileMapping = {
                'vamp-fatale': 'm9s',
                'red-hot-and-deep-blue': 'm10s',
                'the-tyrant': 'm11s',
                'lindwurm': 'm12s_p1',
                'lindwurm-ii': 'm12s_p2',
                'futures-rewritten': 'futures_rewritten',
                'dancing-mad': 'dancing_mad',
                'the-unending-coil-of-bahamut': 'the_unending_coil_of_bahamut',
                'the-weapons-refrain': 'the_weapons_refrain',
                'the-epic-of-alexander': 'the_epic_of_alexander',
                'dragonsongs-reprise': 'dragonsongs_reprise',
                'the-omega-protocol': 'the_omega_protocol'
            };

            const fileName = fileMapping[bossSlug] || bossSlug;

            try {
                const url = `./data/${fileName}.json`;

                const res = await fetch(url);
                if (!res.ok) throw new Error(`Boss 文件 ${fileName}.json 未找到`);
                
                const data = await res.json();
                
                const list = Array.isArray(data) ? data : Object.values(data);

                return list.map(spell => {
                    const type = normalizeBossTimelineType(spell.type);
                    const isTimelineMarker = type !== "phase" && type !== "window";
                    return {
                        id: spell.id || spell.spell_id,
                        name: spell.name || 'Unknown',
                        time: (spell.time > 10000) ? (spell.time / 1000) : (spell.time || spell.timestamp || 0),
                        duration: spell.duration || (isTimelineMarker ? 1 : 0),
                        color: getBossTimelineColor(type, spell.color),
                        icon: spell.icon ? `./images/spells/${spell.icon}` : null,
                        name_i18n: spell.name_i18n || {},
                        actionId: spell.action_id || spell.actionId || null,
                        phaseIndex: spell.phase_index === null || spell.phase_index === undefined ? null : Number(spell.phase_index),
                        phaseTime: spell.phase_time === null || spell.phase_time === undefined ? null : Number(spell.phase_time),
                        phaseName: spell.phase_name || spell.phaseName || "",
                        type
                    };
                }).sort((a, b) => a.time - b.time);

            } catch (e) {
                console.warn(`[离线模式] 无法加载 ${fileName}，Boss 轴将隐藏。`, e);
                return []; 
            }
        };
        
        const calculateCastTracks = (casts) => {
            if (!casts || casts.length === 0) return { tracks: [], maxTracks: 1 };
            const sortedCasts = [...casts].sort((a, b) => a.timestamp - b.timestamp);

            const tracks = [];
            const results = [];

            sortedCasts.forEach(cast => {
                const castEnd = cast.timestamp + Math.max(cast.duration || 0, 5) + 2; 
                let placed = false;
                for (let i = 0; i < tracks.length; i++) {
                    if (tracks[i] <= cast.timestamp) {
                        tracks[i] = castEnd;
                        results.push({ ...cast, trackIndex: i });
                        placed = true;
                        break;
                    }
                }
                if (!placed) {
                    results.push({ ...cast, trackIndex: tracks.length });
                    tracks.push(castEnd);
                }
            });

            return { processedCasts: results, maxTracks: Math.max(1, tracks.length) };
        };

        // --- Components ---
        const CategoryIcon = ({ type }) => {
            switch(type) {
                case 'swords': return <Swords size={14} />;
                case 'shield': return <Shield size={14} />;
                case 'shieldAlert': return <ShieldAlert size={14} />;
                case 'zap': return <Zap size={14} />;
                default: return <MoreHorizontal size={14} />;
            }
        };

        const RenderIcon = ({ spell, className }) => {
            const imgUrl = spell.image || spell.icon;
            // loading="lazy": 时间轴横向很长, 视口外成千上万的图标不必立刻请求 (886 个图标一次全拉会拖垮加载)
            if (imgUrl) return <img src={imgUrl} alt={spell.name} draggable={false} loading="lazy" decoding="async" className={`w-full h-full object-cover ${className}`} />;
            return <div className={`flex items-center justify-center w-full h-full text-sm select-none bg-gray-700 ${className}`}>{spell.char || (spell.name ? spell.name[0] : '?')}</div>;
        };

        const PlayerNameCell = ({ name, dps, reportId, fightId, region }) => {
            const [viewMode, setViewMode] = useState('dps');
            const timeoutRef = useRef(null);

            // 卸载时清掉挂起的定时器, 避免对已卸载组件 setState
            useEffect(() => () => {
                if (timeoutRef.current) clearTimeout(timeoutRef.current);
            }, []);

            const handleMouseEnter = () => {
                if (timeoutRef.current) clearTimeout(timeoutRef.current);
                setViewMode('name');
            };

            const handleMouseLeave = () => {
                timeoutRef.current = setTimeout(() => {
                    setViewMode('dps');
                }, 5000); 
            };

            const url = getFFLogsUrl(reportId, fightId, region);

            return (
                <a 
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 relative h-full flex items-center pr-2 cursor-pointer group/link hover:bg-white/5 transition-colors rounded"
                    onMouseEnter={handleMouseEnter}
                    onMouseLeave={handleMouseLeave}
                    title="Open in FF Logs"
                    onClick={(e) => e.stopPropagation()} 
                >
                    <span 
                        className={`absolute inset-0 flex items-center font-bold text-[#00FF96] drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)] transition-opacity duration-500 ${viewMode === 'dps' ? 'opacity-100' : 'opacity-0'}`}
                        style={{ fontSize: '19px', lineHeight: 1 }}
                    >
                        {Math.round(dps).toLocaleString()}
                    </span>
                    
                    <span 
                        className={`absolute inset-0 flex items-center font-bold text-white truncate transition-opacity duration-500 underline decoration-gray-500 group-hover/link:decoration-[#00FF96] drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)] ${viewMode === 'name' ? 'opacity-100' : 'opacity-0'}`}
                        style={{ fontSize: '15px' }}
                    >
                        {name}
                        <ExternalLink size={12} className="ml-1 opacity-50 group-hover/link:opacity-100" />
                    </span>
                </a>
            );
        };

        const BuddyNameCell = ({ name, dps }) => {
            const [isHovering, setIsHovering] = useState(false);

            return (
                <div
                    className="flex-1 w-full min-w-0 min-h-[24px] self-stretch relative flex items-center pr-2 cursor-default"
                    onMouseEnter={() => setIsHovering(true)}
                    onMouseOver={() => setIsHovering(true)}
                    onPointerEnter={() => setIsHovering(true)}
                    onMouseLeave={() => setIsHovering(false)}
                    onPointerLeave={() => setIsHovering(false)}
                    title={name}
                >
                    <span
                        className={`absolute inset-0 flex items-center font-bold text-[#00FF96] drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)] transition-opacity duration-150 ${isHovering ? 'opacity-0' : 'opacity-100'}`}
                        style={{ fontSize: '17px', lineHeight: 1 }}
                    >
                        {Math.round(dps).toLocaleString()}
                    </span>
                    <span
                        className={`absolute inset-0 flex items-center font-bold text-gray-300 truncate transition-opacity duration-150 drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)] ${isHovering ? 'opacity-100' : 'opacity-0'}`}
                        style={{ fontSize: '13px' }}
                    >
                        {name}
                    </span>
                </div>
            );
        };

        const KillTimeFilter = ({ filterRange, onApply, t }) => {
            const [isOpen, setIsOpen] = useState(false);
            const ref = useRef(null);

            const [minM, setMinM] = useState('');
            const [minS, setMinS] = useState('');
            const [maxM, setMaxM] = useState('');
            const [maxS, setMaxS] = useState('');

            const formatDisplay = () => {
                if (filterRange.min === 0 && filterRange.max >= 9999) return t("killTime");
                const formatTime = (totalSec) => {
                    if (totalSec >= 9999) return "Max";
                    const m = Math.floor(totalSec / 60);
                    const s = totalSec % 60;
                    return `${m}:${s.toString().padStart(2, '0')}`;
                };
                return `${formatTime(filterRange.min)} - ${formatTime(filterRange.max)}`;
            };

            useEffect(() => {
                if (isOpen) {
                    const hasMin = filterRange.min > 0;
                    const hasMax = filterRange.max < 9999;
                    setMinM(hasMin ? Math.floor(filterRange.min / 60).toString() : '');
                    setMinS(hasMin ? (filterRange.min % 60).toString() : '');
                    setMaxM(hasMax ? Math.floor(filterRange.max / 60).toString() : '');
                    setMaxS(hasMax ? (filterRange.max % 60).toString() : '');
                }
            }, [isOpen, filterRange]);

            useEffect(() => {
                const handleClickOutside = (event) => {
                    if (ref.current && !ref.current.contains(event.target)) setIsOpen(false);
                };
                document.addEventListener('mousedown', handleClickOutside);
                return () => document.removeEventListener('mousedown', handleClickOutside);
            }, []);

            const handleApply = () => {
                const minSeconds = (parseInt(minM || 0) * 60) + parseInt(minS || 0);
                let maxSeconds = 99999;
                if (maxM !== '' || maxS !== '') {
                    maxSeconds = (parseInt(maxM || 0) * 60) + parseInt(maxS || 0);
                }
                
                if (minSeconds > maxSeconds && maxSeconds !== 99999) {
                     onApply({ min: maxSeconds, max: minSeconds });
                } else {
                     onApply({ min: minSeconds, max: maxSeconds });
                }
                setIsOpen(false);
            };

            const handleReset = () => {
                onApply({ min: 0, max: 99999 });
                setIsOpen(false);
            }

            const inputClass = "w-12 bg-[#252525] border border-gray-700 rounded p-1 text-center text-white text-sm focus:border-[#00FF96] focus:outline-none";

            return (
                <div className="relative" ref={ref}>
                    <button
                        onClick={() => setIsOpen(!isOpen)}
                        className={`flex h-7 items-center gap-1.5 px-2 border rounded text-xs transition-colors ${ (filterRange.min > 0 || filterRange.max < 9999) ? 'bg-[#00FF96]/20 border-[#00FF96] text-white' : 'bg-black/30 border-gray-700/80 text-gray-400 hover:border-[#00FF96]'}`}
                    >
                        <Timer size={13} />
                        <span>{formatDisplay()}</span>
                        <ChevronDown size={12} />
                    </button>

                    {isOpen && (
                        <div className="absolute top-full right-0 mt-2 w-64 rounded-md border border-gray-700 bg-[#151515] p-3 shadow-2xl z-[8000] flex flex-col gap-3">
                            <h3 className="text-xs font-bold text-gray-500 uppercase">{t("filterKillTime")}</h3>
                            
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-gray-300 w-10">{t("min")}</span>
                                <div className="flex items-center gap-1">
                                    <input type="number" placeholder="M" value={minM} onChange={(e) => setMinM(e.target.value)} className={inputClass} />
                                    <span className="text-gray-500">:</span>
                                    <input type="number" placeholder="S" value={minS} onChange={(e) => setMinS(e.target.value)} className={inputClass} />
                                </div>
                            </div>

                            <div className="flex items-center justify-between">
                                <span className="text-sm text-gray-300 w-10">{t("max")}</span>
                                <div className="flex items-center gap-1">
                                    <input type="number" placeholder="M" value={maxM} onChange={(e) => setMaxM(e.target.value)} className={inputClass} />
                                    <span className="text-gray-500">:</span>
                                    <input type="number" placeholder="S" value={maxS} onChange={(e) => setMaxS(e.target.value)} className={inputClass} />
                                </div>
                            </div>

                            <div className="flex items-center justify-between pt-2 border-t border-gray-700 mt-1">
                                <button onClick={handleReset} className="h-7 px-2.5 rounded border border-gray-700/80 text-[11px] font-bold uppercase tracking-wide text-gray-400 hover:border-gray-500 hover:text-gray-300 transition-colors">{t("reset")}</button>
                                <button onClick={handleApply} className="h-7 px-3 rounded bg-[#00FF96] text-[11px] font-bold uppercase tracking-wide text-black hover:bg-[#00cc78] transition-colors">{t("apply")}</button>
                            </div>
                        </div>
                    )}
                </div>
            );
        };

        const CompositionFilter = ({ activeFilterSpecs, onApply, t, uiLanguage }) => {
            const [isOpen, setIsOpen] = useState(false);
            const [tempSelected, setTempSelected] = useState(new Set(activeFilterSpecs));
            const ref = useRef(null);

            useEffect(() => {
                if (isOpen) setTempSelected(new Set(activeFilterSpecs));
            }, [isOpen, activeFilterSpecs]);

            useEffect(() => {
                const handleClickOutside = (event) => {
                    if (ref.current && !ref.current.contains(event.target)) setIsOpen(false);
                };
                document.addEventListener('mousedown', handleClickOutside);
                return () => document.removeEventListener('mousedown', handleClickOutside);
            }, []);

            const toggleSpec = (specId) => {
                const newSet = new Set(tempSelected);
                if (newSet.has(specId)) newSet.delete(specId); else newSet.add(specId);
                setTempSelected(newSet);
            };

            const handleApply = () => {
                onApply(tempSelected);
                setIsOpen(false);
            };

            return (
                <div className="relative" ref={ref}>
                    <button
                        onClick={() => setIsOpen(!isOpen)}
                        className={`flex h-7 items-center gap-1.5 px-2 border rounded text-xs transition-colors ${activeFilterSpecs.size > 0 ? 'bg-[#00FF96]/20 border-[#00FF96] text-white' : 'bg-black/30 border-gray-700/80 text-gray-400 hover:border-[#00FF96]'}`}
                    >
                        <span>{t("with")} {activeFilterSpecs.size > 0 && `(${activeFilterSpecs.size})`}</span>
                        <ChevronDown size={12} />
                    </button>

                    {isOpen && (
                        <div className="absolute top-full right-0 mt-2 w-80 rounded-md border border-gray-700 bg-[#151515] p-3 shadow-2xl z-[8000] flex flex-col gap-3 max-h-[500px] overflow-y-auto custom-scrollbar">
                            <div className="flex flex-col gap-4">
                                {SPECS.map((group, idx) => (
                                    <div key={idx} className="flex flex-col gap-2">
                                        <span className="text-[10px] uppercase text-gray-500 font-bold">{getSpecGroupLabel(group.label, t)}</span>
                                        <div className="flex flex-wrap gap-2">
                                            {group.items.filter(item => !item.combined).map(item => {
                                                const isSelected = tempSelected.has(item.id);
                                                const itemName = getLocalizedSpecName(item.id, uiLanguage);
                                                return (
                                                    <button
                                                        key={item.id}
                                                        onClick={() => toggleSpec(item.id)}
                                                        className={`w-9 h-9 flex items-center justify-center rounded border transition-all relative ${isSelected ? 'bg-[#333] border-[#00FF96]' : 'bg-[#252525] border-transparent hover:bg-[#333]'}`}
                                                        title={itemName}
                                                    >
                                                        <img src={`./images/classes/${item.icon}`} alt={itemName} draggable={false} className="w-full h-full object-cover rounded-sm" />
                                                        {isSelected && <div className="absolute inset-0 border-2 border-[#00FF96] rounded pointer-events-none"></div>}
                                                    </button>
                                                );
                                            })}
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <div className="flex items-center justify-between pt-2 border-t border-gray-700">
                                <button onClick={() => setIsOpen(false)} className="h-7 px-2.5 rounded border border-gray-700/80 text-[11px] font-bold uppercase tracking-wide text-gray-400 hover:border-gray-500 hover:text-gray-300 transition-colors">{t("cancel")}</button>
                                <button onClick={handleApply} className="h-7 px-3 rounded bg-[#00FF96] text-[11px] font-bold uppercase tracking-wide text-black hover:bg-[#00cc78] transition-colors">{t("confirm")}</button>
                            </div>
                        </div>
                    )}
                </div>
            );
        };

        const SpecSelector = ({ selectedSpec, onChange, t, uiLanguage }) => {
            const [isOpen, setIsOpen] = useState(false);
            const ref = useRef(null);

            const currentSpecItem = SPECS.flatMap(g => g.items).find(i => i.id === selectedSpec);
            const currentName = getLocalizedSpecName(selectedSpec, uiLanguage);
            const currentIsCombined = Boolean(currentSpecItem?.combined);

            const CombinedMark = ({ compact = false }) => (
                <span
                    className={`${compact ? 'h-full w-full text-[9px]' : 'h-5 min-w-[34px] px-1.5 text-[10px]'} flex items-center justify-center rounded-sm border border-[#00FF96]/70 bg-[#00FF96]/10 font-black font-mono uppercase tracking-wide text-[#00FF96]`}
                >
                    COM
                </span>
            );

            useEffect(() => {
                const handleClickOutside = (event) => {
                    if (ref.current && !ref.current.contains(event.target)) setIsOpen(false);
                };
                document.addEventListener('mousedown', handleClickOutside);
                return () => document.removeEventListener('mousedown', handleClickOutside);
            }, []);

            return (
                <div className="relative" ref={ref}>
                    <button
                        onClick={() => setIsOpen(!isOpen)}
                        className="flex h-7 items-center gap-1.5 px-2 bg-[#101010] border border-gray-700/80 rounded text-xs hover:border-[#00FF96]/70 transition-colors"
                    >
                        {currentIsCombined ? (
                            <CombinedMark />
                        ) : (
                            <img src={`./images/classes/${currentSpecItem?.icon || 'Red_Mage.png'}`} alt={currentName} draggable={false} className="w-4 h-4 object-contain" />
                        )}
                        <span className="font-medium text-white">{currentName}</span>
                        <ChevronDown size={12} className="text-gray-500" />
                    </button>

                    {isOpen && (
                        <div className="absolute top-full left-0 mt-2 w-64 rounded-md border border-gray-700 bg-[#151515] p-2 shadow-2xl z-[8000] flex flex-col gap-2 max-h-[400px] overflow-y-auto custom-scrollbar">
                            {SPECS.map((group, idx) => (
                                <div key={idx} className="flex flex-col gap-1">
                                    <span className="text-[10px] uppercase text-gray-500 font-bold px-1">{getSpecGroupLabel(group.label, t)}</span>
                                    <div className="flex flex-wrap gap-1">
                                        {group.items.map(item => {
                                            const itemName = getLocalizedSpecName(item.id, uiLanguage);
                                            return (
                                                <button 
                                                    key={item.id}
                                                    onClick={() => { onChange(item.id); setIsOpen(false); }}
                                                    className={`w-8 h-8 flex items-center justify-center rounded border transition-all overflow-hidden ${selectedSpec === item.id ? 'bg-[#333] border-[#00FF96]' : 'bg-[#252525] border-transparent hover:bg-[#333] hover:border-[#00FF96]'}`}
                                                    title={itemName}
                                                >
                                                    {item.combined ? (
                                                        <CombinedMark compact />
                                                    ) : (
                                                        <img src={`./images/classes/${item.icon}`} alt={itemName} draggable={false} className="w-full h-full object-cover" />
                                                    )}
                                                </button>
                                            );
                                        })}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            );
        };

        // --- Main App ---
        const App = () => {
            const getQueryParam = (param, defaultValue) => {
                const urlParams = new URLSearchParams(window.location.search);
                return urlParams.get(param) || defaultValue;
            };
            const initialBossSlug = getQueryParam('boss', 'vamp-fatale');
            const initialSpecSlug = getQueryParam('spec', 'redmage-redmage');
            const initialImportedLogState = readStoredImportedLogs(initialBossSlug);
            const [uiLanguage, setUiLanguage] = useState(getInitialUiLanguage);
            const t = useCallback((key) => translate(uiLanguage, key), [uiLanguage]);
            const currentLanguage = UI_LANGUAGES.find(lang => lang.id === uiLanguage) || UI_LANGUAGES[0];

            const [zoom, setZoom] = useState(getInitialZoom);
            // 横向虚拟化的触发器: 值本身只用来让 React 在滚过一个 chunk 时重渲染,
            // 真正的可见窗口每次渲染时从当前 scrollLeft 现算 (见 cullT0/cullT1)
            const [scrollCullChunk, setScrollCullChunk] = useState(0);
            const handleTimelineScroll = useCallback((e) => {
                const sc = e.currentTarget;
                // 内容整体都在"视口+两侧余量"内时 (低缩放, 例如一屏看 8 分钟),
                // 裁剪窗口永远覆盖全场 —— 此时绝不能触发补渲染, 否则拖动中
                // 每滚 1200px 就会白白全量重渲染一次, 反而更卡。
                if (sc.scrollWidth <= sc.clientWidth + 2 * SCROLL_CULL_MARGIN_PX) return;
                const chunk = Math.round(sc.scrollLeft / SCROLL_CULL_CHUNK_PX);
                // startTransition: 补渲染是低优先级的, 不阻塞拖动本身的滚动帧
                React.startTransition(() => {
                    setScrollCullChunk(prev => (prev === chunk ? prev : chunk));
                });
            }, []);
            // 视口尺寸变化时强制一次补渲染 (裁剪窗口是现算的, chunk 只是触发器)
            useEffect(() => {
                const onResize = () => setScrollCullChunk(c => c + 1);
                window.addEventListener('resize', onResize);
                return () => window.removeEventListener('resize', onResize);
            }, []);
            const [isCollapsed, setIsCollapsed] = useState(true); 
            const [leftPanelCollapsed, setLeftPanelCollapsed] = useState(() => (window.innerWidth || 1280) < 720);
            // 移动端: 控制栏在 375px 宽的屏幕上要吃掉 376px 高度 (近半个屏幕),
            // 所以窄屏下默认收起, 只留一行"控制 + 折叠 + 缩放", 把屏幕让给时间轴
            const [isMobile, setIsMobile] = useState(() => (window.innerWidth || 1280) < 768);
            const [controlsOpen, setControlsOpen] = useState(false);
            useEffect(() => {
                const mq = window.matchMedia('(max-width: 767px)');
                const onChange = (e) => setIsMobile(e.matches);
                setIsMobile(mq.matches);
                if (mq.addEventListener) {
                    mq.addEventListener('change', onChange);
                    return () => mq.removeEventListener('change', onChange);
                }
                mq.addListener(onChange); // Safari < 14
                return () => mq.removeListener(onChange);
            }, []);
            const controlsVisible = !isMobile || controlsOpen;
            const leftPanelWidth = leftPanelCollapsed ? LEFT_PANEL_COLLAPSED_WIDTH : LEFT_PANEL_WIDTH;
            
            // NEW: Highlighted Row State (MULTI-SELECT)
            const [selectedRowIds, setSelectedRowIds] = useState(new Set());
            const [focusedSpellId, setFocusedSpellId] = useState(null);
            // NEW: Separated Curated List State
            const [curatedRowIds, setCuratedRowIds] = useState(new Set());

            // NEW FEATURE: Curation Mode States
            const [isSelectionMode, setIsSelectionMode] = useState(false);
            const [isCurated, setIsCurated] = useState(false);

            const [selectedBoss, setSelectedBoss] = useState(initialBossSlug);
            const [selectedSpec, setSelectedSpec] = useState(initialSpecSlug);
            
            const [selectedRegion, setSelectedRegion] = useState('All');

            const [activeFilterSpecs, setActiveFilterSpecs] = useState(new Set()); 
            const [killTimeRange, setKillTimeRange] = useState({ min: 0, max: 99999 });

            const [spellCategories, setSpellCategories] = useState({});
            const [spells, setSpells] = useState({});
            const [bossMechanics, setBossMechanics] = useState([]);
            const [rankData, setRankData] = useState([]);
            const [importedRows, setImportedRows] = useState(initialImportedLogState.rows);
            const [importedSpellSelections, setImportedSpellSelections] = useState(initialImportedLogState.selections);
            const [importSpellMenuRowId, setImportSpellMenuRowId] = useState(null);
            const [loading, setLoading] = useState(true);
            const [importModalOpen, setImportModalOpen] = useState(false);
            const [importUrl, setImportUrl] = useState("");
            const [importPlayers, setImportPlayers] = useState([]);
            const [importMeta, setImportMeta] = useState(null);
            const [importError, setImportError] = useState("");
            const [importLoading, setImportLoading] = useState(false);
            const [apiHelpOpen, setApiHelpOpen] = useState(false);
            const [userFflogsCredentials, setUserFflogsCredentials] = useState(readStoredUserFflogsCredentials);
            const [manualFflogsClientId, setManualFflogsClientId] = useState("");
            const [manualFflogsClientSecret, setManualFflogsClientSecret] = useState("");
            const [apiHelpError, setApiHelpError] = useState("");

            const [showDuration, setShowDuration] = useState(true);
            const [showCooldown, setShowCooldown] = useState(false);
            const [showSkillTimes, setShowSkillTimes] = useState(true);
            
            const [showPhases, setShowPhases] = useState(true);
            const [phaseAlignIndex, setPhaseAlignIndex] = useState(null);
            const [showBossRow, setShowBossRow] = useState(true);
            const [showLimitBreak, setShowLimitBreak] = useState(true);
            const [bossTimelineTypeVisibility, setBossTimelineTypeVisibility] = useState({
                mech: true,
                tb: true,
                aoe: true
            });
            const [showBuddy, setShowBuddy] = useState(getInitialBuddyVisibility);
            const [showDancerTangoBuddyWindow, setShowDancerTangoBuddyWindow] = useState(false);
            const [buddySpellMaps, setBuddySpellMaps] = useState({});
            const [buddySpellSelections, setBuddySpellSelections] = useState({});
            const [buddySpellMenuSpec, setBuddySpellMenuSpec] = useState(null);
            // 打开中的技能分类弹出面板 (null = 都关着); 取代原先仅 OTHERS 用的布尔开关
            const [openSpellMenuCat, setOpenSpellMenuCat] = useState(null);

            const [selectedSpells, setSelectedSpells] = useState(new Set());
            // 预展开的"可见技能 id"集合: 把逐 cast 的 isSpellSlotSelected 全表扫描
            // (O(casts x spells)) 换成一次 useMemo 展开 + O(1) 的 Set.has 查询
            const visibleSpellIdSet = useMemo(
                () => expandSelectedSpellSlots(selectedSpells, spells),
                [selectedSpells, spells]
            );
            const buddyVisibleSpellIdSets = useMemo(() => {
                const sets = {};
                for (const [slug, sel] of Object.entries(buddySpellSelections)) {
                    sets[slug] = expandSelectedSpellSlots(sel, buddySpellMaps[slug] || {});
                }
                return sets;
            }, [buddySpellSelections, buddySpellMaps]);
            const [timeRangeSelection, setTimeRangeSelection] = useState(null);
            const scrollContainerRef = useRef(null);
            const suppressRowClickRef = useRef(false);
            const buddyMenuRef = useRef(null);
            const otherMenuRef = useRef(null);
            const timeRangeSelectionRef = useRef(null);
            // 拖拽选区 overlay 的 DOM 引用: 拖动过程中直接改 style, 不走 React 重渲染
            const selectionOverlayRef = useRef(null);
            // 时间轴内容包裹层: 拖动期间对它整体禁用 pointer-events
            const timelineContentRef = useRef(null);

            useEffect(() => {
                try {
                    localStorage.setItem(UI_LANGUAGE_STORAGE_KEY, uiLanguage);
                } catch (e) {}
                document.documentElement.lang = uiLanguage;
            }, [uiLanguage]);

            useEffect(() => {
                writeBuddyVisibility(showBuddy);
            }, [showBuddy]);

            useEffect(() => {
                if (selectedSpec !== 'dancer-dancer') {
                    setShowDancerTangoBuddyWindow(false);
                }
            }, [selectedSpec]);

            useEffect(() => {
                const stored = readStoredImportedLogs(selectedBoss);
                setImportedRows(stored.rows);
                setImportedSpellSelections(stored.selections);
                setImportSpellMenuRowId(null);
            }, [selectedBoss]);

            const cycleUiLanguage = useCallback(() => {
                setUiLanguage(prev => {
                    const currentIndex = UI_LANGUAGES.findIndex(lang => lang.id === prev);
                    return UI_LANGUAGES[(currentIndex + 1) % UI_LANGUAGES.length].id;
                });
            }, []);

            const spellColorMap = useMemo(() => {
                const map = {};
                let colorIdx = 0;
                const sortedSpellIds = Object.keys(spells).sort();

                sortedSpellIds.forEach(spellId => {
                    map[spellId] = DURATION_PALETTE[colorIdx % DURATION_PALETTE.length];
                    colorIdx++;
                });
                return map;
            }, [spells]);

            const spellsByCategory = useMemo(() => {
                const grouped = {};
                getDisplaySpells(spells)
                    .sort((a, b) => a.load_order - b.load_order)
                    .forEach(spell => {
                        const category = spell.category || "MAJOR";
                        if (!grouped[category]) grouped[category] = [];
                        grouped[category].push(spell);
                    });
                return grouped;
            }, [spells]);

            const isCombined = isCombinedSpec(selectedSpec);
            const dancerBuddySpecOptions = useMemo(() => {
                if (selectedSpec !== 'dancer-dancer') return [];
                const seen = new Set();
                rankData.forEach(row => {
                    (row.buddies || (row.buddy ? [row.buddy] : [])).forEach(buddy => {
                        if (buddy?.specSlug && buddy.specSlug !== selectedSpec) {
                            seen.add(buddy.specSlug);
                        }
                    });
                });
                return [...seen].map(getSpecInfo).filter(Boolean);
            }, [selectedSpec, rankData]);
            const buddySpecOptions = useMemo(
                () => {
                    if (isCombinedSpec(selectedSpec)) return getCombinedSpecOptions(selectedSpec);
                    if (selectedSpec === 'dancer-dancer') return dancerBuddySpecOptions;
                    return getBuddySpecOptions(selectedSpec);
                },
                [selectedSpec, dancerBuddySpecOptions]
            );
            const isBuddySupported = supportsBuddy(selectedSpec);
            const buddySpellColorMaps = useMemo(() => {
                const result = {};
                Object.entries(buddySpellMaps).forEach(([specSlug, spellMap]) => {
                    const map = {};
                    let colorIdx = 0;
                    Object.keys(spellMap || {}).sort().forEach(spellId => {
                        map[spellId] = DURATION_PALETTE[colorIdx % DURATION_PALETTE.length];
                        colorIdx++;
                    });
                    result[specSlug] = map;
                });
                return result;
            }, [buddySpellMaps]);

            const dragInfo = useRef({
                isDown: false,
                startX: 0,
                startY: 0,
                scrollLeft: 0,
                moved: false
            });
            const pendingIconPressRef = useRef(null);

            const setDraggingCursor = useCallback((isDragging) => {
                if (!scrollContainerRef.current) return;
                scrollContainerRef.current.style.cursor = isDragging ? 'grabbing' : '';
                // 注意: 不要在这里对内容区切换 pointer-events —— 它是继承属性,
                // 在几万节点的子树上切换会触发一次全树样式重算 (起手一帧卡顿),
                // hover 状态集体掉落/恢复还会造成闪烁。命中测试的成本由 canvas
                // 渲染路径解决 (canvas 本身 pointer-events:none, DOM 里没有 cast 节点)。
            }, []);

            useEffect(() => {
                const load = async () => {
                    setLoading(true);
                    // 除 fetchRankings 依赖主技能表外, 其余请求相互独立:
                    // 全部并发发出, 消除原先 3-4 轮串行 await 的网络瀑布
                    const combinedConfig = getCombinedConfig(selectedSpec);
                    const partySpecOptions = combinedConfig
                        ? getCombinedSpecOptions(selectedSpec)
                        : (selectedSpec === 'dancer-dancer'
                            ? getAllPlayableSpecs().filter(spec => spec.id !== selectedSpec)
                            : getBuddySpecOptions(selectedSpec));
                    const [cats, sps, mechs, buddyEntries] = await Promise.all([
                        fetchSpellCategories(),
                        combinedConfig ? Promise.resolve({}) : fetchSpellData(selectedSpec, selectedBoss),
                        fetchBossMechanics(selectedBoss),
                        Promise.all(
                            partySpecOptions.map(async spec => [spec.id, await fetchSpellData(spec.id, selectedBoss)])
                        )
                    ]);
                    const nextBuddySpellMaps = Object.fromEntries(buddyEntries);

                    const ranks = await fetchRankings(selectedSpec, selectedBoss, sps, selectedRegion);

                    setSpellCategories(cats);
                    setSpells(sps);
                    setBossMechanics(mechs);
                    setRankData(ranks);
                    setBuddySpellMaps(nextBuddySpellMaps);
                    setBuddySpellSelections(Object.fromEntries(
                        buddyEntries.map(([specSlug, spellMap]) => [
                            specSlug,
                            readStoredSpellSelection(specSlug, spellMap) || new Set(getDefaultSelectedSpellIds(spellMap, cats))
                        ])
                    ));
                    setBuddySpellMenuSpec(null);
                    setOpenSpellMenuCat(null);
                    if (!supportsBuddy(selectedSpec)) {
                        setBuddySpellMenuSpec(null);
                    }
                    
                    const storedSelectedIds = readStoredSpellSelection(selectedSpec, sps);
                    const defaultSelectedIds = getDefaultSelectedSpellIds(sps, cats);
                    setSelectedSpells(storedSelectedIds !== null ? storedSelectedIds : new Set(defaultSelectedIds));

                    setLoading(false);
                };
                load();
            }, [selectedBoss, selectedSpec, selectedRegion]); 

            useEffect(() => {
                const handleClickOutside = (event) => {
                    if (buddyMenuRef.current && !buddyMenuRef.current.contains(event.target)) {
                        setBuddySpellMenuSpec(null);
                    }
                    if (otherMenuRef.current && !otherMenuRef.current.contains(event.target)) {
                        setOpenSpellMenuCat(null);
                    }
                };
                document.addEventListener('mousedown', handleClickOutside);
                return () => document.removeEventListener('mousedown', handleClickOutside);
            }, []);

            const focusedSpellGroups = useMemo(() => [
                new Set([30, 43, 3638, 16152]), // Tank invulnerabilities
                new Set([37013, 37016]), // Scholar Concitation / Accession
                RAID_BUFF_FOCUS_IDS
            ], []);
            const getFocusedSpellGroup = useCallback((spellId) => {
                const id = Number(spellId);
                return focusedSpellGroups.find(group => group.has(id)) || null;
            }, [focusedSpellGroups]);
            const isFocusedSpellId = useCallback((spellId) => {
                const id = Number(spellId);
                if (!focusedSpellId) return false;
                const focusedGroup = getFocusedSpellGroup(focusedSpellId);
                if (focusedGroup) {
                    return focusedGroup.has(id);
                }
                return Number(focusedSpellId) === id;
            }, [focusedSpellId, getFocusedSpellGroup]);
            const toggleFocusedSpell = useCallback((spellId) => {
                const id = Number(spellId);
                setFocusedSpellId(prev => {
                    const prevGroup = getFocusedSpellGroup(prev);
                    const nextGroup = getFocusedSpellGroup(id);
                    if (prevGroup && nextGroup && prevGroup === nextGroup) {
                        return null;
                    }
                    return Number(prev) === id ? null : id;
                });
            }, [getFocusedSpellGroup]);
            const handleSpellIconMouseDown = useCallback((e, spellId) => {
                if (e.button !== 0) return;
                e.preventDefault();

                const pressedElement = e.currentTarget;
                pendingIconPressRef.current = {
                    element: pressedElement,
                    spellId: Number(spellId),
                    startX: e.clientX,
                    startY: e.clientY
                };

                const handleIconMouseUp = (event) => {
                    window.removeEventListener('mouseup', handleIconMouseUp);

                    const pending = pendingIconPressRef.current;
                    pendingIconPressRef.current = null;
                    if (!pending || pending.element !== pressedElement) return;

                    const delta = Math.hypot(event.clientX - pending.startX, event.clientY - pending.startY);
                    const releaseTarget = document.elementFromPoint(event.clientX, event.clientY);
                    const releasedOnSameIcon = releaseTarget && pending.element.contains(releaseTarget);

                    if (delta < DRAG_THRESHOLD && !dragInfo.current.moved && releasedOnSameIcon) {
                        toggleFocusedSpell(pending.spellId);
                    }
                };

                window.addEventListener('mouseup', handleIconMouseUp);
            }, [toggleFocusedSpell]);

            const toggleSpell = (spellId) => {
                const spell = spells[spellId];
                if (!spell) return;
                const newSet = toggleSpellSlot(selectedSpells, spells, spell);
                writeStoredSpellSelection(selectedSpec, newSet, spells);
                setSelectedSpells(newSet);
            };

            const toggleCategory = (catKey) => {
                const spellsInCat = getDisplaySpells(spells).filter(s => s.category === catKey);
                const allSelected = spellsInCat.every(s => isSpellSlotSelected(spells, selectedSpells, s));
                const newSet = new Set(selectedSpells);
                spellsInCat.forEach(s => {
                    getSpellSlotIds(spells, s).forEach(id => {
                        if (allSelected) newSet.delete(id); else newSet.add(id);
                    });
                });
                writeStoredSpellSelection(selectedSpec, newSet, spells);
                setSelectedSpells(newSet);
            };

            // NEW: Global Toggle Logic
            const toggleAllSpells = () => {
                if (selectedSpells.size > 0) {
                    // Hide All
                    const newSet = new Set();
                    writeStoredSpellSelection(selectedSpec, newSet, spells);
                    setSelectedSpells(newSet);
                } else {
                    // Show All
                    const allIds = Object.values(spells).map(s => Number(s.id));
                    const newSet = new Set(allIds);
                    writeStoredSpellSelection(selectedSpec, newSet, spells);
                    setSelectedSpells(newSet);
                }
            };

            const toggleImportedSpell = (rowId, spellMap, spellId) => {
                setImportedSpellSelections(prev => {
                    const current = new Set(prev[rowId] || []);
                    const spell = spellMap?.[spellId] || spellMap?.[String(spellId)];
                    if (!spell) return prev;
                    const nextSelection = toggleSpellSlot(current, spellMap, spell);
                    const next = { ...prev, [rowId]: current };
                    next[rowId] = nextSelection;
                    writeStoredImportedLogs(selectedBoss, importedRows, next);
                    return next;
                });
            };

            const toggleImportedCategory = (rowId, spellMap, catKey) => {
                const spellsInCat = getDisplaySpells(spellMap).filter(s => s.category === catKey);
                setImportedSpellSelections(prev => {
                    const current = new Set(prev[rowId] || []);
                    const allSelected = spellsInCat.every(s => isSpellSlotSelected(spellMap, current, s));
                    spellsInCat.forEach(s => {
                        getSpellSlotIds(spellMap, s).forEach(id => {
                            if (allSelected) current.delete(id); else current.add(id);
                        });
                    });
                    const next = { ...prev, [rowId]: current };
                    writeStoredImportedLogs(selectedBoss, importedRows, next);
                    return next;
                });
            };

            const toggleAllImportedSpells = (rowId, spellMap) => {
                setImportedSpellSelections(prev => {
                    const current = new Set(prev[rowId] || []);
                    const allIds = Object.values(spellMap).map(s => Number(s.id));
                    const next = { ...prev, [rowId]: current.size > 0 ? new Set() : new Set(allIds) };
                    writeStoredImportedLogs(selectedBoss, importedRows, next);
                    return next;
                });
            };

            const toggleBuddySpell = (specSlug, spellId) => {
                setBuddySpellSelections(prev => {
                    const current = new Set(prev[specSlug] || []);
                    const spellMap = buddySpellMaps[specSlug] || {};
                    const spell = spellMap[spellId];
                    if (!spell) return prev;
                    const next = toggleSpellSlot(current, spellMap, spell);
                    writeStoredSpellSelection(specSlug, next, spellMap);
                    return { ...prev, [specSlug]: next };
                });
            };

            const toggleBuddyCategory = (specSlug, catKey) => {
                const spellMap = buddySpellMaps[specSlug] || {};
                const spellsInCat = getDisplaySpells(spellMap).filter(s => s.category === catKey);
                setBuddySpellSelections(prev => {
                    const current = new Set(prev[specSlug] || []);
                    const allSelected = spellsInCat.every(s => isSpellSlotSelected(spellMap, current, s));
                    spellsInCat.forEach(s => {
                        getSpellSlotIds(spellMap, s).forEach(id => {
                            if (allSelected) current.delete(id); else current.add(id);
                        });
                    });
                    writeStoredSpellSelection(specSlug, current, spellMap);
                    return { ...prev, [specSlug]: current };
                });
            };

            const toggleAllBuddySpells = (specSlug) => {
                const spellMap = buddySpellMaps[specSlug] || {};
                setBuddySpellSelections(prev => {
                    const current = new Set(prev[specSlug] || []);
                    const allIds = Object.values(spellMap).map(s => Number(s.id));
                    const next = current.size > 0 ? new Set() : new Set(allIds);
                    writeStoredSpellSelection(specSlug, next, spellMap);
                    return { ...prev, [specSlug]: next };
                });
            };

            const toggleBossTimelineType = (type) => {
                setBossTimelineTypeVisibility(prev => ({
                    ...prev,
                    [type]: !prev[type]
                }));
            };

            const saveManualFflogsToken = () => {
                const clientId = manualFflogsClientId.trim();
                const clientSecret = manualFflogsClientSecret.trim();
                if (!clientId || !clientSecret) {
                    setApiHelpError(t("missingFflogsToken"));
                    return;
                }
                writeStoredUserFflogsCredentials(clientId, clientSecret);
                setUserFflogsCredentials({ clientId, clientSecret });
                setManualFflogsClientId("");
                setManualFflogsClientSecret("");
                setApiHelpError("");
                setApiHelpOpen(false);
            };

            const clearUserFflogsToken = () => {
                writeStoredUserFflogsCredentials("", "");
                setUserFflogsCredentials({ clientId: "", clientSecret: "" });
                setManualFflogsClientId("");
                setManualFflogsClientSecret("");
                setApiHelpError("");
            };

            const postImportLog = async (path, payload) => {
                const headers = { "Content-Type": "application/json" };
                if (userFflogsCredentials.clientId && userFflogsCredentials.clientSecret) {
                    headers["X-MSpec-FFLogs-Client-ID"] = userFflogsCredentials.clientId;
                    headers["X-MSpec-FFLogs-Client-Secret"] = userFflogsCredentials.clientSecret;
                }
                const res = await fetch(`/api/import_log/${path}`, {
                    method: "POST",
                    headers,
                    body: JSON.stringify(payload)
                });
                if (!res.ok) {
                    const text = await res.text();
                    let message = text || `Import failed (${res.status})`;
                    try {
                        message = JSON.parse(text).detail || message;
                    } catch (e) {}
                    const error = new Error(message);
                    error.status = res.status;
                    throw error;
                }
                return res.json();
            };

            const getImportErrorMessage = (error) => {
                const message = error?.message || "";
                const normalizedMessage = message.toLowerCase();
                const usingUserCredentials = Boolean(userFflogsCredentials.clientId && userFflogsCredentials.clientSecret);
                if (usingUserCredentials && [401, 403, 500].includes(error?.status)) return t("invalidFflogsCredentials");
                if (usingUserCredentials && normalizedMessage.includes("internal server error")) return t("invalidFflogsCredentials");
                if (error?.status === 429 || message.includes("正在使用的玩家过多") || message.includes("IMPORT_LOG_RATE_LIMITED")) return t("importRateLimitError");
                if (normalizedMessage.includes("numeric fight query parameter")) return t("numericFightError");
                if (normalizedMessage.includes("could not find report id")) return t("missingReportIdError");
                if (normalizedMessage.includes("report not found")) return t("reportNotFoundError");
                if (normalizedMessage.includes("no permission")) return t("noReportPermissionError");
                if (normalizedMessage.includes("fight not found")) return t("fightNotFoundError");
                if (normalizedMessage.includes("player not found")) return t("playerNotFoundError");
                if (normalizedMessage.includes("internal server error")) return t("importGenericError");
                return message || t("importGenericError");
            };

            const handleLoadImportPlayers = async () => {
                setImportError("");
                setImportPlayers([]);
                setImportMeta(null);
                setImportLoading(true);
                try {
                    const cachedData = getCachedImportPlayers(selectedBoss, importUrl);
                    if (cachedData) {
                        setImportPlayers(cachedData.players || []);
                        setImportMeta(cachedData);
                        return;
                    }
                    const data = await postImportLog("players", { url: importUrl });
                    setImportPlayers(data.players || []);
                    setImportMeta(data);
                    writeStoredImportFightPlayers(selectedBoss, data);
                } catch (error) {
                    if (error.status === 429) setApiHelpOpen(true);
                    if ((userFflogsCredentials.clientId && userFflogsCredentials.clientSecret) && [401, 403, 500].includes(error.status)) {
                        const previousClientId = userFflogsCredentials.clientId;
                        setApiHelpOpen(true);
                        writeStoredUserFflogsCredentials("", "");
                        setUserFflogsCredentials({ clientId: "", clientSecret: "" });
                        setManualFflogsClientId(previousClientId);
                        setManualFflogsClientSecret("");
                    }
                    setImportError(getImportErrorMessage(error) || t("importGenericError"));
                } finally {
                    setImportLoading(false);
                }
            };

            const handleImportPlayer = async (player) => {
                setImportError("");
                setImportLoading(true);
                try {
                    const cachedRowId = importMeta?.report_id && importMeta?.fight_id
                        ? getImportedLogRowId(importMeta.report_id, importMeta.fight_id, player.source_id)
                        : null;
                    if (cachedRowId) {
                        const cache = readStoredImportedLogCache(selectedBoss);
                        const cachedRow = cache.rows.find(row => row.id === cachedRowId);
                        if (cachedRow) {
                            const cachedSelection = cache.selections[cachedRowId]
                                || new Set(getDefaultSelectedSpellIds(cachedRow.spells || {}, spellCategories));
                            const nextImportedRows = [cachedRow, ...importedRows.filter(row => row.id !== cachedRow.id)];
                            const nextImportedSelections = {
                                ...importedSpellSelections,
                                [cachedRow.id]: cachedSelection
                            };
                            setImportedRows(nextImportedRows);
                            setImportedSpellSelections(nextImportedSelections);
                            writeStoredImportedLogs(selectedBoss, nextImportedRows, nextImportedSelections, {
                                unhideRowIds: [cachedRow.id]
                            });
                            setImportModalOpen(false);
                            return;
                        }
                    }
                    const data = await postImportLog("casts", { url: importUrl, source_id: player.source_id });
                    const durationSeconds = (data.duration || 0) / 1000;
                    const specSpellMap = await fetchSpellData(data.player.spec_slug, selectedBoss);
                    const importedSpells = mergeSpellMaps(specSpellMap, data.spells || {});
                    const importedRow = {
                        id: getImportedLogRowId(data.report_id, data.fight_id, data.player.source_id),
                        name: data.player.name,
                        specSlug: data.player.spec_slug,
                        sourceId: data.player.source_id,
                        reportId: data.report_id,
                        fightId: data.fight_id,
                        title: data.title,
                        kill: data.kill,
                        percent: data.percent,
                        killTimeSeconds: durationSeconds,
                        killTime: formatTime(durationSeconds),
                        spells: importedSpells,
                        phases: (data.phases || []).map(p => ({
                            name: p.name || "Phase",
                            timestamp: p.time !== undefined ? p.time : ((p.ts || 0) / 1000)
                        })),
                        casts: (data.casts || []).map(c => {
                            const spell = isLimitBreakSpellId(c.spell_id) ? getLimitBreakSpell(c.spell_id) : (importedSpells[String(c.spell_id)] || {});
                            return {
                                spellId: c.spell_id,
                                timestamp: c.ts ? c.ts / 1000 : 0,
                                duration: c.duration || spell.duration || 0,
                                isLimitBreak: isLimitBreakSpellId(c.spell_id)
                            };
                        })
                    };
                    const nextImportedRows = [importedRow, ...importedRows.filter(row => row.id !== importedRow.id)];
                    const nextImportedSelections = {
                        ...importedSpellSelections,
                        [importedRow.id]: new Set(getDefaultSelectedSpellIds(importedSpells, spellCategories))
                    };
                    setImportedRows(nextImportedRows);
                    setImportedSpellSelections(nextImportedSelections);
                    writeStoredImportedLogs(selectedBoss, nextImportedRows, nextImportedSelections, {
                        unhideRowIds: [importedRow.id]
                    });
                    setImportModalOpen(false);
                } catch (error) {
                    if (error.status === 429) setApiHelpOpen(true);
                    if ((userFflogsCredentials.clientId && userFflogsCredentials.clientSecret) && [401, 403, 500].includes(error.status)) {
                        const previousClientId = userFflogsCredentials.clientId;
                        setApiHelpOpen(true);
                        writeStoredUserFflogsCredentials("", "");
                        setUserFflogsCredentials({ clientId: "", clientSecret: "" });
                        setManualFflogsClientId(previousClientId);
                        setManualFflogsClientSecret("");
                    }
                    setImportError(getImportErrorMessage(error) || t("importGenericError"));
                } finally {
                    setImportLoading(false);
                }
            };

            const getVisibleTimelineWidth = useCallback(() => (
                Math.max(240, (scrollContainerRef.current?.clientWidth || window.innerWidth) - leftPanelWidth - 12)
            ), [leftPanelWidth]);
            const clampVisibleMinutes = (minutes) => Math.max(
                MIN_VISIBLE_MINUTES,
                Math.min(MAX_VISIBLE_MINUTES, Number(minutes))
            );
            const getVisibleMinutesForZoom = (value) => getVisibleTimelineWidth() / (Number(value) * 60);
            const getZoomForVisibleMinutes = (minutes) => getVisibleTimelineWidth() / (clampVisibleMinutes(minutes) * 60);
            const clampZoom = (value) => {
                const minZoom = getZoomForVisibleMinutes(MAX_VISIBLE_MINUTES);
                const maxZoom = getZoomForVisibleMinutes(MIN_VISIBLE_MINUTES);
                return Math.max(minZoom, Math.min(maxZoom, Number(value)));
            };
            const setZoomAroundTime = useCallback((nextZoomValue, anchorTime = null) => {
                const nextZoom = clampZoom(nextZoomValue);
                const container = scrollContainerRef.current;
                const visibleWidth = getVisibleTimelineWidth();
                const oldZoom = Number(zoom) || nextZoom;
                const centerTime = anchorTime !== null && Number.isFinite(anchorTime)
                    ? anchorTime
                    : ((container?.scrollLeft || 0) + visibleWidth / 2) / oldZoom;

                setZoom(nextZoom);
                window.requestAnimationFrame(() => {
                    if (!container) return;
                    const nextScrollLeft = Math.max(0, centerTime * nextZoom - visibleWidth / 2);
                    container.scrollLeft = nextScrollLeft;
                    // 大跳转后立刻 (高优先级) 同步裁剪窗口, 避免短暂空白
                    setScrollCullChunk(Math.round(nextScrollLeft / SCROLL_CULL_CHUNK_PX));
                });
            }, [zoom, getVisibleTimelineWidth, clampZoom]);
            const adjustVisibleMinutes = (direction) => {
                const current = getVisibleMinutesForZoom(zoom);
                const step = current <= 1 ? 0.05 : (current < 5 ? 0.25 : 1);
                setZoomAroundTime(getZoomForVisibleMinutes(current + direction * step));
            };
            const handleZoomIn = () => adjustVisibleMinutes(-1);
            const handleZoomOut = () => adjustVisibleMinutes(1);
            const sliderVisibleMinutes = clampVisibleMinutes(getVisibleMinutesForZoom(zoom));
            useEffect(() => {
                // 缩放拖动中每帧都会变, localStorage 同步写入放到 300ms 防抖后
                const timer = window.setTimeout(() => {
                    try {
                        localStorage.setItem(ZOOM_VISIBLE_MINUTES_STORAGE_KEY, String(Number(sliderVisibleMinutes.toFixed(2))));
                    } catch (e) {}
                }, 300);
                return () => window.clearTimeout(timer);
            }, [sliderVisibleMinutes]);
            // 缩放滑块 rAF 节流: 滑动时 onChange 可高频触发, 每帧最多提交一次 setZoom
            const zoomSliderRafRef = useRef(null);
            const zoomSliderPendingRef = useRef(null);
            const handleZoomSliderChange = (e) => {
                zoomSliderPendingRef.current = e.target.value;
                if (zoomSliderRafRef.current == null) {
                    zoomSliderRafRef.current = window.requestAnimationFrame(() => {
                        zoomSliderRafRef.current = null;
                        setZoomAroundTime(getZoomForVisibleMinutes(zoomSliderPendingRef.current));
                    });
                }
            };
            const formatTime = (s) => `${Math.floor(s / 60)}:${Math.floor(s % 60).toString().padStart(2, '0')}`;
            const formatVisibleRange = (minutes) => minutes < 1
                ? `${Math.round(minutes * 60)}s visible`
                : `${minutes.toFixed(1)} min visible`;
            // 控制栏 toggle 的统一样式: h-7 + rounded + 11px 粗体大写
            // (整行控件共用一套几何/字体, 只用颜色区分语义)
            const displayToggleClass = (active) =>
                `h-7 min-w-[40px] px-2 flex items-center justify-center rounded border text-[11px] font-bold uppercase tracking-wide transition-colors ${
                    active
                        ? 'bg-[#00FF96]/10 border-[#00FF96] text-[#00FF96] shadow-[inset_0_0_0_1px_rgba(0,255,150,0.12)]'
                        : 'bg-[#111] border-gray-700/80 text-gray-500 hover:border-gray-500 hover:text-gray-300'
                }`;

            const getTickSettings = (z) => {
                if (z < 2) return { major: 180, minor: 30 };
                if (z < 5) return { major: 120, minor: 30 };
                if (z < 10) return { major: 60, minor: 10 }; 
                if (z < 30) return { major: 30, minor: 5 };  
                if (z < 60) return { major: 15, minor: 1 };  
                return { major: 10, minor: 1 };              
            };

            const tickSettings = useMemo(() => getTickSettings(zoom), [zoom]);
            const timelinePhases = useMemo(() => {
                const nativePhaseRow = rankData.find(row => row.phases && row.phases.length)
                    || importedRows.find(row => row.phases && row.phases.length);
                if (nativePhaseRow) return nativePhaseRow.phases;

                return bossMechanics
                    .filter(m => m.type === "phase" || m.type === "window")
                    .map(m => ({
                        name: m.name,
                        timestamp: m.time,
                        color: m.color
                    }));
            }, [rankData, importedRows, bossMechanics]);
            const resolveBossTimelineTimestamp = useCallback((mechanic, phases = timelinePhases) => {
                const phaseIndex = Number.isInteger(mechanic.phaseIndex) ? mechanic.phaseIndex : null;
                const phaseTime = Number.isFinite(mechanic.phaseTime) ? mechanic.phaseTime : null;
                const phase = phaseIndex === null ? null : (phases || [])[phaseIndex];
                if (phase && phaseTime !== null) {
                    return Number(phase.timestamp || 0) + phaseTime;
                }
                return Number(mechanic.time || 0);
            }, [timelinePhases]);
            const timelineDuration = useMemo(() => {
                const killTimes = rankData.map(row => row.killTimeSeconds || 0);
                const importedKillTimes = importedRows.map(row => row.killTimeSeconds || 0);
                const mechanicEnds = bossMechanics.map(m => resolveBossTimelineTimestamp(m) + (m.duration || 0));
                const importedCastEnds = importedRows.flatMap(row => row.casts.map(cast => (cast.timestamp || 0) + (cast.duration || 0)));
                const buddyCastEnds = (showBuddy || isCombined) ? rankData.flatMap(row => (
                    row.buddies || (row.buddy ? [row.buddy] : [])
                ).flatMap(buddy => (buddy.casts || []).map(cast => {
                    const buddySpellMap = buddySpellMaps[buddy.specSlug] || {};
                    const spell = buddySpellMap[cast.spellId] || {};
                    return (cast.timestamp || 0) + (cast.duration || spell.duration || 0);
                }))) : [];
                return Math.max(FIGHT_DURATION, ...killTimes, ...importedKillTimes, ...mechanicEnds, ...importedCastEnds, ...buddyCastEnds) + 30;
            }, [rankData, bossMechanics, importedRows, buddySpellMaps, showBuddy, isCombined, resolveBossTimelineTimestamp]);
            const zoomToTimeRange = useCallback((startTime, endTime) => {
                const start = Math.max(0, Math.min(Number(startTime) || 0, Number(endTime) || 0));
                const end = Math.min(timelineDuration, Math.max(Number(startTime) || 0, Number(endTime) || 0));
                const rangeSeconds = Math.max(1, end - start);
                const paddedStart = Math.max(0, start - Math.min(5, rangeSeconds * 0.1));
                const paddedEnd = Math.min(timelineDuration, end + Math.min(5, rangeSeconds * 0.1));
                const visibleSeconds = Math.max(1, paddedEnd - paddedStart);
                const nextZoom = clampZoom(getVisibleTimelineWidth() / visibleSeconds);

                setZoom(nextZoom);
                window.requestAnimationFrame(() => {
                    if (!scrollContainerRef.current) return;
                    const nextScrollLeft = Math.max(0, paddedStart * nextZoom);
                    scrollContainerRef.current.scrollLeft = nextScrollLeft;
                    // 大跳转后立刻 (高优先级) 同步裁剪窗口, 避免短暂空白
                    setScrollCullChunk(Math.round(nextScrollLeft / SCROLL_CULL_CHUNK_PX));
                });
            }, [timelineDuration, getVisibleTimelineWidth, clampZoom]);
            const timelineWidth = timelineDuration * zoom;
            // 横向虚拟化的可见时间窗口 (秒)。scrollCullChunk 变化触发本次渲染,
            // 窗口本身从当前 scrollLeft 现算, 保证缩放后立即正确。
            void scrollCullChunk; // 仅作为渲染触发器
            const cullScrollLeft = scrollContainerRef.current ? scrollContainerRef.current.scrollLeft : 0;
            const cullViewportPx = scrollContainerRef.current ? scrollContainerRef.current.clientWidth : window.innerWidth;
            const cullT0 = (cullScrollLeft - SCROLL_CULL_MARGIN_PX) / zoom;
            const cullT1 = (cullScrollLeft + cullViewportPx + SCROLL_CULL_MARGIN_PX) / zoom;
            // 标尺刻度最多上千个, 只在时长/刻度密度变化时重建, 不随每次渲染重算
            const rulerTicks = useMemo(() => {
                const count = Math.ceil(timelineDuration / tickSettings.minor) + 1;
                return Array.from({ length: count }, (_, i) => {
                    const time = i * tickSettings.minor;
                    return { time, isMajor: time % tickSettings.major === 0 };
                });
            }, [timelineDuration, tickSettings]);
            const rowGridStyle = useMemo(() => ({
                backgroundImage: "linear-gradient(to right, rgba(31,41,55,0.2) 1px, transparent 1px)",
                backgroundSize: `${tickSettings.major * zoom}px 100%`,
                backgroundPosition: "0 0"
            }), [tickSettings.major, zoom]);
            const bossTimelineMechanics = useMemo(
                () => bossMechanics.filter(m => (
                    m.type !== "phase"
                    && m.type !== "window"
                    && bossTimelineTypeVisibility[normalizeBossTimelineType(m.type)]
                )).map(m => ({
                    ...m,
                    displayTime: resolveBossTimelineTimestamp(m)
                })).sort((a, b) => a.displayTime - b.displayTime),
                [bossMechanics, bossTimelineTypeVisibility, resolveBossTimelineTimestamp]
            );
            // 导入行的重计算 (spell map 深拷贝 + 排序 + track 打包) 从每次渲染
            // 提升到 useMemo, 只在真正相关的输入变化时重算
            const importedRowModels = useMemo(() => importedRows.map(importedRow => {
                const rowHeight = 32;
                const trackHeight = 30;
                const rowPhases = importedRow.phases && importedRow.phases.length
                    ? importedRow.phases
                    : timelinePhases;
                const sameSpecAsTimeline = importedRow.specSlug === selectedSpec;
                const importedSpellMap = markSpellMapRepresentativesForContentLevel(
                    sameSpecAsTimeline ? { ...importedRow.spells, ...spells } : importedRow.spells,
                    getBossContentLevel(selectedBoss)
                );
                const storedImportedSpellSelection = importedSpellSelections[importedRow.id];
                const importedVisibleSpellIds = sameSpecAsTimeline
                    ? selectedSpells
                    : expandSelectedSpellSlots(
                        storedImportedSpellSelection || new Set(getDefaultSelectedSpellIds(importedSpellMap || {}, spellCategories)),
                        importedSpellMap || {}
                    );
                const importedVisibleDisplaySpellCount = getSelectedDisplaySpellCount(importedSpellMap, importedVisibleSpellIds);
                const visibleImportedCasts = importedRow.casts.filter(cast => (
                    isLimitBreakSpellId(cast.spellId)
                        ? showLimitBreak
                        : importedVisibleSpellIds.has(Number(cast.spellId))
                ));
                const { processedCasts: packedImportedCasts, maxTracks: importedMaxTracks } = isCollapsed
                    ? { processedCasts: visibleImportedCasts.map(c => ({ ...c, trackIndex: 0 })), maxTracks: 1 }
                    : calculateCastTracks(visibleImportedCasts);
                // 每个 cast 的 spell 对象和条形颜色预解析 (DOM 与 canvas 共用)
                const processedImportedCasts = packedImportedCasts.map((cast, cIdx) => {
                    const spell = isLimitBreakSpellId(cast.spellId) ? getLimitBreakSpell(cast.spellId) : (importedSpellMap[String(cast.spellId)] || {
                        id: cast.spellId,
                        name: `ID: ${cast.spellId}`,
                        image: null,
                        cd: 0,
                        color: '#666666'
                    });
                    const barColor = sameSpecAsTimeline
                        ? (spellColorMap[cast.spellId] || spell.color || DURATION_PALETTE[cIdx % DURATION_PALETTE.length])
                        : (spell.color || DURATION_PALETTE[cIdx % DURATION_PALETTE.length]);
                    return { ...cast, spell, barColor };
                });
                const totalHeight = isCollapsed ? rowHeight : Math.max(rowHeight, importedMaxTracks * trackHeight);
                const specInfo = getSpecInfo(importedRow.specSlug);
                const specName = getLocalizedSpecName(importedRow.specSlug, uiLanguage);
                const endLabel = importedRow.kill ? "Kill" : "Wipe";
                const percentLabel = !importedRow.kill && importedRow.percent ? ` ${Number(importedRow.percent).toFixed(1)}%` : "";
                return {
                    importedRow,
                    rowPhases,
                    sameSpecAsTimeline,
                    importedSpellMap,
                    importedVisibleSpellIds,
                    importedVisibleDisplaySpellCount,
                    processedImportedCasts,
                    totalHeight,
                    specInfo,
                    specName,
                    endLabel,
                    percentLabel
                };
            }), [importedRows, timelinePhases, selectedSpec, spells, selectedBoss, importedSpellSelections, selectedSpells, spellCategories, showLimitBreak, isCollapsed, uiLanguage, spellColorMap]);

            const getDancerTangoWindows = useCallback((casts = []) => (
                (casts || [])
                    .filter(cast => Number(cast.spellId) === DANCER_DEVILMENT_ID)
                    .map(cast => {
                        const start = Number(cast.timestamp || 0) - DANCER_TANGO_EARLY_SECONDS;
                        const duration = Number(cast.duration || DANCER_TANGO_DURATION_SECONDS);
                        return {
                            start: Math.max(0, start),
                            end: Number(cast.timestamp || 0) + duration
                        };
                    })
                    .filter(window => Number.isFinite(window.start) && Number.isFinite(window.end) && window.end >= window.start)
            ), []);
            const rowHasDancerTangoWindow = useCallback((row) => getDancerTangoWindows(row?.casts || []).length > 0, [getDancerTangoWindows]);
            const getPhaseAnchorTimestamp = useCallback((phases, phaseIndex) => {
                if (phaseIndex === null || phaseIndex === undefined) return 0;
                const phase = (phases || [])[phaseIndex];
                return Number(phase?.timestamp || 0);
            }, []);
            const getPhaseOffset = useCallback((phases) => {
                if (phaseAlignIndex === null) return 0;
                const rowAnchor = getPhaseAnchorTimestamp(phases, phaseAlignIndex);
                const rulerAnchor = getPhaseAnchorTimestamp(timelinePhases, phaseAlignIndex);
                if (!rowAnchor && phaseAlignIndex > 0) return 0;
                return rowAnchor - rulerAnchor;
            }, [phaseAlignIndex, timelinePhases, getPhaseAnchorTimestamp]);
            const getAlignedLeft = useCallback((timestamp, phases) => (
                `${(Number(timestamp || 0) - getPhaseOffset(phases)) * zoom}px`
            ), [getPhaseOffset, zoom]);
            const togglePhaseAlignment = useCallback((phaseIndex) => {
                setPhaseAlignIndex(prev => prev === phaseIndex ? null : phaseIndex);
            }, []);

            // 玩家行渲染模型: 过滤/技能可见性/track 打包/伙伴行/每个 cast 的
            // spell 与颜色, 全部提升到 useMemo。DOM 渲染和 canvas 绘制共用同一份
            // 数据, 且只在真正相关的输入变化时重算 (缩放/滚动/选中行都不触发)。
            const playerRowModels = useMemo(() => rankData
                .filter(row => {
                    // 1. Composition Filter
                    if (activeFilterSpecs.size > 0) {
                        const comp = row.composition || [];
                        for (let spec of activeFilterSpecs) {
                            if (!comp.includes(spec)) return false;
                        }
                    }
                    // 2. Kill Time Filter
                    if (row.killTimeSeconds < killTimeRange.min) return false;
                    if (row.killTimeSeconds > killTimeRange.max) return false;

                    // 3. CURATION FILTER (New Logic: check curatedRowIds instead of selectedRowIds)
                    if (isCurated && !curatedRowIds.has(row.id)) return false;

                    return true;
                })
                .map((row) => {
                    const visibleCasts = row.casts
                        .map(cast => {
                            const castSpellMap = row.isCombined ? (buddySpellMaps[cast.specSlug] || {}) : spells;
                            const spell = isLimitBreakSpellId(cast.spellId) ? getLimitBreakSpell(cast.spellId) : (castSpellMap[cast.spellId] || {});
                            return {
                                ...cast,
                                duration: cast.duration || spell.duration || 0
                            };
                        })
                        .filter(cast => {
                            if (isLimitBreakSpellId(cast.spellId)) return showLimitBreak;
                            // 预展开集合 O(1) 查询, 等价于原先的 selectedIds.has || isSpellSlotSelected 全表扫描
                            const visibleIds = row.isCombined ? (buddyVisibleSpellIdSets[cast.specSlug] || EMPTY_SPELL_ID_SET) : visibleSpellIdSet;
                            return visibleIds.has(Number(cast.spellId));
                        });
                    const { processedCasts: packedCasts, maxTracks } = isCollapsed
                        ? { processedCasts: visibleCasts.map(c => ({ ...c, trackIndex: 0 })), maxTracks: 1 }
                        : calculateCastTracks(visibleCasts);
                    // 每个 cast 的 spell 对象和条形颜色预解析 (DOM 与 canvas 共用)
                    const processedCasts = packedCasts.map(cast => {
                        const castSpellMap = row.isCombined ? (buddySpellMaps[cast.specSlug] || {}) : spells;
                        const castColorMap = row.isCombined ? (buddySpellColorMaps[cast.specSlug] || {}) : spellColorMap;
                        const spell = isLimitBreakSpellId(cast.spellId) ? getLimitBreakSpell(cast.spellId) : (castSpellMap[cast.spellId] || {
                            id: cast.spellId,
                            name: `ID: ${cast.spellId}`,
                            image: null, // 没有图片
                            cd: 0,
                            color: '#666666' // 默认给个灰色
                        });
                        const barColor = isLimitBreakSpellId(cast.spellId)
                            ? spell.color
                            : (castColorMap[cast.spellId] || spell.color || '#ffffff');
                        return { ...cast, spell, barColor };
                    });

                    // COMPACT MODE: 32px height per row
                    const rowHeight = 32;
                    const trackHeight = 30; // Height per sub-row when expanded
                    const totalHeight = isCollapsed ? rowHeight : Math.max(rowHeight, maxTracks * trackHeight);
                    const buddyRowHeight = rowHeight;
                    const buddyTrackHeight = trackHeight;
                    const rowBuddies = row.isCombined
                        ? (row.buddy ? [row.buddy] : [])
                        : (showBuddy && isBuddySupported ? (row.buddies || (row.buddy ? [row.buddy] : [])) : []);
                    const dancerTangoWindows = showDancerTangoBuddyWindow && selectedSpec === 'dancer-dancer'
                        ? getDancerTangoWindows(row.casts || [])
                        : [];
                    const isInDancerTangoWindow = (cast) => (
                        !showDancerTangoBuddyWindow
                        || selectedSpec !== 'dancer-dancer'
                        || dancerTangoWindows.some(window => (
                            Number(cast.timestamp || 0) >= window.start
                            && Number(cast.timestamp || 0) <= window.end
                        ))
                    );
                    const buddyRows = rowBuddies.map((buddy, buddyIdx) => {
                        const buddySpecSlug = buddy?.specSlug || "";
                        const buddySpellMap = buddySpecSlug === selectedSpec ? spells : (buddySpellMaps[buddySpecSlug] || {});
                        const buddyColorMap = buddySpecSlug === selectedSpec
                            ? spellColorMap
                            : (buddySpellColorMaps[buddySpecSlug] || {});
                        const buddyCasts = (buddy.casts || []).map(cast => ({
                            ...cast,
                            duration: cast.duration || (isLimitBreakSpellId(cast.spellId)
                                ? getLimitBreakSpell(cast.spellId).duration
                                : (buddySpellMap[cast.spellId] ? buddySpellMap[cast.spellId].duration : 0))
                        }));
                        const buddyVisibleIds = buddySpecSlug === selectedSpec
                            ? visibleSpellIdSet
                            : (buddyVisibleSpellIdSets[buddySpecSlug] || EMPTY_SPELL_ID_SET);
                        const visibleBuddyCasts = buddyCasts.filter(cast => (
                            isInDancerTangoWindow(cast)
                            && (
                                isLimitBreakSpellId(cast.spellId)
                                    ? showLimitBreak
                                    // 预展开集合 O(1) 查询, 等价于原先的 has || isSpellSlotSelected 扫描
                                    : buddyVisibleIds.has(Number(cast.spellId))
                            )
                        ));
                        const { processedCasts: packedBuddyCasts, maxTracks: buddyMaxTracks } = isCollapsed
                            ? { processedCasts: visibleBuddyCasts.map(c => ({ ...c, trackIndex: 0 })), maxTracks: 1 }
                            : calculateCastTracks(visibleBuddyCasts);
                        const processedBuddyCasts = packedBuddyCasts.map((cast, cIdx) => {
                            const spell = isLimitBreakSpellId(cast.spellId) ? getLimitBreakSpell(cast.spellId) : (buddySpellMap[cast.spellId] || {
                                id: cast.spellId,
                                name: `ID: ${cast.spellId}`,
                                image: null,
                                cd: 0,
                                color: '#666666'
                            });
                            const barColor = isLimitBreakSpellId(cast.spellId)
                                ? spell.color
                                : (buddyColorMap[cast.spellId] || spell.color || DURATION_PALETTE[cIdx % DURATION_PALETTE.length]);
                            return { ...cast, spell, barColor };
                        });
                        const buddyTotalHeight = isCollapsed ? buddyRowHeight : Math.max(buddyRowHeight, buddyMaxTracks * buddyTrackHeight);
                        return {
                            buddy,
                            buddyIdx,
                            buddySpellMap,
                            buddyColorMap,
                            processedBuddyCasts,
                            buddyTotalHeight
                        };
                    });
                    const showBuddyRow = buddyRows.length > 0;
                    const rowPhases = row.phases && row.phases.length
                        ? row.phases
                        : bossMechanics
                            .filter(m => m.type === "phase" || m.type === "window")
                            .map(m => ({
                                name: m.name,
                                timestamp: m.time,
                                color: m.color
                            }));
                    return {
                        row,
                        processedCasts,
                        totalHeight,
                        buddyRows,
                        showBuddyRow,
                        rowPhases,
                        dancerTangoWindows
                    };
                }), [
                rankData, activeFilterSpecs, killTimeRange, isCurated, curatedRowIds,
                buddySpellMaps, spells, showLimitBreak, visibleSpellIdSet, buddyVisibleSpellIdSets,
                isCollapsed, showBuddy, isBuddySupported, showDancerTangoBuddyWindow, selectedSpec,
                bossMechanics, spellColorMap, buddySpellColorMaps, getDancerTangoWindows,
            ]);

            // ==================== Canvas 渲染层 (组件侧) ====================
            const castCanvasRef = useRef(null);
            const castRowElsRef = useRef(new Map());   // rowKey -> { el, params }
            const drawStateRef = useRef(null);
            const drawScheduledRef = useRef(false);
            const castTooltipRef = useRef(null);
            const tooltipRafRef = useRef(null);
            const pendingCanvasPressRef = useRef(null);
            const canvasIconHitRef = useRef(false);
            const handleCanvasCastPressRef = useRef(null);

            // 已绘制的内容区域 (内容坐标), 滚动时用来判断是否需要重画
            const drawnRegionRef = useRef(null);

            const drawCastCanvas = useCallback(() => {
                drawScheduledRef.current = false;
                const canvas = castCanvasRef.current;
                const sc = scrollContainerRef.current;
                const state = drawStateRef.current;
                if (!canvas || !sc || !state) return;

                const dpr = window.devicePixelRatio || 1;
                // 用内容包裹层的自然尺寸 (不能用 scrollWidth: canvas 自己也是
                // 滚动溢出的一部分, 会造成尺寸反馈循环/幽灵滚动区)
                const contentEl = timelineContentRef.current;
                const contentW = contentEl ? contentEl.offsetWidth : sc.scrollWidth;
                const contentH = contentEl ? contentEl.offsetHeight : sc.scrollHeight;
                // 画布覆盖 "视口 + 余量", 以内容坐标绝对定位在滚动内容里 ——
                // 滚动时由合成器原生移动 (与 DOM 刻度严格同步), 无需每帧重画
                const originX = Math.max(0, Math.min(sc.scrollLeft - CANVAS_MARGIN_X, contentW));
                const originY = Math.max(0, Math.min(sc.scrollTop - CANVAS_MARGIN_Y, contentH));
                const width = Math.max(1, Math.min(sc.clientWidth + 2 * CANVAS_MARGIN_X, contentW - originX));
                const height = Math.max(1, Math.min(sc.clientHeight + 2 * CANVAS_MARGIN_Y, contentH - originY));

                canvas.style.left = `${originX}px`;
                canvas.style.top = `${originY}px`;
                canvas.style.width = `${width}px`;
                canvas.style.height = `${height}px`;
                const devW = Math.round(width * dpr);
                const devH = Math.round(height * dpr);
                if (canvas.width !== devW || canvas.height !== devH) {
                    canvas.width = devW;
                    canvas.height = devH;
                }
                const ctx = canvas.getContext('2d');
                // 平移到内容坐标系: 之后所有绘制直接用内容坐标
                ctx.setTransform(dpr, 0, 0, dpr, -originX * dpr, -originY * dpr);
                ctx.clearRect(originX, originY, width, height);

                const y0 = originY;
                const y1 = originY + height;
                for (const entry of castRowElsRef.current.values()) {
                    const { el, params } = entry;
                    if (!el || !el.isConnected) continue;
                    const rowTop = el.offsetTop;
                    if (rowTop + params.totalHeight < y0 || rowTop > y1) continue;
                    drawRowCasts(ctx, params, rowTop, state, originX, originX + width);
                }

                drawnRegionRef.current = { x0: originX, x1: originX + width, y0, y1, contentW, contentH };
            }, []);

            const scheduleCastCanvasDraw = useCallback(() => {
                if (RENDER_MODE !== 'canvas' || drawScheduledRef.current) return;
                drawScheduledRef.current = true;
                window.requestAnimationFrame(drawCastCanvas);
            }, [drawCastCanvas]);

            // 滚动时只做边界检查: 接近已绘区边缘才重画 (平移本身零成本)
            const checkCanvasRegionOnScroll = useCallback(() => {
                const sc = scrollContainerRef.current;
                const region = drawnRegionRef.current;
                if (!sc) return;
                if (!region) { scheduleCastCanvasDraw(); return; }
                const needX = (sc.scrollLeft < region.x0 + CANVAS_REDRAW_SLACK && region.x0 > 0)
                    || (sc.scrollLeft + sc.clientWidth > region.x1 - CANVAS_REDRAW_SLACK && region.x1 < region.contentW);
                const needY = (sc.scrollTop < region.y0 + CANVAS_REDRAW_SLACK && region.y0 > 0)
                    || (sc.scrollTop + sc.clientHeight > region.y1 - CANVAS_REDRAW_SLACK && region.y1 < region.contentH);
                if (needX || needY) scheduleCastCanvasDraw();
            }, [scheduleCastCanvasDraw]);

            // 行注册: 行 DOM 挂载/更新时把元素和绘制参数写进 map (canvas 按 offsetTop 定位)
            const registerCastRowRef = (key, params) => (el) => {
                if (RENDER_MODE !== 'canvas') return;
                if (el) castRowElsRef.current.set(key, { el, params });
                else castRowElsRef.current.delete(key);
            };

            // 每次 React 提交后同步绘制状态并重画 (transition 被丢弃的渲染不会走到这里)
            useEffect(() => {
                if (RENDER_MODE !== 'canvas') return;
                drawStateRef.current = {
                    zoom,
                    showCooldown,
                    showDuration,
                    showSkillTimes,
                    isCollapsed,
                    focusedSpellId,
                    isFocusedSpellId,
                    getPhaseOffset,
                    leftPanelWidth,
                    formatTime,
                };
                handleCanvasCastPressRef.current = handleCanvasCastPress;
                scheduleCastCanvasDraw();
            });

            // 图标异步加载完成 -> 重画; 容器尺寸变化 -> 重画; 滚动 -> 仅做边界检查
            // 注意 deps 里必须有 loading: 首次挂载时组件还在 loading 早退分支,
            // 滚动容器 ref 是 null, 什么都挂不上; loading 结束后 effect 重跑才真正挂上。
            // (之前漏了这个 dep, 纵向滚动永远不触发补画 —— "往下滚看不到东西"的根因)
            useEffect(() => {
                if (RENDER_MODE !== 'canvas') return;
                castCanvasRedrawHook = scheduleCastCanvasDraw;
                const sc = scrollContainerRef.current;
                let ro = null;
                if (sc) {
                    sc.addEventListener('scroll', checkCanvasRegionOnScroll, { passive: true });
                    if (typeof ResizeObserver !== 'undefined') {
                        ro = new ResizeObserver(scheduleCastCanvasDraw);
                        ro.observe(sc);
                    }
                }
                return () => {
                    castCanvasRedrawHook = null;
                    if (sc) sc.removeEventListener('scroll', checkCanvasRegionOnScroll);
                    if (ro) ro.disconnect();
                };
            }, [scheduleCastCanvasDraw, checkCanvasRegionOnScroll, loading]);

            // 命中测试: 视口坐标 -> 命中的 cast 图标 (逆聚焦绘制顺序: 上层优先)
            const hitTestCastIcon = useCallback((clientX, clientY) => {
                if (RENDER_MODE !== 'canvas') return null;
                const sc = scrollContainerRef.current;
                const state = drawStateRef.current;
                if (!sc || !state) return null;
                const rect = sc.getBoundingClientRect();
                const xView = clientX - rect.left;
                const yView = clientY - rect.top;
                if (xView < state.leftPanelWidth || yView < RULER_HEIGHT_PX) return null;
                if (xView > sc.clientWidth || yView > sc.clientHeight) return null;
                const contentY = yView + sc.scrollTop;
                const scrollLeft = sc.scrollLeft;

                for (const [key, entry] of castRowElsRef.current) {
                    const { el, params } = entry;
                    if (!el || !el.isConnected) continue;
                    const rowTop = el.offsetTop;
                    if (contentY < rowTop || contentY >= rowTop + params.totalHeight) continue;

                    const { casts, totalHeight, trackHeight, rowPhases, killTimeSeconds } = params;
                    const phaseOffset = state.getPhaseOffset(rowPhases);
                    const focusActive = !!state.focusedSpellId;
                    // 上层的先命中: 聚焦层 (若有) 逆序 -> 普通层逆序
                    for (let pass = 0; pass < (focusActive ? 2 : 1); pass++) {
                        for (let i = casts.length - 1; i >= 0; i--) {
                            const cast = casts[i];
                            const isFocused = focusActive && state.isFocusedSpellId(cast.spellId);
                            if (focusActive && ((pass === 0) !== isFocused)) continue;
                            const timeUntilKill = killTimeSeconds ? (killTimeSeconds - cast.timestamp) : 99999;
                            if (timeUntilKill <= 0) continue;
                            const currentTrackHeight = state.isCollapsed ? totalHeight : trackHeight;
                            const iconHeight = currentTrackHeight * 0.9;
                            const yTop = rowTop + (state.isCollapsed ? 0 : cast.trackIndex * trackHeight);
                            const iconY = yTop + (currentTrackHeight - iconHeight) / 2;
                            if (contentY < iconY || contentY > iconY + iconHeight) continue;
                            const alignedT = Number(cast.timestamp || 0) - phaseOffset;
                            const xIcon = state.leftPanelWidth + alignedT * state.zoom - scrollLeft;
                            if (xView >= xIcon && xView <= xIcon + iconHeight) {
                                return { key, cast, spell: cast.spell };
                            }
                        }
                    }
                    return null; // 命中了这一行但没点到图标
                }
                return null;
            }, []);

            // canvas 模式下的图标按下逻辑 (对齐 DOM 的 handleSpellIconMouseDown:
            // 按下+原地松开+没有发生拖动 => 切换聚焦)
            const handleCanvasCastPress = useCallback((e, hit) => {
                if (e.button !== 0) return;
                e.preventDefault();
                pendingCanvasPressRef.current = {
                    spellId: Number(hit.cast.spellId),
                    key: hit.key,
                    startX: e.clientX,
                    startY: e.clientY
                };
                const handleUp = (event) => {
                    window.removeEventListener('mouseup', handleUp);
                    const pending = pendingCanvasPressRef.current;
                    pendingCanvasPressRef.current = null;
                    if (!pending) return;
                    const delta = Math.hypot(event.clientX - pending.startX, event.clientY - pending.startY);
                    const releaseHit = hitTestCastIcon(event.clientX, event.clientY);
                    const releasedOnSameIcon = releaseHit
                        && releaseHit.key === pending.key
                        && Number(releaseHit.cast.spellId) === pending.spellId;
                    if (delta < DRAG_THRESHOLD && !dragInfo.current.moved && releasedOnSameIcon) {
                        toggleFocusedSpell(pending.spellId);
                    }
                };
                window.addEventListener('mouseup', handleUp);
            }, [hitTestCastIcon, toggleFocusedSpell]);

            // 悬浮提示 (替代 DOM 图标的原生 title)
            const hideCastTooltip = useCallback(() => {
                if (castTooltipRef.current) castTooltipRef.current.style.display = 'none';
            }, []);
            const handleCanvasTooltipMove = useCallback((e) => {
                if (RENDER_MODE !== 'canvas') return;
                if (tooltipRafRef.current !== null) return;
                const { clientX, clientY } = e;
                tooltipRafRef.current = window.requestAnimationFrame(() => {
                    tooltipRafRef.current = null;
                    const tooltip = castTooltipRef.current;
                    if (!tooltip) return;
                    if (dragInfo.current.isDown || timeRangeSelectionRef.current) {
                        tooltip.style.display = 'none';
                        return;
                    }
                    const hit = hitTestCastIcon(clientX, clientY);
                    const state = drawStateRef.current;
                    if (hit && state) {
                        tooltip.textContent = `${hit.spell.name} (${state.formatTime(hit.cast.timestamp)})`;
                        tooltip.style.display = 'block';
                        tooltip.style.left = `${clientX + 12}px`;
                        tooltip.style.top = `${clientY + 14}px`;
                    } else {
                        tooltip.style.display = 'none';
                    }
                });
            }, [hitTestCastIcon]);
            // ================== Canvas 渲染层 (组件侧, 结束) ==================


            const onRulerMouseDown = useCallback((e) => {
                if (e.button !== 0 || e.target.closest('button, a, input, select, textarea')) return;
                e.preventDefault();
                e.stopPropagation();

                const container = scrollContainerRef.current;
                if (!container) return;
                // mousedown 时缓存一次 rect, 拖动中不再每次 mousemove 强制 layout
                const rectLeft = container.getBoundingClientRect().left;
                const timeFromClientX = (clientX) => {
                    const timelineX = container.scrollLeft + (clientX - rectLeft) - leftPanelWidth;
                    return Math.max(0, Math.min(timelineDuration, timelineX / zoom));
                };

                const startTime = timeFromClientX(e.clientX);
                timeRangeSelectionRef.current = {
                    startTime,
                    endTime: startTime
                };
                // setState 只在 mousedown/mouseup 各调一次 (挂载/卸载 overlay);
                // 拖动中的选区更新走命令式 DOM 写入 + rAF 合帧, 避免整棵树每帧重渲染
                setTimeRangeSelection({ startTime, endTime: startTime });

                let rafId = null;
                const paintOverlay = () => {
                    rafId = null;
                    const pending = timeRangeSelectionRef.current;
                    const overlay = selectionOverlayRef.current;
                    if (!pending || !overlay) return;
                    overlay.style.left = `${Math.min(pending.startTime, pending.endTime) * zoom}px`;
                    overlay.style.width = `${Math.max(2, Math.abs(pending.endTime - pending.startTime) * zoom)}px`;
                };

                const handleRangeMouseMove = (event) => {
                    const pending = timeRangeSelectionRef.current;
                    if (!pending) return;
                    pending.endTime = timeFromClientX(event.clientX);
                    if (rafId === null) rafId = window.requestAnimationFrame(paintOverlay);
                };

                const handleRangeMouseUp = (event) => {
                    window.removeEventListener('mousemove', handleRangeMouseMove);
                    window.removeEventListener('mouseup', handleRangeMouseUp);
                    if (rafId !== null) window.cancelAnimationFrame(rafId);

                    const pending = timeRangeSelectionRef.current;
                    timeRangeSelectionRef.current = null;
                    setTimeRangeSelection(null);
                    if (!pending) return;

                    const endTime = timeFromClientX(event.clientX);
                    if (Math.abs(endTime - pending.startTime) >= 2) {
                        zoomToTimeRange(pending.startTime, endTime);
                    }
                };

                window.addEventListener('mousemove', handleRangeMouseMove);
                window.addEventListener('mouseup', handleRangeMouseUp);
            }, [leftPanelWidth, timelineDuration, zoom, zoomToTimeRange]);

            const onMouseDown = useCallback((e) => {
                if (e.button !== 0 || !scrollContainerRef.current) return;
                if (e.target.closest('button, a, input, select, textarea')) return;
                // canvas 模式: 按在技能图标上时先登记图标按下
                // (与 DOM 模式中图标 onMouseDown 和容器拖拽 handler 并行触发的行为一致)
                if (RENDER_MODE === 'canvas') {
                    const hit = hitTestCastIcon(e.clientX, e.clientY);
                    canvasIconHitRef.current = !!hit;
                    // 经 ref 取最新版本, 避免本 useCallback 的空依赖捕获到过期闭包
                    if (hit && handleCanvasCastPressRef.current) handleCanvasCastPressRef.current(e, hit);
                }
                e.preventDefault();

                dragInfo.current = {
                    isDown: true,
                    startX: e.pageX,
                    startY: e.pageY,
                    scrollLeft: scrollContainerRef.current.scrollLeft,
                    moved: false
                };
                
                window.addEventListener('mousemove', onMouseMove);
                window.addEventListener('mouseup', onMouseUp);
            }, []);

            const onDragStart = useCallback((e) => {
                e.preventDefault();
                dragInfo.current.isDown = false;
                dragInfo.current.moved = false;
                setDraggingCursor(false);
            }, [setDraggingCursor]);

            const onMouseMove = useCallback((e) => {
                if (!dragInfo.current.isDown) return;

                const deltaX = e.pageX - dragInfo.current.startX;
                const deltaY = e.pageY - dragInfo.current.startY;
                if (!dragInfo.current.moved && Math.hypot(deltaX, deltaY) >= DRAG_THRESHOLD) {
                    dragInfo.current.moved = true;
                    setDraggingCursor(true);
                }

                if (!dragInfo.current.moved) return;

                e.preventDefault();
                // 高轮询率鼠标 (125-1000Hz) 每帧可能来多次 mousemove, scrollLeft 写入合并到每帧一次
                dragInfo.current.targetScrollLeft = dragInfo.current.scrollLeft - deltaX * 1.5;
                if (dragInfo.current.rafId == null) {
                    dragInfo.current.rafId = window.requestAnimationFrame(() => {
                        dragInfo.current.rafId = null;
                        if (scrollContainerRef.current && dragInfo.current.targetScrollLeft != null) {
                            scrollContainerRef.current.scrollLeft = dragInfo.current.targetScrollLeft;
                        }
                    });
                }
            }, [setDraggingCursor]);

            const onMouseUp = useCallback(() => {
                const didDrag = dragInfo.current.moved;
                dragInfo.current.isDown = false;
                setDraggingCursor(false);

                if (didDrag) {
                    suppressRowClickRef.current = true;
                    window.setTimeout(() => {
                        suppressRowClickRef.current = false;
                    }, 100);
                }
                
                window.removeEventListener('mousemove', onMouseMove);
                window.removeEventListener('mouseup', onMouseUp);
            }, [onMouseMove, setDraggingCursor]);

            useEffect(() => {
                return () => {
                    window.removeEventListener('mousemove', onMouseMove);
                    window.removeEventListener('mouseup', onMouseUp);
                };
            }, [onMouseMove, onMouseUp]);

            const updateUrlAndReload = (key, value) => {
                const url = new URL(window.location);
                url.searchParams.set(key, value);
                if (key === 'boss') {
                    url.searchParams.set('spec', selectedSpec);
                } else if (key === 'spec') {
                    url.searchParams.set('boss', selectedBoss);
                }

                // 缩放偏好是 300ms 防抖写入的, 跳转前先冲刷, 避免刚调好的缩放丢失
                try {
                    localStorage.setItem(ZOOM_VISIBLE_MINUTES_STORAGE_KEY, String(Number(sliderVisibleMinutes.toFixed(2))));
                } catch (e) {}
                window.location.href = url.toString();
            };

            // FEATURE: Handle Confirm Selection
            const handleConfirmSelection = () => {
                if (selectedRowIds.size === 0) {
                    alert(t("selectAtLeastOneRow"));
                    return;
                }
                
                // 1. Move current selection to curated list (Visibility)
                setCuratedRowIds(new Set(selectedRowIds));
                
                // 2. Clear current selection (Highlight Border) - This fixes your issue!
                setSelectedRowIds(new Set());
                
                setIsCurated(true);
                setIsSelectionMode(false);
            };

            // FEATURE: Handle Cancel/Exit
            const handleExitCuration = () => {
                setIsCurated(false);
                setIsSelectionMode(false);
                setCuratedRowIds(new Set()); // Clear curated list on exit
                // Note: We might want to clear selectedRowIds (Green lines) too, or keep them. 
                // Let's clear them to be clean.
                // setSelectedRowIds(new Set()); 
            };


            // 行折叠与缩放控件: 桌面端放在控制栏右侧, 移动端放在收起后的紧凑行里
            const rowCollapseButton = (
                <button
                    onClick={() => setIsCollapsed(!isCollapsed)}
                    className={`h-7 w-7 flex shrink-0 items-center justify-center rounded border transition-colors ${!isCollapsed ? 'border-[#00FF96] bg-[#00FF96]/10 text-[#00FF96]' : 'border-gray-700/80 bg-[#111] text-gray-400 hover:border-gray-500 hover:text-gray-300'}`}
                    title={isCollapsed ? t("expandRows") : t("collapseRows")}
                >
                    <Layers size={16} />
                </button>
            );
            const zoomCluster = (
                <>
                    <button onClick={handleZoomIn} className="h-7 w-7 flex shrink-0 items-center justify-center rounded border border-gray-700/80 bg-[#111] text-gray-400 hover:border-gray-500 hover:text-[#00FF96] transition-colors"><ZoomIn size={15} /></button>
                    <input
                        type="range"
                        min={MIN_VISIBLE_MINUTES}
                        max={MAX_VISIBLE_MINUTES}
                        step="0.05"
                        value={Number(sliderVisibleMinutes.toFixed(2))}
                        onChange={handleZoomSliderChange}
                        className={`${isMobile ? 'h-4 w-24' : 'h-2 w-28'} cursor-pointer accent-[#00FF96]`}
                        title={formatVisibleRange(sliderVisibleMinutes)}
                    />
                    <button onClick={handleZoomOut} className="h-7 w-7 flex shrink-0 items-center justify-center rounded border border-gray-700/80 bg-[#111] text-gray-400 hover:border-gray-500 hover:text-[#00FF96] transition-colors"><ZoomOut size={15} /></button>
                </>
            );

            if (loading) return <div className="app-shell bg-[#121212] flex items-center justify-center text-[#00FF96]">{t("loading")}</div>;

            return (
                <div className="flex flex-col app-shell bg-[#121212] text-gray-300 font-sans overflow-hidden">

                {/* Navbar: 只保留"看什么"的选择 (Boss/职业/区服), 工具类按钮全部
                    下放到时间轴上方的工具行 —— 让顶部尽量轻 */}
                <nav className="h-11 bg-[#1a1a1a] border-b border-gray-800 flex items-center justify-between gap-2 px-2 sm:px-3 shrink-0 z-[7000]">
                    <div className="flex items-center gap-1.5 sm:gap-3 min-w-0 flex-1">
                        {/* 窄屏隐藏站名, 把宽度让给 Boss/职业/区服三个选择器 */}
                        <a href="main_menu.html#" className="hidden sm:flex text-lg font-bold tracking-tight text-white items-center select-none hover:opacity-80 transition-opacity shrink-0" style={{ textDecoration: 'none' }}>
                            <span style={{ color: THEME_COLOR }} className="mr-0.5">M</span>-Spec
                        </a>
                        <div className="relative min-w-0 flex-1 sm:flex-none">
                            <select
                                value={selectedBoss}
                                onChange={(e) => updateUrlAndReload('boss', e.target.value)}
                                className="nav-select h-7 w-full sm:w-auto sm:min-w-[150px] appearance-none rounded border border-gray-700/80 bg-[#101010] px-2 sm:px-2.5 pr-7 text-xs font-medium text-gray-100 outline-none transition-colors hover:border-[#00FF96]/70 focus:border-[#00FF96] cursor-pointer"
                            >
                                {BOSS_GROUPS.map(group => (
                                    <optgroup key={group.labelKey} label={t(group.labelKey)}>
                                        {group.items.map(boss => (
                                            <option key={boss.id} value={boss.id}>{getLocalizedBossName(boss.id, uiLanguage)}</option>
                                        ))}
                                    </optgroup>
                                ))}
                            </select>
                            <ChevronDown size={12} className="pointer-events-none absolute right-2 top-1/2 -translate-y-1/2 text-gray-500" />
                        </div>
                        <SpecSelector
                            selectedSpec={selectedSpec}
                            onChange={(id) => updateUrlAndReload('spec', id)}
                            t={t}
                            uiLanguage={uiLanguage}
                        />
                        <div className="relative shrink-0">
                            <select
                                value={selectedRegion}
                                onChange={(e) => setSelectedRegion(e.target.value)}
                                className="nav-select h-7 w-[58px] appearance-none rounded border border-gray-700/80 bg-[#101010] px-2 pr-6 text-xs font-medium text-gray-100 outline-none transition-colors hover:border-[#00FF96]/70 focus:border-[#00FF96] cursor-pointer"
                                title={t("region")}
                            >
                                <option value="All">{t("all")}</option>
                                <option value="JP">JP</option>
                                <option value="NA">NA</option>
                                <option value="EU">EU</option>
                                <option value="OC">OC</option>
                                <option value="CN">CN</option>
                                <option value="KR">KR</option>
                            </select>
                            <ChevronDown size={12} className="pointer-events-none absolute right-2 top-1/2 -translate-y-1/2 text-gray-500" />
                        </div>
                    </div>
                    {/* Right side with Discord Icon */}
                    <div className="flex items-center gap-1.5 shrink-0">
                        <button
                            onClick={cycleUiLanguage}
                            className="h-7 min-w-[38px] sm:min-w-[44px] rounded border border-gray-700/80 bg-black/30 px-1.5 sm:px-2 text-[11px] font-black text-gray-400 transition-colors hover:border-[#00FF96] hover:text-white"
                            title={t("language")}
                        >
                            {currentLanguage.label}
                        </button>
                        <a
                            href="https://discord.gg/SZRX5fVUeG"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="hidden sm:block text-[#5865F2] hover:text-white transition-colors p-1.5"
                            title="Join Discord"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 127.14 96.36" fill="currentColor">
                                <path d="M107.7,8.07A105.15,105.15,0,0,0,81.47,0a72.06,72.06,0,0,0-3.36,6.83A97.68,97.68,0,0,0,49,6.83,72.37,72.37,0,0,0,45.64,0,105.89,105.89,0,0,0,19.39,8.09C2.79,32.65-1.71,56.6.54,80.21h0A105.73,105.73,0,0,0,32.71,96.36,77.11,77.11,0,0,0,39.6,85.25a68.42,68.42,0,0,1-10.85-5.18c.91-.66,1.8-1.34,2.66-2a75.57,75.57,0,0,0,64.32,0c.87.71,1.76,1.39,2.66,2a68.68,68.68,0,0,1-10.87,5.19,77,77,0,0,0,6.89,11.1A105.25,105.25,0,0,0,126.6,80.22c2.36-24.44-2-47.27-18.9-72.15ZM42.45,65.69C36.18,65.69,31,60,31,53s5-12.74,11.43-12.74S54,46,53.89,53,48.84,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.25,60,73.25,53s5.06-12.74,11.44-12.74S96.23,46,96.12,53,91.08,65.69,84.69,65.69Z"/>
                            </svg>
                        </a>
                    </div>
                </nav>

                {importModalOpen && (
                    // z 要压过导航(7000)/工具栏(5000)/标尺(3000), 否则弹窗会被它们盖住
                    <div className="fixed inset-0 z-[9000] flex items-center justify-center bg-black/70">
                        <div className="w-[520px] max-w-[calc(100vw-32px)] rounded-md border border-gray-700 bg-[#151515] shadow-2xl">
                            <div className="flex items-center justify-between border-b border-gray-800 px-4 py-3">
                                <div className="font-bold text-white">{t("importPull")}</div>
                                <button
                                    onClick={() => setImportModalOpen(false)}
                                    className="text-gray-500 hover:text-white"
                                    title={t("close")}
                                >
                                    <XCircle size={18} />
                                </button>
                            </div>
                            <div className="space-y-3 p-4">
                                <input
                                    value={importUrl}
                                    onChange={(e) => setImportUrl(e.target.value)}
                                    placeholder="https://www.fflogs.com/reports/...?...fight=9&type=damage-done"
                                    className="w-full rounded border border-gray-700 bg-black/40 px-3 py-2 text-sm text-white outline-none focus:border-[#00FF96]"
                                />
                                <div className="text-[11px] leading-relaxed text-gray-500">
                                    {t("importUrlHelp")}
                                </div>
                                <div className="flex items-center gap-2">
                                    <button
                                        onClick={handleLoadImportPlayers}
                                        disabled={importLoading || !importUrl.trim()}
                                        className="rounded-sm border border-[#00FF96] bg-[#00FF96]/10 px-3 py-1.5 text-sm font-bold text-[#00FF96] disabled:cursor-not-allowed disabled:border-gray-700 disabled:text-gray-600"
                                    >
                                        {importLoading ? t("loading") : t("loadPlayers")}
                                    </button>
                                    {importMeta && (
                                        <span className="truncate text-xs text-gray-500">
                                            {importMeta.report_id} / fight {importMeta.fight_id}
                                        </span>
                                    )}
                                </div>
                                {importError && (
                                    <div className="rounded border border-red-500/40 bg-red-950/30 px-3 py-2 text-xs text-red-300">
                                        {importError}
                                    </div>
                                )}
                                {importPlayers.length > 0 && (
                                    <div className="max-h-72 overflow-auto rounded border border-gray-800 bg-black/20">
                                        {importPlayers.map(player => {
                                            const specInfo = getSpecInfo(player.spec_slug);
                                            const specName = getLocalizedSpecName(player.spec_slug, uiLanguage);
                                            const specIcon = specInfo.icon ? `./images/classes/${specInfo.icon}` : null;
                                            return (
                                                <button
                                                    key={player.source_id}
                                                    onClick={() => handleImportPlayer(player)}
                                                    disabled={importLoading}
                                                    className="flex w-full items-center gap-3 border-b border-gray-800 px-3 py-2.5 text-left text-sm hover:bg-white/5 disabled:cursor-wait"
                                                >
                                                    <span className="flex h-8 w-8 shrink-0 items-center justify-center overflow-hidden rounded border border-gray-700 bg-[#111]">
                                                        {specIcon ? (
                                                            <img src={specIcon} alt={specName} draggable={false} className="h-full w-full object-cover" />
                                                        ) : (
                                                            <span className="text-[10px] font-black text-gray-400">{specName.slice(0, 2).toUpperCase()}</span>
                                                        )}
                                                    </span>
                                                    <span className="min-w-0 flex-1">
                                                        <span className="block truncate font-bold text-white">{player.name}</span>
                                                        <span className="block text-[11px] font-bold uppercase tracking-wide text-gray-500">{specName}</span>
                                                    </span>
                                                    <span className="text-xs font-mono text-gray-600">#{player.source_id}</span>
                                                </button>
                                            );
                                        })}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                )}

                {apiHelpOpen && (
                    <div className="fixed inset-0 z-[120] flex items-center justify-center bg-black/75">
                        <div className="max-h-[88vh] w-[680px] max-w-[calc(100vw-28px)] overflow-auto rounded-md border border-gray-700 bg-[#181818] shadow-2xl">
                            <div className="flex items-center justify-between border-b border-gray-800 px-5 py-4">
                                <div>
                                    <div className="text-base font-black text-white">{t("apiLimitTitle")}</div>
                                    <div className="mt-1 text-xs text-gray-500">{t("apiLimitSubtitle")}</div>
                                </div>
                                <button onClick={() => setApiHelpOpen(false)} className="text-gray-500 hover:text-white" title={t("close")}>
                                    <XCircle size={20} />
                                </button>
                            </div>
                            <div className="space-y-4 p-5 text-sm text-gray-300">
                                <div className="rounded border border-yellow-500/30 bg-yellow-950/20 px-3 py-2 text-xs leading-relaxed text-yellow-100/90">
                                    {t("apiDisclosure")}
                                </div>

                                <div className="space-y-2">
                                    <div className="font-black text-white">{t("apiTokenInstructionsTitle")}</div>
                                    <div className="text-xs leading-relaxed text-gray-400">
                                        {t("apiTokenInstructionsBody")}
                                    </div>
                                    <div className="grid gap-2">
                                        <CopyValue value="https://www.fflogs.com/api/clients/" label={t("apiClientPageLabel")} t={t} />
                                        <CopyValue value="M-Spec personal import" label={t("apiClientNameLabel")} t={t} />
                                        <CopyValue value="https://raalm.com/m-spec/main_menu.html#" label={t("apiRedirectUrlLabel")} t={t} />
                                        <div className="rounded border border-gray-800 bg-black/25 p-2">
                                            <div className="mb-1 text-[10px] font-black uppercase tracking-wide text-gray-500">{t("apiPublicClientLabel")}</div>
                                            <div className="text-xs text-gray-300">{t("apiPublicClientValue")}</div>
                                        </div>
                                    </div>
                                </div>

                                <div className="border-t border-gray-800 pt-4">
                                    <div className="mb-2 text-xs font-bold uppercase tracking-wide text-gray-500">{t("apiTokenInputLabel")}</div>
                                    <div className="grid gap-2 sm:grid-cols-[1fr_1fr_auto]">
                                        <input
                                            value={manualFflogsClientId}
                                            onChange={(e) => setManualFflogsClientId(e.target.value)}
                                            placeholder={t("apiClientIdPlaceholder")}
                                            className="min-w-0 flex-1 rounded border border-gray-700 bg-black/40 px-3 py-2 text-sm text-white outline-none focus:border-[#00FF96]"
                                        />
                                        <input
                                            value={manualFflogsClientSecret}
                                            onChange={(e) => setManualFflogsClientSecret(e.target.value)}
                                            placeholder={t("apiClientSecretPlaceholder")}
                                            className="min-w-0 flex-1 rounded border border-gray-700 bg-black/40 px-3 py-2 text-sm text-white outline-none focus:border-[#00FF96]"
                                        />
                                        <button onClick={saveManualFflogsToken} className="rounded-sm border border-gray-700 px-3 py-1.5 text-sm font-bold text-gray-300 hover:border-[#00FF96] hover:text-white">
                                            {t("save")}
                                        </button>
                                    </div>
                                </div>

                                {userFflogsCredentials.clientId && userFflogsCredentials.clientSecret && (
                                    <div className="flex items-center justify-between rounded border border-[#00FF96]/30 bg-[#00FF96]/10 px-3 py-2 text-xs text-[#00FF96]">
                                        <span>{t("savedUserApiNotice")}</span>
                                        <button onClick={clearUserFflogsToken} className="rounded border border-[#00FF96]/40 px-2 py-1 font-bold hover:bg-[#00FF96]/10">
                                            {t("clear")}
                                        </button>
                                    </div>
                                )}

                                {apiHelpError && (
                                    <div className="rounded border border-red-500/40 bg-red-950/30 px-3 py-2 text-xs text-red-300">
                                        {apiHelpError}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                )}

                {/* Control Bar — 按功能分区:
                    [技能选择: ALL 总开关 + 四类平铺 + OTHERS + LB] [BOSS TIMELINE: 行开关+类型+阶段] [伙伴] | [工具] [视图: 条/标签+折叠+缩放]
                    移动端: 整块收起, 只留一行紧凑控件 (点"控制"展开) */}
                <div className="bg-[#181818] border-b border-gray-800 px-2 sm:px-4 py-2 shrink-0 flex flex-wrap items-start gap-x-4 gap-y-2 overflow-visible no-scrollbar shadow-md z-[5000]">
                    {isMobile && (
                        <div className="flex w-full items-center gap-1.5">
                            <button
                                onClick={() => setControlsOpen(v => !v)}
                                className={`flex h-7 items-center gap-1.5 px-2 rounded border text-[11px] font-bold uppercase tracking-wide transition-colors ${
                                    controlsOpen
                                        ? 'bg-[#00FF96]/10 border-[#00FF96] text-[#00FF96]'
                                        : 'bg-[#111] border-gray-700/80 text-gray-400'
                                }`}
                            >
                                <SlidersHorizontal size={13} />
                                <span>{t("controls")}</span>
                                <ChevronDown size={12} className={`transition-transform ${controlsOpen ? 'rotate-180' : ''}`} />
                            </button>
                            <div className="ml-auto flex items-center gap-1.5">
                                {rowCollapseButton}
                                {zoomCluster}
                            </div>
                        </div>
                    )}
                    {controlsVisible && (<>
                    {/* 技能分类筛选: 核心四类 (CD/单减/团减/功能) 平铺展示 —— 这是页面的
                        主角; 只有条目多的 OTHERS 用"计数按钮 + 弹出面板"收纳。
                        ALL 是技能选择的总开关, 所以放在这个区的最前面 */}
                    <div className="flex min-w-0 flex-1 flex-wrap items-start gap-x-5 gap-y-2" ref={otherMenuRef}>
                        {!isCombined && (
                            <div className="flex flex-col gap-1">
                                <span className="h-[15px]"></span>
                                <div className="flex h-8 items-center">
                                    <button
                                        title={selectedSpells.size > 0 ? t("hideAllSpells") : t("showAllSpells")}
                                        onClick={toggleAllSpells}
                                        className={displayToggleClass(selectedSpells.size > 0)}
                                    >
                                        {t("all")}
                                    </button>
                                </div>
                            </div>
                        )}
                        {!isCombined && Object.entries(spellCategories).map(([catKey, category]) => {
                            const categorySpells = spellsByCategory[catKey] || [];
                            const selectedCount = getSelectedDisplaySpellCount(spells, selectedSpells, catKey);
                            const isMenuOpen = openSpellMenuCat === catKey;
                            if (catKey !== "OTHER") {
                                return (
                                    <div key={catKey} className="flex flex-col gap-1">
                                        <div className="flex items-center gap-1 text-[10px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:text-white" onClick={() => toggleCategory(catKey)}>
                                            <CategoryIcon type={category.iconType} /> {getCategoryLabel(category, t)}
                                        </div>
                                        <div className="flex flex-wrap items-center gap-1.5">
                                            {categorySpells.map(spell => {
                                                const isSelected = isSpellSlotSelected(spells, selectedSpells, spell);
                                                return (
                                                    <button
                                                        key={spell.id}
                                                        onClick={() => toggleSpell(spell.id)}
                                                        className={`relative w-8 h-8 rounded border transition-all duration-200 group overflow-hidden ${isSelected ? 'border-transparent opacity-100 shadow-[0_0_10px_rgba(255,255,255,0.1)] grayscale-0' : 'border-gray-800 opacity-30 grayscale hover:opacity-70 hover:border-gray-600'}`}
                                                        title={spell.name}
                                                    >
                                                        <RenderIcon spell={spell} />
                                                    </button>
                                                );
                                            })}
                                        </div>
                                    </div>
                                );
                            }
                            return (
                                <div key={catKey} className="relative flex flex-col gap-1">
                                    <div
                                        className="flex items-center gap-1 text-[10px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:text-white"
                                        onClick={() => toggleCategory(catKey)}
                                        title={t("all")}
                                    >
                                        <CategoryIcon type={category.iconType} /> {getCategoryLabel(category, t)}
                                    </div>
                                    <div className="flex h-8 items-center">
                                        <button
                                            onClick={(event) => {
                                                event.stopPropagation();
                                                setOpenSpellMenuCat(prev => prev === catKey ? null : catKey);
                                            }}
                                            className={`h-7 min-w-[54px] px-2 flex items-center justify-center gap-1 rounded border text-[11px] font-bold tracking-wide transition-all ${
                                                selectedCount > 0
                                                    ? 'bg-[#00FF96]/10 border-[#00FF96] text-[#00FF96] shadow-[inset_0_0_0_1px_rgba(0,255,150,0.12)]'
                                                    : 'bg-[#111] border-gray-700/80 text-gray-500 hover:border-gray-500 hover:text-gray-300'
                                            }`}
                                            title={getCategoryLabel(category, t)}
                                        >
                                            {selectedCount}/{categorySpells.length}
                                            <ChevronDown size={11} className={`transition-transform ${isMenuOpen ? 'rotate-180' : ''}`} />
                                        </button>
                                    </div>
                                    {isMenuOpen && (
                                        <div
                                            className="absolute top-full left-0 mt-2 z-[6500] w-[420px] max-w-[calc(100vw-2rem)] rounded-md border border-gray-700 bg-[#151515] p-3 shadow-2xl"
                                            onClick={(event) => event.stopPropagation()}
                                        >
                                            <div className="mb-2 flex items-center justify-between border-b border-gray-800 pb-2">
                                                <div>
                                                    <div className="flex items-center gap-1 text-xs font-black uppercase tracking-wide text-white">
                                                        <CategoryIcon type={category.iconType} /> {getCategoryLabel(category, t)}
                                                    </div>
                                                    <div className="text-[10px] font-mono text-gray-500">{selectedCount} / {categorySpells.length} {t("shown")}</div>
                                                </div>
                                                <button
                                                    onClick={() => toggleCategory(catKey)}
                                                    className="h-7 px-2.5 rounded border border-gray-700/80 text-[11px] font-bold uppercase tracking-wide text-gray-400 hover:border-[#00FF96] hover:text-white transition-colors"
                                                >
                                                    {t("all")}
                                                </button>
                                            </div>
                                            <div className="max-h-[360px] overflow-y-auto pr-1 custom-scrollbar">
                                                <div className="grid grid-cols-8 gap-1.5">
                                                    {categorySpells.map(spell => {
                                                        const isSelected = isSpellSlotSelected(spells, selectedSpells, spell);
                                                        return (
                                                            <button
                                                                key={spell.id}
                                                                onClick={() => toggleSpell(spell.id)}
                                                                className={`relative h-8 w-8 rounded border transition-all duration-200 group overflow-hidden ${isSelected ? 'border-transparent opacity-100 shadow-[0_0_10px_rgba(255,255,255,0.1)] grayscale-0' : 'border-gray-800 opacity-30 grayscale hover:opacity-70 hover:border-gray-600'}`}
                                                                title={spell.name}
                                                            >
                                                                <RenderIcon spell={spell} />
                                                            </button>
                                                        );
                                                    })}
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            );
                        })}

                        <div className="flex flex-col gap-1">
                            <div className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">
                                {t("limitBreak")}
                            </div>
                            <button
                                title={t("showLimitBreak")}
                                onClick={() => setShowLimitBreak(prev => !prev)}
                                className={`relative h-8 w-8 overflow-hidden rounded border transition ${
                                    showLimitBreak
                                        ? 'border-[#00FF96] opacity-100 shadow-[0_0_10px_rgba(0,255,150,0.12)] grayscale-0'
                                        : 'border-gray-800 opacity-30 grayscale hover:opacity-70 hover:border-gray-600'
                                }`}
                            >
                                <img src={LIMIT_BREAK_ICON} alt="Limit Break" draggable={false} className="h-full w-full object-cover" />
                            </button>
                        </div>

                        {isBuddySupported && (
                            <div className="flex flex-col gap-1 border-l border-gray-700 pl-4 shrink-0" ref={buddyMenuRef}>
                                <div className="flex items-center gap-1 text-[10px] font-bold text-gray-500 uppercase tracking-wider">
                                    {t("party")}
                                </div>
                                <div className="flex items-center gap-0.5 h-8">
                                    {selectedSpec === 'dancer-dancer' && (
                                        <button
                                            title={t("zoomTechnicalTangoWindow")}
                                            onClick={() => {
                                                setShowBuddy(true);
                                                setShowDancerTangoBuddyWindow(prev => !prev);
                                            }}
                                            disabled={!rankData.some(rowHasDancerTangoWindow)}
                                            className={`${displayToggleClass(showDancerTangoBuddyWindow)} px-3 disabled:cursor-not-allowed disabled:opacity-35`}
                                        >
                                            {t("technicalTangoWindow")}
                                        </button>
                                    )}
                                    {!isCombined && (
                                        <button
                                            title={t("showBuddy")}
                                            onClick={() => setShowBuddy(prev => !prev)}
                                            className={`${displayToggleClass(showBuddy)} px-3`}
                                        >
                                            {t("buddy")}
                                        </button>
                                    )}
                                    {(isCombined || showBuddy) && buddySpecOptions.map(specInfo => {
                                        const spellMap = buddySpellMaps[specInfo.id] || {};
                                        const selectedIds = buddySpellSelections[specInfo.id] || new Set();
                                        const specName = getLocalizedSpecName(specInfo.id, uiLanguage);
                                        const selectedBuddyDisplayCount = getSelectedDisplaySpellCount(spellMap, selectedIds);
                                        return (
                                            <div key={`buddy-filter-${specInfo.id}`} className="relative">
                                                <button
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        setBuddySpellMenuSpec(prev => prev === specInfo.id ? null : specInfo.id);
                                                    }}
                                                    className={`h-8 min-w-[30px] border-0 bg-transparent p-0 overflow-visible rounded-sm transition flex items-center justify-center ${selectedBuddyDisplayCount > 0 ? 'opacity-100' : 'opacity-35 grayscale hover:opacity-70'}`}
                                                    title={`${specName} buddy spells`}
                                                >
                                                    <img src={`./images/classes/${specInfo.icon}`} alt={specName} draggable={false} className="h-7 w-7 rounded-sm object-cover shadow-sm" />
                                                </button>
                                                {buddySpellMenuSpec === specInfo.id && (
                                                    <div
                                                        className="absolute top-full right-0 mt-2 z-[6000] w-[360px] rounded-md border border-gray-700 bg-[#151515] p-3 shadow-2xl"
                                                        onClick={(e) => e.stopPropagation()}
                                                    >
                                                        <div className="mb-2 flex items-center justify-between border-b border-gray-800 pb-2">
                                                            <div className="flex min-w-0 items-center gap-2">
                                                                <img src={`./images/classes/${specInfo.icon}`} alt="" draggable={false} className="h-6 w-6 rounded-sm object-cover" />
                                                                <div className="min-w-0">
                                                                    <div className="truncate text-xs font-bold text-white">{specName}</div>
                                                                    <div className="text-[10px] font-mono text-gray-500">{selectedBuddyDisplayCount} {t("shown")}</div>
                                                                </div>
                                                            </div>
                                                            <button
                                                                onClick={() => toggleAllBuddySpells(specInfo.id)}
                                                                className="h-7 px-2.5 rounded border border-gray-700/80 text-[11px] font-bold uppercase tracking-wide text-gray-400 hover:border-[#00FF96] hover:text-white transition-colors"
                                                            >
                                                                {t("all")}
                                                            </button>
                                                        </div>
                                                        <div className="space-y-3">
                                                            {Object.entries(spellCategories).map(([catKey, category]) => {
                                                                const categorySpells = getDisplaySpells(spellMap)
                                                                    .filter(spell => spell.category === catKey)
                                                                    .sort((a, b) => a.load_order - b.load_order);
                                                                if (!categorySpells.length) return null;
                                                                return (
                                                                    <div key={`buddy-cat-${specInfo.id}-${catKey}`} className="space-y-1">
                                                                        <button
                                                                            onClick={() => toggleBuddyCategory(specInfo.id, catKey)}
                                                                            className="flex items-center gap-1 text-[10px] font-bold uppercase tracking-wide text-gray-500 hover:text-white"
                                                                        >
                                                                            <CategoryIcon type={category.iconType} /> {getCategoryLabel(category, t)}
                                                                        </button>
                                                                        <div className="flex flex-wrap gap-1.5">
                                                                            {categorySpells.map(spell => {
                                                                                const isSelected = isSpellSlotSelected(spellMap, selectedIds, spell);
                                                                                return (
                                                                                    <button
                                                                                        key={`buddy-spell-${specInfo.id}-${spell.id}`}
                                                                                        onClick={() => toggleBuddySpell(specInfo.id, spell.id)}
                                                                                        className={`h-8 w-8 overflow-hidden rounded border transition ${isSelected ? 'border-transparent opacity-100 grayscale-0' : 'border-gray-800 opacity-30 grayscale hover:opacity-70 hover:border-gray-600'}`}
                                                                                        title={spell.name}
                                                                                    >
                                                                                        <RenderIcon spell={spell} />
                                                                                    </button>
                                                                                );
                                                                            })}
                                                                        </div>
                                                                    </div>
                                                                );
                                                            })}
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        )}

                        {/* BOSS TIMELINE: 同一个功能的所有开关放在一起 ——
                            行显示开关(boss头像) + 事件类型(MECH/TB/AOE) + 阶段线(PHASES) */}
                        <div className="flex flex-col gap-1 border-l border-gray-700 pl-4 shrink-0">
                            <div className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">
                                {t("bossTimeline")}
                            </div>
                            <div className="flex items-center gap-1 h-8">
                                <div className={`w-8 h-8 mr-1 rounded border-2 overflow-hidden cursor-pointer transition ${showBossRow ? 'border-[#00FF96] opacity-100' : 'border-gray-700 opacity-50 grayscale'}`} onClick={() => setShowBossRow(!showBossRow)} title={t("showBossRow")}>
                                    <img src="./images/classes/inv_achievement_raiddragon_sarkareth.jpg" alt="Boss" draggable={false} className="w-full h-full object-cover" />
                                </div>
                                {Object.entries(BOSS_TIMELINE_TYPES).map(([type, config]) => {
                                    const active = bossTimelineTypeVisibility[type];
                                    return (
                                        <button
                                            key={`boss-timeline-toggle-${type}`}
                                            title={`${t("showBossTimelineType")} ${getBossTimelineTypeLabel(type, t)}`}
                                            onClick={() => toggleBossTimelineType(type)}
                                            className="h-7 min-w-[40px] px-2 flex items-center justify-center rounded border text-[11px] font-bold uppercase tracking-wide transition-colors"
                                            style={{
                                                borderColor: active ? config.color : '#374151',
                                                color: active ? config.color : '#6b7280',
                                                backgroundColor: active ? `${config.color}1f` : '#111'
                                            }}
                                        >
                                            {getBossTimelineTypeLabel(type, t)}
                                        </button>
                                    );
                                })}
                                <button title={t("phases")} onClick={() => setShowPhases(!showPhases)} className={displayToggleClass(showPhases)}>{t("phases")}</button>
                            </div>
                        </div>

                        {/* NEW: Global Toggle */}
                        <div className="hidden">
                            <div 
                                className="hidden" 
                                onClick={toggleAllSpells}
                                title={selectedSpells.size > 0 ? "隐藏所有技能" : "显示所有技能"}
                            >
                                <span className="flex items-center gap-1">
                                    <SlidersHorizontal size={14} />
                                    {t("all")}
                                </span>
                            </div>
                            <div className="flex items-center gap-1.5 h-8">
                                <button
                                    onClick={toggleAllSpells}
                                    className={`h-8 px-3 flex items-center justify-center rounded border text-[11px] font-black tracking-wide transition-all ${selectedSpells.size > 0 ? 'bg-white/10 border-gray-500 text-white' : 'bg-transparent border-gray-800 text-gray-500 hover:border-gray-600 hover:text-white'}`}
                                >
                                    {t("all")}
                                </button>
                            </div>
                        </div>

                    </div>
                    <div className="hidden flex-1"></div>
                    {/* 工具组: 从顶部导航下放, 紧凑样式, 不与主角 (技能分类) 抢戏。
                        窄屏允许换行, 否则 375px 下最后一个按钮会被裁掉 */}
                    <div className="flex flex-wrap items-center gap-1.5 self-center sm:ml-auto sm:flex-nowrap sm:shrink-0">
                        <CompositionFilter activeFilterSpecs={activeFilterSpecs} onApply={setActiveFilterSpecs} t={t} uiLanguage={uiLanguage} />
                        <KillTimeFilter filterRange={killTimeRange} onApply={setKillTimeRange} t={t} />
                        <button
                            onClick={() => {
                                setImportModalOpen(true);
                                setImportError("");
                            }}
                            className="flex h-7 items-center gap-1.5 px-2 border border-gray-700/80 rounded text-xs text-gray-400 hover:border-[#00FF96] hover:text-white transition-colors bg-black/30"
                            title={t("importLog")}
                        >
                            <ExternalLink size={13} />
                            <span>{t("importLog")}</span>
                        </button>
                        {/* Curation Buttons */}
                        {!isSelectionMode && !isCurated && (
                            <button
                                onClick={() => { setIsSelectionMode(true); setSelectedRowIds(new Set()); }}
                                className="flex h-7 items-center gap-1.5 px-2 border border-gray-700/80 rounded text-xs text-gray-400 hover:border-[#00FF96] hover:text-white transition-colors bg-black/30"
                                title={t("enterCuration")}
                            >
                                <MousePointer2 size={13} />
                                <span>{t("select")}</span>
                            </button>
                        )}
                        {isSelectionMode && (
                            <div className="flex items-center gap-1.5 animate-in fade-in zoom-in duration-200">
                                <span className="text-xs font-bold text-[#3B82F6]">
                                    {t("selected")}: {selectedRowIds.size}
                                </span>
                                <button
                                    onClick={handleConfirmSelection}
                                    className="flex h-7 items-center gap-1 px-2 bg-[#3B82F6] text-white font-bold rounded text-xs hover:bg-blue-600 transition-colors"
                                >
                                    <CheckCircle2 size={13} />
                                    <span>{t("confirm")}</span>
                                </button>
                                <button
                                    onClick={() => setIsSelectionMode(false)}
                                    className="flex h-7 items-center gap-1 px-2 border border-red-500/50 text-red-400 rounded text-xs hover:bg-red-500/10 transition-colors"
                                >
                                    <XCircle size={13} />
                                    <span>{t("cancel")}</span>
                                </button>
                            </div>
                        )}
                        {isCurated && (
                            <button
                                onClick={handleExitCuration}
                                className="flex h-7 items-center gap-1.5 px-2 bg-[#3B82F6]/20 border border-[#3B82F6] text-white rounded text-xs hover:bg-[#3B82F6]/30 transition-colors"
                                title={t("exitCuration")}
                            >
                                <CheckCircle2 size={13} className="text-[#3B82F6]" />
                                <span>{t("curated")} ({curatedRowIds.size})</span>
                                <XCircle size={13} className="opacity-50 hover:opacity-100" />
                            </button>
                        )}
                    </div>
                    {/* 视图控制: 绘制开关(持续条/CD条/时间标签); 移动端移到紧凑行外的展开区 */}
                    <div className="flex items-center gap-1.5 shrink-0 self-center">
                        <button title={t("duration")} onClick={() => setShowDuration(!showDuration)} className={displayToggleClass(showDuration)}>{t("duration")}</button>
                        <button title={t("cooldown")} onClick={() => setShowCooldown(!showCooldown)} className={displayToggleClass(showCooldown)}>CD</button>
                        <button title={t("skillTimeLabels")} onClick={() => setShowSkillTimes(!showSkillTimes)} className={displayToggleClass(showSkillTimes)}>TM</button>
                        {!isMobile && (
                            <>
                                <div className="w-px h-4 bg-gray-700 mx-0.5"></div>
                                {rowCollapseButton}
                                <div className="w-px h-4 bg-gray-700 mx-1"></div>
                                {zoomCluster}
                            </>
                        )}
                    </div>
                    </>)}
                </div>

                {/* Timeline Area */}
                <div className="flex-1 flex overflow-hidden relative">
                    {/* canvas 模式的悬浮提示 (替代 DOM 图标的原生 title) */}
                    {RENDER_MODE === 'canvas' && (
                        <div
                            ref={castTooltipRef}
                            className="fixed z-[9999] pointer-events-none rounded border border-gray-700 bg-black/90 px-2 py-1 text-xs font-bold text-white shadow-lg"
                            style={{ display: 'none' }}
                        />
                    )}
                    <div
                        className="flex-1 overflow-auto bg-[#121212] custom-scrollbar relative cursor-grab"
                        ref={scrollContainerRef}
                        onMouseDown={onMouseDown}
                        onDragStart={onDragStart}
                        onScroll={handleTimelineScroll}
                        // 触摸设备没有 hover: tap 合成的 mousemove 会让提示弹出后一直卡着,
                        // 所以移动端不挂悬浮提示 (改用点击图标聚焦)
                        onMouseMove={RENDER_MODE === 'canvas' && !isMobile ? handleCanvasTooltipMove : undefined}
                        onMouseLeave={RENDER_MODE === 'canvas' && !isMobile ? hideCastTooltip : undefined}
                    >
                        {/* Canvas 渲染层: 放在滚动内容内部, 随内容被合成器原生滚动,
                            与 DOM 刻度/相位线像素级同步; 位置/尺寸由 drawCastCanvas 按
                            当前滚动位置分块设置 (z 序: 行内容 z-10/20 之下 -> 本层 z-[500]
                            -> sticky 左面板 z-[1000] -> 标尺 z-[3000]) */}
                        {RENDER_MODE === 'canvas' && (
                            <canvas ref={castCanvasRef} className="pointer-events-none absolute z-[500]" />
                        )}
                        <div className="min-w-fit pb-10" ref={timelineContentRef}>

                            {/* Sticky Header: Time Ruler */}
                            <div className="sticky top-0 z-[3000] flex h-8 bg-[#202020] border-b border-gray-700/80 shadow-[0_2px_8px_rgba(0,0,0,0.35)]">
                                <div className="sticky left-0 bg-[#202020] border-r border-gray-700/90 shrink-0 flex items-center px-3 text-[11px] font-bold text-gray-500 uppercase z-[3100] left-cell-shadow" style={{ width: `${leftPanelWidth}px` }}>
                                    <button
                                        onClick={() => setLeftPanelCollapsed(prev => !prev)}
                                        className="mr-2 flex h-6 w-6 shrink-0 items-center justify-center rounded border border-gray-700 text-gray-400 hover:border-[#00FF96] hover:text-[#00FF96]"
                                        title={leftPanelCollapsed ? t("expandLeftPanel") : t("collapseLeftPanel")}
                                    >
                                        {leftPanelCollapsed ? <Maximize2 size={13} /> : <Minimize2 size={13} />}
                                    </button>
                                    {!leftPanelCollapsed && (
                                        <>
                                            <div className="w-8 text-center mr-2 text-[#00FF96]">{t("rank")}</div>
                                            <div className="flex-1 text-left">{t("rdps")}</div>
                                            <div className="w-8 text-center text-gray-600">{t("reg")}</div>
                                            <div className="w-8 text-center text-gray-600">{isCombined ? t("spec") : t("pair")}</div>
                                            <div className="w-8 text-center text-gray-600 ml-1">{t("buffs")}</div>
                                        </>
                                    )}
                                </div>
                                <div
                                    className="relative h-full"
                                    style={{ width: `${timelineWidth}px` }}
                                    onMouseDown={onRulerMouseDown}
                                >
                                    {timeRangeSelection && (
                                        <div
                                            ref={selectionOverlayRef}
                                            className="absolute top-0 bottom-0 z-[3200] rounded-sm border border-[#00FF96] bg-[#00FF96]/15 pointer-events-none"
                                            style={{
                                                left: `${Math.min(timeRangeSelection.startTime, timeRangeSelection.endTime) * zoom}px`,
                                                width: `${Math.max(2, Math.abs(timeRangeSelection.endTime - timeRangeSelection.startTime) * zoom)}px`
                                            }}
                                        />
                                    )}
                                    {/* UPDATED: Dynamic Ticks (Feature 1) */}
                                    {rulerTicks.map(({ time, isMajor }, i) => {
                                        // 横向虚拟化: 高缩放下刻度上千个, 窗口外的不渲染
                                        if (time < cullT0 || time > cullT1) return null;
                                        return (
                                            <div 
                                                key={i} 
                                                className="absolute inset-y-0"
                                                style={{ left: `${time * zoom}px` }}
                                            >
                                                <div className={`absolute bottom-0 border-l ${isMajor ? 'border-gray-500/90 h-4' : 'border-gray-700/80 h-2'}`} />
                                                {isMajor && (
                                                    <span
                                                        className="absolute inset-y-0 left-1.5 flex items-center text-[13px] leading-none text-gray-200 font-bold tabular-nums select-none pointer-events-none"
                                                        style={{ fontVariantNumeric: 'tabular-nums' }}
                                                    >
                                                        {formatTime(time)}
                                                    </span>
                                                )}
                                            </div>
                                        );
                                    })}
                                    {showPhases && timelinePhases.map((phase, i) => (
                                        <div
                                            key={`ruler-phase-${i}`}
                                            className="absolute inset-y-0 z-20"
                                            style={{ left: `${phase.timestamp * zoom}px` }}
                                            title={`${phase.name} (${formatTime(phase.timestamp)}) - ${phaseAlignIndex === i ? t("clearPhaseAlignment") : t("alignPhase")}`}
                                        >
                                            <div
                                                className="absolute top-0 bottom-0 border-l-2 pointer-events-none"
                                                style={{ borderColor: phase.color || "rgba(0,255,150,0.9)" }}
                                            />
                                            <button
                                                type="button"
                                                onClick={(event) => {
                                                    event.stopPropagation();
                                                    togglePhaseAlignment(i);
                                                }}
                                                className={`absolute left-1 top-0.5 rounded-sm border px-1 text-[10px] font-black leading-tight shadow-sm whitespace-nowrap transition ${
                                                    phaseAlignIndex === i
                                                        ? 'bg-[#00FF96] text-black border-[#00FF96]'
                                                        : 'text-[#d6fff0] bg-black/85 hover:bg-[#00FF96]/20'
                                                }`}
                                                style={{ borderColor: phaseAlignIndex === i ? "#00FF96" : (phase.color || "rgba(0,255,150,0.65)") }}
                                            >
                                                P{i + 1}
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Timeline Grid */}
                            <div
                                className="absolute top-8 bottom-0 pointer-events-none z-[1]"
                                style={{ left: `${leftPanelWidth}px`, width: `${timelineWidth}px`, ...rowGridStyle }}
                            />

                            {/* Phase Lines */}
                            {showPhases && timelinePhases.length > 0 && (
                                <div className="absolute top-8 bottom-0 right-0 pointer-events-none z-[260]" style={{ left: `${leftPanelWidth}px` }}>
                                    {timelinePhases.map((phase, i) => (
                                        <div
                                            key={i}
                                            className="absolute top-0 bottom-0 border-l-2 border-dashed"
                                            style={{
                                                left: `${phase.timestamp * zoom}px`,
                                                borderColor: 'rgba(0,255,150,0.42)'
                                            }}
                                        />
                                    ))}
                                </div>
                            )}

                            {/* Boss Timeline - Explicitly placed above players */}
                            {showBossRow && (
                                // canvas 模式下 z 要高于画布(500), 否则滚动时下方行的技能会画穿这条 sticky 行
                                <div className={`flex h-10 border-b border-gray-800/60 bg-[#151515] hover:bg-[#1a1a1a] transition-colors group relative sticky top-8 ${RENDER_MODE === 'canvas' ? 'z-[600]' : 'z-40'}`}>
                                    <div className="sticky left-0 bg-[#181818] border-r border-gray-700/90 shrink-0 flex items-center px-3 z-[1000] left-cell-shadow" style={{ width: `${leftPanelWidth}px` }}>
                                        <div className={`font-bold text-gray-300 ${leftPanelCollapsed ? 'w-full text-center text-[10px]' : 'flex-1'}`}>
                                            {leftPanelCollapsed ? 'B' : t("bossTimeline")}
                                        </div>
                                    </div>
                                    <div className="relative h-full z-10 overflow-hidden" style={{ width: `${timelineWidth}px` }}>
                                        {bossTimelineMechanics.map((mech, i) => {
                                            const mechName = getLocalizedBossTimelineName(mech, uiLanguage);
                                            const displayTime = Number(mech.displayTime ?? mech.time ?? 0);
                                            return mech.duration > 0 ? (
                                                /* Standard Boss Bar for duration mechanics */
                                                <div 
                                                    key={i} 
                                                    className="absolute top-1/2 -translate-y-1/2 h-7 rounded-sm border border-white/15 flex items-center justify-center text-[13px] font-bold text-white/95 overflow-hidden shadow-sm" 
                                                    style={{ left: `${displayTime * zoom}px`, width: `${Math.max(mech.duration * zoom, 48)}px`, backgroundColor: getBossTimelineColor(mech.type, mech.color) }} 
                                                    title={`${getBossTimelineTypeLabel(mech.type, t) || t("boss")}: ${mechName} (${formatTime(displayTime)}) - ${mech.duration}s`}
                                                >
                                                    <span className="block max-w-full overflow-hidden whitespace-nowrap px-2 leading-none drop-shadow-[0_1px_1px_rgba(0,0,0,0.75)]">{mechName}</span>
                                                </div>
                                            ) : (
                                                /* Icon Box for instant mechanics */
                                                <div 
                                                    key={i} 
                                                    className="absolute top-1/2 -translate-y-1/2 h-6 w-6 rounded border border-white/20 flex items-center justify-center shadow-sm overflow-hidden" 
                                                    style={{ left: `${displayTime * zoom}px`, backgroundColor: getBossTimelineColor(mech.type, mech.color) }}
                                                    title={`${getBossTimelineTypeLabel(mech.type, t) || t("boss")}: ${mechName} (${formatTime(displayTime)})`}
                                                >
                                                    <RenderIcon spell={{ ...mech, name: mechName }} />
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            )}

                            {/* Imported User Log Rows */}
                            {importedRowModels.map(({
                                importedRow,
                                rowPhases,
                                sameSpecAsTimeline,
                                importedSpellMap,
                                importedVisibleSpellIds,
                                importedVisibleDisplaySpellCount,
                                processedImportedCasts,
                                totalHeight,
                                specInfo,
                                specName,
                                endLabel,
                                percentLabel
                            }) => {
                                const trackHeight = 30;
                                // 横向虚拟化: 相位偏移每行恒定
                                const rowPhaseOffset = getPhaseOffset(rowPhases);

                                return (
                                    <div
                                        key={importedRow.id}
                                        ref={registerCastRowRef(`imported-${importedRow.id}`, {
                                            casts: processedImportedCasts,
                                            totalHeight,
                                            trackHeight,
                                            rowPhases,
                                            killTimeSeconds: importedRow.killTimeSeconds,
                                            durOpacity: 0.9,
                                            fontFactor: 0.62,
                                            textAlpha: 1
                                        })}
                                        onClick={() => {
                                            // canvas 模式: 点击落在技能图标上时不清除聚焦 (对齐 DOM 的 stopPropagation)
                                            if (RENDER_MODE === 'canvas' && canvasIconHitRef.current) return;
                                            setFocusedSpellId(null);
                                        }}
                                        // canvas 模式下行本身不设 z-index (弹出菜单在 sticky 单元格里,
                                        // 由单元格的 z-[8000] 保证盖在 canvas 之上)
                                        className={`flex border-b border-[#00FF96]/20 bg-[#07130f] hover:bg-[#0a1a14] transition-colors group/import relative ${
                                            RENDER_MODE === 'dom' ? (importSpellMenuRowId === importedRow.id ? 'z-[7900]' : 'z-[20]') : ''
                                        }`}
                                        style={{ height: `${totalHeight}px` }}
                                    >
                                        <div className={`sticky left-0 bg-[#0b1713] border-r border-gray-700/90 shrink-0 flex items-center px-3 transition-colors left-cell-shadow ${importSpellMenuRowId === importedRow.id ? 'z-[8000]' : 'z-[1000]'}`} style={{ width: `${leftPanelWidth}px` }}>
                                            {leftPanelCollapsed ? (
                                                <div className="w-full text-center text-[9px] font-black uppercase text-[#00FF96]">LOG</div>
                                            ) : (
                                                <div className="flex min-w-0 flex-1 flex-col">
                                                    <span className="text-[9px] font-black uppercase leading-none text-[#00FF96]">{t("importedLog")}</span>
                                                    <span className="truncate text-[13px] font-bold leading-tight text-white">{importedRow.name}</span>
                                                </div>
                                            )}
                                            {!leftPanelCollapsed && !sameSpecAsTimeline && (
                                                <div className="relative ml-2">
                                                    <button
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            setImportSpellMenuRowId(importSpellMenuRowId === importedRow.id ? null : importedRow.id);
                                                        }}
                                                        className="flex h-6 items-center gap-1 rounded border border-gray-700 bg-black/30 px-2 text-[11px] font-bold text-gray-300 hover:border-[#00FF96] hover:text-white"
                                                        title={`${specName} spell filters`}
                                                    >
                                                        <SlidersHorizontal size={13} />
                                                        {importedVisibleDisplaySpellCount}
                                                    </button>
                                                    {importSpellMenuRowId === importedRow.id && (
                                                        <div
                                                            className="absolute left-0 top-8 z-[8100] w-[360px] rounded-md border border-gray-700 bg-[#151515] p-3 shadow-2xl"
                                                            onClick={(e) => e.stopPropagation()}
                                                        >
                                                            <div className="mb-2 flex items-center justify-between border-b border-gray-800 pb-2">
                                                                <div className="flex min-w-0 items-center gap-2">
                                                                    <div className="min-w-0">
                                                                        <div className="truncate text-xs font-bold text-white">{specName}</div>
                                                                        <div className="text-[10px] font-mono text-gray-500">{importedVisibleDisplaySpellCount} {t("shown")}</div>
                                                                    </div>
                                                                </div>
                                                                <button
                                                                    onClick={() => toggleAllImportedSpells(importedRow.id, importedSpellMap)}
                                                                    className="h-7 px-2.5 rounded border border-gray-700/80 text-[11px] font-bold uppercase tracking-wide text-gray-400 hover:border-[#00FF96] hover:text-white transition-colors"
                                                                >
                                                                    {t("all")}
                                                                </button>
                                                            </div>
                                                            <div className="space-y-3">
                                                                {Object.entries(spellCategories).map(([catKey, category]) => {
                                                                    const categorySpells = getDisplaySpells(importedSpellMap)
                                                                        .filter(spell => spell.category === catKey)
                                                                        .sort((a, b) => a.load_order - b.load_order);
                                                                    if (!categorySpells.length) return null;
                                                                    return (
                                                                        <div key={`import-cat-${catKey}`} className="space-y-1">
                                                                            <button
                                                                                onClick={() => toggleImportedCategory(importedRow.id, importedSpellMap, catKey)}
                                                                                className="flex items-center gap-1 text-[10px] font-bold uppercase tracking-wide text-gray-500 hover:text-white"
                                                                            >
                                                                                <CategoryIcon type={category.iconType} /> {getCategoryLabel(category, t)}
                                                                            </button>
                                                                            <div className="flex flex-wrap gap-1.5">
                                                                                {categorySpells.map(spell => {
                                                                                    const isSelected = isSpellSlotSelected(importedSpellMap, importedVisibleSpellIds, spell);
                                                                                    return (
                                                                                        <button
                                                                                            key={`import-spell-${spell.id}`}
                                                                                            onClick={() => toggleImportedSpell(importedRow.id, importedSpellMap, spell.id)}
                                                                                            className={`h-8 w-8 overflow-hidden rounded border transition ${isSelected ? 'border-transparent opacity-100 grayscale-0' : 'border-gray-800 opacity-30 grayscale hover:opacity-70 hover:border-gray-600'}`}
                                                                                            title={spell.name}
                                                                                        >
                                                                                            <RenderIcon spell={spell} />
                                                                                        </button>
                                                                                    );
                                                                                })}
                                                                            </div>
                                                                        </div>
                                                                    );
                                                                })}
                                                            </div>
                                                        </div>
                                                    )}
                                                </div>
                                            )}
                                            {!leftPanelCollapsed && <button
                                                onClick={() => {
                                                    const nextImportedRows = importedRows.filter(row => row.id !== importedRow.id);
                                                    const nextImportedSelections = { ...importedSpellSelections };
                                                    delete nextImportedSelections[importedRow.id];
                                                    setImportedRows(nextImportedRows);
                                                    setImportedSpellSelections(nextImportedSelections);
                                                    writeStoredImportedLogs(selectedBoss, nextImportedRows, nextImportedSelections, {
                                                        hideRowIds: [importedRow.id]
                                                    });
                                                    if (importSpellMenuRowId === importedRow.id) setImportSpellMenuRowId(null);
                                                }}
                                                className="ml-2 text-gray-500 hover:text-white"
                                                title={t("removeImportedLog")}
                                            >
                                                <XCircle size={15} />
                                            </button>}
                                        </div>
                                        <div className="relative h-full z-10 overflow-hidden" style={{ width: `${timelineWidth}px` }}>
                                            {showPhases && rowPhases.map((phase, pIdx) => (
                                                <div
                                                    key={`import-phase-${pIdx}`}
                                                    className="absolute top-0 bottom-0 border-l-2 pointer-events-none z-[260]"
                                                    style={{
                                                        left: getAlignedLeft(phase.timestamp, rowPhases),
                                                        width: "36px",
                                                        borderColor: phase.color || "rgba(0,255,150,0.76)",
                                                        background: "linear-gradient(90deg, rgba(0,255,150,0.12), rgba(0,255,150,0))"
                                                    }}
                                                    title={`${phase.name} (${formatTime(phase.timestamp)})`}
                                                >
                                                    <span className="absolute top-0 left-1 rounded border border-[#00FF96]/30 bg-black/85 px-1 text-[10px] font-bold text-[#d6fff0] shadow-sm whitespace-nowrap">
                                                        {phase.name}
                                                    </span>
                                                </div>
                                            ))}

                                            {importedRow.killTimeSeconds > 0 && (
                                                <div
                                                    className="absolute top-0 bottom-0 z-50 flex items-center pointer-events-none"
                                                    style={{ left: getAlignedLeft(importedRow.killTimeSeconds, rowPhases) }}
                                                >
                                                    <div className={`h-full w-[3px] ${importedRow.kill ? 'bg-[#00FF96]/80 shadow-[0_0_8px_rgba(0,255,150,0.6)]' : 'bg-red-500/80 shadow-[0_0_8px_rgba(239,68,68,0.7)]'}`}></div>
                                                    <div className={`ml-1 flex items-center gap-1 rounded border px-1.5 py-0.5 text-[11px] font-black uppercase tracking-wide text-white ${importedRow.kill ? 'border-[#00FF96]/50 bg-[#064a31]/90' : 'border-red-500/50 bg-red-950/90'}`}>
                                                        <Flag size={12} />
                                                        <span>{endLabel}</span>
                                                        <span className="font-mono">{importedRow.killTime}</span>
                                                        {percentLabel && <span className="font-mono text-red-200">{percentLabel}</span>}
                                                    </div>
                                                </div>
                                            )}

                                            {RENDER_MODE === 'dom' && processedImportedCasts.map((cast, cIdx) => {
                                                const isFocusedSpell = isFocusedSpellId(cast.spellId);
                                                // spell/barColor 已在 importedRowModels 里预解析
                                                const spell = cast.spell;
                                                const timeUntilKill = importedRow.killTimeSeconds ? (importedRow.killTimeSeconds - cast.timestamp) : 99999;
                                                if (timeUntilKill <= 0) return null;

                                                // 横向虚拟化: 窗口外的 cast 不渲染 (按真实绘制宽度裁剪)
                                                const alignedCastTime = Number(cast.timestamp || 0) - rowPhaseOffset;
                                                if (alignedCastTime > cullT1 || alignedCastTime + Math.max(cast.duration || 0, spell.cd || 0) + 60 / zoom < cullT0) return null;

                                                const barColor = cast.barColor;
                                                const durationWidth = Math.max(0, Math.min((cast.duration || 0) * zoom, timeUntilKill * zoom));
                                                const cdWidth = Math.max(0, Math.min((spell.cd || 0) * zoom, timeUntilKill * zoom));
                                                const currentTrackHeight = isCollapsed ? totalHeight : trackHeight;
                                                const topPos = isCollapsed ? 0 : cast.trackIndex * trackHeight;
                                                const iconHeight = currentTrackHeight * 0.9;

                                                return (
                                                    <div
                                                        key={`${cast.spellId}-${cast.timestamp}-${cast.trackIndex}`}
                                                        className={`absolute flex items-center group/icon select-none transition-opacity duration-150 ${focusedSpellId && !isFocusedSpell ? 'opacity-25' : 'opacity-100'}`}
                                                        style={{
                                                            left: getAlignedLeft(cast.timestamp, rowPhases),
                                                            top: `${topPos}px`,
                                                            height: `${currentTrackHeight}px`,
                                                            zIndex: isFocusedSpell ? 220 + cIdx : 10 + cIdx
                                                        }}
                                                    >
                                                        <div className="relative h-full flex items-center">
                                                            {showCooldown && spell.cd > 0 && cdWidth > 0 && (
                                                                <div
                                                                    className="absolute top-1/2 -translate-y-1/2 h-1/3 rounded-r-sm z-0"
                                                                    style={{
                                                                        left: `${iconHeight / 2}px`,
                                                                        width: `${cdWidth}px`,
                                                                        backgroundColor: hexToRgba(barColor, 0.2)
                                                                    }}
                                                                />
                                                            )}

                                                            {showDuration && durationWidth > 0 && (
                                                                <div
                                                                    className="absolute left-0 z-10 rounded-sm shadow-sm"
                                                                    style={{
                                                                        width: `${durationWidth}px`,
                                                                        height: `${iconHeight}px`,
                                                                        backgroundColor: barColor,
                                                                        opacity: 0.9
                                                                    }}
                                                                />
                                                            )}

                                                            <div
                                                                onMouseDown={(e) => {
                                                                    handleSpellIconMouseDown(e, cast.spellId);
                                                                }}
                                                                onClick={(e) => {
                                                                    e.stopPropagation();
                                                                }}
                                                                className="relative z-20 flex items-center justify-center overflow-hidden rounded-sm bg-black/50"
                                                                style={{
                                                                    height: `${iconHeight}px`,
                                                                    width: `${iconHeight}px`,
                                                                    minWidth: `${iconHeight}px`,
                                                                    boxShadow: isFocusedSpell ? 'inset 0 0 0 2px #00FF96, -2px 0 0 #00FF96, 2px 0 0 #00FF96' : 'none'
                                                                }}
                                                                title={`${spell.name} (${formatTime(cast.timestamp)})`}
                                                            >
                                                                <RenderIcon spell={spell} className="opacity-100" />
                                                            </div>

                                                            {showSkillTimes && (
                                                                <span
                                                                    className="ml-1 font-bold text-white drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)] z-30 pointer-events-none"
                                                                    style={{ fontSize: `${iconHeight * 0.62}px`, lineHeight: 1 }}
                                                                >
                                                                    {formatTime(cast.timestamp)}
                                                                </span>
                                                            )}
                                                        </div>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </div>
                                );
                            })}

                            {/* Player Rows (渲染模型见 playerRowModels useMemo) */}
                            {playerRowModels.map(({
                                row,
                                processedCasts,
                                totalHeight,
                                buddyRows,
                                showBuddyRow,
                                rowPhases,
                            }) => {
                                const trackHeight = 30; // Height per sub-row when expanded
                                const buddyTrackHeight = trackHeight;

                                // FEATURE 2: Check if this row is selected (MULTI-SELECT SUPPORT)
                                const isSelected = selectedRowIds.has(row.id);

                                // Dynamic styles based on Selection Mode
                                const selectionBorderColor = isSelectionMode ? 'border-[#3B82F6]' : 'border-[#00FF96]';
                                const selectionBg = isSelectionMode ? 'bg-[#3B82F6]/10' : 'bg-[#00FF96]/5';

                                // 横向虚拟化: 相位偏移每行恒定, 提出来给 cast 裁剪用
                                const rowPhaseOffset = getPhaseOffset(rowPhases);

                                return (
                                    <React.Fragment key={row.id}>
                                    <div
                                        key={row.id}
                                        ref={registerCastRowRef(`player-${row.id}`, {
                                            casts: processedCasts,
                                            totalHeight,
                                            trackHeight,
                                            rowPhases,
                                            killTimeSeconds: row.killTimeSeconds,
                                            durOpacity: 0.9,
                                            fontFactor: 0.7,
                                            textAlpha: 1
                                        })}
                                        // FEATURE 2: Row Click & Highlight Logic (MULTI-SELECT)
                                        onClick={(e) => {
                                            // canvas 模式: 点击落在技能图标上时不触发行选中
                                            // (对齐 DOM 模式中图标 onClick 的 stopPropagation)
                                            if (RENDER_MODE === 'canvas' && canvasIconHitRef.current) return;
                                            if (suppressRowClickRef.current) {
                                                e.preventDefault();
                                                return;
                                            }
                                            if (focusedSpellId) {
                                                setFocusedSpellId(null);
                                                return;
                                            }
                                            const newSet = new Set(selectedRowIds);
                                            if (newSet.has(row.id)) {
                                                newSet.delete(row.id);
                                            } else {
                                                newSet.add(row.id);
                                            }
                                            setSelectedRowIds(newSet);
                                        }}
                                        className={`flex hover:bg-[#1a1a1a] transition-colors group relative border-b border-gray-800/40 ${
                                            isSelected
                                            // canvas 模式下不能给行加 z-index: 会创建堆叠上下文,
                                            // 把行内 sticky 面板的 z-1000 困住, 压不过 canvas(z-500)
                                            ? `${selectionBg}${RENDER_MODE === 'dom' ? ' z-10' : ''}` // Removed border changes to prevent layout shift
                                            : ''
                                        }`}
                                        // content-visibility 只用于 DOM 渲染路径 (canvas 模式下它的
                                        // paint containment 同样会创建堆叠上下文, 且行已经很轻)
                                        style={RENDER_MODE === 'dom'
                                            ? { height: `${totalHeight}px`, contentVisibility: 'auto', containIntrinsicSize: `auto ${totalHeight}px` }
                                            : { height: `${totalHeight}px` }}
                                    >
                                        {/* Selection Highlight Overlay - Absolute positioned to avoid layout shift */}
                                        {isSelected && (
                                            <div className={`absolute inset-0 border-t-2 border-b-2 ${selectionBorderColor} pointer-events-none z-[60]`}></div>
                                        )}

                                        {/* Sticky Left Panel - Adjusted for Compact Height */}
                                        <div className="sticky left-0 bg-[#161616] group-hover:bg-[#1e1e1e] border-r border-gray-700/90 shrink-0 flex items-center px-3 z-[1000] transition-colors left-cell-shadow" style={{ width: `${leftPanelWidth}px` }}>
                                            {leftPanelCollapsed ? (
                                                <div className="w-full text-center font-mono text-[11px] font-bold text-gray-400">#{row.rank}</div>
                                            ) : (
                                                <>
                                                    <div className="w-8 text-center mr-2 font-mono text-gray-400 text-sm font-semibold">#{row.rank}</div>
                                                    
                                                    {/* MODIFIED: Use PlayerNameCell for Name/DPS toggle and pass report args */}
                                                    <PlayerNameCell 
                                                        name={row.name} 
                                                        dps={row.dps} 
                                                        reportId={row.reportId} 
                                                        fightId={row.fightId} 
                                                        region={row.region} 
                                                    />
                                                    
                                                    <div className="w-8 text-center text-xs font-mono font-bold text-gray-400 bg-[#222] rounded px-1 py-0.5">{row.region}</div>
                                                    
                                                    {/* Partner Column - Only shows for Tank/Healer */}
                                                    <div className="w-8 text-center flex justify-center items-center ml-1">
                                                        {row.isCombined ? (
                                                            row.combinedPlayers?.[0]?.specSlug && getIconForSpec(row.combinedPlayers[0].specSlug) && (
                                                                <img
                                                                    src={`./images/classes/${getIconForSpec(row.combinedPlayers[0].specSlug)}`}
                                                                    alt={row.combinedPlayers[0].specSlug}
                                                                    draggable={false}
                                                                    className="w-6 h-6 object-contain"
                                                                    title={getLocalizedSpecName(row.combinedPlayers[0].specSlug, uiLanguage)}
                                                                />
                                                            )
                                                        ) : (
                                                            row.partner && <img src={row.partner} alt="P" draggable={false} className="w-6 h-6 object-contain" />
                                                        )}
                                                    </div>

                                                    {/* NEW: Buffs Count Column */}
                                                    <div className="w-8 text-center flex justify-center items-center ml-1 font-mono text-sm text-gray-300 font-bold">
                                                        {row.buffCount}
                                                    </div>
                                                </>
                                            )}
                                        </div>

                                        {/* Right Panel: Casts */}
                                        <div className="relative h-full z-10 overflow-hidden" style={{ width: `${timelineWidth}px` }}>
                                            {showPhases && rowPhases.map((phase, pIdx) => (
                                                <div
                                                    key={`phase-${pIdx}`}
                                                    className="absolute top-0 bottom-0 border-l-2 pointer-events-none z-[260]"
                                                    style={{
                                                        left: getAlignedLeft(phase.timestamp, rowPhases),
                                                        width: "36px",
                                                        borderColor: phase.color || "rgba(0,255,150,0.76)",
                                                        background: "linear-gradient(90deg, rgba(0,255,150,0.12), rgba(0,255,150,0))"
                                                    }}
                                                    title={`${phase.name} (${formatTime(phase.timestamp)})`}
                                                >
                                                    <span className="absolute top-0 left-1 text-[10px] font-bold text-[#d6fff0] whitespace-nowrap bg-black/80 border border-[#00FF96]/30 px-1 rounded shadow-sm">
                                                        {phase.name}
                                                    </span>
                                                </div>
                                            ))}
                                            
                                            {/* REMOVED: Deaths Display */}

                                            {/* Kill Time Marker Logic */}
                                            {row.killTimeSeconds && (
                                                <div 
                                                    className="absolute top-0 bottom-0 z-50 flex flex-col items-center pointer-events-none"
                                                    style={{ left: getAlignedLeft(row.killTimeSeconds, rowPhases) }}
                                                >
                                                    {/* Vertical Line */}
                                                    <div className="h-full w-[2px] bg-red-500/60 shadow-[0_0_8px_rgba(239,68,68,0.6)]"></div>
                                                    
                                                    {/* Label - Positioned like a skill icon but text-only */}
                                                    <div className="absolute top-1/2 -translate-y-1/2 left-1 flex items-center z-50">
                                                        {/* Icon Box */}
                                                        <div
                                                            className="flex items-center justify-center rounded-sm bg-red-900/80 border border-red-500/50"
                                                            style={{
                                                                height: `${(isCollapsed ? totalHeight : trackHeight) * 0.85}px`,
                                                                width: `${(isCollapsed ? totalHeight : trackHeight) * 0.85}px`
                                                            }}
                                                        >
                                                            <Flag size={(isCollapsed ? totalHeight : trackHeight) * 0.85 * 0.6} className="text-white" />
                                                        </div>

                                                        {/* Text */}
                                                        <span 
                                                            className="ml-1 font-bold text-white drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)] whitespace-nowrap"
                                                            style={{ fontSize: `${(isCollapsed ? totalHeight : trackHeight) * 0.85 * 0.7}px`, lineHeight: 1 }}
                                                        >
                                                            {row.killTime}
                                                        </span>
                                                    </div>
                                                </div>
                                            )}

                                            {RENDER_MODE === 'dom' && processedCasts.map((cast, cIdx) => {
                                                const isFocusedSpell = isFocusedSpellId(cast.spellId);
                                                // spell/barColor 已在 playerRowModels 里预解析
                                                const spell = cast.spell;

                                                // --- KILL TIME CLIPPING LOGIC ---
                                                const timeUntilKill = row.killTimeSeconds ? (row.killTimeSeconds - cast.timestamp) : 99999;

                                                // If cast starts AFTER kill, skip it
                                                if (timeUntilKill <= 0) return null;

                                                // 横向虚拟化: 视口窗口外的 cast 不渲染
                                                // (按真实绘制宽度裁剪: 图标从 alignedTime 起, CD/持续条延伸 max(duration, cd);
                                                //  cIdx 保持稳定, 颜色/层级不受影响)
                                                const alignedCastTime = Number(cast.timestamp || 0) - rowPhaseOffset;
                                                if (alignedCastTime > cullT1 || alignedCastTime + Math.max(cast.duration || 0, spell.cd || 0) + 60 / zoom < cullT0) return null;

                                                // Vertical positioning
                                                const currentTrackHeight = isCollapsed ? totalHeight : trackHeight;
                                                const topPos = isCollapsed ? 0 : cast.trackIndex * trackHeight;

                                                // Dimensions - Adjusted for Compactness
                                                const iconHeight = currentTrackHeight * 0.9; 
                                                const rawDurationWidth = (cast.duration || 0) * zoom;
                                                const rawCdWidth = (spell.cd || 0) * zoom;
                                                
                                                // Max allowed width (distance to kill time)
                                                const maxVisibleWidth = timeUntilKill * zoom;

                                                // Clamp widths
                                                const durationWidth = Math.max(0, Math.min(rawDurationWidth, maxVisibleWidth));
                                                const cdWidth = Math.max(0, Math.min(rawCdWidth, maxVisibleWidth));

                                                // Color Assignment (Consistent per spell)
                                                const barColor = cast.barColor;

                                                return (
                                                    <div
                                                        key={`${cast.specSlug || ''}-${cast.spellId}-${cast.timestamp}-${cast.trackIndex}`}
                                                        className={`absolute flex items-center group/icon select-none transition-opacity duration-150 ${focusedSpellId && !isFocusedSpell ? 'opacity-25' : 'opacity-100'}`}
                                                        style={{
                                                            left: getAlignedLeft(cast.timestamp, rowPhases),
                                                            top: `${topPos}px`,
                                                            height: `${currentTrackHeight}px`,
                                                            zIndex: isFocusedSpell ? 220 + cIdx : 10 + cIdx // Right skills cover left skills
                                                        }}
                                                    >
                                                        <div className="relative w-full h-full flex items-center">
                                                            
                                                            {/* 1. Cooldown Bar - CLAMPED */}
                                                            {showCooldown && spell.cd > 0 && cdWidth > 0 && (
                                                                <div 
                                                                    className="absolute top-1/2 -translate-y-1/2 h-1/3 rounded-r-sm z-0"
                                                                    style={{
                                                                        left: `${iconHeight/2}px`, 
                                                                        width: `${cdWidth}px`,
                                                                        backgroundColor: hexToRgba(barColor, 0.2)
                                                                    }}
                                                                />
                                                            )}

                                                            {/* 2. Duration Bar - CLAMPED */}
                                                            {showDuration && durationWidth > 0 && (
                                                                <div
                                                                    className="absolute left-0 z-10 rounded-sm shadow-sm"
                                                                    style={{
                                                                        width: `${durationWidth}px`,
                                                                        height: `${iconHeight}px`,
                                                                        backgroundColor: barColor, // Use palette color
                                                                        opacity: 0.9
                                                                    }}
                                                                />
                                                            )}

                                                            {/* 3. Icon */}
                                                            <div
                                                                onMouseDown={(e) => {
                                                                    handleSpellIconMouseDown(e, cast.spellId);
                                                                }}
                                                                onClick={(e) => {
                                                                    e.stopPropagation();
                                                                }}
                                                                className="relative z-20 flex items-center justify-center overflow-hidden rounded-sm bg-black/50"
                                                                style={{
                                                                    height: `${iconHeight}px`,
                                                                    width: `${iconHeight}px`,
                                                                    minWidth: `${iconHeight}px`,
                                                                    boxShadow: isFocusedSpell ? 'inset 0 0 0 2px #00FF96, -2px 0 0 #00FF96, 2px 0 0 #00FF96' : 'none'
                                                                }}
                                                                title={`${spell.name} (${formatTime(cast.timestamp)})`}
                                                            >
                                                                <RenderIcon spell={spell} className="opacity-100" />
                                                            </div>

                                                            {/* 4. Timestamp Text */}
                                                            {showSkillTimes && (
                                                                <span 
                                                                    className="ml-1 font-bold text-white drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)] z-30 pointer-events-none"
                                                                    style={{ fontSize: `${iconHeight * 0.7}px`, lineHeight: 1 }}
                                                                >
                                                                    {formatTime(cast.timestamp)}
                                                                </span>
                                                            )}

                                                        </div>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </div>
                                    {showBuddyRow && buddyRows.map(({
                                        buddy,
                                        buddyIdx,
                                        buddySpellMap,
                                        buddyColorMap,
                                        processedBuddyCasts,
                                        buddyTotalHeight
                                    }) => (
                                        <div
                                            key={`buddy-row-${row.id}-${buddy.sourceId || buddyIdx}-${buddy.specSlug || ""}`}
                                            className="flex bg-[#101614] hover:bg-[#13201b] transition-colors group/buddy relative border-t border-gray-800/40"
                                            style={RENDER_MODE === 'dom'
                                                ? { height: `${buddyTotalHeight}px`, contentVisibility: 'auto', containIntrinsicSize: `auto ${buddyTotalHeight}px` }
                                                : { height: `${buddyTotalHeight}px` }}
                                            ref={registerCastRowRef(`buddy-${row.id}-${buddyIdx}`, {
                                                casts: processedBuddyCasts,
                                                totalHeight: buddyTotalHeight,
                                                trackHeight: buddyTrackHeight,
                                                rowPhases,
                                                killTimeSeconds: row.killTimeSeconds,
                                                durOpacity: 0.88,
                                                fontFactor: 0.58,
                                                textAlpha: 0.9
                                            })}
                                        >
                                            <div className="sticky left-0 bg-[#101614] group-hover/buddy:bg-[#13201b] border-r border-gray-700/90 shrink-0 flex items-center px-3 z-[1000] transition-colors left-cell-shadow" style={{ width: `${leftPanelWidth}px` }}>
                                                {leftPanelCollapsed ? (
                                                    <div className="w-full text-center text-[10px] font-black uppercase tracking-wide text-gray-600">
                                                        {row.isCombined ? 'P' : 'B'}
                                                    </div>
                                                ) : (
                                                    <>
                                                        <div className="w-8 text-center mr-2 text-[10px] font-black uppercase tracking-wide text-gray-600">
                                                            {row.isCombined ? t("pair") : t("buddy")}
                                                        </div>
                                                        <div className="flex h-full min-w-0 flex-1 items-center">
                                                            {row.isCombined ? (
                                                                <div className="min-w-0 truncate text-xs font-bold text-gray-600">
                                                                    {buddy.name}
                                                                </div>
                                                            ) : (
                                                                <BuddyNameCell
                                                                    name={buddy.name}
                                                                    dps={buddy.dps || 0}
                                                                />
                                                            )}
                                                        </div>
                                                        <div className="w-8 ml-1"></div>
                                                        <div className="w-8 ml-1 flex justify-center items-center">
                                                            {row.isCombined && buddy.specSlug && getIconForSpec(buddy.specSlug) && (
                                                                <img
                                                                    src={`./images/classes/${getIconForSpec(buddy.specSlug)}`}
                                                                    alt={buddy.specSlug}
                                                                    draggable={false}
                                                                    className="w-6 h-6 object-contain"
                                                                    title={getLocalizedSpecName(buddy.specSlug, uiLanguage)}
                                                                />
                                                            )}
                                                        </div>
                                                        <div className="w-8 ml-1"></div>
                                                    </>
                                                )}
                                            </div>
                                            <div className="relative h-full z-10 overflow-hidden" style={{ width: `${timelineWidth}px` }}>
                                                {RENDER_MODE === 'dom' && processedBuddyCasts.map((cast, cIdx) => {
                                                    const isFocusedSpell = isFocusedSpellId(cast.spellId);
                                                    // spell/barColor 已在 playerRowModels 里预解析
                                                    const spell = cast.spell;
                                                    const timeUntilKill = row.killTimeSeconds ? (row.killTimeSeconds - cast.timestamp) : 99999;
                                                    if (timeUntilKill <= 0) return null;

                                                    // 横向虚拟化: 窗口外的 cast 不渲染 (按真实绘制宽度裁剪)
                                                    const alignedCastTime = Number(cast.timestamp || 0) - rowPhaseOffset;
                                                    if (alignedCastTime > cullT1 || alignedCastTime + Math.max(cast.duration || 0, spell.cd || 0) + 60 / zoom < cullT0) return null;

                                                    const currentTrackHeight = isCollapsed ? buddyTotalHeight : buddyTrackHeight;
                                                    const topPos = isCollapsed ? 0 : cast.trackIndex * buddyTrackHeight;
                                                    const iconHeight = currentTrackHeight * 0.9;
                                                    const durationWidth = Math.max(0, Math.min((cast.duration || 0) * zoom, timeUntilKill * zoom));
                                                    const cdWidth = Math.max(0, Math.min((spell.cd || 0) * zoom, timeUntilKill * zoom));
                                                    const barColor = cast.barColor;

                                                    return (
                                                        <div
                                                            key={`buddy-cast-${row.id}-${buddyIdx}-${cast.spellId}-${cast.timestamp}-${cast.trackIndex}`}
                                                            className={`absolute flex items-center group/icon select-none transition-opacity duration-150 ${focusedSpellId && !isFocusedSpell ? 'opacity-25' : 'opacity-100'}`}
                                                            style={{
                                                                left: getAlignedLeft(cast.timestamp, rowPhases),
                                                                top: `${topPos}px`,
                                                                height: `${currentTrackHeight}px`,
                                                                zIndex: isFocusedSpell ? 220 + cIdx : 10 + cIdx
                                                            }}
                                                        >
                                                            <div className="relative h-full flex items-center">
                                                                {showCooldown && spell.cd > 0 && cdWidth > 0 && (
                                                                    <div
                                                                        className="absolute top-1/2 -translate-y-1/2 h-1/3 rounded-r-sm z-0"
                                                                        style={{
                                                                            left: `${iconHeight / 2}px`,
                                                                            width: `${cdWidth}px`,
                                                                            backgroundColor: hexToRgba(barColor, 0.2)
                                                                        }}
                                                                    />
                                                                )}
                                                                {showDuration && durationWidth > 0 && (
                                                                    <div
                                                                        className="absolute left-0 z-10 rounded-sm shadow-sm"
                                                                        style={{
                                                                            width: `${durationWidth}px`,
                                                                            height: `${iconHeight}px`,
                                                                            backgroundColor: barColor,
                                                                            opacity: 0.88
                                                                        }}
                                                                    />
                                                                )}
                                                                <div
                                                                    onMouseDown={(e) => {
                                                                        handleSpellIconMouseDown(e, cast.spellId);
                                                                    }}
                                                                    onClick={(e) => {
                                                                        e.stopPropagation();
                                                                    }}
                                                                    className="relative z-20 flex items-center justify-center overflow-hidden rounded-sm bg-black/50"
                                                                    style={{
                                                                        height: `${iconHeight}px`,
                                                                        width: `${iconHeight}px`,
                                                                        minWidth: `${iconHeight}px`,
                                                                        boxShadow: isFocusedSpell ? 'inset 0 0 0 2px #00FF96, -2px 0 0 #00FF96, 2px 0 0 #00FF96' : 'none'
                                                                    }}
                                                                    title={`${spell.name} (${formatTime(cast.timestamp)})`}
                                                                >
                                                                    <RenderIcon spell={spell} className="opacity-100" />
                                                                </div>
                                                                {showSkillTimes && (
                                                                    <span
                                                                        className="ml-1 font-bold text-white/90 drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)] z-30 pointer-events-none"
                                                                        style={{ fontSize: `${iconHeight * 0.58}px`, lineHeight: 1 }}
                                                                    >
                                                                        {formatTime(cast.timestamp)}
                                                                    </span>
                                                                )}
                                                            </div>
                                                        </div>
                                                    );
                                                })}
                                            </div>
                                        </div>
                                    ))}
                                    </React.Fragment>
                                );
                            })}
                        </div>
                    </div>
                </div>
                </div>
            );
        };

        const root = createRoot(document.getElementById('root'));
        root.render(<App />);
