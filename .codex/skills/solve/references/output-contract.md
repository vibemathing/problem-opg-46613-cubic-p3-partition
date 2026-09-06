# 输出与证据契约

`solve` 只定义一个宽松的交互信封，方便不同 Harness 消费。宿主可以增加字段，但不能把模型自报结果
直接当作独立验证。

## 必填与推荐字段

必填四项：`operator_id`、`intent`、`evidence`、`outcome`。

推荐补充：`inputs`、`assumptions`、`precondition_check`、`steps`、`observations`、`uncertainties`、
`next_action`、`source_refs`、`budget_used`；多门验收再补 `required_capabilities` 和
`capability_results`。

```json
{
  "operator_id": "psoa.programming.minimal-reproduction",
  "intent": "确认错误所需的最小输入条件",
  "inputs": ["脱敏失败日志", "可复现环境"],
  "assumptions": [],
  "precondition_check": ["存在可观察失败现象"],
  "steps": ["缩减输入", "重复运行", "记录最小失败案例"],
  "observations": ["仅保留字段 x 时仍失败"],
  "evidence": [
    {"kind": "observed", "ref": "artifact://minimal-failure", "summary": "固定输入下重复失败"}
  ],
  "uncertainties": ["尚未定位根因"],
  "outcome": "succeeded",
  "next_action": "continue",
  "source_refs": ["psoa.programming.minimal-reproduction"]
}
```

## 证据标签

- `observed`：运行、文件、测量或外部来源直接观察到的事实。
- `derived`：由已记录前提按明确规则推导出的结论。
- `experimental`：计算实验、抽样、模拟或启发式结果；支持猜想，不自动构成证明。
- `assumption`：为了继续而明确声明的前提，必须能被后续证据推翻。
- `unknown`：当前无法判断的事项，不能被省略或改写成成功。

## Outcome 与下一步

`outcome` 描述这一次算子，不描述整个任务：

| outcome | 含义 | 常见 next_action |
|---|---|---|
| `succeeded` | 本算子的成功条件有足够证据 | `continue` 或 `stop` |
| `failed` | 动作执行了，但成功条件未满足 | `revise` 或 `switch` |
| `inconclusive` | 证据不足，不能判断成败 | `continue`、`revise` 或 `escalate` |
| `not_applicable` | 前置条件/风险边界不允许使用 | `switch` 或 `escalate` |

如果宿主没有独立 Verifier，至少要把“模型推断”和“外部观察”分开，并把结论降级为 `inconclusive` 或
明确的假设。

## 多门验收

`required_capabilities` 是集合，不是可跳级的成熟度数字。每项能力分别记录 `satisfied`、`missing`、
`failed`、`stale` 或 `not_applicable`，并绑定声明/候选身份、输入摘要、verifier 和回执。只有全部
required 能力满足时，宿主 verifier 才能接纳结果；例如 source 扫描不能代替 build，build 不能代替
kernel，kernel 也不能代替人类题意与语义确认。

## 不允许的输出

- 不写入密钥、完整敏感 prompt、客户数据或未经脱敏的工具结果。
- 不用“未发现反例”替代“已证明”，不用“模型很有信心”替代证据。
- 不把算子文本里的 `operation` 直接当作已授权 shell、网络、实验或生产动作。
