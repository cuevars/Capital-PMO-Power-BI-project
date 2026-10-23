# Power BI Build Guide

## 1. Load data

Power BI Desktop > Home > Get Data > Text/CSV. Import `projects.csv`, `monthly_spend.csv`, and `stage_gates.csv`. In Transform Data, rename them `Projects`, `MonthlySpend`, and `StageGates`. Set types: `Projects[PlanYear]` = whole number, `Projects[ApprovedBudget]` = fixed decimal, `MonthlySpend[ActualSpend]` = fixed decimal, `MonthlySpend[SpendDate]` and `StageGates[ReviewDate]` = date. Close & Apply.

## 2. Model relationships

In Model view create `Projects[ProjectID]` (one) -> `MonthlySpend[ProjectID]` (many), single cross-filter direction, and `Projects[ProjectID]` (one) -> `StageGates[ProjectID]` (many), single cross-filter direction. No direct connection between the two fact tables. Check project IDs are unique in Projects.

## 3. Add DAX

In Modeling > New measure, add formulas **one at a time** from `powerbi/measures.dax` (these are measures, not a single executable script). Set currency formatting for budgets/spend, percentage formatting for rates. Note: `Prior Year Spend` and `YoY Spend Change %` are designed for a **single PlanYear filter**; leave blank when no single year is selected.

## 4. Build the visuals

### Page 1 — Portfolio Overview

- Cards: `Total Budget`, `Total Actual Spend`, `Budget Remaining`, `At Risk Projects`.
- Clustered bar chart: Axis `Projects[BudgetGroup]`, values `Total Budget` and `Total Actual Spend`.
- Donut: legend `Projects[Status]`, values `Project Count`.
- Table: `Projects[ProjectID]`, `Projects[ProjectName]`, `Projects[Facility]`, `Projects[Stage]`, `Projects[Status]`, `Projects[ApprovedBudget]`, `Total Actual Spend`.
- Slicers: `Projects[PlanYear]`, `Projects[BudgetGroup]`, `Projects[Facility]`.

### Page 2 — Governance & Data Quality

- Cards: `Approved Projects`, `Pending Projects`, `Gate Compliance %`.
- Bar chart: Axis `StageGates[Gate]`, values `Count of StageGates[ProjectID]` (choose Count, *not* distinct count, since each gate row is unique within a project).
- Stacked bar: Axis `StageGates[Gate]`, legend `StageGates[DocumentsComplete]`, values count of `StageGates[ProjectID]`.
- Table: `StageGates[ProjectID]`, `StageGates[Gate]`, `StageGates[Decision]`, `StageGates[ReviewDate]`, `StageGates[DocumentsComplete]`.
- Slicer: `Projects[BudgetGroup]`.

### Page 3 — Year-over-Year

- Clustered column chart: Axis `Projects[PlanYear]`, values `Total Budget`, `Total Actual Spend`.
- Matrix: Rows `Projects[BudgetGroup]`, columns `Projects[PlanYear]`, values `Total Budget`, `Total Actual Spend`.
- Slicer: `Projects[PlanYear]` (single-select on if using YoY measures), plus cards `Prior Year Spend` and `YoY Spend Change %`.

### Optional extras

- Add drillthrough page filtered by ProjectID.
- Apply conditional formatting to highlight projects where spend exceeds budget.
- Save screenshots after building the real report in `docs/screenshots/`, then reference them from README.

## 5. GitHub upload

Save report as `Capital-PMO-Portfolio.pbip` (Power BI Desktop project) **inside this repository**. This creates report and semantic-model directories suitable for version control. Or save as `.pbix` if you prefer a single binary. In a terminal:

```bash
git init
git add .
git commit -m "Build synthetic capital PMO Power BI portfolio"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/capital-pmo-powerbi.git
git push -u origin main
```

Create the empty GitHub repository first and replace YOUR_USERNAME. Check no company or confidential information is added. Your `.pbip` needs to be saved in Power BI Desktop; the Python generator cannot produce an authenticated, fully validated Power BI report file.
