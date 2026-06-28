// 作者：阿洋
// Profound Cognition v5.1.0 - WeChat Article Export Typst Template
// 公众号风格 PDF 导出排版

#set document(
  paper: "a4",
  margin: (left: 2cm, right: 2cm, top: 2cm, bottom: 2cm),
)

#set text(
  font: ("Glow Sans SC", "Source Han Sans SC"),
  size: 11pt,
  lang: "zh",
)

#set par(leading: 0.8em, first-line-indent: 0em)

// 与HTML内联样式一致的视觉风格
#show heading.where(level: 1): it => {
  text(16pt, weight: "bold")[#it.body]
  v(0.5em)
}

#show heading.where(level: 2): it => {
  text(14pt, weight: "bold")[#it.body]
  v(0.3em)
}

// 引用块
#let quote-block(content) = {
  block(
    inset: 12pt,
    fill: luma(248),
    stroke: (left: 3pt + green),
  )[#content]
}