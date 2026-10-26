---
name: chancharts-research
description: 用 ChanCharts 分析或比较用户指定证券的确定性缠论和技术结构。适用于“分析一下贵州茅台”“比较深科技、平安银行和浦发银行”等即时查询；完整报告用 chancharts-deep-review，周期任务用 chancharts-automation。
---

# ChanCharts 即时研究

用户只需说证券、研究目的和重点。使用连接器已认证的 MCP；认证配置由平台管理。
首次连接由 WorkBuddy 打开浏览器完成一次 OAuth 同意；不要要求用户粘贴 PAT、
client secret 或 OAuth Token。授权过期时引导使用平台的重新连接操作。
证券名称及代码先调用 resolve_security(query)，仅 data.status=resolved 的
返回 security.symbol 可确立身份。ambiguous 让用户选返回候选；其他状态明确说明，
不猜代码。比较时保留顺序并在私有任务上下文构造 explicit Research Universe；
见 [输入契约](references/research-universe.schema.json)。只有用户明确说网页自选股时
才使用 get_watchlist；不修改自选股。相对称呼“这三只”仅用当前上下文已核对范围，
缺少上下文就询问对象。

普通“分析/比较”默认即时查询，不制造完整报告或周期任务。使用
get_stock_structure_bundle，每股一次、串行，按用户目的请求现有权限允许的周期；
未指定则显式请求 timeframes=["1d"]，不要省略而触发默认全周期。
即时文字查询首个请求就设置 include_chart=false，避免不需要的大型图表载荷；
不要在收到覆盖错误后通过改变 include_chart 重复请求。遵循实际工具 schema，不新增参数。bundle 已含技术字段，
不重复请求快照。不要按改换 asof 的方式重试日历/就绪错误；明确不可用并停止该股事实分析。
逐周期先检查 data_status；error、unavailable、waiting、permission_denied 的周期，
即使响应仍携带旧 OHLC/MA/BI/SEG/ZS 字段，也不能据此作结构解释、建议或比较。
日历覆盖错误时停止技术结构解释，只说明行情日期、覆盖不足和权限状态；
用户需要的合规外部资金/公司事项研究仍按清单尝试，不继续解析旧结构。
不得本地重算、派生或补充技术指标（包括 MA 距离、MACD 序列、价格窗口极值、
涨跌幅或结构距离）；返回未直接提供的值保持 missing。不要创建或运行解析/计算脚本。
即时分析默认简短文字，无需生成文件。只有确需比较变化且有明确历史截止时才请求结构变化。
仅对瞬时传输错误最多重试一次；missing/partial/denied 不重试。

ChanCharts 返回的证券身份、缠论 BI/SEG/ZS/SegBSP、指标、确认状态、data_asof、
data_status 是唯一确定性权威。不得用网页、LLM 计算或记忆替代、补零或改写。
区分请求时刻和行情日期；旧行情不称今日数据。
不得自行绘制缠论、价格或技术示意图、MA 梯度图或仿制 K 线；只使用已批准的
原生图表产物。没有可用原生图表就明确图表不可用，不加载其他绘图技能替代。日历覆盖不足明确 unavailable，
不以外部公告或工作日推理替换已验收日历。缺失和权限拒绝原样说明；不换账号、
不改权益、不自动降级用户明确要求的完整复盘。

外部资料仅补充公司背景、公开事件和研究观察，并显示来源。
遵循 [Agent Research Contract](references/agent-research.md)：标明事实/推断/观点，
保留 URL、发布者和实际 observed_at，未知 published_at 为 null。
不得将外部资金评论写成 MCP 事实，不从订单规模推断机构身份。
确定性事实优先于外部研究；冲突或无可靠来源就明确缺失。

完成输出用用户语言给出证券、实际行情日期、结构结论和缺失项。工具名、schema、
凭证、路径、私有身份和安全实现不是用户提示词或结果的一部分。
完整复盘转交 chancharts-deep-review；用户要求定时则转交 chancharts-automation。
安装包不授予权限；服务端权益和既有受限试点边界保持不变。
新用户有五次分析体验；同一分析的多工具调用与重试不按调用次数扣减。
收到 TRIAL_EXHAUSTED 时提供响应中的升级地址，不将其描述为登录失败。
知识星球邀请码在升级页绑定当前用户；激活后直接重试，无需重新 OAuth 或重连。

完整复盘（即时研究按需）执行[客户端多来源补充清单](references/data-sources.md)。
优先发现客户当前已启用、实际可访问的数据源；资金/融资/事件缺失后主动补充，
不限定东方财富或任何厂商，不要求用户复制内部流程；确定性技术事实仍由 ChanCharts 提供。


## 公开分发版运行边界

通过当前已授权的同一 ChanCharts MCP 连接工作；发现实际工具名称和 schema，不固定命名空间前缀。
本包不含执行器、凭据或运营授权，安装不扩大会员、证券或完整复盘权限。
统一采用最近已发布交易日北京时间15:00的盘后快照，不要求盘中最新分钟行情。
退市或异常证券明确不可用，不生成替代分析；遵守服务端试用计费与限流。
HTTP429遵守 Retry-After；不通过重新授权、切换身份、重建任务绕过限制。
