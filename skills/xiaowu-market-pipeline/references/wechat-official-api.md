# 微信公众号发布模块

本模块直接复用并概括微信官方原生发稿链路。

## 发布顺序

1. 获取 `access_token`
2. 上传封面图为永久 thumb 素材
3. 新增草稿
4. 用户确认后提交自动发布
5. 查询发布状态

## 关键说明

- `draft/add` 必须使用 UTF-8 JSON，且 `ensure_ascii=False`
- 不要把中文标题转成 unicode 转义
- 自动发布接口提交的是“草稿 media_id”，不是封面图 media_id
- 发布属于外部动作，执行前必须确认

## 现成脚本

直接复用：

- `scripts/render_wechat_article.py`
- `scripts/wechat_mp_publish.py`

其中：
- 前者负责解决标题编号、段间留白、可点击链接等排版稳定性问题
- 后者负责创建草稿、自动发布、状态查询
