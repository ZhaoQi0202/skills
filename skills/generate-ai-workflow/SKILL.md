---
name: generate-ai-workflow
description: 为 AI Power 平台生成可直接导入的工作流 JSON。适用于根据自然语言需求设计、拼装、校验并输出 AI Power 工作流；当用户需要把业务需求转换成 AI Power 工作流、选择模板模式、补齐节点配置、生成输入输出 Schema、或生成最终 JSON 文件时使用。
---

# Generate AI Workflow

将用户的自然语言需求，转换为可导入 AI Power 平台的工作流 JSON。

## 目标

完成以下工作：
- 判断用户需求属于哪一类工作流模式
- 读取对应模板作为骨架
- 根据需求补齐节点、变量、Prompt、连线、坐标与 Schema
- 校验结构完整性与变量引用正确性
- 输出可导入的最终 JSON 文件

## 仓库资源

按需读取以下文件：
- `references/node_catalog.json`：节点类型注册表与字段模板
- `references/schema_reference.md`：AI Power 工作流 JSON 结构说明
- `templates/simple_linear.json`：简单线性模式
- `templates/image_analysis.json`：图片分析模式
- `templates/multi_output.json`：多输出模式
- `templates/knowledge_base.json`：知识库增强模式
- `templates/database_query.json`：数据库查询模式
- `templates/complex_review.json`：复杂审核模式

如遇到节点字段不确定、Edge handle 不确定、Schema 映射不确定，先读 `references/`，再修改模板。

## 执行流程

### 1. 需求分析

先把用户需求整理成结构化摘要，至少包括：
- 任务名称
- 输入类型：TEXT / IMAGE / TEXT+IMAGE / 多输入
- 输出类型：TEXT / IMAGE / TABLE / 多输出
- 核心能力：LLM / OCR / Vision / 文生图 / 图生图 / 知识库 / 数据库 / 条件判断
- 是否需要多步骤处理中间结果
- 是否需要知识库
- 是否需要数据库
- 是否需要审核判断
- 额外限制与特殊要求

如果需求本身不完整，先补齐关键缺口，再开始生成 JSON。

### 2. 选择模式模板

按以下规则选择模板：
- 需要数据库查询：`templates/database_query.json`
- 需要审核、材料识别、多条件判断：`templates/complex_review.json`
- 需要知识库检索：`templates/knowledge_base.json`
- 输入包含图片且重点是分析/提取：`templates/image_analysis.json`
- 需要把一个结果拆成多个结构化输出：`templates/multi_output.json`
- 其他常规文本任务：`templates/simple_linear.json`

如果需求跨多种模式：
1. 先选主模式做骨架
2. 再从其他模式补充节点
3. 节点字段以 `references/node_catalog.json` 为准

### 3. 填充模板

#### 3.1 复制模板骨架
读取选中的模板 JSON，保留其整体结构，再做定制。

#### 3.2 生成唯一标识
为以下对象生成新的 ULID：
- 每个节点 `uuid`
- 每条 Edge `id`
- 对应输入输出 Schema 的 `uuid`

要求：
- 全部唯一
- 同步更新所有引用位置
- 不要遗漏 `source`、`target`、`sourceHandle`、`targetHandle`

#### 3.3 填写节点参数
重点处理以下节点：

**输入节点**
- 修改 `inputs[].label`
- 让 `outputs[].name` 更贴近业务语义

**LLM 节点**
- 选择 `channel` 与 `model`
- 按任务设置 `temperature`
- 编写清晰的 `system` Prompt
- 在 `user` 中用 `{{变量名}}` 引用上游结果

**OCR / Vision / Embedding / DB 节点**
- 确保引用变量与输入类型匹配
- 需要用户自行配置的 ID 保留为空并在说明中标出

**输出节点**
- 设置有意义的输出标签
- `param_variable` 必须正确指向上游输出

### 4. 构建数据流

根据节点依赖关系生成或调整 Edge：
- `source` 指向上游节点
- `target` 指向下游节点
- 多输入、多输出场景下优先显式填写 `sourceHandle` / `targetHandle`
- Edge 样式以 `references/node_catalog.json` 的 `edge_template` 为准

### 5. 设置布局

默认从左到右布局：
- 输入节点从 `x=100` 左右开始
- 每一层向右增加约 `400~500px`
- 并行节点上下错开，垂直间距约 `250px`

布局目标：
- 连线尽量直观
- 输入在左，输出在右
- 并行节点不要重叠

### 6. 同步 InputsSchemas / OutputsSchemas

确保：
- 每个 `input_text` / `input_image` 节点都对应一项 `inputsSchemas`
- 每个 `output_text` / `output_image` / `output_table` 节点都对应一项 `outputsSchemas`
- Schema 的 `uuid` 与对应节点一致
- Schema 中的 `outputs` 与节点 `outputs` 完全一致

### 7. 校验

生成后至少逐项检查：
- 顶层包含 `edges`、`inputsSchemas`、`nodes`、`outputsSchemas`
- JSON 可正常解析
- 节点字段完整
- UUID 全局唯一
- Edge 的 `source` / `target` 都能命中现有节点
- 变量 `{{...}}` 都能在上游输出中找到来源
- `inputsSchemas` / `outputsSchemas` 数量与节点数量一致
- 不存在明显循环引用

## 输出要求

默认输出到：

```text
生成的工作流/{工作流名称}.json
```

同时附带一段简要说明，至少包括：
- 工作流名称
- 使用的模式
- 节点清单及用途
- 数据流向说明
- 仍需用户补充配置的项目（如 knowledgeId、embeddingId、database_id 等）

## Prompt 编写要求

为 LLM 节点编写 Prompt 时，遵循以下原则：
- 明确角色
- 明确任务目标
- 明确输出格式
- 明确边界条件与禁区
- 必要时给出 1~2 个格式示例

不要写空泛 Prompt。Prompt 必须直接服务于该节点的输入输出约束。

## 模型选择建议

默认参考：
- 通用文本生成：`azure / gpt-5.2`
- 精确分析或代码：`azure / gpt-4o`
- 多模态理解：`gemini / gemini-3-flash`
- 高性价比文本：`deepseek / deepseek-chat`
- 文生图：`azure / gpt-image-1.5`
- 图生图：`google / gemini-3-pro-image-preview`

如用户已有平台限制，以用户实际可用模型为准。

## 注意事项

- 这是一个“工作流生成”Skill，不负责替用户保管真实 API Key。
- 不要在模板、文档或输出文件中写入真实密钥。
- 如果平台字段与当前参考不一致，以用户实际平台版本为准，并在输出说明中指出差异。
- 如果需求明显超出当前模板覆盖范围，先说明需要混合模式或新增节点，不要假装单模板足够。
