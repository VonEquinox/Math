# 正多边形非负秩研究

研究正多边形松弛矩阵的实非负秩，整理计算机辅助证明、可离线复验的代码与证书。

**正 58 边形的非负秩已确定为 12。正 49 边形仍为 11 或 12，一般精确公式尚未证明或证伪。** 本仓库中的结果尚未经过外部同行评审，不声称完成形式化验证或文献优先权确认。

## 已得到什么

| 对象 | 项目内已复验结论 | 本次发布范围 |
|---|---|---|
| 正 25–32 边形 | 非负秩等于 10 | 附离线证书 |
| 正 33–48 边形 | 非负秩等于 11 | 附离线证书 |
| 正 58 边形 | **非负秩等于 12** | 附归约、最后 76 面排除与精确上界证书 |
| 正 59–60 边形 | 非负秩等于 12 | 附离线证书 |
| 正 61–64 边形 | 非负秩等于 12 | 附终端证书；母几何分类依赖另见复验指南 |
| 正 49 边形 | 六维候选至多两条缺边，且至少 53 个面；包含型十面提升最多共享 31 个原顶点 | 附离线证书 |
| 局部圆弧 | 任意正多边形网格的 4.71° 圆弧上，十面提升最多保留 32 个指定顶点，且 32 可达 | 附离线证书 |
| 精细矩形覆盖猜想 | 存在正多边形使 RRCB ≤ 296 < 297 ≤ 非负秩 | 附证明与独立整数核验 |

最后一行反驳的是“精细矩形覆盖数等于非负秩”的辅助猜想，**不是**本项目的非负秩精确公式猜想。各个边数的精确值不通过对边数的单调性推导。

## 文件与复验

- [成果与边界说明](docs/RESULTS_ZH.md)：定义、精确结果、尚未解决的范围。
- [复验指南](docs/REPRODUCIBILITY_ZH.md)：证书入口、依赖、校验层级。
- [精细矩形覆盖反例的完整证明](docs/RRCB_COUNTEREXAMPLE_ZH.md)。
- [已核验的反例与适用范围](docs/COUNTEREXAMPLES_ZH.md)：区分文献猜想的反例和仅对特定方法有效的反例。
- 正 49、正 58 与局部圆弧离线证书 v3（原档 19,854,095 字节）：[第 1 段](artifacts/regular-polygons-49-58-and-local-arc-certificates.zip.part00)、[第 2 段](artifacts/regular-polygons-49-58-and-local-arc-certificates.zip.part01)。克隆仓库后运行下方命令，会合并为字节完全相同的 ZIP 并校验。
- [正 61–64 边形精确证书](artifacts/regular-polygons-61-64-exact-certificate.zip)（1,863,850 字节）。
- [精细矩形覆盖反例离线包](artifacts/regular-polygon-RRCB-counterexample.zip)。
- 正 58 边形精确值：先读[复验指南](docs/REPRODUCIBILITY_ZH.md#8-正-58-的精确值)，再取[归约到仅余 76 面](artifacts/regular-polygon-58-only76.zip)和[最后 76 面的排除及十二项上界](artifacts/regular-polygon-58-exact-f76.zip)。
- [正 58 边形至少 68 面的补充证书](artifacts/regular-polygon-58-min68-supplement.zip)，叠加到上方 49 / 58 归档的解压目录。
- 正 25–48 的精确证书：[第 1 段](artifacts/regular-polygons-25-48-exact-certificate.zip.part00)、[第 2 段](artifacts/regular-polygons-25-48-exact-certificate.zip.part01)、[第 3 段](artifacts/regular-polygons-25-48-exact-certificate.zip.part02)。
- 正 59 的精确证书：[第 1 段](artifacts/regular-polygon-59-and-49-free-standalone.zip.part00)、[第 2 段](artifacts/regular-polygon-59-and-49-free-standalone.zip.part01)。
- 正 60 的精确证书：[第 1 段](artifacts/regular-polygon-60-exact-certificate.zip.part00)、[第 2 段](artifacts/regular-polygon-60-exact-certificate.zip.part01)。
- [SHA256SUMS](SHA256SUMS) 核对重建后的原始 ZIP；[SHA256SUMS.parts](SHA256SUMS.parts) 核对分段。

先执行文件完整性检查：

```sh
python3 verify_artifacts.py
```

脚本会自动按顺序拼接传输分段。它只检查 SHA-256、ZIP 完整性和安全解压路径，**不等于数学证明的复验**。数学复验请按复验指南在分别解压的目录中执行。较大的计算需要 C++17、Python 3、gzip 和临时磁盘空间。

本次保留已复验归档的原始字节，未重写历史证明。归档中若出现早期的较弱界，以本仓库索引及明确列出的后续证明为准；尤其正 49 的旧“至少 52 面”已经由全部 52 面分支的排除加强为“至少 53 面”。

## 其他数学研究

- [Constant-width higher-rank numerical ranges need not be disks](docs/HIGHER_RANK_NUMERICAL_RANGE_COUNTEREXAMPLES.md)：反驳 Chien–Li–Nakazato 的高阶数值域等宽猜想，给出两个六阶显式反例（秩三勒洛三角形、秩二解析严格凸曲线）及一般压缩秩推广。纯解析证明，无需数值证书；原创性与外部同行审查尚待完成。
