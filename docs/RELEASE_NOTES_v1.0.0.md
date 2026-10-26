# ChanCharts Skills v1.0.0

初次公开发布三个技能：即时研究、完整复盘、自动复盘。

## 下载与安装

下载下方三个技能 ZIP，在 WorkBuddy 的“添加技能 → 上传技能”中分别导入。
不要导入整个仓库的 Source code ZIP。连接 ChanCharts 还需在 WorkBuddy 自定义 MCP 中填写 https://mcp.chancharts.com/mcp 并完成浏览器授权；不粘贴 Token。

仓库 README 同时提供可复制给 Agent 的安装提示词，详细使用方式见 docs/USER_GUIDE.md。

## 本次验证

- 8项独立打包测试通过：内容与哈希、重复构建、引用缺失/越界、凭据特征、执行文件、元信息及版本参数拒绝。
- 三个 SKILL.md 均通过标准格式校验。
- 三包均不含本地执行器、服务器配置、凭据或行情；现有服务器权限与完整复盘 Pilot 不变。
- SHA256SUMS.txt 和 RELEASE_MANIFEST.json 记录确切发布内容。

**验证边界：新公开 ZIP 的真实 WorkBuddy 上传安装尚未执行，不声称已完成该项端到端验收，也未上架 SkillHub。**
此前 OAuth 连接已在真实 WorkBuddy 验证，但不替代新包导入验证。

行情仍为盘后研究；完整复盘、自动任务、文件交付取决于现有服务端权限与客户端能力，安装技能不会自动开通这些能力。
