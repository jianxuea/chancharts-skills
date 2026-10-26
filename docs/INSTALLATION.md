# 安装方式与验证边界

## WorkBuddy

截至2026-10-26查询的官方文档明确提供“添加技能 → 上传技能”，可导入本地技能包：
https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market

官方另介绍 SkillHub 的安装指令，这是另一个分发渠道；本仓库初版没有申报或上架 SkillHub，不能声称已上架。
https://www.codebuddy.cn/docs/workbuddymini/features/Attachments-and-Skills

本仓库提供标准 SKILL.md + references 文件夹和每技能独立 ZIP，不臆造 WorkBuddy 安装命令或强写未核实的全局技能目录。
Agent 安装必须使用当前客户端明确支持的机制；如果没有文件/安装权限，改用人工上传，不以在聊天中读到 SKILL.md 代替实际安装。

## 其他客户端

支持 SKILL.md 的客户端可按各自文档选择本仓库 skills 下的三个子目录；仍需另外具备远程 MCP、OAuth和所需工具/文件交付能力。
本次没有实测其他客户端，不保证兼容。缺少自动化、图表附件或报告工具时明确限制，不伪造替代输出。

## 本次发布核验范围

- 校验三技能的 frontmatter、本地引用、无本地执行器依赖、ZIP内容、SHA256与重复构建一致性。
- 沿用此前真实 WorkBuddy 连接 ChanCharts OAuth 的验证证据，但不把它当作本次 GitHub ZIP 导入验证。
- 新公开 ZIP 的真实 WorkBuddy 上传、技能发现及端到端调用需要安装后实测，发布时如未执行须明确标记未验证。
- 服务端算法、行情、用户权限、OAuth和生产调度不因发布技能改变。
