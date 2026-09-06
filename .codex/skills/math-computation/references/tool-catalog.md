# 数学工具目录

本目录描述项目已配置或明确排除的成熟工具。命令通过 `python3 scripts/check_math_tools.py --profile <profile> --strict` 现场确认；“可用”只表示能生成候选或证据，不表示能解决开放问题。

外部调研清单与本目录严格分离：`surveyed` 只说明找到来源，`source_locked` 只说明固定代码；之后还必须依次达到 `installed`、`smoke_checked`、`evidence_capable`，独立验证器还需 `verifier_admitted`。41 个工具族的保守状态真相源是 `governance/control-plane/math-tool-maturity.v1.json`；未获得相应 `runtime_route`、未列入本目录或现场 strict probe 失败的工具不得由 Router 当作运行能力。

## 运行时边界

| 运行时 | 工具 | 用法 |
|---|---|---|
| 项目 Python `.venv` | SymPy、NumPy、SciPy、mpmath、python-flint、gmpy2、NetworkX、igraph、cvc5、PySAT | 项目脚本、精确/数值计算、图与 SAT/SMT 编排 |
| 系统/独立 Python | Z3、FEniCSx/dolfinx、PETSc、SLEPc、MPI、UFL | 通过 `MATH_TOOLS_SYSTEM_PYTHON` 与 `MATH_TOOLS_FENICS_PYTHON` 固定解释器；不得假定可从项目 `.venv` import |
| 专用 CLI/运行时 | SageMath、GAP、PARI/GP、Singular、Macaulay2、polymake、4ti2、TOPCOM、nauty、MiniSat | 使用各工具原生命令；Sage 可由 `MATH_TOOLS_SAGE` 固定；保存输入文件、版本和输出 |
| Lean 工具链 | Lean、Lake、Mathlib | 归 `math-formalization`；kernel check 不替代陈述忠实性审计 |

## 工具与最小用法

| 类别 | 工具 | 适用问题 | 最小入口 | 证据上限 |
|---|---|---|---|---|
| 精确符号 | SymPy | 代数、微积分、方程、矩阵 | `import sympy as sp` | `symbolic_check` |
| 高精度数值 | mpmath | 任意精度积分、根、常数核对 | `mp.workdps(100)` | `numeric_check` |
| 数值/优化 | NumPy、SciPy | 线性代数、稀疏求解、积分、`scipy.optimize.milp` | 项目 Python | `numeric_check` |
| 精确算术 | python-flint/Arb、gmpy2 | 整数、多项式、球算术、可靠误差界 | `from flint import arb` | `symbolic_check`；区间包含关系需记录精度 |
| 综合 CAS | SageMath | 数论、椭圆曲线、组合、代数几何桥接 | `sage -c '...'` | 计算/符号证据 |
| 数论 | PARI/GP | 整数分解、代数数论、椭圆曲线 | `gp -fq` | 计算/符号证据 |
| 有限代数 | GAP | 有限群、表示、组合结构 | `gap -q` | 有限对象的计算证据 |
| 多项式 | Singular | Gröbner 基、奇点、交换代数 | `Singular -q` | 符号证据 |
| 代数几何 | Macaulay2 (`M2`) | 理想、模、层、代数簇计算 | `M2 --script file.m2` | 符号证据 |
| 多面体 | polymake | 多面体、扇、组合几何 | `polymake script.pl` | 有限计算证据 |
| 整数代数 | 4ti2 | Markov/Graver 基、整数核、格 | `4ti2-zsolve` 等带前缀命令 | 有限计算证据 |
| 三角剖分 | TOPCOM | 点配置、三角剖分、定向拟阵 | `topcom-points2triangs` | 枚举证据 |
| 图论 | NetworkX、igraph | 图构造、算法原型、性质扫描 | 项目 Python | 有限计算证据 |
| 图生成 | nauty/Traces | 同构消重、规范标号、图枚举 | `nauty-geng`、`dreadnaut` | 有界穷举证据 |
| SMT | Z3、cvc5 | 逻辑公式、有限/有界模型、反例 | 系统 `z3`/Python；项目 Python `cvc5` | 对编码公式的判定证据 |
| SAT | PySAT、MiniSat | CNF、组合搜索、证明/反例候选 | `pysat.solvers`、`minisat` | 对编码 CNF 的判定证据 |
| PDE/FEM | FEniCSx/dolfinx | Navier–Stokes 数值离散、残差实验 | `/usr/bin/python3` | `numeric_check`，不能证明全局正则性 |
| 线性/特征值 | PETSc、SLEPc | 大规模稀疏线性系统与谱计算 | `petsc4py`、`slepc4py` | 数值证据 |
| 并行 | MPI/mpi4py | 有界并行计算 | `mpirun`、系统 Python | 运行能力，不是数学证据 |
| 形式化 | Lean/Lake/Mathlib | 定义、引理、内核检查 | `lake env lean Main.lean`；非交互环境可设置 `MATH_TOOLS_LEAN`/`MATH_TOOLS_LAKE` | `kernel_check`；仍需 statement faithfulness |

## Profile 用法

```bash
python3 scripts/check_math_tools.py --profile core --strict
python3 scripts/check_math_tools.py --profile number-theory --strict
python3 scripts/check_math_tools.py --profile complexity --strict
python3 scripts/check_math_tools.py --profile algebraic-geometry --strict
python3 scripts/check_math_tools.py --profile combinatorics --strict
python3 scripts/check_math_tools.py --profile pde --strict
python3 scripts/check_math_tools.py --profile formalization --strict
python3 scripts/check_math_tools.py --profile millennium --strict --json
```

## 明确不装

- Mathematica、Magma：商业许可工具，不伪装为可重建开源依赖；需要时由用户单独授权并固定许可证边界。
- Coq、Isabelle：当前项目可信内核已选 Lean，不为“工具齐全”增加第二条形式化栈。
- OR-Tools：当前整数优化先用 SciPy `milp`，避免扩大 Python 二进制依赖面；真实基准证明不足时再引入。
- 独立 CaDiCaL/Kissat/cvc5 CLI：当前 PySAT、MiniSat、Z3 与 cvc5 Python 已覆盖首批需求；只有基准显示求解器瓶颈时再固定源码版本。

## 结果记录

每次研究运行至少保存：问题与编码版本、工具及版本、运行时、输入文件/脚本、资源预算、命令、退出码、标准输出摘要、完整 artifact 摘要、确定性种子、覆盖范围和 evidence 类型。工具返回成功不自动证明原数学陈述；编码忠实性和一般化步骤必须独立审查。
