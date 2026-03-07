# UI 优化快速参考卡片

## 🎨 设计系统速查

### 间距系统（8px 网格）
```css
--spacing-xs: 4px    /* 微小间距 - 图标间距 */
--spacing-sm: 8px    /* 小间距 - 列表项 */
--spacing-md: 16px   /* 标准间距 - 卡片间距 */
--spacing-lg: 24px   /* 大间距 - 卡片内边距 */
--spacing-xl: 32px   /* 超大间距 - 区域内边距 */
--spacing-2xl: 48px  /* 巨大间距 - 区域外边距 */
```

### 字号系统（1.25 比例）
```css
--text-xs: 10px      /* 标签、徽章 */
--text-sm: 13px      /* 辅助文本、说明 */
--text-base: 16px    /* 正文、叙述 */
--text-lg: 20px      /* 小标题、Section 标题 */
--text-xl: 25px      /* 标题、数值 */
--text-2xl: 31px     /* 大标题、Hero 标题 */
```

### 配色方案
```css
/* 主色调 */
--primary: #0071e3           /* 蓝色 - 按钮、链接、强调 */

/* 背景色 */
--bg: #f5f5f7                /* 浅灰 - 页面背景 */
--surface: rgba(255,255,255,0.72)  /* 毛玻璃 - 卡片背景 */
--surface-solid: #ffffff     /* 纯白 - 实心背景 */

/* 文本色 */
--text-primary: #1d1d1f      /* 主要文本 */
--text-secondary: #6e6e73    /* 次要文本 */
--text-tertiary: #aeaeb2     /* 辅助文本 */

/* 风险色 */
--risk-high: #ff3b30         /* 红色 - 高风险 */
--risk-medium: #ff9500       /* 橙色 - 中风险 */
--risk-low: #34c759          /* 绿色 - 低风险 */
--risk-high-soft: rgba(255,59,48,0.08)
--risk-medium-soft: rgba(255,149,0,0.08)
--risk-low-soft: rgba(52,199,89,0.08)

/* 边框和阴影 */
--border: rgba(0,0,0,0.08)
--border-hover: rgba(0,0,0,0.12)
--shadow: 0 2px 16px rgba(0,0,0,0.06)
--shadow-hover: 0 4px 24px rgba(0,0,0,0.10)

/* 圆角 */
--radius: 16px               /* 大圆角 - 卡片 */
--radius-sm: 10px            /* 小圆角 - 按钮、输入框 */
```

---

## 🎯 图标映射

### Hero 区域（14px）
```python
icon("database", 14, "hero-icon-green")     # 数据库连接成功
icon("database-x", 14, "hero-icon-red")     # 数据库连接失败
icon("users", 14, "hero-icon")              # 患者数量
icon("alert-triangle", 14, "hero-icon")     # 高风险数
```

### 侧边栏标签（12px）
```python
icon("folder", 12, "section-icon")          # Data 标签
icon("bot", 12, "section-icon")             # AI Model 标签
```

### Tab 标签（16px）
```python
icon("activity", 16, "tab-icon")            # AI Risk Summary
icon("clipboard-check", 16, "tab-icon")     # AI Recommended Actions
icon("git-compare", 16, "tab-icon")         # AI Similar Cases
```

### 风险徽章（12px）
```python
icon("alert-triangle", 12, "badge-icon")    # High Risk
icon("alert-circle", 12, "badge-icon")      # Medium Risk
icon("check-circle", 12, "badge-icon")      # Low Risk
```

---

## 🎬 动画效果

### 脉冲动画（高风险徽章）
```css
@keyframes pulse-high {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
animation: pulse-high 2s ease-in-out infinite;
```

### 悬停上浮（Metric Cards）
```css
transform: translateY(-2px);
transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
```

### 悬停右移（Action/Case Cards）
```css
transform: translateX(2px);
transition: all 0.2s ease;
```

### 全局过渡
```css
transition-property: background-color, border-color, color, opacity, transform;
transition-duration: 0.2s;
transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
```

---

## 📱 响应式断点

### 桌面端（≥ 1100px）
- Metric Cards: 4 列
- 完整间距
- 所有功能可见

### 平板端（768px - 1100px）
- Metric Cards: 2 列
- 适中间距
- 布局调整

### 移动端（< 768px）
- Metric Cards: 1 列
- 紧凑间距（--spacing-lg: 1rem, --spacing-xl: 1.5rem）
- 字号缩小（Hero 标题: --text-xl）

---

## 🛠️ 常用代码片段

### 创建图标
```python
def icon(name: str, size: int = 16, css_class: str = "") -> ui.Tag:
    return ui.tags.i({
        "data-lucide": name,
        "class": f"icon {css_class}",
        "style": f"width:{size}px;height:{size}px;stroke-width:2;"
    })
```

