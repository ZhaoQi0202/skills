# generate-ai-workflow

将自然语言需求转换为 **AI Power 平台可导入的工作流 JSON**。

## 这个 Skill 能做什么

适用于以下场景：
- 把一个业务需求转成 AI Power 工作流
- 根据任务类型自动选择工作流模板
- 生成输入节点、LLM 节点、OCR / Vision / 知识库 / 数据库节点
- 生成输出节点与输入输出 Schema
- 生成可交付的最终 JSON 文件

## 当前内置模式

- `simple_linear`：简单线性文本处理
- `image_analysis`：图片识别 / OCR / 图片内容分析
- `multi_output`：一个输入拆成多个结构化输出
- `knowledge_base`：知识库检索增强
- `database_query`：自然语言转 SQL + 数据库查询
- `complex_review`：复杂审核 / 材料识别 / 条件判断

## 目录结构

```text
skills/generate-ai-workflow/
  SKILL.md
  README.md
  references/
    node_catalog.json
    schema_reference.md
  templates/
    simple_linear.json
    image_analysis.json
    multi_output.json
    knowledge_base.json
    database_query.json
    complex_review.json
```

## 使用方式

当用户给出 AI Power 工作流需求时：
1. 先分析需求类型
2. 选择最合适的模板
3. 按参考资料补齐节点字段、Prompt、Edge、Schema
4. 校验 JSON 完整性
5. 输出到 `生成的工作流/{工作流名称}.json`

## 关键参考文件

### `references/node_catalog.json`
节点注册表，定义了：
- 节点类型
- 输入输出字段
- 默认版本
- 说明与约束
- Edge 样式模板

### `references/schema_reference.md`
定义 AI Power 工作流 JSON 的：
- 顶层结构
- Node / Edge 结构
- InputsSchemas / OutputsSchemas 结构
- 变量引用语法
- ULID / UUID 规则

## 注意事项

- 本 Skill 不包含真实密钥或真实业务配置。
- 如果目标平台字段发生变更，需要按实际平台版本修正模板。
- 若需求跨多个模式，应使用“主模板 + 补充节点”的方式组合生成。
