# xiaowu-market-pipeline

《小五的市场笔记》全链路自动化 skill。

该 skill 用于将每日盘后市场复盘流程标准化，包括：

- 抓取 A 股市场数据
- 抓取财经新闻与催化
- 生成结构化复盘正文
- 生成公众号封面 prompt
- 渲染公众号可用 HTML
- 创建微信公众号草稿
- 在具备权限时提交自动发布并查询状态

## 目录结构

```text
xiaowu-market-pipeline/
├── SKILL.md
├── README.md
├── config.template.json
├── references/
└── scripts/
```

## 配置

本 skill 发布到共享 skills 仓库时，不应包含任何真实凭据。

请先复制模板并填写本地配置：

```text
runtime/xiaowu-market-pipeline/config.local.json
```

模板见：

```text
config.template.json
```

需要配置的敏感字段包括：

- `wechat.app_id`
- `wechat.app_secret`
- `image_api.url`
- `image_api.bearer_token`

这些字段仅应保存在本地 `config.local.json` 中，不应提交到 Git 仓库。

## 发布相关说明

- `scripts/render_wechat_article.py`：将 Markdown 渲染为公众号友好的 HTML
- `scripts/wechat_mp_publish.py`：支持基于配置或命令行参数创建草稿、提交自动发布、查询状态

如果公众号账号缺少 `freepublish` 权限，自动发布会返回：

- `errcode: 48001`
- `errmsg: api unauthorized`

这种情况说明账号权限不足，不代表脚本逻辑错误。