### 创建风险徽章
```python
def risk_badge(level: str):
    n = (level or "medium").lower()
    icon_map = {
        "high": "alert-triangle",
        "medium": "alert-circle",
        "low": "check-circle"
    }
    return ui.div(
        {"class": f"badge badge-{n}"},
        icon(icon_map.get(n, "alert-circle"), 12, "badge-icon"),
        ui.span(n.upper())
    )
```

### 创建卡片
```python
ui.div(
    {"class": "panel-card"},
    ui.div({"class": "section-title"}, "标题"),
    ui.div({"class": "content"}, "内容")
)
```

### 创建 Metric Card
```python
ui.div(
    {"class": "metric-card"},
    ui.div({"class": "metric-label"}, "标签"),
    ui.div({"class": "metric-value"}, "数值"),
    ui.div({"class": "metric-footnote"}, "注释")
)
```

---

## ✅ 验证清单

### 视觉质量
- [ ] 无 emoji 残留
- [ ] 图标风格统一
- [ ] 间距符合 8px 网格
- [ ] 颜色不超过 8 种
- [ ] 文本可读性良好

### 交互体验
- [ ] 悬停效果流畅
- [ ] 高风险徽章脉冲
- [ ] 过渡时长 < 300ms
- [ ] 点击反馈清晰

### 响应式
- [ ] 移动端（375px）正常
- [ ] 平板端（768px）正常
- [ ] 桌面端（1440px）正常
- [ ] 图标清晰

### 代码质量
- [ ] 无硬编码颜色
- [ ] 无硬编码间距
- [ ] 变量命名一致
- [ ] 注释清晰

---

## 🚀 快速启动

### 启动应用
```bash
./start_dashboard.sh
```

### 访问地址
```
http://localhost:8001
```

### 测试步骤
1. 检查 Hero 区域图标
2. 检查侧边栏图标
3. 检查 Tab 图标
4. 检查风险徽章
5. 测试悬停效果
6. 测试响应式布局
7. 检查动画效果

---

## 📚 文档索引

- `UI_OPTIMIZATION_PLAN.md` - 详细计划
- `UI_OPTIMIZATION_PROMPT.md` - 执行提示词
- `UI_OPTIMIZATION_COMPLETED.md` - 完成报告
- `UI_OPTIMIZATION_SUMMARY.md` - 最终总结
- `UI_VISUAL_COMPARISON.md` - 视觉对比
- `UI_TESTING_GUIDE.md` - 测试指南
- `UI_QUICK_REFERENCE.md` - 本文档

---

## 🎯 设计原则

### 简约奢华
- 每个元素都有明确目的
- 无冗余设计
- 精致的细节

### 完美间距
- 8px 网格系统
- 组件不拥挤也不浪费空间
- 视觉呼吸感

### 统一配色
- 8 种核心颜色
- 语义化命名
- 一致的透明度

### 流畅交互
- 平滑的过渡
- 丰富的反馈
- 60fps 动画

---

## 💡 最佳实践

### 使用变量
```css
/* ❌ 不要 */
padding: 1rem 1.5rem;
font-size: 0.85rem;
color: #6e6e73;

/* ✅ 要 */
padding: var(--spacing-lg) var(--spacing-xl);
font-size: var(--text-sm);
color: var(--text-secondary);
```

### 使用图标
```python
# ❌ 不要
ui.span("🟢 Connected")

# ✅ 要
ui.div(
    icon("database", 14, "hero-icon-green"),
    ui.span("Connected")
)
```

### 添加过渡
```css
/* ❌ 不要 */
.card:hover {
  background: #fff;
}

/* ✅ 要 */
.card {
  transition: all 0.2s ease;
}
.card:hover {
  background: #fff;
  transform: translateY(-2px);
}
```

---

## 🔧 故障排除

### 图标不显示
1. 检查 Lucide CDN 是否加载
2. 检查 `data-lucide` 属性
3. 检查 `lucide.createIcons()` 是否调用

### 间距不对齐
1. 检查是否使用间距变量
2. 检查是否符合 8px 网格
3. 使用浏览器开发工具测量

### 颜色不一致
1. 检查是否使用颜色变量
2. 避免硬编码颜色值
3. 统一透明度为 0.08

### 动画卡顿
1. 检查是否使用 `transform` 而非 `left/top`
2. 检查过渡时长是否合理
3. 使用 `cubic-bezier` 优化曲线

---

## 📞 联系方式

如有问题或建议，请联系开发团队。

---

**快速参考，随时查阅！** 📖

---

*最后更新: 2026-03-07*
