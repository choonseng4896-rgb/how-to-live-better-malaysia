# 搜索与 SEO 改进审核报告

审核日期：2026-10-15（马来西亚时间）。状态：**待骏成审核；本次不得合并或部署到正式站点。**

## 建议结论

建议批准本次界面与 SEO 基础改进，先用小规模邀请验证社区参与，再扩大推广。实现与测试结果信心高；搜索排名、访问量及贡献人数尚无上线数据，无法承诺。

## 本次修改

1. 页底“关于与资料来源”默认折叠；展开后仍能查到完整来源。每条内容的直接来源、适用范围与核验记录保留。
2. 删除“适用地区”控件及相关筛选代码；内容本身的地域限制仍保留，避免把巴生谷规则泛化为全国。
3. 搜索提供常用词入口、中英马常用词关联、多词 AND 匹配、标题优先排序、关键词高亮、清空按钮、无结果提示、`/` 快捷键与 Escape 清空。
4. 搜索词同步到 `?q=`，刷新恢复，便于分享。搜索状态共用主页 canonical，不伪装成独立 SEO 落地页。
5. 每条建议有稳定 `#tip-ID` 锚点；站内导航和分享可以直达内容。
6. 正文和目录预先写入 HTML，再由 JavaScript 增强搜索与收藏。无脚本时仍有 12 条完整正文、真实来源链接和锚点目录。
7. 加入描述性 title、meta description、canonical、Open Graph、Twitter summary、CollectionPage / ItemList JSON-LD 和 sitemap.xml；未伪造 FAQ、评价、机构背书或多语言全文。
8. 保持上次删除的预算计算器、副标题和首页统计行不再出现。

## 测试结果

### 自动检查：通过

- `python3 scripts/build.py --check`：生成文件与正文数据、模板一致。
- `python3 -m unittest discover -s tests`：**14 / 14 通过**。
- `node scripts/check-js.mjs`：应用 JavaScript 语法通过。
- 新增 6 项 SEO/结构测试：静态正文完整性、来源目录默认关闭、已删除控件、canonical/分享元数据、结构化数据与真实内容一致、站点地图只列规范主页。
- 原有 8 项来源结构、安全嵌入与马来西亚日期边界测试保留。

### 实际浏览器：通过

| 搜索词 | 结果数 | 检查结果 |
| --- | ---: | --- |
| EPF | 1 | 通过；已修复与 deepfakes 中间字母的误匹配 |
| kwsp / 公积金 | 各 1 | 通过 |
| MY 50 | 1 | 通过；可容忍空格与大小写 |
| 存款保障 | 4 | 通过 |
| klinik | 1 | 通过 |
| penipuan | 2 | 通过 |
| PIDM 股票 | 1 | 通过；多词同时匹配 |
| 不存在的内容 | 0 | 通过；显示空状态和重置入口 |
| `<script>` / `[` | 各 0 | 通过；未执行脚本或产生正则错误 |

额外已查：My50 快捷词、高亮、`?q=My50` 分享链接和刷新恢复、`/` 聚焦搜索、Escape 清空、页底来源默认隐藏及可展开。390px 与 1280px 页面宽度均无横向溢出，手机搜索结果进入可见区域。

无脚本验证：使用移除应用脚本的临时副本，确认 12 条正文仍显示、无效交互控件隐藏、目录可跳至对应章节。此副本仅用于 QA，不进入 GitHub 或发布包。不是宣称已测试所有浏览器的禁用脚本设置。

## SEO 可以确认与不能确认的部分

**已确认的是实现条件，而不是流量效果。**初始 HTML 已有正文、标题与规范 URL，sitemap 可被提交；这些有利于搜索引擎理解和发现页面。Google 文档明确不保证某个修改会提高排名。

- 待审核 PR 不会更新生产站；SEO 效果只能批准上线后再观察。
- 尚未配置或验证 Google Search Console，也未向 Google 提交本次 sitemap。没有捏造收录、排名、访问量或抓取结果。
- 本项目部署在 `github.io/how-to-live-better-malaysia/` 子路径；搜索引擎读取域名根目录的 robots.txt，项目子目录的同名文件并不等价。因此未添加一个看起来有效、实际不控制主域名抓取的 robots 文件。
- 单页的 `#tip-ID` 是阅读锚点，不是 12 个可独立索引的页面。内容扩展后，可考虑有独立正文与来源的主题页，而不是制造大量薄弱关键词页。
- 常用中英马搜索词关联，不等于已完成英文或马来文全文翻译；没有设置虚假的 hreflang。
- 未运行 Lighthouse、PageSpeed Insights、Google 富媒体测试或真实多设备实验；没有提供虚构分数。
- 自动测试核对来源字段和页面结构，不重新证明全部政策当前有效；事实审核仍需人阅读原文。

## 审核建议

请确认：页底采用“默认折叠、可展开”，而不是删除证据；新的搜索布局和结果高亮符合预期；本次只涉及阅读与搜索体验，没有新增政策事实。批准后再合并 PR、部署，并在生产网址复查。

## 参考资料

- Google SEO Starter Guide：https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google JavaScript SEO：https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- Google robots.txt 位置要求：https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt
- 原项目阅读体验参考：https://cdyforever.github.io/how-to-live-better/
