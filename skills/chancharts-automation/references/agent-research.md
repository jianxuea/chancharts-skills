# 外部研究输入

此参考只用于资金、公司事项和研究观察的补充；证券身份、OHLCV、技术指标、缠论结构和行情截止时间只采用 ChanCharts 返回值。
即时研究用自然语言概括，完整复盘通过 MCP 的 agent_research 参数提交；不在本地运行报告渲染器。

## 提交格式

遵守同目录的 [JSON Schema](agent-research.schema.json)；服务端还校验时间先后、字段冲突和证券范围。
顶层 schema 为 AGENT_RESEARCH_INPUT_V1，含 generated_at、asof、generator 和 stocks。
generator 为 {"type":"agent","name":"实际助手名称","version":"实际版本"}。
stocks 中每项仅含已解析的 symbol 和需要的研究板块：discussion、comment、logic、risks、conditions、moneyflow_observations、company_events。
每个板块是一条 claim 对象或 claim 数组，不接受裸字符串。

claim 包含 text、statement_type（fact/inference/opinion）、status（supported/unavailable）、sources。
supported fact/inference 至少一个可靠来源；opinion 明确为观点，不冒充事实。
source 包含真实 title、url、publisher、published_at（未知为 null）、observed_at。
URL 是实际来源页面或授权接口地址，不包含凭据；不使用占位发布者、伪造 URL 或 userinfo。
缺失使用 unavailable，保留原因，不能填零、推测机构身份或编造未来解禁。

## 时间与归属

所有时间为带时区的 ISO 8601；先取得资料再冻结秒级 asof，不回填观察时间。
published_at <= observed_at <= asof，observed_at <= generated_at。提交在冻结后15分钟内完成；
行情截止采用最近已发布交易日15:00（北京时间），外部资料观察时间与行情截止是不同概念。
不要为了使二者相同而伪造观察时间；按实际工具合同交由服务端验证。
只提交本次已核对证券范围的子集；禁止注入价格、name、指标、结构、data_asof 等确定性字段。
没有合规补充时省略 agent_research，明确报告可能有缺项，不制造成功。

客户报告保持简洁，不展示内部审计哈希、修复过程或凭据。完整来源和时间证据仍保存在受授权的研究上下文及服务端审计；
隐藏内部流程不等于隐藏影响结论的数据缺失。用户询问依据时提供可核验来源，不编造出处。
