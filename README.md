# skills

一个用于统一管理自研 Agent Skills 的仓库，目录组织参考 Anthropic 的 skills 管理方式。

## 目录结构

```text
skills/
  yingdao-boss-client-fetch/
    SKILL.md
    README.md
    config.template.json
    references/
    scripts/
```

## 当前收录

- `skills/yingdao-boss-client-fetch`：从影刀 Boss 平台抓取指定业务组客户数据，输出共享最新数据文件，供下游分析类 skill 使用。

## 约定

- 每个 skill 独立放在 `skills/{skill-name}/`
- 每个 skill 自带：
  - `SKILL.md`
  - `README.md`
  - `references/`
  - `scripts/`
  - 其他该 skill 私有资源文件
- 不提交真实凭据
- 运行期配置与运行产物放在仓库外部或独立 runtime 目录，不放进 skill 包本体
