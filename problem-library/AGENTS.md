# Problem Library Agent Guide

本目录是公开数学问题目录的本地、可重建镜像。`manifest.json` 是抓取批次和完整性真相源；`records/problems.jsonl` 是查询与研究路由入口；`raw/` 只保存来源响应，不接受人工编辑。

## 目录结构

```text
problem-library/
├── AGENTS.md                 # 数据边界与维护规则
├── README.md                 # 数据范围、许可和使用方法
├── COMPLETION_EXEMPLAR.md    # 本次完成方法与复用边界（人读）
├── COMPLETION_EXEMPLAR.json  # 可重算证据绑定的机器契约
├── RETROSPECTIVE.md          # 项目内复盘草稿，不是全局 canonical record
├── REUSE_SAMPLING.json       # 主要任务复用采样决策
├── AUDIT_CASE_SAMPLING.md    # 缺陷修复后的审计案例采样判定
├── manifest.json             # 批次、来源、计数、哈希与覆盖率
├── schema/
│   ├── candidate-source.schema.json # 候选来源 registry 契约
│   ├── candidate-observation.schema.json # 研究不可准入的候选观察
│   ├── problem.schema.json   # 已准入单条来源记录契约
│   └── canonical-problem.schema.json # ProblemContract v1 唯一输入契约
├── registry/
│   └── candidate-sources.json # 38 个候选来源的角色、许可和状态映射
├── raw/
│   ├── wikipedia/            # MediaWiki API 原始 JSON
│   ├── unsolvedmath/         # HTML 目录页快照，或固定 Hugging Face JSON 分发快照
│   ├── erdosproblems/        # Erdős Problems 快照（见下）
│   └── candidates/           # 只读来源 distribution 与 inventory
├── derived/
│   └── candidate-observations/ # 按输入摘要版本化的本地派生快照（Git ignored）
├── staging/
│   └── admissions/           # 来源级准入审计（Git ignored）
├── records/
│   ├── problems.jsonl        # 三个来源的统一记录流
│   └── canonical-problems.jsonl # 经确认的稳定研究问题
└── indexes/
    ├── catalog.json          # 总量、来源、状态与分类计数
    ├── by-category.json      # 分类到记录 ID 的倒排索引
    └── by-source.json        # 来源到记录 ID 的倒排索引
```

`raw/erdosproblems/` 子结构与不变量：

```text
raw/erdosproblems/
├── discovery.json           # robots Content-Signal、sitemap 探测、规范页快照清单
├── status-inventory.json    # 状态词表（当前 open/solved）
├── gaps.json                # 缺失编号与尾部探针证据（区间内必须为空）
├── aux/                     # /、faq、tags、prizes、lists、definitions、latex/history 样例
├── problems/{NNNN}.html     # 全部问题页（编号 1..N 连续，唯一真相源）
├── bibs/{key}.html          # 唯一书目键的 /bibs 条目（站点侧断链键除外，记 missing）
├── lists/                   # lists-index.json + 每个问题列表键的 search_bib 页
└── tags/                    # tags-index.json + 每个标签页（对账证据）
```

## ProblemContract 数学推理纪律

<!-- MATHEMATICAL_REASONING_DISCIPLINE_V1 -->

ProblemContract 准入必须执行 `governance/standards/MATHEMATICAL_REASONING_DISCIPLINE.md` 的定义先行规则：冻结对象、定义域、量词顺序、定义、前提、公理、目标、精确否定、尺度与极端边界，并登记来源差异和可能的语义重复。来源标题、状态、有限样本或模型概括不得替代 statement-faithfulness 审查；歧义未闭合时禁止进入研究准入。

## 边界与依赖

