# Institutional Migrant-Support Infrastructure and Chinese Settlement Dynamics in Greater Tokyo

*A public-data DF_M01 MVP analysis of population-service alignment and short-term growth*

Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-27
One-page internal brief. Association-only language. No causal-mediation claim. No novelty claim.
M = institutional migrant-support service infrastructure (registered support organizations),
NOT a complete migrant-service ecosystem.

---

## 1. Research question

Does institutional migrant-support infrastructure in Greater Tokyo follow prior Chinese
population concentration, and does it predict subsequent short-term Chinese registered-resident
growth?

---

## 2. Data and design

- Study area: Greater Tokyo municipalities (Tokyo, Saitama, Chiba, Kanagawa).
- Analytical sample: mainland populated complete-case municipalities, N = 218.
- X: Chinese registered-resident stock, 2023.
- M: DF_M01 registered institutional support organizations.
- Y: short-term Chinese registered-stock growth.
- Controls: rail accessibility, housing cost, commercial density, population density,
  non-Chinese foreign stock, prefecture fixed effects.
- Interpretation: temporally ordered associations, not causal mediation.

---

## 3. Conceptual diagram

```
            Prior Chinese stock (X)
                     |
                     |  strong  (+0.427, p < 0.001)
                     v
     Institutional support infrastructure (M)
                     |
                     |  null    (+0.013, p = 0.168)
                     v
        Subsequent Chinese growth (Y)

    Commercial density  ===> strengthens   X -> M   (interaction +0.106, p = 0.040)
    Housing cost        =/=> does not condition  M -> Y   (interaction -0.008, p = 0.267)
```

---

## 4. Key results

| Path / finding | Result | Interpretation |
|---|---|---|
| X -> M | Positive and robust (+0.427, p < 0.001; adj R2 0.842) | Support infrastructure is spatially aligned with prior Chinese population. |
| M -> Y | Null (+0.013, p = 0.168; adj R2 0.019) | No robust short-term service-to-growth association. |
| X x commercial -> M | Positive, partially robust (+0.106, p = 0.040) | Alignment is stronger in commercially dense municipalities. |
| M x housing -> Y | Null (-0.008, p = 0.267) | Growth-side relationship is not conditioned by housing cost. |
| Spatial robustness | Growth-side null survives SLX, spatial-error, spatial-lag (service p 0.18-0.33) | M -> Y null is robust to explicit spatial-dependence modelling. |

All models OLS with HC3 robust standard errors; continuous predictors standardized. Coefficients
are taken from the consolidated baseline and robustness tables; no models were rerun.

---

## 5. Main interpretation

Institutional migrant-support services are strongly aligned with prior Chinese population
concentration, especially in commercially dense municipalities. However, these services do not
robustly predict short-term subsequent Chinese registered-resident growth once urban opportunity
controls, alternative service scaling, timing choices, and spatial dependence are considered.

---

## 6. What this supports / does not support

Supported:
- population-to-service alignment;
- commercial-density conditioning of service formation;
- no robust short-term service-to-growth relationship.

Not supported:
- causal mediation;
- service infrastructure as a short-term driver of Chinese growth;
- full migrant-service ecosystem claims.

---

## 7. Limitations and next step

- DF_M01 is institutional migrant-support infrastructure, not the full migrant-service ecosystem.
- DF_M01 is not China-specific (covers all registered support organizations).
- The complete-case estimand excludes peripheral/tiny municipalities with missing rail/housing
  controls (33 excluded; estimand = mainland populated Greater Tokyo, N = 218).
- Next step: review this brief, then decide whether to validate M05/M06 or prepare external
  outreach.
