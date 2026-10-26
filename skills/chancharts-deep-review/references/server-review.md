# 服务端完整复盘与报告交付

使用当前已认证的 ChanCharts 连接，先发现实际注册的工具名称和输入 schema，不硬编码命名空间前缀。
需要 request_deep_review 和 get_deep_review；缺少入口时明确不可用，不安装本地服务端或运行旧包装器。

1. 用 resolve_security 核实用户指定证券。research_universe 为 {"schema":"RESEARCH_UNIVERSE_INPUT_V1","source":"explicit_symbols","symbols":["000021.SZ"]}；不把示例证券自动加给用户。
   仅用户明确要求网页自选时使用 {"schema":"RESEARCH_UNIVERSE_INPUT_V1","source":"web_watchlist"}。
   完整复盘仍受服务端 Pilot 及权益限制；当前范围限已授权的深科技、平安银行、浦发银行，不代表所有安装者获得权限。
2. 按 data-sources.md 完成可获取的外部资料，按 agent-research.md 准备可选输入。不得为了补齐内容申请新权限或读取其他账号数据。
3. 提交 request_deep_review，参数为 research_universe、review_mode="daily_review_4_timeframes"、cutoff_policy="actual_observations_then_freeze_v1"，以及可选 focus、agent_research。
   不提交 owner、端点、文件路径、执行命令或凭据。不使用内部演练策略替代真实最新复盘。
4. EOD 分析以最近已发布快照交易日北京时间15:00为行情截止。readiness 若为 waiting_for_data、calendar_unavailable、permission_denied 或 no_new_session，按实际状态解释；不改 asof、周期或身份绕过。
5. 得到 review_id 后保留它。pending/running 用 get_deep_review 查询，间隔至少30秒，最多主动等10分钟；仍在运行则保留引用供后续查询，不重复创建分析。
6. complete/partial 时交付真实客户摘要。取报告从 get_deep_review(review_id, artifact_offset=0) 开始，artifact 的 encoding=base64、media_type=application/zip。
   按返回的 next_offset 逐块读取，保留同一 review_id 和偏移；只在当前块完整取得后推进，next_offset=null 才完成。
   串行读取，间隔至少6秒；HTTP429时遵守 Retry-After，单次取块最多重试4次、总等待最多180秒，超出后保留位置供稍后继续。
   无法获知等待时间或客户端未暴露状态时说明稍后继续，不忙循环。不得清限流、更换凭据、重新提交报告来继续下载。
7. 由平台文件能力按顺序重组 ZIP，校验可得的长度与完整性；安全解包拒绝绝对路径、父目录穿越和符号链接，不执行包内代码。
   交付服务返回的 report.html 与 assets 或完整 ZIP；客户端没有文件能力时给真实摘要并说明限制，不伪称报告附件已交付。
8. failed 不交付报告，权限拒绝不换身份或降低用户要求；不能确认提交是否成功时先核对既有任务，禁止自动重提。

任何授权、禁用、额度或真实缺失都以服务端返回为准；失败不应被描述成已完成。
