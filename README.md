# Capital Intelligence | Capital PMO Analytics Dashboard

**Power BI portfolio project | Capital budgeting, project governance, and investment performance**

A three-page Power BI dashboard designed to demonstrate how a Capital Project Management Office (PMO) can monitor capital budgets, expenditures, project health, and stage-gate governance across manufacturing investment portfolios.

> **Data disclaimer:** This is an independent portfolio project using **synthetic/simulated data**. The budgets, projects, facilities, and results are illustrative and do not represent The Hershey Company or any real organization's internal information.

## Dashboard at a glance

| Metric | Result |
| --- | ---: |
| Simulated capital projects | 80 |
| Total approved budget | $172.21M |
| Total actual spend | $70.25M |
| Remaining budget | $101.96M |
| Budget utilization | 40.8% |
| Approved stage-gate reviews | 291 |
| Pending stage-gate reviews | 30 |
| Documentation compliance | 95.3% |

*Figures reflect the unfiltered sample dashboard shown in the screenshots; totals may change when filters are applied. Stage-gate review counts are review records, not distinct projects.*

## Dashboard pages

### 1. Capital Portfolio Overview

![Capital Portfolio Overview](docs/screenshots/Portfolio-Overview.png)

Provides an at-a-glance view of capital investment performance, including:

- Approved budget, actual spending, and remaining budget KPIs
- Budget versus spending by budget group (Confectionery, International, Salty)
- Project status distribution across On Track, Completed, At Risk, and Delayed
- Interactive Plan Year and Facility slicers

**Portfolio status:** 34 On Track, 27 Completed, 13 At Risk, and 6 Delayed projects.

### 2. Project Governance & Compliance

![Project Governance and Compliance](docs/screenshots/project-governance.png)

Tracks the simulated capital stage-gate review process through:

- Approved and pending review counts
- Documentation completeness rate
- Review decisions by gate: Intake, Business Case, Design, Approval, Execution, and Closeout
- A detailed review register with Project ID, Gate, Decision, DocumentsComplete, and ReviewDate

The page is designed to demonstrate how project approval governance and documentation quality can be monitored.

### 3. Capital Investment Trends

![Capital Investment Trends](docs/screenshots/year-over-year.png)

Compares approved capital budgets and actual expenditures for FY2025–2027, including:

- Annual budget versus actual expenditure chart
- Budget utilization KPI
- Budget group/year comparison matrix
- Interactive Budget Group slicer

## Tools and techniques

- **Power BI Desktop:** Data modeling, interactive reports, slicers, KPI cards, clustered charts, donut chart, table, and matrix
- **DAX:** Measures for total budget, actual spend, budget remaining, utilization, approval counts, pending reviews, and documentation compliance
- **Power Query:** Data-type preparation and loading
- **Relational modeling:** One-to-many relationships from `Projects` to `MonthlySpend` and `StageGates` via `ProjectID`

### Example DAX measures

```dax
Total Budget = SUM('Projects'[ApprovedBudget])

Total Actual Spend = SUM('MonthlySpend'[ActualSpend])

Budget Remaining = [Total Budget] - [Total Actual Spend]

Budget Utilization % = DIVIDE([Total Actual Spend], [Total Budget], 0)

Approved Reviews =
CALCULATE(COUNTROWS('StageGates'), 'StageGates'[Decision] = "Approved")

Pending Reviews =
CALCULATE(COUNTROWS('StageGates'), 'StageGates'[Decision] = "Pending")

Documentation Compliance % =
DIVIDE(
    CALCULATE(COUNTROWS('StageGates'), 'StageGates'[DocumentsComplete] = "Yes"),
    COUNTROWS('StageGates'),
    0
)
```

## Data model

The dashboard uses three logical tables:

| Table | Purpose | Key fields |
| --- | --- | --- |
| `Projects` | Capital project portfolio, budgets, status, and organizational attributes | `ProjectID`, `ApprovedBudget`, `BudgetGroup`, `PlanYear`, `Facility`, `Status` |
| `MonthlySpend` | Expenditure records associated with projects | `ProjectID`, `ActualSpend`, `SpendDate` |
| `StageGates` | Review decisions and documentation compliance | `ProjectID`, `Gate`, `Decision`, `DocumentsComplete`, `ReviewDate` |

Relationships: `Projects[ProjectID]` (1) → `MonthlySpend[ProjectID]` (*) and `Projects[ProjectID]` (1) → `StageGates[ProjectID]` (*).

## How to explore

1. Open the Power BI Desktop `.pbix` file **if included in this repository**.
2. Navigate between the three report pages.
3. Use the slicers to filter by year, facility, or budget group.
4. Inspect the charts, review register, and summary KPIs.

If the `.pbix` file is not uploaded, the screenshots above provide a static overview of the completed report. The project does **not** require Power BI Service sign-in to view a local `.pbix` in Power BI Desktop.

## Project purpose

This project was created to practice capital PMO analytics workflows: portfolio-level budget monitoring, expenditure tracking, year-over-year comparison, and stage-gate review governance. It is a **self-directed demonstration**, not a deployed enterprise system or evidence of real-world capital budget management.

## Repository organization

```text
capital-pmo-powerbi/
├── README.md
├── Capital-PMO-Dashboard.pbix       # Add your local Power BI report here
└── docs/
    └── screenshots/
        ├── Portfolio-Overview.png
        ├── project-governance.png
        └── year-over-year.png
```

The `.pbix` file is **not included in the downloadable package** unless you add it yourself. Upload any supporting synthetic CSVs or scripts you used if you want the repository to be reproducible.
