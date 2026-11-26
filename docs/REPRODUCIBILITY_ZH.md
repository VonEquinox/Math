# 离线复验指南

## 1. 检查归档

在仓库根目录执行：

```sh
python3 verify_artifacts.py
```

程序按顺序拼接必要的传输分段，逐字节核对清单中的 ZIP 的 SHA-256，并检查各成员的 CRC 和路径。这只是完整性核对，不执行数学证明。

## 2. 分别解压

```sh
mkdir -p replay/polygons replay/rrcb replay/exact61-64
unzip artifacts/regular-polygons-49-58-and-local-arc-certificates.zip -d replay/polygons
unzip artifacts/regular-polygon-RRCB-counterexample.zip -d replay/rrcb
unzip artifacts/regular-polygons-61-64-exact-certificate.zip -d replay/exact61-64
```

各个包必须放在不同目录，避免同名文件覆盖。归档原始字节未修改。`replay/` 是本地生成内容，不应提交。

## 3. 小型独立反例

```sh
cd replay/rrcb
python3 verify_rrcb_counterexample.py
```

只需要 Python 3。它核对整数二项式上界、有限域运算和编码根数界；完整数学论证仍需结合 `README.md` 阅读，无需显式生成巨大松弛矩阵。

## 4. 正 49、正 58 与局部圆弧

以下命令均从 `replay/polygons/` 执行，需要 Unix shell、C++17 编译器、Python 3、gzip。请阅读每个对应证明文件后选择命令；耗时和临时磁盘用量因机器及入口不同。

| 要复验的结论 | 命令 |
|---|---|
| 正 49 的 52 面全部分支 | `sh CODE/r8_s49_f52_all_replay.sh` |
| 只检查上一项的末端标号匹配与填面 | `sh CODE/r8_s49_f52_all_replay.sh --terminal` |
| 正 49 的包含型共享顶点上限 31 | `sh CODE/r8_s49_containing32_replay.sh` |
| 交叉多面体顶点图的有限构型 | `sh CODE/r8_general_cross_types.sh` |
| 正 58 的全网格自由容量 32 | `sh CODE/r8_general_s58_free32.sh` |
| 正 58 排除交叉多面体顶点图 | `sh CODE/r8_general_s58_nocross.sh` |
| 正 58 六维候选至少 67 面 | `sh CODE/r8_general_s58_min67.sh` |
| 从局部完整目录重建上一项所用截面 | `sh CODE/r8_general_s58_min67.sh --rebuild`（先按下方勘误修正输入生成） |
| 4.71° 局部圆弧锐界 32 | `sh CODE/r7_general_short33_replay.sh` |

**正 58 可选重建入口勘误。** 原档的默认终端命令不受影响。若要从母分类重新生成，可选的 --rebuild 入口需要 32 面层；原始 CODE/r3_geom_fill.cpp 默认只输出 33 面及以上。请在解压的一次性副本中把 if(nf>=33) 改成 if(nf>=32)，再运行重建。否则会在输入 SHA 检查停止，不会静默通过。仍可直接复验默认终端。

一些完整重建会产生约 GB 量级的临时文件。脚本的正常退出会清理其自行创建的临时目录。不要用仅末端复验替代对源目录完备性和几何归约的审阅。

## 5. 正 61–64 的精确终端证书

```sh
cd replay/exact61-64
sh CODE/replay_61_64.sh
```

需要 Python 3.10+、C++17 和 gzip。该入口复核随包临界模板与算术终端。母几何分类及五个完整模板层来自同仓库的正 25–48 原始包；按脚本说明引用那些模板后可运行 `sh CODE/replay_61_64.sh full`，核对临界模板与母分类一致并重建相应共点表。不要把终端复验说成已经从零复算所有分类。

## 6. 历史文档与发布边界

- 正 49 / 58 合集是结构性证书选集，不是精确秩的证明；正 25–48、58、59、60 和 61–64 的精确证书各自保存。
- 个别说明保留了前一阶段的较弱界，以 `README_ZH.md`、`R8_S49_D6_F52_ALL.md` 与 `R8_S58_MIN67.md` 的明确后续结论为准。
- 归档中的 `OPTIONAL/` 补充命题不是当前精确秩结果的必要组成部分。
- 某些历史证明引用其他归档的文本或早期几何生成说明。附带的终端数据不是这些论证的替代品；完整依赖应按原证明追溯。
- 本发布没有附加软件许可证，也不替第三方目录或论文重新授权；请保留原始来源标注。

### 较大归档的传输分段

较大的原始 ZIP 在仓库里按 .zip.part00、.zip.part01 等连续编号存放。克隆仓库后，先在仓库根目录运行 python3 verify_artifacts.py。该程序会按顺序拼接并核对原档 SHA-256，然后再按上述指南解压。单独下载时，需把全部分段都存入 artifacts/。

