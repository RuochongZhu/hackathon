'/Users/zhuricardo/Desktop/hackathon/aisystemshackathon-main'这是黑客松的一些信息 完整的要求以及例子。详细阅
  读。最重要的是'/Users/zhuricardo/Desktop/hackathon/aisystemshackathon-main/docs/criteria.md'和'/Users/
  zhuricardo/Desktop/hackathon/aisystemshackathon-main/docs/prompts.md'我们选择第二个Prompt 2 — Digital Health
 
  Patient Digital Twins
 
  A regional hospital network is struggling to allocate ICU beds, predict readmissions, and manage appointment
  no-shows.
 
  Your team's job is to build a data-driven platform that uses synthetic patient data to create 'digital twin'
  profiles and generate actionable predictions for clinical decision-makers.
 
  Example Queries
 
  "Which patients in this cohort are at highest risk of 30-day readmission?"
  "Under today's admission forecast, when will ICU capacity reach 90%?"
  "How does this patient's profile compare to historical cases with similar risk factors?"
  Reference Data
 
  Design your own patient schema (e.g., patient ID, age, diagnosis codes, admission date, vitals, risk scores -
  up to you!) and generate synthetic records.
 
  我现在需要你先做计划 首先是你开发的详细计划和测试 怎么确保每个部分独立正确运行 以及交互不出错并且符合预期 在
  这之前人类对于dgital ocean , supabase 以及各种调取数据的api(对接各种公开数据集（或者自己使用仿真技术生成数据
  集）)给出完整的编程方案 以及我这边初始以及每一步的辅助。以及外部的各种配置。以及最重要的你需要的每一步的
  skills清单表格。方便你进行安装。注意严格符合标准 并且参照给出例子（demos）目前的想法是先只做predict
  readmissions 然后根据预测结果让 gen ai进行一些扩展 分析 既扩展定性分析也扩展定量分析 要成熟的基本面+预测分析
  的框架 要成熟和稳定。页面要简洁和优美。