---
name: xiaowu-market-pipeline
description: 《小五的市场笔记》全链路自动化 Skill。适用于需要从 A 股市场数据抓取、财经新闻抓取、主线与催化分析、文章生成、公众号封面 prompt 生成、封面图生成，到微信公众号草稿创建/自动发布/发布状态查询的完整流程。用于搭建、执行、排查或标准化每日盘后市场方向复盘内容流水线。
---

# Xiaowu Market Pipeline

将《小五的市场笔记》做成一条完整流水线：从“数据与新闻”到“文章与封面”，再到“公众号草稿或发布”。

## 全链路工作流

1. 抓取今日股市数据
2. 抓取与主线相关的财经新闻
3. 生成盘后复盘正文
4. 生成封面图 prompt
5. 调用图片接口生成 21:9 封面
6. 通过微信官方 API 创建草稿
7. 在用户明确确认后自动发布
8. 查询发布状态

## 什么时候使用这个 Skill

当任务涉及以下任一场景时，使用本 Skill：
- 生成《小五的市场笔记》当天盘后复盘
- 复用既定模板写市场复盘文章
- 为市场复盘文章生成公众号封面 prompt
- 将文章与封面送进微信公众号草稿箱
- 自动发布公众号文章并查询状态
- 排查全链路中任何环节的问题：数据源、新闻源、封面生成、公众号 API、排版、编码等


## 首次配置

发布到共享 skills 仓库时，不要携带任何真实凭据。

应只保留 `config.template.json`，并在本机运行时创建：

```text
runtime/xiaowu-market-pipeline/config.local.json
```

至少需要本地配置以下敏感字段：
- `wechat.app_id`
- `wechat.app_secret`
- `image_api.url`
- `image_api.bearer_token`

不要把真实 `config.local.json`、封面图、草稿结果、发布结果提交到 skill 仓库。

## 模块划分

### 模块 1：市场数据
读取 `references/market-data.md`。

当前已验证的主路径是 AkShare，至少包括：
- 指数日线
- 市场情绪总览
- 涨停池
- 行业板块排行
- 概念板块排行

### 模块 2：财经新闻与催化
读取 `references/news-and-catalysts.md`。

当前策略：
- 第一优先：搜索聚合抓当日财经新闻
- 第二优先：财联社、证券时报等直抓做辅助
- 目标：为“催化与后续观察”模块提供 3~5 条有效催化

### 模块 3：正文生成
读取 `references/article-template.md`。

如需将正文送入公众号草稿，不要临时手写 HTML；改为读取 `references/wechat-formatting.md`，并优先使用 `scripts/render_wechat_article.py` 生成稳定版 HTML。

《小五的市场笔记》默认结构：
- 结论
- 指数与市场情绪
- 今日主线
- 盘面理解
- 催化与后续观察
- 明日重点观察
- 小五一句话收口

风格要求：
- 冷静
- 礼貌
- 克制
- 专业
- 先结论，后依据
- 高智感、低情绪噪音
- 可读但不过度表演

### 模块 4：封面 prompt 生成
读取 `references/cover-prompt.md`。

当前固定方向：
- 21:9 横版
- Mondo 海报风
- 概念化表达，不写实
- 深色背景 + 科技冷光
- 少元素、大留白、强主视觉
- 适配公众号标题叠加

### 模块 5：公众号发布
读取 `references/wechat-official-api.md`。

默认使用微信官方原生 API：
- 获取 token
- 上传封面素材
- 新增草稿
- 提交自动发布
- 查询发布状态

## 本地配置

发布到 skills 仓库时，不要携带任何真实鉴权信息。

只保留 `config.template.json` 作为模板；本机运行时，从：

```text
runtime/xiaowu-market-pipeline/config.local.json
```

读取真实配置。至少包括：

- `image_api.url`
- `image_api.bearer_token`
- `wechat.app_id`
- `wechat.app_secret`

不要把真实值写进：
- `SKILL.md`
- `README.md`
- `references/*.md`
- `scripts/*.py`

## 安全规则

- 创建草稿通常可以直接执行。
- 自动发布属于真实外部动作；执行前必须得到用户明确确认。
- 如需发布状态追踪，保留 `draft media_id` 与 `publish_id`。

## 推荐执行顺序

### A. 内容生成阶段
1. 用 AkShare 抓取盘后数据
2. 抓取新闻并筛选催化
3. 生成完整文章正文
4. 生成封面图 prompt
5. 调用图片接口生成封面图

### B. 发稿阶段
1. 上传封面图为永久 thumb 素材
2. 将文章送入公众号草稿箱
3. 用户确认后，调用自动发布
4. 查询发布状态并记录结果

## 脚本

### 微信公众号官方原生脚本
优先组合使用：

- `scripts/render_wechat_article.py`
- `scripts/wechat_mp_publish.py`
- `scripts/requirements.txt`

其中：
- `render_wechat_article.py` 用于把结构化正文渲染为更适合公众号草稿的 HTML
- `wechat_mp_publish.py` 用于创建草稿、提交自动发布、查询发布状态

详细说明见：
- `references/wechat-formatting.md`
- `references/publishing-script.md`

## 常见问题

- 数据抓到了，但文章质量不稳定：先检查 `references/article-template.md` 里的结构与风格要求。
- 新闻很多但“催化与后续观察”很乱：先筛到 3~5 条，并明确每条新闻对应的方向、类型、强度。
- 封面图不稳定：回到 `references/cover-prompt.md`，保持风格骨架不变，只替换主题层。
- 草稿接口报标题超长：先检查 JSON 是否 UTF-8 且 `ensure_ascii=False`，不要先假设真的是字数超限。
- 外链不可点击：不要只塞裸文本 URL；优先用 `scripts/render_wechat_article.py` 输出 `<a href="...">标题</a>`，并同时保留完整 URL 作为备用显示。

## 参考资料

按需读取以下文件：
- `references/market-data.md`
- `references/news-and-catalysts.md`
- `references/article-template.md`
- `references/cover-prompt.md`
- `references/wechat-formatting.md`
- `references/wechat-official-api.md`
- `references/publishing-script.md`