- 上游：Wikipedia MediaWiki API、UnsolvedMath 公开目录分页/Hugging Face 固定 JSON 分发与 Erdős Problems 站点页面。
- 下游：`scripts/query_problem_library.py`、研究选题、来源核验和后续去重/补全流程。
- Wikipedia 记录继承 CC BY-SA 4.0，必须保留来源、版本和归属。
- UnsolvedMath HTML 目录未发现公开许可声明；只规范化目录事实与简短卡片摘要，不镜像详情正文。Hugging Face `ulamai/UnsolvedMath` metadata 当前声明 CC BY 4.0，但链接来源材料仍受各自条款约束；使用固定 revision 和文件哈希，不把 moving `main` 当作证据。
- ErdősProblems 依 robots.txt Content-Signal（`search=yes, ai-train=no, use=reference`）按 reference 用途保存公开问题事实；不抓论坛评论、用户页与点赞反应；陈述归属 Thomas Bloom 与贡献者，陈述本身为站长改写，以原站为准。
- 三个来源的来源数据、原始快照、manifest 与派生索引只留本地，不进入公开 Git；需要时通过抓取器重建。
- `raw/` 是证据缓存，不是可编辑知识；刷新只能运行抓取脚本。UnsolvedMath 原站返回 challenge/429 时必须保留失败并改用显式 Hugging Face 分发模式，禁止绕过反爬挑战。`raw/candidates/consolidated/` 旧七字段输出不是契约，CLI 已转交 versioned CandidateObservation builder。
- `derived/candidate-observations/` 必须绑定 inventory、parser、schema 和 registry 摘要；历史快照不可静默修补，输入变化必须产生新 snapshot ID。
- CandidateObservation 永远 `admission.state=candidate` 且 `research_eligible=false`；`answered` 不是 solved，`resolved` 不是 established，Lean build 也不是原题忠实。
- 候选 Git 来源禁止在抓取器内 `reset --hard`；必须进入 `vendor/sources.lock.json` 的无工作树固定 reference，固定 commit 不等于执行准入。
- UnsolvedMath 的公开 ID/详情 URL 存在一对多冲突，不得作为主键；本地 ID 由卡片内容指纹生成，冲突组必须进入 manifest。Hugging Face 模式还绑定不可移动的 dataset revision、`problems.json`/`statistics.json` 摘要和显式 scope；`site-compatible` 只排除 OWR set 15，不等同于已成功重新抓取原站页面。
- ErdősProblems 编号是稳定主键候选（1..N 连续，区间内不允许缺口；尾部以 30 个连续缺失结束枚举）；本地记录 ID 仍使用内容指纹，不假设站点编号永不变。
- ErdősProblems 真实问题按是否存在 `.problem-box` 判定；“No results” 页返回 HTTP 200，禁止按状态码判定。
- 书目键 `/bibs/{key}` 存在少量站点侧 404（如 `Mc21`、`92`）；这类键记入 missing 且不得缓存占位，任何本地书目缺口都必须能在 manifest 对账。
- 来源记录不能直接作为 canonical Problem；归一化问题必须有版本化陈述和稳定来源 URL，本地来源记录存在时再校验其 ID。
- canonical Problem 必须冻结 domain、quantifiers、definitions、assumptions、allowed_axioms、固定 acceptance policy 与可执行 constraints；禁止恢复 `open|solved|refuted` status。
- 任何“完整”声明必须同时满足：目录声明总数、解析总数、本地唯一 ID、源 ID 冲突账本、所有原始页哈希和索引一致性全部通过。

## 维护命令

```bash
python3 scripts/fetch_erdosproblems.py all     # 三来源统一重建（推荐入口）
python3 scripts/fetch_erdosproblems.py crawl   # 仅网络抓取 ErdősProblems
python3 scripts/fetch_erdosproblems.py build   # 仅本地重算记录/索引/manifest
python3 scripts/fetch_problem_library.py       # 旧入口；只重建两来源，之后必须重跑 build
python3 scripts/fetch_problem_library.py --refresh
python3 scripts/fetch_problem_library.py --refresh --unsolvedmath-source huggingface --unsolvedmath-hf-scope site-compatible
python3 scripts/validate_problem_library.py
python3 scripts/test_problem_library.py
python3 scripts/build_candidate_observations.py
python3 scripts/validate_candidate_problem_library.py [--verify-raw]
python3 scripts/test_validate_candidate_problem_library.py
python3 scripts/audit_candidate_admission.py --source clay
python3 scripts/query_problem_library.py --collection admitted --text riemann --limit 10
python3 scripts/query_problem_library.py --collection candidates --source theoremdb --status-class open_claimed
```

多 Agent 并行警告：`fetch_erdosproblems.py` 与 `fetch_problem_library.py` 都会整体重写 `problems.jsonl`、manifest 与索引。
并行重建时最后写入者生效，可能互相覆盖对方来源；同一时间只允许一个进程重建问题库，任何重建完成后重跑校验。

新增或改变来源适配器时，先保存可复现的代表性结构证据，再修改解析器；结构漂移必须 fail-closed，禁止用空字段或旧缓存伪装成功。
