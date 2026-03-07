# TwinReadmit UI 优化计划

## 项目概述
将 TwinReadmit 仪表板优化为高端、专业的医疗数据可视化平台，符合瑞士水疗中心般的简约奢华美学。

---

## 设计原则

### 核心美学
- **简约奢华 (Minimalist Premium)**: 类似瑞士高端水疗中心的设计语言
- **专业医疗级**: 适合专业人士每月支付数千美元的产品质量
- **Steve Jobs 标准**: 极致简洁、完美间距、精心打磨的细节

### 设计规范
1. **图标优先**: 用专业图标系统替换所有 emoji
2. **完美间距**: 组件之间既不拥挤也不浪费空间
3. **统一色板**: 选择并严格遵循一套内聚的配色方案
4. **响应式设计**: 桌面和移动端都保持优雅体验

---

## 阶段一：顶部数据可视化重构 (待其他团队完成)

### 1.1 饼图组件 - Cohort 风险分布
**位置**: 替换当前的四个指标卡片左侧区域

**功能需求**:
- 显示当前 cohort 的总患者数
- 高风险患者占比（饼图形式）
- 三种风险等级的分布：High / Medium / Low

**设计规格**:
```
组件尺寸: 320px × 280px
饼图直径: 200px
中心空白: 120px (用于显示核心指标)
颜色方案:
  - High Risk: #ff3b30 (红色)
  - Medium Risk: #ff9500 (橙色)
  - Low Risk: #34c759 (绿色)
  - 背景: rgba(255, 255, 255, 0.72)
```

**数据展示**:
- 中心大数字: 高风险占比百分比
- 下方标签: "High-risk patients"
- 底部统计: "Total: XXX patients"

**交互**:
- Hover 显示具体数值
- 点击扇区高亮对应风险等级的患者

---

### 1.2 箱线图组件 - 三类 Cohort 风险对比
**位置**: 替换当前的四个指标卡片右侧区域

**功能需求**:
- 横向显示三个 cohort 的风险分布箱线图
- 标记当前选中患者在其 cohort 中的风险位置
- 显示中位数、四分位数、异常值

**设计规格**:
```
组件尺寸: 520px × 280px
箱线图方向: 横向 (Horizontal)
箱体宽度: 40px
颜色方案:
  - 箱体填充: rgba(0, 113, 227, 0.12)
  - 箱体边框: #0071e3
  - 中位线: #1d1d1f (粗 2px)
  - 当前患者标记: #ff3b30 (红色圆点，直径 10px)
  - 异常值: rgba(0, 0, 0, 0.3) (小圆点)
```

**数据展示**:
- Y 轴: 三个 cohort 名称
- X 轴: 风险概率 (0% - 100%)
- 当前患者位置: 红色标记点 + 虚线指示
- Tooltip: 显示具体数值和百分位数

**交互**:
- Hover 显示详细统计信息
- 点击箱线图切换到对应 cohort

---

## 阶段二：全局 UI 优化

### 2.1 图标系统集成

**图标库选择**: Lucide Icons (或 Heroicons)
- 轻量级、现代、专业
- 与医疗场景契合
- 支持多种尺寸和样式

**需要替换的图标位置**:
1. **Hero 区域状态点** → 改为图标
   - Supabase live: 数据库图标 (database-check)
   - Patients count: 用户组图标 (users)
   - High-risk: 警告图标 (alert-triangle)

2. **侧边栏标签** → 添加图标
   - Data 区域: 文件夹图标 (folder)
   - Cohort 选择: 图层图标 (layers)
   - Patient 选择: 用户图标 (user)
   - AI Model: 机器人图标 (bot)

3. **Tab 标签** → 添加图标
   - AI Risk Summary: 分析图标 (activity)
   - AI Recommended Actions: 清单图标 (clipboard-check)
   - AI Similar Cases: 对比图标 (git-compare)

4. **风险徽章** → 添加图标前缀
   - High: 警告三角 (alert-triangle)
   - Medium: 信息圆圈 (alert-circle)
   - Low: 对勾圆圈 (check-circle)

**实现方式**:
```python
# 在 ui_app.py 中添加图标辅助函数
def icon(name: str, size: int = 16) -> ui.Tag:
    return ui.tags.i(
        {"class": f"lucide lucide-{name}", "style": f"width:{size}px;height:{size}px;"}
    )

# 在 HTML head 中引入 Lucide CDN
ui.tags.script(src="https://unpkg.com/lucide@latest")
ui.tags.script("lucide.createIcons();")
```

---

### 2.2 间距系统优化

**当前问题**:
- 某些卡片间距不一致
- 内边距在不同组件中差异较大
- 响应式断点下间距比例失调

