# 离线复验指南

## 1. 检查归档

在仓库根目录执行：

```sh
python3 verify_artifacts.py
```

程序逐字节核对三个 ZIP 的 SHA-256，并检查各成员的 CRC 和路径。这只是完整性核对，不执行数学证明。

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
| 从局部完整目录重建上一项所用截面 | `sh CODE/r8_general_s58_min67.sh --rebuild` |
| 4.71° 局部圆弧锐界 32 | `sh CODE/r7_general_short33_replay.sh` |

一些完整重建会产生约 GB 量级的临时文件。脚本的正常退出会清理其自行创建的临时目录。不要用仅末端复验替代对源目录完备性和几何归约的审阅。

## 5. 正 61–64 的精确终端证书

```sh
cd replay/exact61-64
sh CODE/replay_61_64.sh
```

需要 Python 3.10+、C++17 和 gzip。该入口复核随包临界模板与算术终端。母几何分类及五个完整模板层来自尚未收入本批的正 25–48 原始包；补齐那些模板后可运行 `sh CODE/replay_61_64.sh full`，核对临界模板与母分类一致并重建相应共点表。不要把终端复验说成已经从零复算所有分类。

## 6. 历史文档与发布边界

- 当前归档主要是正 49、正 58 及局部圆弧的证书选集，不是项目全部成果的总包。
- 个别说明保留了前一阶段的较弱界，以 `README_ZH.md`、`R8_S49_D6_F52_ALL.md` 与 `R8_S58_MIN67.md` 的明确后续结论为准。
- 归档中的 `OPTIONAL/` 补充命题不是当前精确秩结果的必要组成部分。
- 某些历史证明引用其他归档的文本或早期几何生成说明。附带的终端数据不是这些论证的替代品；完整依赖应按原证明追溯。
- 本发布没有附加软件许可证，也不替第三方目录或论文重新授权；请保留原始来源标注。

### 49 / 58 合集的传输分段

这一份原始 ZIP 在仓库里以 .zip.part00 和 .zip.part01 存放。克隆仓库后，先在仓库根目录运行 python3 verify_artifacts.py。该程序会按顺序拼接并核对原档 SHA-256，然后再按上述指南解压。单独下载时，需把两段都存入 artifacts/。
