import json, random, os, math
from pathlib import Path
from datetime import datetime, timedelta

HERE = Path(__file__).parent
DATA_DIR = HERE.parent / "data"

def gen_census(n=2000):
    random.seed(42)
    education_levels = ["High School", "Some College", "Associate Degree", "Bachelor's Degree",
                       "Master's Degree", "Professional Degree", "Doctorate"]
    edu_weights = [25, 15, 10, 30, 12, 5, 3]
    edu_income_base = [30000, 35000, 40000, 55000, 75000, 120000, 100000]
    occupations = {
        "Tech": {"edu_min": 3, "income_mult": 1.5, "weight": 0.18},
        "Healthcare": {"edu_min": 2, "income_mult": 1.3, "weight": 0.12},
        "Education": {"edu_min": 3, "income_mult": 0.9, "weight": 0.10},
        "Finance": {"edu_min": 3, "income_mult": 1.6, "weight": 0.12},
        "Manufacturing": {"edu_min": 1, "income_mult": 0.8, "weight": 0.10},
        "Retail": {"edu_min": 0, "income_mult": 0.6, "weight": 0.13},
        "Government": {"edu_min": 2, "income_mult": 1.0, "weight": 0.08},
        "Service": {"edu_min": 0, "income_mult": 0.5, "weight": 0.10},
        "Construction": {"edu_min": 0, "income_mult": 0.7, "weight": 0.05},
        "Agriculture": {"edu_min": 0, "income_mult": 0.5, "weight": 0.02},
    }
    marital = ["Married", "Single", "Divorced", "Widowed"]
    marital_weights = [50, 35, 12, 3]
    races = ["White", "Black", "Asian", "Hispanic", "Other"]
    race_weights = [60, 12, 6, 18, 4]
    relationships = ["Husband", "Wife", "Son", "Daughter", "Not-in-family", "Unmarried", "Other-relative"]
    native_countries = ["United-States", "Mexico", "Philippines", "Germany", "India", "Canada", "England", "China"]
    out = []
    for i in range(n):
        age = max(18, min(int(random.gauss(42, 15)), 80))
        edu_idx = random.choices(range(len(education_levels)), weights=edu_weights, k=1)[0]
        edu = education_levels[edu_idx]
        occ_names = list(occupations.keys())
        occ_weights_list = [occupations[o]["weight"] for o in occ_names]
        occ_idx = random.choices(range(len(occ_names)), weights=occ_weights_list, k=1)[0]
        occ = occ_names[occ_idx]
        occ_info = occupations[occ]
        base_income = edu_income_base[edu_idx] * occ_info["income_mult"]
        age_effect = 1.0
        if 25 <= age <= 55:
            age_effect = 1.0 + (age - 25) * 0.01
        elif age > 55:
            age_effect = max(0.8, 1.3 - (age - 55) * 0.01)
        income = max(15000, int(random.gauss(base_income * age_effect, base_income * 0.3)))
        capital_gain = 0
        if random.random() < 0.15:
            capital_gain = max(0, int(random.lognormvariate(8, 1.5)))
        capital_loss = 0
        if random.random() < 0.08:
            capital_loss = max(0, int(random.lognormvariate(6, 1.2)))
        hours_base = 40 if occ not in ["Tech", "Finance"] else 45
        if age > 60:
            hours_base -= 5
        hours_week = max(10, min(int(random.gauss(hours_base, 8)), 80))
        marital_status = random.choices(marital, weights=marital_weights, k=1)[0]
        if age < 25:
            marital_status = random.choices(["Single", "Married"], weights=[80, 20], k=1)[0]
        elif age > 70:
            marital_status = random.choices(["Married", "Widowed", "Divorced"], weights=[50, 30, 20], k=1)[0]
        income_bracket = ">50K" if income > 50000 else "<=50K"
        out.append({
            "id": f"census_{i:06d}",
            "age": age,
            "education": edu,
            "education_num": edu_idx + 1,
            "occupation": occ,
            "marital_status": marital_status,
            "race": random.choices(races, weights=race_weights, k=1)[0],
            "sex": random.choice(["Male", "Female"]),
            "capital_gain": capital_gain,
            "capital_loss": capital_loss,
            "hours_per_week": hours_week,
            "native_country": random.choices(native_countries, weights=[70,5,5,3,3,3,3,3], k=1)[0],
            "relationship": random.choices(relationships, weights=[30,30,10,10,10,5,5], k=1)[0],
            "income_bracket": income_bracket,
            "income_amount": income,
            "age_group": "18-24" if age < 25 else "25-34" if age < 35 else "35-44" if age < 45 else "45-54" if age < 55 else "55-64" if age < 65 else "65+",
            "net_capital": capital_gain - capital_loss,
            "work_intensity": round(hours_week / 40, 2),
        })
    return out

def main():
    data = gen_census()
    DATA_DIR.mkdir(exist_ok=True)
    out = DATA_DIR / "dataset.json"
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Generated {len(data)} census income records")
    print(f"Saved to {out}")

if __name__ == "__main__":
    main()
