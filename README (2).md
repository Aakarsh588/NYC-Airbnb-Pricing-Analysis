# What Actually Drives Airbnb Pricing in NYC?

**A marketplace pricing case study — SQL, Power BI, hypothesis testing, and a first pass at regression, on 48,895 real Airbnb listings**

---

## Brief

A hospitality marketplace (Airbnb) wants to understand what genuinely drives listing price: room type, neighbourhood, host behavior, or something else entirely? This analysis moves beyond single-factor comparisons to test several hypotheses rigorously — confirming real drivers, ruling out plausible-but-false ones, and being honest about how much price variation remains unexplained.

**Dataset:** 48,895 real NYC Airbnb listings via Inside Airbnb (2019 snapshot) — genuinely messy: a 2019-era CSV export containing 184 rows with malformed text encoding (unescaped quote characters that scrambled column alignment), over 20% missing review data, and price outliers ($0 and $10,000 listings) requiring investigation rather than blind removal.

**Tools used:** SQL (SQLite) · Python (pandas, SciPy for hypothesis testing, scikit-learn for regression) · Power BI for an interactive dashboard.

---

## Insight

**Data quality, handled deliberately, not glossed over.** 184 rows (0.4%) were corrupted by malformed quote characters in the source CSV and excluded after verification. Price outliers were evaluated individually rather than removed by threshold alone: $10,000 listings with zero availability were excluded as inactive/junk data, while $0-priced listings with genuine review activity (some with 90+ reviews) were identified as a likely data-collection gap rather than fake listings, and excluded only from price-specific analysis.

**Confirmed driver #1 — Room type.** Entire home/apt averages $211 vs. Private room's $89 (t = 59.98, p < 0.001) — real, but expected: larger private spaces cost more.

**Confirmed driver #2 — Neighbourhood, controlling for room type (the headline finding).** Manhattan carries a genuine price premium over every other borough, **within every room type**, not just because it has more entire-apartment listings:

| Room Type | Bronx | Brooklyn | **Manhattan** | Queens | Staten Island |
|---|---|---|---|---|---|
| Entire home/apt | $128 | $177 | **$249** | $147 | $174 |
| Private room | $67 | $77 | **$117** | $69 | $62 |
| Shared room | $60 | $51 | **$89** | $69 | $57 |

Manhattan leads in every tier — roughly **2x the Bronx** for entire homes. This is the more useful, less obvious finding: it isn't just "Manhattan has more expensive listing types," it's a consistent location premium independent of what's being rented.

**Ruled out, explicitly.** `minimum_nights` (correlation 0.04) and host listing count (0.06) show no meaningful relationship with price — worth reporting as confirmed non-factors, not just omitting them.

**A basic regression to quantify multiple drivers at once** *(built with AI assistance to interpret coefficients and model fit — a first step beyond single-factor testing)*: combining room type, neighbourhood, minimum nights, reviews, and availability into one model explains only **R² ≈ 0.10** of price variation. Read honestly, this means the confirmed drivers above are real but explain a small share of the full picture — the remaining ~90% likely comes from listing-specific factors (unit quality, amenities, photos, host reputation) not captured in this dataset. Reporting a weak R² honestly, rather than overselling the model, is itself part of the finding.

---

## Idea

**Recommendation:** location and room type are real, defensible levers for baseline pricing guidance — Manhattan hosts can credibly price above other boroughs regardless of unit type — but a pricing or growth team should not rely on these structural factors alone. With ~90% of price variation unexplained by location/type/host-activity data, the bigger opportunity lies in listing-level signals (photos, descriptions, amenities) that this dataset doesn't capture — a natural next research question, not a gap in this analysis.

---

## Results

An interactive Power BI dashboard models price by neighbourhood and room type with a live room-type filter, KPI summary cards, and an explicit callout of the headline finding:

![Interactive Power BI dashboard: Average Price by Neighbourhood and Room Type, with KPI cards and a Manhattan premium callout](assets/dashboard.png)

**Full pipeline:**
1. Identified and excluded 184 rows corrupted by malformed CSV quoting, verified via Power Query's error detection
2. Investigated price outliers individually (availability and review signals) rather than applying a blind threshold
3. Ran two-sample t-tests to confirm room type and neighbourhood as statistically real price drivers
4. Used correlation analysis to rule out minimum_nights and host listing count as price factors
5. Built a multi-factor linear regression to quantify combined explanatory power, reporting R² honestly rather than overstating model fit
6. Designed an interactive Power BI dashboard with a deliberate visual hierarchy — KPI cards, the evidence chart, and a plain-language insight callout placed directly beside it

*Analysis conducted with Claude as an active technical collaborator — used for debugging, statistical validation, and building the regression component, with every result independently cross-checked against SQL and pandas before being trusted.*

---

## Files in this repository
- `airbnb_analysis.py` — full analysis code: cleaning, SQL queries, hypothesis tests, correlation checks, and the regression model, exactly as written and run
- `airbnb_nyc.csv` — source dataset
- `assets/dashboard.png` — Power BI dashboard screenshot
