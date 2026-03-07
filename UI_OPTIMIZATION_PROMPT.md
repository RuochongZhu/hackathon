# UI 优化执行提示词

## 给 AI 助手的指令

你现在需要优化 TwinReadmit 医疗仪表板的 UI，使其达到瑞士高端水疗中心般的简约奢华美学标准。

---

## 核心要求

### 设计目标
将当前的医疗数据仪表板改造成：
- **极致简约**: 每个元素都有明确目的，无冗余设计
- **专业高端**: 符合专业人士每月支付数千美元的产品质量
- **完美间距**: 组件之间既不拥挤也不浪费空间
- **图标优先**: 用专业图标系统完全替换 emoji
- **统一配色**: 严格遵循精简的配色方案

### 美学参考
- Apple Health App (简洁、专业)
- Epic MyChart (医疗级可靠性)
- Stripe Dashboard (数据可视化)
- Linear App (现代交互)

---

## 执行步骤

### Phase 1: 图标系统集成 (优先级: 高)

#### 1.1 添加 Lucide Icons
在 `dashboard/ui_app.py` 的 `app_ui` 中添加：

```python
# 在 ui.tags.head() 中添加
ui.tags.script(src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"),
ui.tags.script("""
    document.addEventListener('DOMContentLoaded', function() {
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    });
"""),
```

#### 1.2 创建图标辅助函数
在 `dashboard/ui_app.py` 顶部添加：

```python
def icon(name: str, size: int = 16, css_class: str = "") -> ui.Tag:
    """生成 Lucide 图标"""
    return ui.tags.i({
        "data-lucide": name,
        "class": f"icon {css_class}",
        "style": f"width:{size}px;height:{size}px;stroke-width:2;"
    })
```

#### 1.3 替换所有 emoji 和状态点

**Hero 区域** (第 258-263 行):
```python
# 原代码
ui.div({"class": f"hero-meta-dot {dot}"}), label

# 改为
icon("database" if connected else "database-x", 14, "hero-icon"), label
icon("users", 14, "hero-icon"), f"{n_patients} patients"
icon("alert-triangle", 14, "hero-icon"), f"{n_high} high-risk"
```

**侧边栏标签** (第 74, 83 行):
```python
# 原代码
ui.div({"class": "sidebar-section-label"}, "Data")

# 改为
ui.div(
    {"class": "sidebar-section-label"},
    icon("folder", 12, "section-icon"),
    ui.span("Data")
)

# AI Model 部分同理
ui.div(
    {"class": "sidebar-section-label"},
    icon("bot", 12, "section-icon"),
    ui.span("AI Model")
)
```

**Tab 标签** (第 97, 116, 134 行):
```python
# 原代码
ui.nav_panel("AI Risk Summary", ...)

# 改为
ui.nav_panel(
    ui.div(
        {"class": "tab-label"},
        icon("activity", 16, "tab-icon"),
        ui.span("AI Risk Summary")
    ),
    ...
)

# 其他 tabs:
# "AI Recommended Actions" → icon("clipboard-check")
# "AI Similar Cases" → icon("git-compare")
```

**风险徽章** (第 29-31 行):
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

---

### Phase 2: 间距系统优化

#### 2.1 更新 CSS 变量
在 `dashboard/styles.py` 的 `:root` 中添加：

```css
/* 间距系统 (8px 网格) */
--spacing-xs: 0.25rem;   /* 4px */
--spacing-sm: 0.5rem;    /* 8px */
--spacing-md: 1rem;      /* 16px */
--spacing-lg: 1.5rem;    /* 24px */
--spacing-xl: 2rem;      /* 32px */
--spacing-2xl: 3rem;     /* 48px */
```

#### 2.2 统一卡片间距
替换所有硬编码的 padding/margin：

```css
/* Metric cards */
.metric-card {
    padding: var(--spacing-lg) var(--spacing-md);
    margin-bottom: var(--spacing-md);
}

/* Panel cards */
.panel-card {
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-md);
}

/* AI workspace */
.ai-main-panel {
    padding: var(--spacing-xl) var(--spacing-lg);
}

.ai-chat-panel {
    padding: var(--spacing-lg);
}
```

---

### Phase 3: 配色精简

#### 3.1 更新颜色变量
在 `dashboard/styles.py` 中替换 `:root` 部分：

```css
:root {
    /* 主色调 */
    --primary: #0071e3;
    --bg: #f5f5f7;
    --surface: rgba(255, 255, 255, 0.72);
    --surface-solid: #ffffff;

    /* 边框和阴影 */
    --border: rgba(0, 0, 0, 0.08);
    --border-hover: rgba(0, 0, 0, 0.12);
    --shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
    --shadow-hover: 0 4px 24px rgba(0, 0, 0, 0.10);

    /* 文本层级 */
    --text-primary: #1d1d1f;
    --text-secondary: #6e6e73;
    --text-tertiary: #aeaeb2;

    /* 功能色 (仅用于风险指示) */
    --risk-high: #ff3b30;
    --risk-medium: #ff9500;
    --risk-low: #34c759;
    --risk-high-soft: rgba(255, 59, 48, 0.08);
    --risk-medium-soft: rgba(255, 149, 0, 0.08);
    --risk-low-soft: rgba(52, 199, 89, 0.08);

    /* 圆角 */
    --radius: 16px;
    --radius-sm: 10px;

    /* 毛玻璃效果 */
    --blur: blur(40px) saturate(180%);
}
```

