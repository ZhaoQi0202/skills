# 封面图片生成模块

## 目标

为《小五的市场笔记》生成稳定风格的公众号封面图。

## 固定风格

- 21:9 横版
- Mondo 海报风
- 概念化表达，不写实
- 冷静、克制、高级
- 深色背景 + 科技冷光
- 少元素、大留白、强主视觉
- 适配公众号标题叠加

## 固定骨架 Prompt

```text
A cinematic 21:9 Mondo-style editorial cover for a Chinese stock market daily review. Sophisticated, sharp, calm, high-end design. Dark navy background, strong negative space, retro screen-print texture, limited palette, minimalist symbolic composition, premium WeChat article cover aesthetic. No crowded charts, no realistic trading screen, no photorealism, no cartoon style, no excessive text.
```

## 每天替换的主题层

```text
Theme: [当天市场主线与判断].
Visual concept: [核心视觉隐喻].
Main elements: [抽象元素].
Color mood: [色彩方案].
Wide panoramic 21:9 composition, visually powerful, suitable as a WeChat article cover.
```

## 当前已验证的图片生成接口

接口示例：

```bash
curl "https://power-api.yingdao.com/oapi/power/v1/rest/flow/9c51e590-70ea-4f2e-a616-2e94c26e0113/execute" \
  -X POST \
  -d '{"input":{"input_text_0":"PROMPT"}}' \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 返回结果

成功时，接口会返回图片 URL。

## 使用要求

- 每天只替换主题层，不改风格骨架
- 主题必须从当天正文中提炼
- 不要生成普通科技壁纸式封面
- 不要堆股票代码、K线图、交易屏
