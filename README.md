# 好好生活 · 马来西亚 🇲🇾

**一份有来源、可纠错、由大家共同完善的马来西亚生活指南。**

[阅读网页](https://choonseng4896-rgb.github.io/how-to-live-better-malaysia/) · [贡献指南](CONTRIBUTING.md) · [来源与核验记录](SOURCES.md) · [提供资料 / 报错](https://github.com/choonseng4896-rgb/how-to-live-better-malaysia/issues/new/choose)

我们希望每一个马来西亚人都能参与：分享本地数据、核对政策、纠正错误、改善翻译或代码。中文、Bahasa Melayu、English 投稿都欢迎。不会写代码也可以通过 Issue 提供资料。

> **Sumbangan semua rakyat Malaysia dialu-alukan. Sertakan sumber yang boleh disemak.**
> **All Malaysians are welcome to contribute. Please include verifiable sources.**

## 先诚实说明当前进度

- 公开种子版：**12 条附直接来源内容、8 份一手资料、5 个已有内容主题**。来源来自 EPF、PIDM、MySejahtera、TNG Digital、BNM 和 WHO。
- 初版其余 **33 条未达到逐项来源标准的草稿**保存在 `drafts/`，不进入正式页面。其中部分主题已被新的有来源内容替换。
- 初始内容由 AI 辅助整理，已读取对应来源正文；**尚未经过社区独立复核**，不冒充专家审核或官方背书。
- “可选动作”属于编辑者依据资料提出的建议，和来源直接支持的事实分开。
- 这不是原书 528 条的完整马来西亚翻译，也不承诺一个预算适合全国所有城市。

## 谁可以编辑？

任何人都可以 Fork、编辑并提交 Pull Request（修改提案）；维护者核对来源后合并到正式版本。任何人也都可以提交 Issue。

**开放贡献不等于所有人直接覆盖主分支。**正式内容的可信度需要审核。加入贡献者名单无需提交身份证、国籍证明或个人地址。

## 内容标准

每条正式内容必须有：直接来源链接、支持位置、适用范围、资料时期、正文核对日期、建议复核期限与审核状态。不能把新闻标题、AI 回答、搜索摘要或机构主页当成整条结论的证明。

- 政策与资格：优先政府、监管机构、运营方正式规则。
- 价格：写明日期、地点、单位、样本与额外费用；不可把个别账单泛化成全国平均。
- 健康：优先卫生部门或正式公共卫生指南，不用个人经验替代医疗结论。
- 数据计算：写清输入、单位、公式、汇率日期与缺失值处理。
- AI：可以协助翻译、整理和找资料，但投稿者必须读原文并逐项核对。不得编造论文、链接、金额或审核人。

详见 [证据标准](EVIDENCE_POLICY.md)。自动检查只检查结构，不证明结论正确。

## 阅读与运行

无需安装依赖。双击 `dist/index.html` 即可离线阅读。官方外链需联网。

修改正文请编辑 `content/items.json` 与 `content/sources.json`，然后运行：

```bash
python3 scripts/build.py
python3 scripts/build.py --check
python3 -m unittest discover -s tests
```

需要 Python 3.9 或以上。页面支持关键词搜索、收藏、明暗主题和打印。收藏在本机浏览器保存。

```text
content/       正式正文、来源注册表与章节
scripts/       验证与网页生成器
templates/    网页模板
dist/         生成的离线网页
drafts/       待补证据草稿，不进入网页
tests/        来源门槛与安全输出测试
.github/      投稿、纠错、PR 模板与自动检查 / Pages 发布
```

## 搜索与 SEO

正文在构建时写入 HTML，无 JavaScript 时仍可阅读。搜索支持常用中英马关键词、多词匹配、高亮、快捷词及可分享查询链接；这不代表完整多语言翻译。页底资料清单默认折叠，每条内容的来源记录保留。

页面有 canonical、分享元数据、CollectionPage / ItemList 结构化数据与 sitemap.xml；搜索结果页共用主页 canonical。Search Console 提交及搜索排名需上线后单独观察，不保证收录或流量。

参见 [待审核报告](docs/review-report.md) 与 [公众参与试运行方案](docs/community-plan.md)。

## 一起补齐马来西亚

欢迎为 Johor、Kedah、Kelantan、Melaka、Negeri Sembilan、Pahang、Perak、Perlis、Pulau Pinang、Sabah、Sarawak、Selangor、Terengganu，以及 Kuala Lumpur、Putrajaya、Labuan 补充资料。已有种子内容主要为全国性资源和巴生谷交通，不能代表全国覆盖完成。

优先方向：租房与居家、各州交通、门诊入口、合理的饮食预算、工作与学习、家庭支出及数字安全。提交资料时保留来源的局限和城市差异。

## 许可与致谢

原创代码与原创摘要使用 [MIT License](LICENSE)。引用网页、机构名称、数据及其他第三方材料不因此改变其原有权利；本项目不重新授权第三方正文、标识或图片。

灵感来自 [cdyforever/how-to-live-better](https://github.com/cdyforever/how-to-live-better) 与其上游 [eternity4719/HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter)。本项目重新编写内容与页面，未复制原书正文，不代表上述作者或引用机构的认可。