## 7. 正 25–48、59 与 60 的精确值

先运行该指南第 1 步重建原始 ZIP，并将三个归档解压到不同目录。

- 正 25–48：从归档里的 README.md 进入。正 25–32 的入口是 sh CODE/r2_replay_exact_25_32.sh；正 33–48 按 R4_33_36_README_ZH.md 和 R3_37_48_README_ZH.md 的入口分别核验。
- 正 59：在对应解压目录运行 sh CODE/r6_general_s59_replay.sh。
- 正 60：在对应解压目录运行 sh CODE/r8_s60_full_replay.sh；先读 R8_S60_EXACT.md。

各包使用原始安装前提、模板与目录名。进行数学复验时，请采用归档自己的入口，不要在不同包间任意覆盖文件。

## 8. 正 58 的精确值

**结论：正 58 的非负秩为 12。** 早期资料中的“仍是 11 或 12”属于历史记录。新的证书用两份冻结原始档分别处理归约到只余 76 面，以及排除这最后的 76 面；四次反射给出精确匹配的 12 项上界。此结果不是对一般猜想的证伪。

先从仓库根目录运行第 1 步的完整性脚本，把分段恢复为原始 ZIP。此处各份档案是同一研究目录的叠加层，**只对下列这组正 58 证书按照给定顺序解压到同一个新目录**：

```sh
mkdir -p replay/exact58
for archive in \
  regular-polygons-49-58-and-local-arc-certificates.zip \
  regular-polygon-58-min68-supplement.zip \
  regular-polygon-58-at-least-71-facets.zip \
  regular-polygon-58-after71-structure.zip \
  regular-polygon-58-only76.zip \
  regular-polygon-58-exact-f76.zip
do
  unzip -o "artifacts/$archive" -d replay/exact58
done
cd replay/exact58
```

三份先前的结构性补充填齐 68→70→71 的几何分类和 36 面局部三角形排除。其中 [至少 71 面汇总](../artifacts/regular-polygon-58-at-least-71-facets.zip)含 70 面归约所需的 38 面、32 标记排除数据；[71 面后续结构](../artifacts/regular-polygon-58-after71-structure.zip)含 36 面、31 标记的独立终端。最先叠加的 min68 补充已修复从母分类重建时四缺边星形的排除；其历史默认终端不受影响。正 60 的独立归档提供 51 个母种子覆盖真实 37 种旧多面体的证明背景，请在其自己的目录中阅读 `R8_S60_EXACT.md`（正 58 档已附复跑所用的冻结种子数据）。

在合并后的目录按阶段运行；需要小端 Linux、GNU 工具、C++17、Python 3.10+、gzip、xz：

| 阶段 | 命令 |
|---|---|
| 早期完整边图、32 个自由标记上限、排除交叉顶点图 | `sh CODE/r8_general_s58_free32.sh` 和 `sh CODE/r8_general_s58_nocross.sh`，阅读 `R8_S58_COMPLETE_GRAPH.md` |
| 早期 67、68、70、71 面界 | 依次 `sh CODE/r8_general_s58_min67.sh`、`sh CODE/r8_general_s58_min68.sh`、`sh CODE/r8_general_s58_min70.sh`、`sh CODE/r8_general_s58_min71.sh` |
| 后续 36 面、31 标记的三角形缺边排除 | `sh CODE/r8_general_s58_after71.sh` |
| 75 面若可行则需要 40 面、32 标记的局部图型 | `sh CODE/r8_general_s58_f75.sh` |
| 正 58 排除全部 40 面、32 标记局部图型 | `sh CODE/r9_general_s58_min76.sh` |
| 直接排除 77 面 | `sh CODE/r9_general_s58_f77.sh` |
| 排除最后的 76 面，核验 12 项上界 | `sh CODE/r9_general_s58_e1.sh` |

阅读 `R9_S58_ONLY76.md` 与 `R9_S58_EXACT.md` 了解各有限覆盖的完备性与假设。末行默认使用冻结目录；`--horizon` 从 51 种母种子重建可见面候选并做逐个精确同构核对，`--marked` 重建实际正规网格标记，`--full` 两者都做。77 面入口默认逐行核验冻结的 42,099 型有理实现目录；只有从作者原始坐标额外重建目录的可选 `--full <坐标文件.xz>` 需要另取来源文件和 GMP（见 `R8_S58_E0_HITTINGSET.md`），不影响常规离线复验。各层内部均区分有限枚举、精确算术终端和数学归约，零容差才可排除候选；仅验末端不能代替全证据链。
