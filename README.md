# ChanCharts Skills

把 ChanCharts 的股票研究、完整复盘和定时复盘流程交给你的 AI 助手。
本仓库只发布技能说明与公开协议，不包含行情、服务端代码、账号或凭据。

## 选哪个技能？

| 技能 | 用途 | 示例 |
| --- | --- | --- |
| chancharts-research | 日常查询、股票比较 | “用 ChanCharts 分析深科技。” |
| chancharts-deep-review | 在已有权限下生成完整复盘报告 | “给深科技做一份完整复盘。” |
| chancharts-automation | 用客户端任务功能安排定时复盘 | “每个交易日北京时间20:30复盘深科技。” |

建议安装全部三个技能。安装技能不代表开通完整复盘权限；免费5次分析、会员、Pilot及证券范围仍由服务端判断。
行情用于最近已发布收盘快照的研究，不是实时行情。仅供学习、研究与复盘参考。

## 先连接 ChanCharts

在 WorkBuddy 自定义 MCP 中添加下面配置，点击连接，在浏览器同意授权后返回客户端。不填写 Token 或密钥。

```json
{"mcpServers":{"chancharts":{"type":"http","url":"https://mcp.chancharts.com/mcp"}}}
```

上述 URL 填入 WorkBuddy，不是供浏览器直接打开的介绍页面。

## 方法一：自己下载并导入（推荐）

1. 打开 [Releases](https://github.com/jianxuea/chancharts-skills/releases/latest)。
2. 下载 chancharts-research.zip、chancharts-deep-review.zip、chancharts-automation.zip。
3. 在 WorkBuddy 的“添加技能 → 上传技能”中分别选择 ZIP。不同版本入口名称可能略有不同。
4. 在技能列表中确认三个名称已出现，开始对话时按需选用。

不要把 GitHub 自动生成的整个仓库 Source code ZIP 当作单个技能包。每个发布 ZIP 只含一个技能目录及其引用资料。
Release 同时提供 SHA256SUMS.txt 和发布清单，可用于校验下载文件。

## 方法二：让 Agent 帮你安装

复制下面这段话到你使用的助手。不同客户端的安装能力不同；无法自动安装时，助手应给出文件并让你按方法一导入。

> 请从 https://github.com/jianxuea/chancharts-skills 安装 chancharts-research、chancharts-deep-review、chancharts-automation 三个技能。先核实仓库与最新正式 Release，读取 README、目标 SKILL.md 和引用文件，检查权限与内容。只安装这三个目录及其 references，遵守当前客户端支持的技能安装流程；已有同名技能时先说明差异，不直接覆盖用户修改。若客户端不支持自动安装，请下载三个发布 ZIP 并告诉我如何导入，不要凭空创建配置字段或声称已安装。不要下载或运行服务端代码，不要索取或读取我的 Token、Cookie、邀请码，不修改已有 MCP 连接。安装后报告版本和实际安装位置；连接授权由我在浏览器完成。

## 使用与限制

- [完整用户说明](docs/USER_GUIDE.md)：连接、5次体验、升级、复盘、定时任务和常见问题。
- [客户端与安装支持边界](docs/INSTALLATION.md)：官方依据、已验证内容和未验证事项。
- 体验用尽在 https://chancharts.com/mcp/upgrade 查看权益；激活后无需重新连接。
- 完整复盘仍受原 Pilot/权益控制，安装技能不会使所有用户获得完整报告能力。
- 定时任务由客户端创建；本地任务需要电脑和客户端运行，不保证关机后执行。
- 外部资料仅用实际可访问、合法授权的数据源，拿不到就明确缺失，不编造数字。

## 维护与构建

Python 3.11+，构建无需额外依赖：

```text
python -m unittest discover -s tests -v
python tools/build_release.py --version v1.0.0
```

构建检查本地引用完整、单技能包范围、凭据特征及哈希清单；dist 不进入源码仓库。
发布包没有可执行安装脚本，不需要安装 ChanCharts 服务端、Python 环境或下载行情来使用技能。
许可证见 LICENSE。技能开放不代表后端服务、行情和第三方资料获得相同授权。
