---
name: chancharts-deep-review
description: 通过已认证的 ChanCharts MCP 请求或复用完整四周期复盘，无需本地仓库。适用于“给这三只做一份完整复盘”；即时分析用 chancharts-research，定时安排用 chancharts-automation。
---

# ChanCharts 完整复盘

连接器使用 WorkBuddy 内建 OAuth；不得提示用户粘贴 PAT、client secret 或 Token。
若返回 TRIAL_EXHAUSTED，保留连接并引导打开响应中的升级地址；知识星球激活后
在同一连接直接重试，不要求重新 OAuth。

承接会话中的证券；用 resolve_security 核对名称和代码，歧义时询问。
默认使用 explicit_symbols，仅用户明确选择时使用 web_watchlist。
现有受限试点只允许深科技、平安银行、浦发银行和已授权身份，不扩权限或降规格。

按[服务端复盘](references/server-review.md)调用已认证 ChanCharts MCP。
不依赖本地 ChanCharts 仓库、Python 执行器、操作员配置或 Windows 路径。
若当前连接未提供服务入口，说明该连接尚未启用完整复盘服务，不调用旧本地包装器。
交易日历、行情、技术结构和 data_asof 以 ChanCharts 确定性事实为准。
覆盖未知或数据等待时停止生成，明确等待状态，不把历史报告称作最新报告。

资金观察、公司事件、研究观察按照[多来源清单](references/data-sources.md)
使用客户当前可访问的数据源，包含事实依据、风险和具体观察条件，再精简到报告。
不固定任何供应商，不假定申万、Wind、iFinD或东方财富已安装。
通过[Agent Contract](references/agent-research.md)提交补充内容，不覆盖技术事实。
报告保留可核验来源于私有审计，正文不添加来源行或内部流程说明。

同一逻辑请求优先复用服务返回的已提交结果，保留 complete/partial 的真实含义。
仅交付服务返回的客户摘要和认证产物；不附审计、凭证、调用日志、私有身份或路径。
需要定时安排时转 chancharts-automation，使用平台原生 Automation 和交付能力。
用户和 Automation 提示词只表达证券、目的、时间频率和个性化重点。


## 公开分发版运行边界

通过当前已授权的同一 ChanCharts MCP 连接工作；发现实际工具名称和 schema，不固定命名空间前缀。
本包不含执行器、凭据或运营授权，安装不扩大会员、证券或完整复盘权限。
统一采用最近已发布交易日北京时间15:00的盘后快照，不要求盘中最新分钟行情。
退市或异常证券明确不可用，不生成替代分析；遵守服务端试用计费与限流。
HTTP429遵守 Retry-After；不通过重新授权、切换身份、重建任务绕过限制。

报告下载的分块、限流与断点恢复见 [服务端复盘](references/server-review.md)。
