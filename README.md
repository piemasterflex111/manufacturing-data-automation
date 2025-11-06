# Manufacturing Data Automation

## 🎯 Objective
Automate the collection and analysis of production station logs to calculate key manufacturing metrics like:
- First-Pass Yield (FPY)
- Failure Pareto
- Cost of Poor Quality (CoPQ)

This replaces manual Excel work with reproducible, traceable Python automation.

---

## 🧱 Project Structure
manufacturing-data-automation/
│
├── scripts/
│ └── merge_and_fpy.py # Main automation script
│
├── data/
│ ├── raw/ # Raw CSVs exported from test/weld stations
│ └── processed/ # Consolidated and computed outputs
│
├── requirements.txt # Python dependencies
└── README.md


---

## ⚙️ How to Run
```bash
# 1. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run script
python scripts\merge_and_fpy.py

Outputs will appear in data/processed/:

all_logs_consolidated.csv

daily_fpy.csv

failure_pareto.csv

(optional) daily_cost.csv

📊 Example Output
date	units_built	units_pass	fpy_pct
2025-11-01	100	88	88.0
2025-11-02	95	91	95.8
fail_code	count	cum_pct
VOLT_LOW	15	41.6
CURR_NOISE	12	74.6
CONTACT	8	100.0
🧠 Skills Demonstrated

Python pandas for data wrangling

File system automation with pathlib

FPY and Pareto analysis for yield tracking

Data reproducibility and traceability best practices

GitHub version control for continuous improvement

🚀 Next Steps

Connect outputs to a Power BI dashboard

Add API integration to pull data from MES or SharePoint

Include SPC metrics (Cp, Cpk, trend monitoring)

Develop automated email reporting script

📚 Author

Payam Adloo
Manufacturing Engineer | Process Data Automation | Yield Optimization


---

Once you commit and push:
```powershell
git add README.md
git commit -m "Added professional project README"
git push


Would you like me to generate an example README screenshot section (with fake FPY chart + Pareto chart images) to make your GitHub visually stronger?