**新的间距系统** (基于 8px 网格):
```css
--spacing-xs: 0.25rem;   /* 4px */
--spacing-sm: 0.5rem;    /* 8px */
--spacing-md: 1rem;      /* 16px */
--spacing-lg: 1.5rem;    /* 24px */
--spacing-xl: 2rem;      /* 32px */
--spacing-2xl: 3rem;     /* 48px */
```

**应用规则**:
- 卡片外边距: `--spacing-md` (16px)
- 卡片内边距: `--spacing-lg` (24px)
- 组件间距: `--spacing-md` (16px)
- 文本行距: 1.6 (医疗文档标准)
- 标题与内容间距: `--spacing-sm` (8px)

---

### 2.3 配色方案精简

**当前配色** (保留核心色):
```css
/* 主色调 - 保持不变 */
--primary: #0071e3;      /* 蓝色 - 专业、信任 */
--surface: rgba(255, 255, 255, 0.72);  /* 毛玻璃效果 */
--bg: #f5f5f7;           /* 浅灰背景 */

/* 功能色 - 仅用于风险指示 */
--risk-high: #ff3b30;    /* 红色 - 高风险 */
--risk-medium: #ff9500;  /* 橙色 - 中风险 */
--risk-low: #34c759;     /* 绿色 - 低风险 */

/* 文本层级 - 简化为三级 */
--text-primary: #1d1d1f;    /* 主要文本 */
--text-secondary: #6e6e73;  /* 次要文本 */
--text-tertiary: #aeaeb2;   /* 辅助文本 */

/* 边框和阴影 - 统一透明度 */
--border: rgba(0, 0, 0, 0.08);
--shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
```

**移除不必要的颜色**:
- 删除多余的橙色、绿色变体
- 统一所有 soft 背景色的透明度为 0.08
- 减少 hover 状态的颜色变化

---

### 2.4 排版系统优化

**字体栈**:
```css
font-family:
  -apple-system,
  BlinkMacSystemFont,
  "SF Pro Display",  /* 标题 */
  "SF Pro Text",     /* 正文 */
  "Inter",           /* 备用 */
  sans-serif;
```

**字号系统** (基于模块化比例 1.25):
```css
--text-xs: 0.64rem;   /* 10px - 标签 */
--text-sm: 0.8rem;    /* 13px - 辅助文本 */
--text-base: 1rem;    /* 16px - 正文 */
--text-lg: 1.25rem;   /* 20px - 小标题 */
--text-xl: 1.563rem;  /* 25px - 标题 */
--text-2xl: 1.953rem; /* 31px - 大标题 */
```

**字重规范**:
- Regular (400): 正文
- Medium (500): 强调文本
- Semibold (600): 小标题
- Bold (700): 标题和数值

---

### 2.5 组件细节打磨

#### Metric Cards (指标卡片)
**优化项**:
- 添加微妙的渐变背景
- Hover 时轻微上浮效果 (translateY(-2px))
- 数值使用等宽数字字体 (tabular-nums)
- 添加加载骨架屏动画

#### Risk Badges (风险徽章)
**优化项**:
- 添加图标前缀
- 增加内边距使其更易点击
- 添加脉冲动画（仅高风险）
- 统一圆角为 999px

#### AI Narrative (AI 叙述文本)
**优化项**:
- 增加行高至 1.7 提升可读性
- 添加首字母下沉效果
- 段落间距增加至 1em
- 添加渐入动画

#### Chat Interface (聊天界面)
**优化项**:
- 消息气泡添加尾巴指示
- 打字动画效果
- 滚动条美化
- 发送按钮添加加载状态

---

## 阶段三：响应式优化

### 3.1 断点系统
```css
/* 移动端 */
@media (max-width: 640px) { ... }

/* 平板 */
@media (min-width: 641px) and (max-width: 1024px) { ... }

/* 桌面 */
@media (min-width: 1025px) { ... }

/* 大屏 */
@media (min-width: 1440px) { ... }
```

### 3.2 移动端特殊处理
- 侧边栏改为底部抽屉
- 指标卡片改为横向滚动
- 图表自动切换为移动端优化版本
- 聊天界面全屏显示

---

## 阶段四：动画和交互

