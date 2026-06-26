# Institutional Migrant-Support Infrastructure and Chinese Settlement Dynamics in Greater Tokyo

A public-data DF_M01 MVP analysis of population-service alignment and short-term growth

Association-only. No causal-mediation claim. M = institutional migrant-support infrastructure.

---

### Research question

Does institutional migrant-support infrastructure follow prior Chinese population, and does it
predict subsequent short-term Chinese registered-resident growth?

### Design

- Area: Greater Tokyo municipalities
- Sample: mainland populated complete-case, N = 218
- X: Chinese registered stock, 2023
- M: DF_M01 registered support organizations
- Y: short-term Chinese registered-stock growth
- Controls: rail, housing cost, commercial density, population density, non-Chinese stock, prefecture FE
- Reading: temporally ordered associations, not mediation

### Pathway

```
Prior Chinese stock (X)
   | strong  +0.427 (p < 0.001)
   v
Support infrastructure (M)
   | null    +0.013 (p = 0.168)
   v
Subsequent Chinese growth (Y)

Commercial density strengthens X -> M  (+0.106, p = 0.040)
Housing cost does not condition M -> Y (-0.008, p = 0.267)
```

### Key results

| Path | Result | Reading |
|---|---|---|
| X -> M | +0.427, p < 0.001 | robust alignment |
| M -> Y | +0.013, p = 0.168 | null |
| X x commercial -> M | +0.106, p = 0.040 | partially robust |
| M x housing -> Y | -0.008, p = 0.267 | null |
| Spatial robustness | service p 0.18-0.33 | null survives SLX / error / lag |

### Bottom line

Support services align strongly with prior Chinese population (stronger where commercial density
is high) but do not robustly predict short-term subsequent Chinese growth under urban-opportunity
controls, alternative scaling, timing, and spatial dependence.

### Supports

- population-to-service alignment
- commercial-density conditioning of service formation
- no robust short-term service-to-growth relationship

### Does not support

- causal mediation
- service infrastructure as a short-term growth driver
- full migrant-service ecosystem claims

### Limitations / next step

- M is institutional support infrastructure, not the full ecosystem; not China-specific.
- Complete-case estimand excludes peripheral/tiny municipalities (N = 218).
- Next: review brief, then decide M05/M06 validation vs external outreach.