#### 3.2 移除冗余颜色
删除以下变量：
- `--accent`, `--accent-soft` (用 `--primary` 替代)
- `--red`, `--orange`, `--green` (用 `--risk-*` 替代)
- `--red-soft`, `--orange-soft`, `--green-soft` (用 `--risk-*-soft` 替代)
- `--risk-neutral` (用 `--text-tertiary` 替代)

#### 3.3 全局替换颜色引用
在整个 CSS 中：
- `var(--accent)` → `var(--primary)`
- `var(--red)` → `var(--risk-high)`
- `var(--orange)` → `var(--risk-medium)`
- `var(--green)` → `var(--risk-low)`

---

### Phase 4: 排版优化

#### 4.1 更新字体栈
```css
body {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif;
    font-size: 16px;
    line-height: 1.6;
}
```

#### 4.2 添加字号系统
```css
:root {
    --text-xs: 0.64rem;   /* 10px */
    --text-sm: 0.8rem;    /* 13px */
    --text-base: 1rem;    /* 16px */
    --text-lg: 1.25rem;   /* 20px */
    --text-xl: 1.563rem;  /* 25px */
    --text-2xl: 1.953rem; /* 31px */
}
```

#### 4.3 应用字号系统
```css
.hero-title { font-size: var(--text-2xl); }
.section-title { font-size: var(--text-lg); }
.metric-value { font-size: var(--text-xl); }
.metric-label { font-size: var(--text-xs); }
body, .ai-narrative { font-size: var(--text-base); }
.hero-meta-item { font-size: var(--text-sm); }
```

---

### Phase 5: 组件细节打磨

#### 5.1 Metric Cards 悬停效果
```css
.metric-card {
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-hover);
    border-color: var(--border-hover);
}
```

#### 5.2 Risk Badges 脉冲动画
```css
@keyframes pulse-high {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.badge-high {
    animation: pulse-high 2s ease-in-out infinite;
}
```

#### 5.3 AI Narrative 首字母下沉
```css
.ai-narrative::first-letter {
    font-size: 1.5em;
    font-weight: 700;
    color: var(--primary);
    float: left;
    line-height: 1;
    margin-right: 0.1em;
}
```

#### 5.4 Chat 打字动画
```css
@keyframes typing {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 1; }
}

.chat-ai.typing::after {
    content: "●●●";
    animation: typing 1.5s infinite;
    margin-left: 0.5rem;
}
```

---

### Phase 6: 图标样式

在 `dashboard/styles.py` 中添加：

```css
/* 图标通用样式 */
.icon {
    display: inline-block;
    vertical-align: middle;
    stroke: currentColor;
    fill: none;
}

.hero-icon {
    color: var(--text-tertiary);
    margin-right: var(--spacing-xs);
}

.section-icon {
    color: var(--text-tertiary);
    margin-right: var(--spacing-xs);
}

.tab-icon {
    margin-right: var(--spacing-sm);
}

.badge-icon {
    margin-right: var(--spacing-xs);
}

.tab-label {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}

/* 侧边栏标签图标对齐 */
.sidebar-section-label {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
}
```

---

### Phase 7: 响应式优化

确保所有断点下间距保持一致：

```css
@media (max-width: 768px) {
    :root {
        --spacing-lg: 1rem;    /* 减小移动端内边距 */
        --spacing-xl: 1.5rem;
    }

    .metric-card {
        padding: var(--spacing-md);
    }

    .ai-main-panel {
        padding: var(--spacing-lg);
    }
}
```

---

## 验证清单

完成后检查以下项目：

### 视觉质量
- [ ] 页面中无任何 emoji
- [ ] 所有图标风格统一 (Lucide)
- [ ] 间距符合 8px 网格
- [ ] 颜色使用不超过 8 种
- [ ] 所有文本可读性良好

### 交互体验
- [ ] 卡片悬停有平滑动画
- [ ] 高风险徽章有脉冲效果
- [ ] 所有过渡时长 < 300ms
- [ ] 点击反馈清晰

### 响应式
- [ ] 移动端 (375px) 布局正常
- [ ] 平板 (768px) 布局正常
- [ ] 桌面 (1440px) 布局正常
- [ ] 图标在所有尺寸下清晰

### 代码质量
- [ ] 无硬编码的颜色值
- [ ] 无硬编码的间距值
- [ ] CSS 变量命名一致
- [ ] 代码注释清晰

---

## 注意事项

1. **保持功能完整**: 只改样式，不改逻辑
2. **渐进式修改**: 一次改一个组件，测试后再继续
3. **备份原文件**: 修改前备份 `ui_app.py` 和 `styles.py`
4. **测试真实数据**: 用实际数据测试边界情况
5. **保持一致性**: 所有图标、间距、颜色都要统一

---

## 预期效果

完成后，仪表板应该：
- 看起来像 Apple 设计的医疗产品
- 每个像素都经过精心打磨
- 专业到让用户愿意为此付费
- 简洁到让 Steve Jobs 满意

开始执行时，按照 Phase 1 → Phase 7 的顺序逐步进行。
