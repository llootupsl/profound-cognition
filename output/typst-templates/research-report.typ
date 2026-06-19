// 作者：阿洋
// 页模板宏自包含于本文件
// Profound Cognition v5.1.0 - Research Report Typst Template
// 全息框架 3 部分 × 14 维度 × 40 方面 排版模板

#set document(
  title: none,
  author: none,
  paper: "a4",
  margin: (left: 2.5cm, right: 2.5cm, top: 2.5cm, bottom: 2.5cm),
)

#set text(
  font: ("Glow Sans SC", "Source Han Sans SC", "Noto Sans CJK SC", "SimSun"),
  size: 11pt,
  lang: "zh",
)

#set heading(numbering: "1.1")
#set par(leading: 0.65em, first-line-indent: 2em)

// 封面页
#let cover-page(title, subtitle, date, author, version) = {
  v(4cm)
  align(center, {
    text(24pt, weight: "bold")[#title]
    v(1em)
    text(14pt, style: "italic")[#subtitle]
    v(3cm)
    grid(
      columns: (auto, auto),
      rows: 3,
      align: (left, left),
      [日期：], [#date],
      [作者：], [#author],
      [版本：], [#version],
    )
  })
  pagebreak()
}

// 目录页
#let toc-page() = {
  text(18pt, weight: "bold")[目录]
  v(1em)
  outline(
    indent: 2em,
    depth: 3,
  )
  pagebreak()
}

// 维度页模板
#let dimension-page(number, title, aspects) = {
  pagebreak()
  text(16pt, weight: "bold")[维度 #number：#title]
  v(1em)
  for aspect in aspects {
    text(13pt, weight: "bold")[#aspect.name]
    v(0.5em)
    [#aspect.content]
    v(1em)
  }
}

// 附录页
#let appendix-page(title, content) = {
  pagebreak()
  text(16pt, weight: "bold")[附录：#title]
  v(1em)
  content
}

// 全息框架 3 部分排版宏
#let part-i-content(content) = {
  pagebreak()
  text(20pt, weight: "bold")[第一部分：问题认知与定义]
  v(1em)
  content
}

#let part-ii-content(content) = {
  pagebreak()
  text(20pt, weight: "bold")[第二部分：全维全域分析]
  v(1em)
  content
}

#let part-iii-content(content) = {
  pagebreak()
  text(20pt, weight: "bold")[第三部分：极限决策推理]
  v(1em)
  content
}

// 元维度页（深度层维度 9-14）
#let meta-dim-page(num, title, body) = {
  pagebreak()
  align(center, {
    text(18pt, weight: "bold")[深度层 · 维度 #num]
    v(0.5em)
    text(14pt, style: "italic")[#title]
  })
  v(1.5em)
  line(length: 100%, stroke: 0.5pt + gray)
  v(1em)
  body
}

// 哲学三核（本体论 · 认识论 · 价值论）
#let philosophy-core(onto, epis, axio) = {
  pagebreak()
  align(center, {
    text(20pt, weight: "bold")[哲学三核]
    v(0.5em)
    text(12pt, style: "italic")[本体论 · 认识论 · 价值论]
  })
  v(2em)

  // 本体论 Ontology
  block(
    inset: 10pt,
    fill: rgb("#f5f0eb"),
    radius: 4pt,
    stroke: 0.5pt + rgb("#8b7355"),
    [
      text(14pt, weight: "bold")[一、本体论（Ontology）]
      v(0.8em)
      #onto
    ]
  )
  v(1em)

  // 认识论 Epistemology
  block(
    inset: 10pt,
    fill: rgb("#ebf0f5"),
    radius: 4pt,
    stroke: 0.5pt + rgb("#55708b"),
    [
      text(14pt, weight: "bold")[二、认识论（Epistemology）]
      v(0.8em)
      #epis
    ]
  )
  v(1em)

  // 价值论 Axiology
  block(
    inset: 10pt,
    fill: rgb("#f0ebf5"),
    radius: 4pt,
    stroke: 0.5pt + rgb("#70558b"),
    [
      text(14pt, weight: "bold")[三、价值论（Axiology）]
      v(0.8em)
      #axio
    ]
  )
}

// 科学层（TM01-TM07 主题模型块）
#let science-layer(tm_blocks) = {
  pagebreak()
  align(center, {
    text(20pt, weight: "bold")[科学层分析]
    v(0.5em)
    text(12pt, style: "italic")[TM01 ← TM02 ← TM03 ← TM04 ← TM05 ← TM06 ← TM07]
  })
  v(2em)

  for (idx, block) in tm_blocks.enumerate() {
    let tm_num = calc.min(idx + 1, 7)
    block(
      inset: 10pt,
      fill: rgb("#f8f9fa"),
      radius: 4pt,
      stroke: 0.5pt + rgb("#6c757d"),
      [
        text(13pt, weight: "bold")[TM0#tm_num · #block.at("title", default: "主题模型")]
        v(0.6em)
        #block.content
      ]
    )
    if idx < tm_blocks.len() - 1 {
      align(center, text(16pt, fill: rgb("#adb5bd"))[↓])
      v(0.3em)
    }
  }
}

// 决策演化路径（多路线决策）
#let decision-routes(routes) = {
  pagebreak()
  align(center, {
    text(20pt, weight: "bold")[决策演化路径]
    v(0.5em)
    text(12pt, style: "italic")[Multi-Decision Evolution Routes]
  })
  v(2em)

  for (idx, route) in routes.enumerate() {
    let route_num = idx + 1
    block(
      inset: 12pt,
      fill: rgb("#fff9f0"),
      radius: 4pt,
      stroke: 0.5pt + rgb("#d4a373"),
      [
        text(13pt, weight: "bold")[路径 #route_num：#route.name]
        v(0.5em)
        text(11pt, fill: rgb("#6c757d"))[#route.description]
        v(0.6em)
        if route.outcome != none {
          text(11pt, weight: "bold", fill: rgb("#2d6a4f"))[预期结果：]#text(11pt)[#route.outcome]
        }
        v(0.3em)
        if route.risk != none {
          text(11pt, weight: "bold", fill: rgb("#c1121f"))[风险提示：]#text(11pt)[#route.risk]
        }
      ]
    )
    if idx < routes.len() - 1 {
      v(0.8em)
      align(center, text(16pt, fill: rgb("#d4a373"))[⇢])
      v(0.3em)
    }
  }
}

// 代码块样式
#show raw.where(block: true): set text(
  font: ("Fragment Mono", "JetBrains Mono", "Cascadia Code", "Consolas"),
  size: 9pt,
)

// 表格样式
#show table: set text(size: 10pt)