# 发布脚本说明

脚本位置：

```text
scripts/render_wechat_article.py
scripts/wechat_mp_publish.py
```

其中：
- `render_wechat_article.py` 负责把正文 Markdown 渲染成更适合公众号草稿的 HTML
- `wechat_mp_publish.py` 负责《小五的市场笔记》流程中的“微信公众号发布阶段”，走微信官方原生 API。

## 本地配置

发布到共享 skills 仓库时，只保留 `config.template.json`。
真实配置应放在本机：

```text
runtime/xiaowu-market-pipeline/config.local.json
```

建议结构：

```json
{
  "wechat": {
    "app_id": "",
    "app_secret": "",
    "author": "小五",
    "source_url": ""
  },
  "image_api": {
    "url": "",
    "bearer_token": ""
  }
}
```

## 支持的动作

### 1. 创建草稿
输入：
- `app_id`
- `app_secret`
- `cover`
- `title`
- `author`
- `digest`
- `content_file`
- `source_url`

动作：
- 获取 token
- 压缩封面图
- 上传封面图为永久 thumb 素材
- 新增草稿

输出：
- `thumb.media_id`
- `draft.media_id`

### 2. 提交自动发布
输入：
- `app_id`
- `app_secret`
- `draft_media_id`

动作：
- 调用 `freepublish/submit`

输出：
- 微信发布接口返回结果（通常包含 `publish_id`）

### 3. 查询发布状态
输入：
- `app_id`
- `app_secret`
- `publish_id`

动作：
- 调用 `freepublish/get`

输出：
- 当前发布状态

## 示例

### 先渲染 HTML

```bash
python3 skills/xiaowu-market-pipeline/scripts/render_wechat_article.py \
  --input /path/to/article.md \
  --output /path/to/article.html
```

### 创建草稿

```bash
python3 skills/xiaowu-market-pipeline/scripts/wechat_mp_publish.py \
  --config ./runtime/xiaowu-market-pipeline/config.local.json \
  --cover /path/to/cover.jpg \
  --title "小五的市场笔记｜每日盘后市场方向复盘（2026 年 3 月 10 日）" \
  --author "小五" \
  --digest "今天市场整体偏强，情绪明显修复，科技方向重新成为盘面主线。" \
  --content-file /path/to/article.html \
  --source-url "https://example.com/source"
```

### 提交自动发布

```bash
python3 skills/xiaowu-market-pipeline/scripts/wechat_mp_publish.py \
  --config ./runtime/xiaowu-market-pipeline/config.local.json \
  --draft-media-id DRAFT_MEDIA_ID \
  --publish
```

### 查询发布状态

```bash
python3 skills/xiaowu-market-pipeline/scripts/wechat_mp_publish.py \
  --config ./runtime/xiaowu-market-pipeline/config.local.json \
  --publish-id PUBLISH_ID \
  --status
```

## 注意事项

- `draft/add`、`freepublish/submit`、`freepublish/get` 都使用 UTF-8 JSON。
- 发送 JSON 时必须使用 `ensure_ascii=False`。
- 自动发布属于外部动作，执行前必须确认。
- 不要临时手写 HTML；优先先跑 `render_wechat_article.py`。
- 一级标题固定使用“一、二、三……”结构。
- 板块留白不要依赖 Markdown 空行，要通过 HTML 样式显式控制。
- 链接优先输出 `<a href="...">...</a>`，并保留完整 URL 作为备用显示。

## 权限问题说明

如果创建草稿成功，但自动发布返回：

- `errcode: 48001`
- `errmsg: api unauthorized`

通常表示当前公众号账号不具备 `freepublish/submit` 接口权限。
这属于账号能力边界，不代表脚本逻辑错误。


## 本地配置文件

推荐将微信公众号配置放在：

```text
runtime/xiaowu-market-pipeline/config.local.json
```

仓库中只保留 `config.template.json`，不要提交真实 `app_id`、`app_secret`、图片接口 token。

当前 `wechat_mp_publish.py` 支持通过命令行显式传入 `--app-id` 与 `--app-secret`；如需长期本地使用，建议由外部流程先读取本地配置，再传入脚本。

## 已知权限问题

如果 `freepublish/submit` 返回：

```json
{
  "errcode": 48001,
  "errmsg": "api unauthorized ..."
}
```

通常表示当前公众号账号没有自动发布权限；此时脚本可以创建草稿，但无法自动正式发布。这属于账号权限边界，不一定是脚本错误。
