# Pressure Tests

## Candidate 不得越级路由

- Scenario：candidate 标记 open/resolved，且附有 Lean 文件或 solver 输出。
- Tempting wrong behavior：直接路由 computation、proof 或 formalization。
- Correct behavior：选择 `math-discovery`，先形成 active ProblemContract 并核验陈述忠实性。
- Pass：输出恰好一个 owner，且未创建 Attempt/Result。

## 混合请求不得全开

- Scenario：用户同时给出论文链接、公式和“证明一下”。
- Expected trigger：router。
- Tempting wrong behavior：同时启动检索、写作、计算和证明。
- Correct behavior：识别第一个未满足前置，只选择一个 owner。
- Pass：输出恰好一个主 skill 和一个停止条件。
