# M-Spec 服务器运维手册 (t3.small 优化)

本文档配合 2026-08 的性能优化改动。代码层面的优化(缓存策略、gzip、
uvicorn 参数、updater `--once` 模式)`git pull` 即生效;下面是需要在
服务器上**手动执行一次**的操作,按收益排序。

## 0. 本次部署的注意事项

- 前端不再依赖任何 CDN(Tailwind/Babel/esm.sh 全部移除),改为加载
  预编译产物 `front_end/dist/app.js` + `app.css`(已提交进 git,服务器
  **不需要装 Node**)。改前端源码后在开发机跑
  `python scripts/build_frontend.py` 再提交。
- 本次 pull 会从 git 里删掉误提交的 `.venv/`(约 5600 个文件)和
  `.DS_Store` 等垃圾文件,`front_end/data` 的生成文件不受影响
  (deploy 脚本自带备份/恢复逻辑)。
- `main.py` 现在默认 `access_log=False`(请求日志看 Apache 的),
  `limit_concurrency=100`,信任来自 127.0.0.1 的 X-Forwarded-* 头。

## 1. updater 改成 cron 一次性模式(省 ~200MB 常驻内存)

现状:`updater.py` 常驻后台,每小时干 1 分钟活、睡 59 分钟,却一直
占着 ~200MB —— 这台机器 swap 已经吃了 866MB,这就是主要嫌疑人。

```bash
# 1) 停掉常驻 updater
pkill -f "python3 updater.py"

# 2) crontab -e 加一行 (nice/ionice 让它永远让路给网页请求):
0 * * * * cd /home/bitnami/m-spec && flock -n /tmp/mspec-updater.lock nice -n 19 ionice -c3 python3 updater.py --once >> updater.log 2>&1
```

然后把 `scripts/server_redeploy.sh` 里的 `START_UPDATER=0` 环境变量传入
(或直接不再调用 start_updater),避免 deploy 又把常驻进程拉起来。

> t3.small 每小时只挣 24 个 CPU 积分(基线单核 20%)。updater 每轮
> 全速抓 21 个职业是唯一的持续 CPU 消耗者;`nice` + `--once` +
> 重新启用的 WCL 并发信号量(建议在 .env 设 `CONCURRENT_CONNECTIONS=4`)
> 可以把尖峰压平,避免积分见底后整机(含 WordPress/MariaDB)被限速。

## 2. 让 Apache 直接伺服静态文件(最大的 CPU 节省)

现在每个 PNG 图标请求都要穿过 uvicorn + Python 中间件。在 vhost 配置
里加(**排除规则必须放在 catch-all ProxyPass 之前**):

```apache
ProxyPass /images !
ProxyPass /dist !
ProxyPass /lorrgs_assets !
Alias /images  /home/bitnami/m-spec/front_end/images
Alias /dist    /home/bitnami/m-spec/front_end/dist
Alias /lorrgs_assets /home/bitnami/m-spec/lorrgs_assets

<Directory /home/bitnami/m-spec/front_end>
    Require all granted
    Options -Indexes
    EnableSendfile On
</Directory>

# 缓存头 (与 Python 端策略一致)
<LocationMatch "^/images/">
    Header set Cache-Control "public, max-age=604800, stale-while-revalidate=86400"
</LocationMatch>
<LocationMatch "^/dist/">
    Header set Cache-Control "public, max-age=31536000, immutable"
</LocationMatch>

# 压缩: 只压文本, 不压图片; 注意别和 Python 端重复压缩 (Alias 路径归 Apache 压)
AddOutputFilterByType DEFLATE application/json text/html text/css application/javascript
DeflateCompressionLevel 4
```

注意:`/data` 建议**继续走 Python**(StaticFiles 的 ETag/304 逻辑与
no-cache 策略已经配好;mod_deflate 会改 ETag,除非配了
`DeflateAlterETag NoChange`,2.4.12+)。

## 3. Apache event MPM 缩容(防 OOM)

`MaxRequestWorkers 400 / ThreadsPerChild 25` 对 1.9GB 内存太激进
(可能拉起 16 个子进程)。建议:

```apache
<IfModule mpm_event_module>
    ServerLimit              3
    StartServers             1
    MinSpareThreads          10
    MaxSpareThreads          50
    ThreadsPerChild          25
    MaxRequestWorkers        75
    MaxConnectionsPerChild   10000
</IfModule>
KeepAlive On
KeepAliveTimeout 3
MaxKeepAliveRequests 500
```

## 4. 磁盘清理(一次性,~1.5GB+)

```bash
# 三份重复的前端数据备份 (366MB) —— deploy 脚本现在会自动只保留 2 份
ls -dt ~/mspec-data-backup-* | tail -n +3 | xargs -r rm -rf

# /var/log 863MB
sudo journalctl --vacuum-size=100M
# 并在 /etc/systemd/journald.conf 设 SystemMaxUse=100M

# 归档: 新代码已改为 gzip 写入 (~85-90% 更小), 旧的未压缩归档可压掉:
find ~/m-spec/archives -name '*.json' -exec gzip {} \;
# 保留天数可调 (默认 14): 在 .env 设 MSPEC_ARCHIVE_RETENTION_DAYS=7

# git pull 后瘦身仓库 (移除 .venv 的历史对象引用):
git gc --prune=now
```

## 5. 日志轮转

`/etc/logrotate.d/mspec`:

```
/home/bitnami/m-spec/main.log /home/bitnami/m-spec/updater.log /home/bitnami/m-spec/dmu_refresh.log {
    weekly
    rotate 4
    compress
    missingok
    notifempty
    copytruncate
}
```

Apache 的 access log 可以加一条不记图标请求,减少写盘:

```apache
SetEnvIf Request_URI "\.(png|jpg|webp)$" dontlog
CustomLog ${APACHE_LOG_DIR}/access.log combined env=!dontlog
```

## 6. 内核/环境微调(可选)

```bash
# swap 已被压过, 降低换出倾向
sudo sysctl vm.swappiness=10   # 持久化写 /etc/sysctl.d/99-mspec.conf

# glibc malloc arena 限制, 降低 Python 进程内存碎片
# (加到启动 main.py 的环境里, 如 .env 或 systemd unit)
export MALLOC_ARENA_MAX=2
```

## 7. 已知的后续优化空间(未做,按需)

- **图标转 WebP**:886 个 PNG 共 11.6MB,`cwebp -q 80` 能压到 ~4MB。
  需要同步改 JSON 里的 icon 文件名引用,收益在长缓存生效后有限。
- **移除死路由**:`/api/tasks`、SQS、auth 等 AWS 依赖路由在自托管
  部署下不可用(假凭据),前端也不调用;可从
  `lorrgs_api/routes/api.py` 注释掉相应 router 进一步瘦身。
- **spec_ranking JSON 按区服拆分**:现在单文件含 global+CN+KR,
  区服筛选在前端做;拆开可以少传 2/3 的数据。
