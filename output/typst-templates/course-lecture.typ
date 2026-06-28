// 作者：阿洋
// Profound Cognition v5.1.0 - Course Lecture Typst Template
// 幻灯片式讲义排版

#set document(
  paper: "presentation-16-9",
  margin: (left: 1cm, right: 1cm, top: 0.8cm, bottom: 0.8cm),
)

#set text(
  font: ("Glow Sans SC", "Source Han Sans SC"),
  size: 14pt,
  lang: "zh",
)

#set heading(numbering: "1.")

// 幻灯片页
#let slide(title, content) = {
  pagebreak()
  text(18pt, weight: "bold")[#title]
  v(1em)
  content
}

// 概念图嵌入区域
#let concept-figure(description) = {
  align(center, {
    rect(
      width: 80%,
      height: 5cm,
      stroke: 0.5pt + gray,
      fill: luma(240),
    )[
      #text(size: 10pt, fill: gray)[概念图：]
      #text(size: 9pt, fill: gray)[#description]
    ]
  })
}

// 练习/讨论题排版块
#let exercise(question) = {
  block(
    inset: 8pt,
    fill: luma(245),
    stroke: 0.5pt + blue,
    radius: 4pt,
  )[
    *练习/讨论：* #question
  ]
}