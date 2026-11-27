# 证据、版本与离线复验

## 原档身份

冻结原档：`regular-polygon-capacity-theory-2026-11-27-2200.zip`，24,793,417 字节。

SHA-256:

```text
3e6509df4b450d6bda4547d58315da9612fe392343c78344e9ff9909c917183a
```

本次整理实际核对了最新 ZIP 的 252 项根清单，以及其中 23 个互异内嵌 ZIP 的 CRC 和已有清单；合计 24 个互异 ZIP。00:00 原档无根级 SHA256SUMS.txt，只能做 CRC 和父档所给的字节校验。**这不是数学全量复跑，也不是外部同行审查。**

原档在资料库中；本次 GitHub 文本提交没有包含大二进制文件。完整补充包按哈希保留原始文件，清单见 [SOURCE_INVENTORY.tsv](SOURCE_INVENTORY.tsv)。如补齐原始二进制，可放在 `artifacts/research-snapshots/2026-11-27/`，不要覆盖旧归档或把外层补充包整个作为 Git blob。

字节检查（需要 Python 3.9+）：

```sh
python3 code/verify_capacity_snapshot.py /path/to/regular-polygon-capacity-theory-2026-11-27-2200.zip
```

## 数学复跑（原档完整解压后）

进入冻结原档解压目录。需 Python 3、NumPy、SciPy、标准 C++17 编译器、xz 等。以下是原档提供的复验入口：

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
sha256sum -c SHA256SUMS.txt
python3 -IB capacity_program/edition_2200/verify_history_archives.py
python3 -IB CODE/verify_22_absolute_ten_facet_shadow_bound.py
python3 -IB CODE/verify_22_stable_window_certificates_from_original_catalogues.py --include38
python3 -IB THEORY/capacity_geometric/verify_all_even_cube_projection_frontiers_actual_masks_and_hidden_vertex_ledger.py
python3 -IB THEORY/capacity_geometric/verify_twisted_true_sixteen_gate_and_all_one_line_cube_projection_minimizers.py
```

原档 `capacity_program/edition_2200/CHECKS.json` 提供输入、脚本哈希与原始运行结果；`SOURCE_INDEX.tsv` 定位所有本层文件；`ROOT_INTEGRATION_2200.md` 和 `capacity_program/edition_2200/DEPENDENCY_MAP_ZH.md` 给出未解桥梁。完整历史在嵌套的 `history/` 中，旧证明未改写。

几何凸包的容差测试、有限域／整数精确检查、以及全称解析证明属于不同证据层级。不得以文件哈希校验替代任何数学步骤。

## 37 角通用容量定理的证据链

秩三松弛表、十项分解和 Sylvester 不等式给出两岸真实有界提升，至少一岸维数至多五。经极对偶和保持截面角数的泛化扰动，五维十顶点单纯多胞体的面数为 $42-2k$，若至少有 37 个截面角，只需检查 42、40、38 面三类原图。真实截面相交的原面必须在十个锚点的商空间半周翻号扫描中同时保留。每个真实正负半球诱导复形的 Euler 示性数均为 1；算法对未知翻号顺序和符号赋值作必要条件外覆盖，而非假设一个特定定向拟阵。各锚允许独立顺序，但共享同一批舍弃原面预算。

原档独立全量复播（不是本次新运行）的终端摘要：

| 原面数 | 输入候选 | 搜索节点 | 幸存 |
|---:|---:|---:|---:|
| 42 | 159375 | 480877717 | 0 |
| 40 | 648392 | 624761056 | 0 |
| 38 | 444813 | 76929028 | 0 |

原始记录 `ROOT_INDEPENDENT_118Q_REPLAY_2200.txt`。正式证明位于：

`THEORY/capacity_stress/118Q_NO_CONVEX_POLYGON_WITH_THIRTY_SEVEN_VERTICES_HAS_A_TEN_FACET_LIFT_BY_A_COMMON_FACET_BUDGET_ON_TEN_TRUE_POLAR_EQUATORS.md`。

完整性依赖 [Miyata–Padrol](https://arxiv.org/abs/1408.0688) 的枚举、[Firsching](https://arxiv.org/abs/1508.02531) 的可实现性分类，以及非最大面数的递归可见性外覆盖（原档 118O、118P）。取 159375 个可实现面格，不把坐标样例当作所有几何实现。详细外部输入与哈希见 `capacity_program/edition_2200/DATA_PROVENANCE_ZH.md`。

## 必须分开的 33–36 证据链

旧正 25–48 ZIP 的 `R4_33_36_README_ZH.md` 声称完整正 33–36 的非负秩为 11，引用正则三角化外覆盖、共同商空间符号、退化极限以及精确乘积终端比较。其独立终端日志为：

```text
n 33 templates 337577 tried 18743581 holes 0 strict 18743581 accepted 0
n 34 templates 23374 tried 462838 holes 0 strict 462838 accepted 0
n 35 templates 1108 tried 6946 holes 0 strict 6946 accepted 0
n 36 templates 42 tried 42 holes 0 strict 42 accepted 0
```

该日志只能核对已给模板的终端，不替代完备外覆盖的独立验证。旧档复验入口：

```sh
sh CODE/r4_replay_independent_metrics.sh
sh CODE/r4_replay_regular33_36.sh terminal
REPLAY_JOBS=8 sh CODE/r4_replay_regular33_36.sh all
```

22:00 档明确不以该旧链为前提，只报告整阶 37–48，33–36 在新链中尚未闭合。没有找到已正式撤回旧证明的材料，也没有在本次完成旧链的独立全量审计；因此当前对外索引将 33–36 标记为历史精确声明、待复核，不作无证据的确认或否定。

## 优先审计顺序

1. 旧 R4 完备外覆盖和全覆盖复跑，解决 33–36 状态不一致。
2. 22:00 通用 37 角下界的维数平衡、扰动、共同原面预算及三类图录覆盖。
3. 窗口严格正参数、两侧真实外翼、完整镜像读回以及无限族传递。
4. 任意维数几何定理的真极点、正高度、面格和等号条件。
5. 一般容量进入引理仍需新证明；现有局部结论不能代替它。
