# skills

一个用于统一管理自研 Agent Skills 的仓库，目录组织参考 Anthropic 的 skills 管理方式。

## 仓库目标

这个仓库用于集中管理 Boss 自己开发的各类 skill，统一目录结构、文档规范和资源组织方式，便于：

- 持续扩展多个 skill
- 统一维护 `SKILL.md`、脚本与参考资料
- 后续迁移到其他 Agent / Runtime 时保持结构稳定
- 避免把不同 skill 的脚本和参考文件混放在仓库顶层

## 顶层结构

仓库顶层只保留少量公共文件：

```text
.
├── README.md
├── .gitignore
└── skills/
```

说明：

- 顶层 **不再放** `SKILL.md`、`references/`、`scripts/`、`config.template.json` 这类单个 skill 私有文件
- 每个 skill 的全部内容都应收敛到 `skills/{skill-name}/` 目录下

## Skill 目录规范

每个 skill 独立放在：

```text
skills/{skill-name}/
```

推荐结构：

```text
skills/
  yingdao-boss-client-fetch/
    SKILL.md
    README.md
    config.template.json
    references/
    scripts/
```

其中：

- `SKILL.md`：Agent 读取的核心 skill 说明
- `README.md`：该 skill 的人类可读文档
- `config.template.json`：不含敏感信息的配置模板
- `references/`：接口说明、资料、设计笔记
- `scripts/`：该 skill 的执行脚本与依赖文件

## 当前收录

- `skills/yingdao-boss-client-fetch`
  - 从影刀 Boss 平台抓取指定业务组客户数据
  - 输出共享最新数据文件
  - 供后续分析类 skill 直接消费

- `skills/xiaowu-market-pipeline`
  - 生成《小五的市场笔记》市场复盘文章与公众号封面
  - 渲染公众号 HTML
  - 创建草稿、提交发布、查询发布状态

## 约定

- 每个 skill 独立维护在 `skills/{skill-name}/`
- 不提交真实凭据
- 运行期配置与运行产物放在仓库外部或独立 runtime 目录，不放进 skill 包本体
- 如果新增 skill，优先复制一个已有 skill 的目录骨架再修改，保持结构统一

## 后续扩展建议

后面如果新增多个 skill，可以继续在 `skills/` 下并列扩展，例如：

```text
skills/
  yingdao-boss-client-fetch/
  yingdao-boss-client-analysis/
  wechat-draft-publisher/
```

这样仓库会更像一个稳定的自研 skills registry，而不是单个 skill 的临时仓库。

## 维护建议

- 新增 skill 前，优先阅读 `CONTRIBUTING.md`
- 尽量保持所有 skill 目录骨架一致
- 不要把某个 skill 的脚本或 references 再放回仓库顶层
