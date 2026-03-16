# xiaowu-market-pipeline

《小五的市场笔记》全链路自动化 skill。

用于从 A 股市场数据与财经新闻出发，生成公众号复盘文章、封面 prompt，并通过微信公众号接口创建草稿、提交发布、查询状态。

## 目录结构

```text
xiaowu-market-pipeline/
├── SKILL.md
├── README.md
├── config.template.json
├── references/
└── scripts/
```

## 配置说明

本 skill 发布到 skills 仓库时，不包含任何真实鉴权信息。

请在本地创建：

```text
runtime/xiaowu-market-pipeline/config.local.json
```

配置示例：

```json
{
  "image_api": {
    "url": "",
    "bearer_token": ""
  },
  "wechat": {
    "app_id": "",
    "app_secret": "",
    "author": "小五",
    "source_url": ""
  }
}
```

说明：
- `image_api.*`：封面图生成接口配置
- `wechat.app_id` / `wechat.app_secret`：微信公众号接口凭据
- `wechat.author`：默认作者名，可选
- `wechat.source_url`：默认原文链接，可选

## 安全约定

- 不提交任何真实 token、secret、cookie、账号信息
- 不提交 `config.local.json`
- 不提交 runtime 产物（文章 HTML、封面图、发布结果等）
