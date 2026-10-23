"""Generate deterministic, fictional capital portfolio datasets for Power BI."""
from pathlib import Path
import csv, random, datetime, calendar

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data'
OUT.mkdir(exist_ok=True)
rng = random.Random(2027)
facilities = [ ('Hershey-like Confectionery East','Confectionery','United States'), ('Confectionery West','Confectionery','United States'), ('Salty Snacks Central','Salty','United States'), ('International Plant North','International','Canada'), ('International Plant South','International','Mexico') ]
# Generic fictional names. Not affiliated with, or reflective of, any actual company's budgets.
facilities[0] = ('Confectionery East','Confectionery','United States')
types = ['Packaging','Process Equipment','Utilities','Safety','Automation','Infrastructure']
stages = ['Intake','Business Case','Design','Approval','Execution','Closeout']
statuses = ['On Track','At Risk','Delayed','Completed']
projects=[]; spend=[]; approvals=[]
for i in range(1,81):
    pid=f'CAP-{i:04d}'
    facility, group, country = facilities[(i-1)%len(facilities)]
    year = 2025 + ((i-1)%3)
    budget = rng.randrange(180000, 3900000, 10000)
    stage = rng.choices(stages, weights=[10,12,14,14,35,15])[0]
    status = rng.choices(statuses, weights=[52,22,13,13])[0]
    if stage == 'Closeout': status = 'Completed'
    approved = stage in ('Approval','Execution','Closeout')
    projects.append(dict(ProjectID=pid, ProjectName=f'{types[(i-1)%len(types)]} Modernization {i:02d}', Facility=facility, BudgetGroup=group, Country=country, PlanYear=year, ProjectType=types[(i-1)%len(types)], Stage=stage, Status=status, ApprovedBudget=budget, ApprovalStatus='Approved' if approved else 'Pending'))
    # 12 monthly spend records per project; budget usage varies with project stage and status.
    factor = {'Intake':0.015,'Business Case':0.04,'Design':0.13,'Approval':0.24,'Execution':0.66,'Closeout':0.98}[stage]
    if status == 'At Risk': factor *= 1.12
    if status == 'Delayed': factor *= .76
    factor *= rng.uniform(.75,1.34)
    actual_total = round(budget*factor,2)
    weights=[rng.uniform(.2,1.8) for _ in range(12)]; weight_sum=sum(weights)
    amounts=[round(actual_total*w/weight_sum,2) for w in weights]
    amounts[-1]=round(actual_total-sum(amounts[:-1]),2)
    for month,amount in enumerate(amounts,1):
        spend.append(dict(ProjectID=pid, SpendDate=datetime.date(year,month, min(15,calendar.monthrange(year,month)[1])).isoformat(), ActualSpend=f'{amount:.2f}', CostCategory=['Equipment','Installation','Engineering','Materials'][month%4]))
    for n, stage_name in enumerate(stages[:stages.index(stage)+1]):
        decision = 'Approved' if n < stages.index(stage) or approved else 'Pending'
        approvals.append(dict(ProjectID=pid, Gate=stage_name, Decision=decision, ReviewDate=datetime.date(year,min(n+1,12),10).isoformat(), DocumentsComplete='Yes' if decision=='Approved' else rng.choice(['Yes','No'])))

def write_csv(name, rows):
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
write_csv('projects.csv',projects)
write_csv('monthly_spend.csv',spend)
write_csv('stage_gates.csv',approvals)
print(f'Generated {len(projects)} projects, {len(spend)} spend rows, {len(approvals)} stage gate rows')