### 4.1 微交互动画
```css
/* 全局过渡 */
* {
  transition:
    background-color 0.2s ease,
    border-color 0.2s ease,
    transform 0.2s ease,
    opacity 0.2s ease;
}

/* 卡片悬停 */
.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* 加载动画 */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* 渐入动画 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### 4.2 数据加载状态
- 骨架屏 (Skeleton screens)
- 进度指示器
- 加载完成的成功提示

---

## 实施步骤

### Step 1: 准备工作 (5分钟)
- [ ] 安装 Lucide Icons CDN
- [ ] 创建新的 CSS 变量系统
- [ ] 备份当前 styles.py

### Step 2: 图标系统 (15分钟)
- [ ] 创建 icon() 辅助函数
- [ ] 替换 Hero 区域的状态点
- [ ] 为侧边栏标签添加图标
- [ ] 为 Tab 标签添加图标
- [ ] 优化风险徽章

### Step 3: 间距优化 (10分钟)
- [ ] 定义新的间距变量
- [ ] 更新所有卡片的 padding/margin
- [ ] 调整组件间距
- [ ] 测试响应式断点

### Step 4: 配色精简 (10分钟)
- [ ] 移除不必要的颜色变量
- [ ] 统一透明度值
- [ ] 更新所有颜色引用
- [ ] 测试对比度符合 WCAG AA

### Step 5: 排版优化 (10分钟)
- [ ] 更新字体栈
- [ ] 应用新的字号系统
- [ ] 调整行高和字重
- [ ] 优化标题层级

### Step 6: 组件打磨 (20分钟)
- [ ] 优化 Metric Cards
- [ ] 优化 Risk Badges
- [ ] 优化 AI Narrative
- [ ] 优化 Chat Interface

### Step 7: 动画添加 (15分钟)
- [ ] 添加全局过渡
- [ ] 实现卡片悬停效果
- [ ] 添加加载动画
- [ ] 实现渐入动画

### Step 8: 响应式测试 (10分钟)
- [ ] 测试移动端 (375px, 414px)
- [ ] 测试平板 (768px, 1024px)
- [ ] 测试桌面 (1280px, 1440px, 1920px)
- [ ] 修复布局问题

### Step 9: 最终打磨 (5分钟)
- [ ] 检查所有间距
- [ ] 验证颜色一致性
- [ ] 测试所有交互
- [ ] 性能优化

---

## 待集成组件 (其他团队)

### 饼图组件接口
```python
def cohort_risk_pie_chart(
    cohort_total: int,
    high_count: int,
    medium_count: int,
    low_count: int
) -> ui.Tag:
    """
    生成 cohort 风险分布饼图

    返回: Plotly 或 ECharts 图表组件
    """
    pass
```

### 箱线图组件接口
```python
def cohort_risk_boxplot(
    cohort_data: dict[str, list[float]],
    current_patient_risk: float,
    current_cohort: str
) -> ui.Tag:
    """
    生成三类 cohort 风险对比箱线图

    参数:
    - cohort_data: {"baseline": [...], "cardiology": [...], "surgery": [...]}
    - current_patient_risk: 当前患者的风险值
    - current_cohort: 当前患者所属的 cohort

    返回: Plotly 或 ECharts 图表组件
    """
    pass
```

---

## 成功标准

### 视觉质量
- [ ] 所有间距符合 8px 网格系统
- [ ] 颜色使用不超过 8 种
- [ ] 所有图标风格统一
- [ ] 无 emoji 残留

### 交互体验
- [ ] 所有悬停效果流畅 (60fps)
- [ ] 加载状态清晰可见
- [ ] 点击反馈即时
- [ ] 动画时长不超过 300ms

### 响应式
- [ ] 移动端 (320px+) 完全可用
- [ ] 平板端布局合理
- [ ] 桌面端充分利用空间
- [ ] 大屏 (1920px+) 不过度拉伸

### 性能
- [ ] 首屏加载 < 2s
- [ ] 交互响应 < 100ms
- [ ] 无布局抖动 (CLS < 0.1)
- [ ] 无内存泄漏

---

## 参考资源

### 设计灵感
- Apple Health App
- Epic MyChart
- Stripe Dashboard
- Linear App

### 图标库
- Lucide Icons: https://lucide.dev
- Heroicons: https://heroicons.com

### 配色工具
- Coolors: https://coolors.co
- Adobe Color: https://color.adobe.com

### 可访问性
- WCAG 2.1 Guidelines
- WebAIM Contrast Checker

---

## 注意事项

1. **不要过度设计**: 保持简洁，每个元素都要有明确目的
2. **保持一致性**: 使用设计系统，避免特例
3. **优先可用性**: 美观不能牺牲功能性
4. **测试真实数据**: 用实际数据测试边界情况
5. **渐进增强**: 确保基础功能在所有设备上可用

---

## 时间估算

- **阶段一** (待其他团队): 2-3 小时
- **阶段二** (全局优化): 1.5 小时
- **阶段三** (响应式): 30 分钟
- **阶段四** (动画): 30 分钟
- **总计**: 约 4.5-5 小时

---

## 下一步行动

1. **立即开始**: 阶段二的图标系统和间距优化（不依赖其他团队）
2. **并行等待**: 阶段一的图表组件由其他团队开发
3. **最后集成**: 将图表组件集成到优化后的 UI 中

准备好后，请告知我开始执行哪个阶段！
