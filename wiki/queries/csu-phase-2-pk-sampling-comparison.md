---
title: CSU Phase 2 PK sampling comparison
tags:
  - type/query
---
# CSU Phase 2 PK sampling comparison

This page is a **vault-grounded comparison of what the current local wiki layer does and does not confirm** about **PK sampling strategy** across the main CSU Phase 2 competitor programs.

It is intentionally conservative.

The key practical question is not just whether PK was mentioned, but whether the current vault gives us enough to reason about:

- **exposure-response analysis**
- **dose-response interpretation**
- **dose selection**
- **population-wide sparse PK versus richer PK characterization**

## Bottom line

Across the current promoted vault layer, the competitor programs fall into three practical buckets:

- **Actual schedule recovered and usable now**
  - [Remibrutinib](../programs/remibrutinib.md)
  - [Fenebrutinib](../programs/fenebrutinib.md)
- **PK clearly part of the study design, but exact Phase 2 operational schedule still under-described in the promoted page**
  - [Barzolvolimab](../programs/barzolvolimab.md)
- **PK layer still thin / not clearly summarized in the promoted page**
  - [Rilzabrutinib](../programs/rilzabrutinib.md)
  - [EVO756](../programs/evo756.md)

## Comparison table

| Program | Trial | Modality | Dose-ranging structure | **PK schedule** | **Schedule citation** | Current classification | Usefulness for PK / ER inference | Confidence in current vault answer | Best next-source target for enrichment |
|---|---|---|---|---|---|---|---|---|---|
| [Remibrutinib](../programs/remibrutinib.md) | [NCT03926611](../trials/remibrutinib-nct03926611-phase-2b.md) | Oral BTK inhibitor | **7-arm Phase 2b dose-finding** study with **6 active regimens plus placebo** | **No Day 1 PK**; **Week 4 / Day 29**; **Week 12 / Day 85**; protocol says **limited sampling up to 4 hours**, across all cohorts; unscheduled visit PK option also shown in the assessment schedule. | `tmp/remibrutinib_nct03926611_layout.txt#L494-L497`; `#L1596-L1617`; `#L2015-L2026` | **Actual schedule recovered; limited rich steady-state PK embedded in main study** | **High**. Strong oral comparator for ER-informed dose selection, especially for tying exposure to a Week 4 decision point and comparing QD vs BID behavior. | **High** for Week 4 / Week 12 / no Day 1 / limited up-to-4h characterization; **moderate** for exact within-visit sample times because Appendix 6 details were not preserved in the public PDF. | Recover Appendix 6 or equivalent detailed within-visit time grid if available in local source stack. |
| [Fenebrutinib](../programs/fenebrutinib.md) | [NCT03137069](../trials/fenebrutinib-nct03137069.md) | Oral BTK inhibitor | Phase 2 **pilot plus dose-ranging** study with separate cohort structure | **Day 1**; **Week 1**; **Week 6**; **Week 12**; **Early termination**. Protocol rationale says these were **multiple pre-dose plasma concentrations** for exposure-response and dose selection. | `tmp/fenebrutinib_nct03137069_layout.txt#L1429-L1434`; `#L4106-L4107` | **Actual schedule recovered; sparse pre-dose/trough-like PK design** | **High** for lean ER-oriented sparse PK logic; less useful for precise peak characterization. | **High** for the repeated pre-dose intent and main timepoints; **moderate** for any finer operational handling not visible in the extracted schedule. | Promote any remaining cohort-specific PK operational details if recovered from protocol appendices or manuscript supplements. |
| [Rilzabrutinib](../programs/rilzabrutinib.md) | [NCT05107115](../trials/rilzabrutinib-nct05107115.md) | Oral BTK inhibitor | **4-arm Phase 2 dose-ranging** study with **3 active regimens plus placebo** | **Not currently recoverable in promoted vault layer**. | [Trial page note](../trials/rilzabrutinib-nct05107115.md) | **Relevant comparator with thin promoted PK layer** | **Low to moderate right now**; useful structurally, weak as a PK-design anchor until enriched. | **High** for the statement that current PK detail is thin. | Recover and promote protocol, poster, or supplement detail describing PK sampling if available locally. |
| [Barzolvolimab](../programs/barzolvolimab.md) | [NCT05368285](../trials/barzolvolimab-nct05368285.md) | Anti-KIT monoclonal antibody | Placebo-controlled **16-week core dose-finding** study with active extension reflected in 6 CT.gov arm groups | **Exact Phase 2 operational schedule not yet promoted on-page**; PK/PD clearly in scope. | [Trial page note](../trials/barzolvolimab-nct05368285.md) | **Biologic comparator with PK/PD clearly in scope but schedule not yet promoted** | **High** for biologic comparator logic, but less directly usable than remibrutinib/fenebrutinib for oral-schedule design. | **Moderate**. | Promote manuscript-level schedule/characterization detail into the Phase 2 page. |
| [EVO756](../programs/evo756.md) | [NCT06873516](../trials/evo756-nct06873516.md) | Oral MRGPRX2 antagonist | Global randomized **Phase 2b oral dose-ranging** study with **3 active regimens plus placebo** | **Not currently recoverable in promoted vault layer**. | [Trial page note](../trials/evo756-nct06873516.md) | **Potentially important comparator with currently underbuilt PK layer** | **Low right now** for PK design inference. | **High** for the statement that current PK detail is thin. | Enrich from sponsor initiation materials and later protocol/manuscript/poster sources as they enter the vault. |

## Actual recovered schedules

### Remibrutinib — NCT03926611
- **No Day 1 PK assessment**
- **PK at Week 4 / Day 29**
- **PK at Week 12 / Day 85**
- **Limited sampling up to 4 hours**
- PK described as across **all cohorts**
- Protocol goal was to relate exposure to **AUC/Cmax** and PK/PD readouts

**Schedule citation**
- `tmp/remibrutinib_nct03926611_layout.txt#L494-L497`
- `tmp/remibrutinib_nct03926611_layout.txt#L1596-L1617`
- `tmp/remibrutinib_nct03926611_layout.txt#L2015-L2026`

### Fenebrutinib — NCT03137069
- **Day 1**
- **Week 1**
- **Week 6**
- **Week 12**
- **Early termination**
- Protocol rationale says these were **multiple pre-dose plasma concentrations** for **exposure-response analysis** and future **dose selection**

**Schedule citation**
- `tmp/fenebrutinib_nct03137069_layout.txt#L1429-L1434`
- `tmp/fenebrutinib_nct03137069_layout.txt#L4106-L4107`

## Practical read

- **Best current oral PK design anchors:** remibrutinib and fenebrutinib, because the actual schedules are now recoverable and citable.
- **Remibrutinib** looks like the better template if the goal is **decision-relevant steady-state PK** tied to a key efficacy readout.
- **Fenebrutinib** looks like the better template if the goal is **lean sparse pre-dose ER sampling**.
- **Best current biologic PK/PD comparator:** barzolvolimab, but the exact Phase 2 operational schedule still needs promotion.
- **Most limited current PK pages:** rilzabrutinib and EVO756.

## Schedule citations

- **Remibrutinib actual schedule:** `tmp/remibrutinib_nct03926611_layout.txt#L494-L497`, `#L1596-L1617`, `#L2015-L2026`
- **Fenebrutinib actual schedule:** `tmp/fenebrutinib_nct03137069_layout.txt#L1429-L1434`, `#L4106-L4107`

## Recommended next vault actions

1. Keep **remibrutinib** as the anchor oral comparator for limited-rich steady-state PK design.
2. Keep **fenebrutinib** as the anchor oral comparator for sparse pre-dose ER-focused PK design.
3. Add a short PK design paragraph to the **barzolvolimab** Phase 2 page separating biologic-style PK/PD characterization from oral small-molecule strategy.
4. Keep **rilzabrutinib** and **EVO756** marked as **PK-underdescribed** until stronger local evidence is promoted.

## Source notes

This comparison is based on the current promoted wiki trial pages:
- [Remibrutinib NCT03926611](../trials/remibrutinib-nct03926611-phase-2b.md)
- [Fenebrutinib NCT03137069](../trials/fenebrutinib-nct03137069.md)
- [Rilzabrutinib NCT05107115](../trials/rilzabrutinib-nct05107115.md)
- [Barzolvolimab NCT05368285](../trials/barzolvolimab-nct05368285.md)
- [EVO756 NCT06873516](../trials/evo756-nct06873516.md)

The goal here is to reflect **what the vault currently knows in promoted form**, not to over-claim from deeper raw materials that have not yet been surfaced cleanly into the public trial pages.
