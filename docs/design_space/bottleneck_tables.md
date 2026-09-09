# Phase A bottleneck tables (generated artifact)

Verbatim stdout of:

    cd ~/telo/feasibility && uv run python scripts/build_bottleneck_tables.py \
        --run abl_20260902_phaseA --pairs-run abl_20260902_phaseA_pairs

Every number below is read from `results/ablation/abl_20260902_phaseA/{summary.json,attribution.csv}`
and `results/ablation/abl_20260902_phaseA_pairs/summary.json`. Do not hand-edit; regenerate.
`docs/design_space/bottleneck_decomposition.md` embeds the ladder tables and the interaction
tables and refers here for the 16 per-cell attribution tables.

---

Run `abl_20260902_phaseA`: 100 common-random-number runs per configuration, master seed 20260901, horizon 5.0 y after 365 d warm-up, tau = 0.99, q = 0.9, designs = optimized:opt_20260902T043854Z. Status-quo utilization (demand / effective saleable capacity of the S0 plant): sodium_bicarbonate_8_4_50ml 1.245, norepinephrine_1mgml_4ml 0.778. PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS

**Mean fill rate by configuration (fraction)**

| configuration | sodium S0 | sodium S1 | sodium S2 | sodium S3 | sodium S4 | sodium S5 | sodium S6 | sodium S7 | norepinephrine S0 | norepinephrine S1 | norepinephrine S2 | norepinephrine S3 | norepinephrine S4 | norepinephrine S5 | norepinephrine S6 | norepinephrine S7 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 0.720 | 0.728 | 0.993 | 0.993 | 0.993 | 0.932 | 0.932 | 0.866 | 0.983 | 0.985 | 0.993 | 0.993 | 0.993 | 0.990 | 0.990 | 0.957 |
| loo:capacity_shortfall | 0.973 | 0.982 | 0.999 | 0.993 | 0.993 | 0.992 | 0.992 | 0.972 | 0.985 | 0.986 | 0.994 | 0.993 | 0.993 | 0.991 | 0.991 | 0.958 |
| loo:surge_headroom | 0.727 | 0.735 | 0.993 | 0.993 | 0.993 | 0.933 | 0.933 | 0.871 | 0.986 | 0.987 | 0.993 | 0.994 | 0.993 | 0.990 | 0.990 | 0.959 |
| loo:inventory_timing | 0.721 | 0.797 | 0.997 | 0.997 | 0.999 | 0.932 | 0.932 | 0.891 | 0.995 | 0.997 | 0.997 | 0.997 | 0.999 | 0.990 | 0.990 | 0.976 |
| loo:api_lead_time | 0.718 | 0.728 | 0.992 | 0.989 | 0.991 | 0.813 | 0.813 | 0.864 | 0.984 | 0.986 | 0.992 | 0.990 | 0.993 | 0.954 | 0.954 | 0.954 |
| loo:component_lead_time | 0.719 | 0.729 | 0.992 | 0.991 | 0.991 | 0.811 | 0.811 | 0.864 | 0.983 | 0.985 | 0.992 | 0.991 | 0.993 | 0.954 | 0.954 | 0.955 |
| loo:release_queue | 0.720 | 0.729 | 0.993 | 0.993 | 0.993 | 0.933 | 0.933 | 0.868 | 0.984 | 0.987 | 0.992 | 0.993 | 0.994 | 0.990 | 0.990 | 0.959 |
| loo:sterility_delay | 0.720 | 0.730 | 0.994 | 0.995 | 0.994 | 0.933 | 0.933 | 0.870 | 0.986 | 0.989 | 0.995 | 0.995 | 0.996 | 0.991 | 0.991 | 0.965 |
| loo:deviation_rejection | 0.727 | 0.735 | 0.993 | 0.992 | 0.993 | 0.934 | 0.934 | 0.870 | 0.985 | 0.986 | 0.993 | 0.993 | 0.994 | 0.991 | 0.991 | 0.960 |
| loo:demand_variance | 0.720 | 0.728 | 0.992 | 0.994 | 0.992 | 0.932 | 0.932 | 0.867 | 0.980 | 0.980 | 0.992 | 0.994 | 0.993 | 0.990 | 0.990 | 0.955 |
| loo:demand_covariance | 0.724 | 0.733 | 0.993 | 0.994 | 0.993 | 0.933 | 0.933 | 0.869 | 0.985 | 0.986 | 0.993 | 0.993 | 0.993 | 0.990 | 0.990 | 0.958 |
| loo:common_cause | 0.743 | 0.753 | 0.995 | 0.993 | 0.993 | 0.936 | 0.936 | 0.878 | 0.991 | 0.991 | 0.994 | 0.993 | 0.994 | 0.992 | 0.992 | 0.967 |
| loo:supplier_concentration | 0.725 | 0.734 | 0.994 | 0.995 | 0.995 | 0.934 | 0.934 | 0.873 | 0.989 | 0.990 | 0.994 | 0.995 | 0.996 | 0.994 | 0.994 | 0.972 |
| loo:site_failures | 0.739 | 0.748 | 0.994 | 0.995 | 0.995 | 0.935 | 0.935 | 0.879 | 0.990 | 0.992 | 0.994 | 0.995 | 0.995 | 0.993 | 0.993 | 0.970 |
| loo:contract_insufficiency | 0.720 | 0.728 | 0.993 | 0.996 | 0.993 | 0.932 | 0.932 | 0.866 | 0.983 | 0.985 | 0.993 | 0.997 | 0.993 | 0.990 | 0.990 | 0.957 |
| loo:regulatory_unavailability | 0.720 | 0.728 | 0.993 | 0.993 | 0.993 | 0.932 | 0.932 | 0.997 | 0.983 | 0.985 | 0.993 | 0.993 | 0.993 | 0.990 | 0.990 | 0.997 |
| loo:commissioning_delay | 0.720 | 0.728 | 0.997 | 0.993 | 1.000 | 0.999 | 0.999 | 0.866 | 0.983 | 0.985 | 0.997 | 0.993 | 0.999 | 0.999 | 0.999 | 0.957 |
| loo:fixed_quality_cost | 0.720 | 0.728 | 0.993 | 0.993 | 0.993 | 0.932 | 0.932 | 0.866 | 0.983 | 0.985 | 0.993 | 0.993 | 0.993 | 0.990 | 0.990 | 0.957 |
| loo:replicated_validation_cost | 0.720 | 0.728 | 0.993 | 0.993 | 0.993 | 0.932 | 0.932 | 0.866 | 0.983 | 0.985 | 0.993 | 0.993 | 0.993 | 0.990 | 0.990 | 0.957 |
| loo:capital_cost | 0.720 | 0.728 | 0.993 | 0.993 | 0.993 | 0.932 | 0.932 | 0.866 | 0.983 | 0.985 | 0.993 | 0.993 | 0.993 | 0.990 | 0.990 | 0.957 |
| loo:lost_sales_window | 0.714 | 0.725 | 0.996 | 0.998 | 0.995 | 0.937 | 0.937 | 0.869 | 0.989 | 0.991 | 0.997 | 0.998 | 0.998 | 0.993 | 0.993 | 0.973 |
| loo:horizon_10y | 0.704 | 0.708 | 0.996 | 0.992 | 0.996 | 0.966 | 0.966 | 0.833 | 0.984 | 0.985 | 0.996 | 0.993 | 0.996 | 0.994 | 0.994 | 0.959 |
| quiet_all | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:capacity_shortfall | 0.794 | 0.881 | 1.000 | 1.000 | 1.000 | 0.878 | 0.878 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:surge_headroom | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:inventory_timing | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:api_lead_time | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:component_lead_time | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:release_queue | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:sterility_delay | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:deviation_rejection | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:demand_variance | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:demand_covariance | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:common_cause | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 0.999 | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.993 | 0.993 | 1.000 |
| addin:supplier_concentration | 0.998 | 0.999 | 0.999 | 0.999 | 0.999 | 0.998 | 0.998 | 0.999 | 0.999 | 0.999 | 0.999 | 0.998 | 0.999 | 0.995 | 0.995 | 0.998 |
| addin:site_failures | 0.997 | 1.000 | 1.000 | 1.000 | 1.000 | 0.998 | 0.998 | 1.000 | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 0.991 | 1.000 |
| addin:contract_insufficiency | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:regulatory_unavailability | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| addin:commissioning_delay | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| bounds:ss365 | 0.722 | 0.722 | 0.990 | 0.983 | 0.985 | 0.935 | 0.935 | 0.868 | 0.977 | 0.977 | 0.991 | 0.971 | 0.985 | 0.987 | 0.987 | 0.948 |
| bounds:ss365+base_stock | 0.856 | 0.856 | 1.000 | 0.999 | 1.000 | 1.000 | 1.000 | 0.963 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

**P(fill >= 0.99) by configuration**

| configuration | sodium S0 | sodium S1 | sodium S2 | sodium S3 | sodium S4 | sodium S5 | sodium S6 | sodium S7 | norepinephrine S0 | norepinephrine S1 | norepinephrine S2 | norepinephrine S3 | norepinephrine S4 | norepinephrine S5 | norepinephrine S6 | norepinephrine S7 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 0.00 | 0.00 | 0.89 | 0.86 | 0.79 | 0.00 | 0.00 | 0.19 | 0.56 | 0.65 | 0.84 | 0.86 | 0.86 | 0.72 | 0.72 | 0.21 |
| loo:capacity_shortfall | 0.42 | 0.50 | 0.99 | 0.88 | 0.81 | 0.80 | 0.80 | 0.45 | 0.59 | 0.64 | 0.90 | 0.88 | 0.86 | 0.75 | 0.75 | 0.22 |
| loo:surge_headroom | 0.00 | 0.00 | 0.89 | 0.88 | 0.81 | 0.00 | 0.00 | 0.20 | 0.62 | 0.69 | 0.87 | 0.91 | 0.86 | 0.72 | 0.72 | 0.23 |
| loo:inventory_timing | 0.00 | 0.00 | 0.93 | 0.95 | 0.98 | 0.00 | 0.00 | 0.29 | 0.90 | 0.94 | 0.93 | 0.94 | 0.98 | 0.73 | 0.73 | 0.47 |
| loo:api_lead_time | 0.00 | 0.00 | 0.85 | 0.76 | 0.79 | 0.00 | 0.00 | 0.17 | 0.58 | 0.61 | 0.81 | 0.75 | 0.83 | 0.23 | 0.23 | 0.20 |
| loo:component_lead_time | 0.00 | 0.00 | 0.86 | 0.74 | 0.77 | 0.00 | 0.00 | 0.17 | 0.53 | 0.63 | 0.81 | 0.81 | 0.82 | 0.22 | 0.22 | 0.20 |
| loo:release_queue | 0.00 | 0.00 | 0.88 | 0.89 | 0.84 | 0.00 | 0.00 | 0.17 | 0.63 | 0.66 | 0.83 | 0.86 | 0.86 | 0.72 | 0.72 | 0.25 |
| loo:sterility_delay | 0.00 | 0.00 | 0.90 | 0.90 | 0.87 | 0.00 | 0.00 | 0.21 | 0.66 | 0.68 | 0.90 | 0.90 | 0.88 | 0.73 | 0.73 | 0.31 |
| loo:deviation_rejection | 0.00 | 0.00 | 0.86 | 0.81 | 0.84 | 0.00 | 0.00 | 0.20 | 0.60 | 0.62 | 0.86 | 0.85 | 0.88 | 0.75 | 0.75 | 0.21 |
| loo:demand_variance | 0.00 | 0.00 | 0.85 | 0.87 | 0.79 | 0.00 | 0.00 | 0.18 | 0.49 | 0.47 | 0.84 | 0.87 | 0.79 | 0.72 | 0.72 | 0.21 |
| loo:demand_covariance | 0.00 | 0.00 | 0.89 | 0.89 | 0.81 | 0.00 | 0.00 | 0.18 | 0.63 | 0.64 | 0.85 | 0.87 | 0.85 | 0.72 | 0.72 | 0.21 |
| loo:common_cause | 0.00 | 0.00 | 0.93 | 0.88 | 0.81 | 0.00 | 0.00 | 0.19 | 0.75 | 0.76 | 0.92 | 0.86 | 0.87 | 0.78 | 0.78 | 0.28 |
| loo:supplier_concentration | 0.00 | 0.00 | 0.90 | 0.90 | 0.86 | 0.00 | 0.00 | 0.18 | 0.64 | 0.69 | 0.88 | 0.89 | 0.91 | 0.83 | 0.83 | 0.34 |
| loo:site_failures | 0.00 | 0.00 | 0.93 | 0.92 | 0.91 | 0.00 | 0.00 | 0.21 | 0.80 | 0.85 | 0.92 | 0.94 | 0.94 | 0.81 | 0.81 | 0.31 |
| loo:contract_insufficiency | 0.00 | 0.00 | 0.89 | 0.99 | 0.79 | 0.00 | 0.00 | 0.19 | 0.56 | 0.65 | 0.84 | 0.98 | 0.86 | 0.72 | 0.72 | 0.21 |
| loo:regulatory_unavailability | 0.00 | 0.00 | 0.89 | 0.86 | 0.79 | 0.00 | 0.00 | 0.95 | 0.56 | 0.65 | 0.84 | 0.86 | 0.86 | 0.72 | 0.72 | 0.94 |
| loo:commissioning_delay | 0.00 | 0.00 | 0.95 | 0.86 | 1.00 | 0.99 | 0.99 | 0.19 | 0.56 | 0.65 | 0.95 | 0.86 | 0.99 | 0.99 | 0.99 | 0.21 |
| loo:fixed_quality_cost | 0.00 | 0.00 | 0.89 | 0.86 | 0.79 | 0.00 | 0.00 | 0.19 | 0.56 | 0.65 | 0.84 | 0.86 | 0.86 | 0.72 | 0.72 | 0.21 |
| loo:replicated_validation_cost | 0.00 | 0.00 | 0.89 | 0.86 | 0.79 | 0.00 | 0.00 | 0.19 | 0.56 | 0.65 | 0.84 | 0.86 | 0.86 | 0.72 | 0.72 | 0.21 |
| loo:capital_cost | 0.00 | 0.00 | 0.89 | 0.86 | 0.79 | 0.00 | 0.00 | 0.19 | 0.56 | 0.65 | 0.84 | 0.86 | 0.86 | 0.72 | 0.72 | 0.21 |
| loo:lost_sales_window | 0.00 | 0.00 | 0.93 | 0.97 | 0.87 | 0.00 | 0.00 | 0.22 | 0.74 | 0.78 | 0.95 | 0.96 | 0.92 | 0.80 | 0.80 | 0.46 |
| loo:horizon_10y | 0.00 | 0.00 | 0.93 | 0.78 | 0.85 | 0.00 | 0.00 | 0.06 | 0.47 | 0.51 | 0.91 | 0.88 | 0.94 | 0.77 | 0.77 | 0.07 |
| quiet_all | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:capacity_shortfall | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:surge_headroom | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:inventory_timing | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:api_lead_time | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:component_lead_time | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:release_queue | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:sterility_delay | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:deviation_rejection | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:demand_variance | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:demand_covariance | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:common_cause | 0.98 | 1.00 | 1.00 | 1.00 | 1.00 | 0.97 | 0.97 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.75 | 0.75 | 1.00 |
| addin:supplier_concentration | 0.96 | 0.99 | 0.99 | 0.99 | 0.99 | 0.95 | 0.95 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.87 | 0.87 | 0.97 |
| addin:site_failures | 0.89 | 1.00 | 1.00 | 1.00 | 1.00 | 0.93 | 0.93 | 1.00 | 0.99 | 0.99 | 1.00 | 1.00 | 1.00 | 0.72 | 0.72 | 1.00 |
| addin:contract_insufficiency | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:regulatory_unavailability | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| addin:commissioning_delay | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| bounds:ss365 | 0.00 | 0.00 | 0.68 | 0.24 | 0.56 | 0.00 | 0.00 | 0.19 | 0.28 | 0.28 | 0.74 | 0.01 | 0.32 | 0.60 | 0.60 | 0.02 |
| bounds:ss365+base_stock | 0.00 | 0.00 | 1.00 | 0.98 | 1.00 | 1.00 | 1.00 | 0.62 | 0.99 | 0.99 | 1.00 | 0.99 | 1.00 | 1.00 | 1.00 | 0.99 |

**Shortage days per year by configuration**

| configuration | sodium S0 | sodium S1 | sodium S2 | sodium S3 | sodium S4 | sodium S5 | sodium S6 | sodium S7 | norepinephrine S0 | norepinephrine S1 | norepinephrine S2 | norepinephrine S3 | norepinephrine S4 | norepinephrine S5 | norepinephrine S6 | norepinephrine S7 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 268.683 | 265.582 | 14.184 | 22.337 | 17.794 | 68.029 | 68.029 | 129.072 | 25.545 | 23.203 | 15.800 | 18.751 | 15.668 | 13.294 | 13.294 | 64.549 |
| loo:capacity_shortfall | 34.357 | 33.013 | 3.004 | 20.127 | 16.854 | 14.088 | 14.088 | 45.206 | 24.191 | 22.387 | 13.322 | 18.775 | 15.396 | 11.890 | 11.890 | 64.579 |
| loo:surge_headroom | 268.607 | 265.254 | 13.736 | 21.553 | 16.708 | 67.947 | 67.947 | 127.944 | 22.405 | 20.253 | 14.428 | 18.625 | 14.984 | 12.204 | 12.204 | 62.149 |
| loo:inventory_timing | 247.204 | 175.680 | 3.088 | 2.922 | 0.570 | 67.791 | 67.791 | 93.069 | 3.062 | 1.900 | 3.028 | 2.500 | 0.254 | 7.273 | 7.273 | 16.082 |
| loo:api_lead_time | 268.963 | 265.476 | 15.034 | 24.863 | 18.198 | 182.251 | 182.251 | 130.870 | 24.375 | 21.505 | 16.382 | 21.363 | 15.840 | 54.433 | 54.433 | 63.889 |
| loo:component_lead_time | 268.875 | 265.364 | 14.758 | 24.077 | 18.184 | 182.273 | 182.273 | 129.924 | 25.772 | 23.097 | 16.308 | 20.553 | 15.852 | 54.189 | 54.189 | 65.293 |
| loo:release_queue | 265.884 | 262.292 | 13.786 | 20.643 | 15.238 | 68.369 | 68.369 | 127.325 | 24.089 | 21.605 | 15.192 | 17.888 | 13.512 | 12.612 | 12.612 | 59.086 |
| loo:sterility_delay | 254.071 | 251.000 | 12.468 | 16.682 | 10.233 | 68.761 | 68.761 | 122.143 | 21.163 | 18.843 | 12.320 | 14.668 | 8.947 | 11.040 | 11.040 | 47.140 |
| loo:deviation_rejection | 267.641 | 264.392 | 14.138 | 23.185 | 16.592 | 68.461 | 68.461 | 127.695 | 23.057 | 21.553 | 14.952 | 19.649 | 14.704 | 11.380 | 11.380 | 60.318 |
| loo:demand_variance | 268.067 | 263.496 | 14.360 | 11.664 | 16.532 | 67.011 | 67.011 | 127.317 | 24.251 | 24.075 | 14.400 | 9.251 | 11.802 | 9.867 | 9.867 | 54.838 |
| loo:demand_covariance | 268.713 | 265.260 | 13.484 | 21.563 | 17.074 | 67.987 | 67.987 | 127.872 | 23.433 | 21.713 | 15.108 | 18.561 | 15.376 | 12.680 | 12.680 | 63.335 |
| loo:common_cause | 266.510 | 262.484 | 11.524 | 20.385 | 16.708 | 67.669 | 67.669 | 126.285 | 15.228 | 14.006 | 12.334 | 18.423 | 14.916 | 11.012 | 11.012 | 54.898 |
| loo:supplier_concentration | 268.159 | 264.864 | 13.336 | 20.679 | 16.154 | 67.397 | 67.397 | 127.521 | 20.841 | 18.649 | 14.436 | 16.944 | 14.076 | 10.905 | 10.905 | 52.805 |
| loo:site_failures | 266.725 | 263.098 | 11.832 | 18.657 | 15.678 | 67.709 | 67.709 | 125.753 | 16.522 | 14.152 | 12.408 | 16.150 | 14.386 | 10.675 | 10.675 | 55.896 |
| loo:contract_insufficiency | 268.683 | 265.582 | 14.184 | 11.402 | 17.794 | 68.029 | 68.029 | 129.072 | 25.545 | 23.203 | 15.800 | 6.013 | 15.668 | 13.294 | 13.294 | 64.549 |
| loo:regulatory_unavailability | 268.683 | 265.582 | 14.184 | 22.337 | 17.794 | 68.029 | 68.029 | 7.041 | 25.545 | 23.203 | 15.800 | 18.751 | 15.668 | 13.294 | 13.294 | 6.615 |
| loo:commissioning_delay | 268.683 | 265.582 | 5.073 | 22.337 | 1.498 | 0.678 | 0.678 | 129.072 | 25.545 | 23.203 | 5.883 | 18.751 | 2.008 | 1.696 | 1.696 | 64.549 |
| loo:fixed_quality_cost | 268.683 | 265.582 | 14.184 | 22.337 | 17.794 | 68.029 | 68.029 | 129.072 | 25.545 | 23.203 | 15.800 | 18.751 | 15.668 | 13.294 | 13.294 | 64.549 |
| loo:replicated_validation_cost | 268.683 | 265.582 | 14.184 | 22.337 | 17.794 | 68.029 | 68.029 | 129.072 | 25.545 | 23.203 | 15.800 | 18.751 | 15.668 | 13.294 | 13.294 | 64.549 |
| loo:capital_cost | 268.683 | 265.582 | 14.184 | 22.337 | 17.794 | 68.029 | 68.029 | 129.072 | 25.545 | 23.203 | 15.800 | 18.751 | 15.668 | 13.294 | 13.294 | 64.549 |
| loo:lost_sales_window | 264.470 | 264.770 | 24.273 | 24.483 | 21.889 | 71.970 | 71.970 | 133.994 | 39.255 | 34.035 | 26.790 | 21.217 | 17.194 | 23.335 | 23.335 | 95.423 |
| loo:horizon_10y | 269.013 | 267.496 | 10.400 | 24.265 | 10.515 | 34.318 | 34.318 | 152.590 | 26.560 | 24.478 | 10.408 | 20.503 | 9.272 | 7.735 | 7.735 | 66.442 |
| quiet_all | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| addin:capacity_shortfall | 218.870 | 121.413 | 0.000 | 0.000 | 0.000 | 131.066 | 131.066 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| addin:surge_headroom | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| addin:inventory_timing | 6.381 | 2.830 | 0.072 | 0.696 | 0.272 | 2.194 | 2.194 | 0.238 | 2.484 | 2.532 | 0.060 | 0.132 | 0.282 | 6.819 | 6.819 | 0.890 |
| addin:api_lead_time | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| addin:component_lead_time | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| addin:release_queue | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| addin:sterility_delay | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| addin:deviation_rejection | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| addin:demand_variance | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| addin:demand_covariance | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| addin:common_cause | 0.800 | 0.000 | 0.000 | 0.000 | 0.000 | 1.050 | 1.050 | 0.000 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 | 5.631 | 5.631 | 0.000 |
| addin:supplier_concentration | 1.412 | 0.356 | 0.340 | 0.452 | 0.276 | 0.952 | 0.952 | 0.508 | 0.506 | 0.460 | 0.504 | 0.586 | 0.220 | 2.732 | 2.732 | 0.974 |
| addin:site_failures | 1.982 | 0.000 | 0.000 | 0.000 | 0.000 | 1.520 | 1.520 | 0.000 | 0.280 | 0.230 | 0.000 | 0.000 | 0.000 | 5.213 | 5.213 | 0.000 |
| addin:contract_insufficiency | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| addin:regulatory_unavailability | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| addin:commissioning_delay | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| bounds:ss365 | 269.469 | 269.469 | 23.599 | 42.476 | 33.405 | 67.617 | 67.617 | 133.402 | 44.268 | 44.268 | 22.943 | 63.827 | 30.936 | 25.079 | 25.079 | 86.530 |
| bounds:ss365+base_stock | 120.234 | 120.234 | 0.000 | 0.714 | 0.000 | 0.140 | 0.140 | 30.734 | 0.254 | 0.254 | 0.000 | 0.288 | 0.000 | 0.000 | 0.000 | 0.230 |

**Capacity utilization (served / saleable capacity over the measured horizon)**

| configuration | sodium S0 | sodium S1 | sodium S2 | sodium S3 | sodium S4 | sodium S5 | sodium S6 | sodium S7 | norepinephrine S0 | norepinephrine S1 | norepinephrine S2 | norepinephrine S3 | norepinephrine S4 | norepinephrine S5 | norepinephrine S6 | norepinephrine S7 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 0.938 | 0.947 | 0.714 | 1.044 | 0.271 | 0.205 | 0.205 | 1.127 | 0.800 | 0.801 | 0.707 | 0.652 | 0.257 | 0.203 | 0.203 | 0.778 |
| quiet_all | 0.777 | 0.777 | 0.429 | 0.627 | 0.163 | 0.131 | 0.131 | 0.777 | 0.777 | 0.777 | 0.680 | 0.627 | 0.247 | 0.196 | 0.196 | 0.777 |

**Attribution, sodium_bicarbonate_8_4_50ml, S0** (base fill 0.720, P(meet) 0.00; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| capacity_shortfall | capacity | mechanism | 0.253 | 0.206 | 0.42 | 1.00 | -234.3 | 860238 |
| common_cause | dependence | mechanism | 0.023 | 0.001 | 0.00 | 0.02 | -2.2 | 78494 |
| site_failures | capacity | mechanism | 0.019 | 0.003 | 0.00 | 0.11 | -2.0 | 62774 |
| horizon_10y | structure | structure | -0.017 | - | 0.00 | - | 0.3 | 16696 |
| deviation_rejection | quality | mechanism | 0.007 | 0.000 | 0.00 | 0.00 | -1.0 | -3251 |
| surge_headroom | demand | mechanism | 0.006 | 0.000 | 0.00 | 0.00 | -0.1 | 93 |
| lost_sales_window | structure | structure | -0.006 | - | 0.00 | - | -4.2 | -733 |
| supplier_concentration | supply | mechanism | 0.005 | 0.002 | 0.00 | 0.04 | -0.5 | 16075 |
| demand_covariance | demand | mechanism | 0.004 | 0.000 | 0.00 | 0.00 | 0.0 | 46 |
| api_lead_time | supply | mechanism | -0.002 | 0.000 | 0.00 | 0.00 | 0.3 | -6821 |
| component_lead_time | supply | mechanism | -0.001 | 0.000 | 0.00 | 0.00 | 0.2 | -3918 |
| inventory_timing | inventory | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | -21.5 | 21781 |
| demand_variance | demand | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.6 | 226 |
| sterility_delay | release | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -14.6 | 4397 |
| release_queue | release | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -2.8 | 929 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| commissioning_delay | time | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -3119412 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -650982 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -6703202 |

**Attribution, sodium_bicarbonate_8_4_50ml, S1** (base fill 0.728, P(meet) 0.00; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| capacity_shortfall | capacity | mechanism | 0.254 | 0.119 | 0.50 | 1.00 | -232.6 | 874785 |
| inventory_timing | inventory | mechanism | 0.069 | 0.000 | 0.00 | 0.00 | -89.9 | 228465 |
| common_cause | dependence | mechanism | 0.025 | 0.000 | 0.00 | 0.00 | -3.1 | 76586 |
| horizon_10y | structure | structure | -0.020 | - | 0.00 | - | 1.9 | 93426 |
| site_failures | capacity | mechanism | 0.019 | 0.000 | 0.00 | 0.00 | -2.5 | 58145 |
| deviation_rejection | quality | mechanism | 0.007 | 0.000 | 0.00 | 0.00 | -1.2 | -3385 |
| surge_headroom | demand | mechanism | 0.007 | 0.000 | 0.00 | 0.00 | -0.3 | -1905 |
| supplier_concentration | supply | mechanism | 0.006 | 0.001 | 0.00 | 0.01 | -0.7 | 16475 |
| demand_covariance | demand | mechanism | 0.005 | 0.000 | 0.00 | 0.00 | -0.3 | -122 |
| lost_sales_window | structure | structure | -0.003 | - | 0.00 | - | -0.8 | -1042 |
| sterility_delay | release | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | -14.6 | 3856 |
| component_lead_time | supply | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | -0.2 | 3243 |
| release_queue | release | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | -3.3 | 1484 |
| demand_variance | demand | mechanism | -0.000 | 0.000 | 0.00 | 0.00 | -2.1 | -2504 |
| api_lead_time | supply | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.1 | 629 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| commissioning_delay | time | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -3119412 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -650982 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -6703202 |

**Attribution, sodium_bicarbonate_8_4_50ml, S2** (base fill 0.993, P(meet) 0.89; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| capacity_shortfall | capacity | mechanism | 0.006 | 0.000 | 0.10 | 0.00 | -11.2 | 106718 |
| inventory_timing | inventory | mechanism | 0.005 | 0.000 | 0.04 | 0.00 | -11.1 | 227261 |
| commissioning_delay | time | mechanism | 0.005 | 0.000 | 0.06 | 0.00 | -9.1 | 61456 |
| lost_sales_window | structure | structure | 0.004 | - | 0.04 | - | 10.1 | 39775 |
| horizon_10y | structure | structure | 0.003 | - | 0.04 | - | -3.8 | 175791 |
| common_cause | dependence | mechanism | 0.002 | 0.000 | 0.04 | 0.00 | -2.7 | 20712 |
| sterility_delay | release | mechanism | 0.002 | 0.000 | 0.01 | 0.00 | -1.7 | 19331 |
| site_failures | capacity | mechanism | 0.001 | 0.000 | 0.04 | 0.00 | -2.4 | 17020 |
| api_lead_time | supply | mechanism | -0.001 | 0.000 | -0.04 | 0.00 | 0.9 | -4369 |
| supplier_concentration | supply | mechanism | 0.001 | 0.001 | 0.01 | 0.01 | -0.8 | 3608 |
| component_lead_time | supply | mechanism | -0.001 | 0.000 | -0.03 | 0.00 | 0.6 | -3145 |
| surge_headroom | demand | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | -0.4 | -23096 |
| release_queue | release | mechanism | 0.000 | 0.000 | -0.01 | 0.00 | -0.4 | 7829 |
| demand_covariance | demand | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.7 | -13216 |
| deviation_rejection | quality | mechanism | 0.000 | 0.000 | -0.03 | 0.00 | -0.0 | -29420 |
| demand_variance | demand | mechanism | -0.000 | 0.000 | -0.04 | 0.00 | 0.2 | -15967 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -6622592 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -1952945 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -12625043 |

**Attribution, sodium_bicarbonate_8_4_50ml, S3** (base fill 0.993, P(meet) 0.86; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| lost_sales_window | structure | structure | 0.005 | - | 0.11 | - | 2.1 | 29620 |
| api_lead_time | supply | mechanism | -0.004 | 0.000 | -0.10 | 0.00 | 2.5 | -13835 |
| inventory_timing | inventory | mechanism | 0.004 | 0.000 | 0.09 | 0.00 | -19.4 | 63240 |
| contract_insufficiency | contract | mechanism | 0.003 | 0.000 | 0.13 | 0.00 | -10.9 | 24627934 |
| component_lead_time | supply | mechanism | -0.002 | 0.000 | -0.12 | 0.00 | 1.7 | -7901 |
| supplier_concentration | supply | mechanism | 0.002 | 0.001 | 0.04 | 0.01 | -1.7 | 6567 |
| site_failures | capacity | mechanism | 0.002 | 0.000 | 0.06 | 0.00 | -3.7 | 6609 |
| sterility_delay | release | mechanism | 0.001 | 0.000 | 0.04 | 0.00 | -5.7 | 6519 |
| deviation_rejection | quality | mechanism | -0.001 | 0.000 | -0.05 | 0.00 | 0.8 | -37855 |
| horizon_10y | structure | structure | -0.001 | - | -0.08 | - | 1.9 | 141958 |
| demand_variance | demand | mechanism | 0.001 | 0.000 | 0.01 | 0.00 | -10.7 | -2546 |
| demand_covariance | demand | mechanism | 0.000 | 0.000 | 0.03 | 0.00 | -0.8 | -17895 |
| capacity_shortfall | capacity | mechanism | 0.000 | 0.000 | 0.02 | 0.00 | -2.2 | 8707 |
| release_queue | release | mechanism | -0.000 | 0.000 | 0.03 | 0.00 | -1.7 | -1418 |
| surge_headroom | demand | mechanism | 0.000 | 0.000 | 0.02 | 0.00 | -0.8 | -31579 |
| common_cause | dependence | mechanism | 0.000 | 0.000 | 0.02 | 0.00 | -2.0 | 2513 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| commissioning_delay | time | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -10213745 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -1952945 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -17525182 |

**Attribution, sodium_bicarbonate_8_4_50ml, S4** (base fill 0.993, P(meet) 0.79; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| commissioning_delay | time | mechanism | 0.007 | 0.000 | 0.21 | 0.00 | -16.3 | 12759 |
| inventory_timing | inventory | mechanism | 0.007 | 0.000 | 0.19 | 0.00 | -17.2 | 219384 |
| horizon_10y | structure | structure | 0.004 | - | 0.06 | - | -7.3 | 143300 |
| lost_sales_window | structure | structure | 0.003 | - | 0.08 | - | 4.1 | 20945 |
| site_failures | capacity | mechanism | 0.003 | 0.000 | 0.12 | 0.00 | -2.1 | 15410 |
| supplier_concentration | supply | mechanism | 0.002 | 0.001 | 0.07 | 0.01 | -1.6 | 7726 |
| sterility_delay | release | mechanism | 0.002 | 0.000 | 0.08 | 0.00 | -7.6 | 24676 |
| component_lead_time | supply | mechanism | -0.001 | 0.000 | -0.02 | 0.00 | 0.4 | -4869 |
| api_lead_time | supply | mechanism | -0.001 | 0.000 | 0.00 | 0.00 | 0.4 | -4983 |
| surge_headroom | demand | mechanism | 0.001 | 0.000 | 0.02 | 0.00 | -1.1 | -26155 |
| common_cause | dependence | mechanism | 0.001 | 0.000 | 0.02 | 0.00 | -1.1 | 2854 |
| capacity_shortfall | capacity | mechanism | 0.001 | 0.000 | 0.02 | 0.00 | -0.9 | 1939 |
| demand_variance | demand | mechanism | -0.001 | 0.000 | 0.00 | 0.00 | -1.3 | -7989 |
| demand_covariance | demand | mechanism | 0.001 | 0.000 | 0.02 | 0.00 | -0.7 | -13736 |
| release_queue | release | mechanism | 0.000 | 0.000 | 0.05 | 0.00 | -2.6 | 5263 |
| deviation_rejection | quality | mechanism | 0.000 | 0.000 | 0.05 | 0.00 | -1.2 | -32879 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -13737128 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -1952945 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -22561226 |

**Attribution, sodium_bicarbonate_8_4_50ml, S5** (base fill 0.932, P(meet) 0.00; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| capacity_shortfall | capacity | mechanism | 0.060 | 0.122 | 0.80 | 1.00 | -53.9 | 208132 |
| component_lead_time | supply | mechanism | -0.121 | 0.000 | 0.00 | 0.00 | 114.2 | -410804 |
| api_lead_time | supply | mechanism | -0.119 | 0.000 | 0.00 | 0.00 | 114.2 | -405643 |
| commissioning_delay | time | mechanism | 0.067 | 0.000 | 0.99 | 0.00 | -67.4 | 200470 |
| horizon_10y | structure | structure | 0.033 | - | 0.00 | - | -33.7 | 203915 |
| lost_sales_window | structure | structure | 0.004 | - | 0.00 | - | 3.9 | 38888 |
| common_cause | dependence | mechanism | 0.003 | 0.001 | 0.00 | 0.03 | -0.4 | 23741 |
| site_failures | capacity | mechanism | 0.003 | 0.002 | 0.00 | 0.07 | -0.3 | 20978 |
| supplier_concentration | supply | mechanism | 0.002 | 0.002 | 0.00 | 0.05 | -0.6 | 7368 |
| deviation_rejection | quality | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | 0.4 | -28604 |
| sterility_delay | release | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | 0.7 | 15876 |
| surge_headroom | demand | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | -0.1 | -22305 |
| demand_covariance | demand | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | -0.0 | -14542 |
| release_queue | release | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.3 | 4318 |
| inventory_timing | inventory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.2 | 101513 |
| demand_variance | demand | mechanism | -0.000 | 0.000 | 0.00 | 0.00 | -1.0 | -9273 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -20561762 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -8137270 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -32037962 |

**Attribution, sodium_bicarbonate_8_4_50ml, S6** (base fill 0.932, P(meet) 0.00; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| capacity_shortfall | capacity | mechanism | 0.060 | 0.122 | 0.80 | 1.00 | -53.9 | 208132 |
| component_lead_time | supply | mechanism | -0.121 | 0.000 | 0.00 | 0.00 | 114.2 | -410804 |
| api_lead_time | supply | mechanism | -0.119 | 0.000 | 0.00 | 0.00 | 114.2 | -405643 |
| commissioning_delay | time | mechanism | 0.067 | 0.000 | 0.99 | 0.00 | -67.4 | 200470 |
| horizon_10y | structure | structure | 0.033 | - | 0.00 | - | -33.7 | 203915 |
| lost_sales_window | structure | structure | 0.004 | - | 0.00 | - | 3.9 | 38888 |
| common_cause | dependence | mechanism | 0.003 | 0.001 | 0.00 | 0.03 | -0.4 | 23741 |
| site_failures | capacity | mechanism | 0.003 | 0.002 | 0.00 | 0.07 | -0.3 | 20978 |
| supplier_concentration | supply | mechanism | 0.002 | 0.002 | 0.00 | 0.05 | -0.6 | 7368 |
| deviation_rejection | quality | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | 0.4 | -28604 |
| sterility_delay | release | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | 0.7 | 15876 |
| surge_headroom | demand | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | -0.1 | -22305 |
| demand_covariance | demand | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | -0.0 | -14542 |
| release_queue | release | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.3 | 4318 |
| inventory_timing | inventory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.2 | 101513 |
| demand_variance | demand | mechanism | -0.000 | 0.000 | 0.00 | 0.00 | -1.0 | -9273 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -22030459 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -9764724 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -32037962 |

**Attribution, sodium_bicarbonate_8_4_50ml, S7** (base fill 0.866, P(meet) 0.19; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| regulatory_unavailability | regulatory | mechanism | 0.131 | 0.000 | 0.76 | 0.00 | -122.0 | 519326 |
| capacity_shortfall | capacity | mechanism | 0.106 | 0.000 | 0.26 | 0.00 | -83.9 | 471928 |
| horizon_10y | structure | structure | -0.033 | - | -0.13 | - | 23.5 | -66310 |
| inventory_timing | inventory | mechanism | 0.025 | 0.000 | 0.10 | 0.00 | -36.0 | 158653 |
| site_failures | capacity | mechanism | 0.013 | 0.000 | 0.02 | 0.00 | -3.3 | 47898 |
| common_cause | dependence | mechanism | 0.011 | 0.000 | 0.00 | 0.00 | -2.8 | 42169 |
| supplier_concentration | supply | mechanism | 0.007 | 0.001 | -0.01 | 0.01 | -1.6 | 21655 |
| surge_headroom | demand | mechanism | 0.004 | 0.000 | 0.01 | 0.00 | -1.1 | -9674 |
| deviation_rejection | quality | mechanism | 0.004 | 0.000 | 0.01 | 0.00 | -1.4 | -19661 |
| sterility_delay | release | mechanism | 0.003 | 0.000 | 0.02 | 0.00 | -6.9 | 82520 |
| lost_sales_window | structure | structure | 0.003 | - | 0.03 | - | 4.9 | 9723 |
| demand_covariance | demand | mechanism | 0.003 | 0.000 | -0.01 | 0.00 | -1.2 | -7312 |
| api_lead_time | supply | mechanism | -0.002 | 0.000 | -0.02 | 0.00 | 1.8 | -16754 |
| component_lead_time | supply | mechanism | -0.002 | 0.000 | -0.02 | 0.00 | 0.9 | -11856 |
| release_queue | release | mechanism | 0.001 | 0.000 | -0.02 | 0.00 | -1.7 | 21413 |
| demand_variance | demand | mechanism | 0.001 | 0.000 | -0.01 | 0.00 | -1.8 | -49718 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| commissioning_delay | time | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -7649265 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -1301963 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -13213017 |

**Attribution, norepinephrine_1mgml_4ml, S0** (base fill 0.983, P(meet) 0.56; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| inventory_timing | inventory | mechanism | 0.012 | 0.000 | 0.34 | 0.00 | -22.5 | 104294 |
| common_cause | dependence | mechanism | 0.007 | 0.000 | 0.19 | 0.00 | -10.3 | 23408 |
| site_failures | capacity | mechanism | 0.007 | 0.001 | 0.24 | 0.01 | -9.0 | 21878 |
| lost_sales_window | structure | structure | 0.006 | - | 0.18 | - | 13.7 | 8567 |
| supplier_concentration | supply | mechanism | 0.005 | 0.001 | 0.08 | 0.01 | -4.7 | 13863 |
| demand_variance | demand | mechanism | -0.003 | 0.000 | -0.07 | 0.00 | -1.3 | -15083 |
| sterility_delay | release | mechanism | 0.003 | 0.000 | 0.10 | 0.00 | -4.4 | 11024 |
| surge_headroom | demand | mechanism | 0.002 | 0.000 | 0.06 | 0.00 | -3.1 | -13816 |
| demand_covariance | demand | mechanism | 0.002 | 0.000 | 0.07 | 0.00 | -2.1 | -7644 |
| deviation_rejection | quality | mechanism | 0.002 | 0.000 | 0.04 | 0.00 | -2.5 | -17961 |
| capacity_shortfall | capacity | mechanism | 0.001 | 0.000 | 0.03 | 0.00 | -1.4 | 3744 |
| api_lead_time | supply | mechanism | 0.001 | 0.000 | 0.02 | 0.00 | -1.2 | 1276 |
| release_queue | release | mechanism | 0.001 | 0.000 | 0.07 | 0.00 | -1.5 | 4401 |
| component_lead_time | supply | mechanism | -0.000 | 0.000 | -0.03 | 0.00 | 0.2 | 127 |
| horizon_10y | structure | structure | 0.000 | - | -0.09 | - | 1.0 | 87661 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| commissioning_delay | time | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -3119412 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -650982 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -6703202 |

**Attribution, norepinephrine_1mgml_4ml, S1** (base fill 0.985, P(meet) 0.65; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| inventory_timing | inventory | mechanism | 0.012 | 0.000 | 0.29 | 0.00 | -21.3 | 132252 |
| site_failures | capacity | mechanism | 0.007 | 0.000 | 0.20 | 0.01 | -9.1 | 19914 |
| lost_sales_window | structure | structure | 0.006 | - | 0.13 | - | 10.8 | 8910 |
| common_cause | dependence | mechanism | 0.006 | 0.000 | 0.11 | 0.00 | -9.2 | 20942 |
| demand_variance | demand | mechanism | -0.006 | 0.000 | -0.18 | 0.00 | 0.9 | -26259 |
| supplier_concentration | supply | mechanism | 0.005 | 0.001 | 0.04 | 0.01 | -4.6 | 13819 |
| sterility_delay | release | mechanism | 0.003 | 0.000 | 0.03 | 0.00 | -4.4 | 13977 |
| surge_headroom | demand | mechanism | 0.002 | 0.000 | 0.04 | 0.00 | -3.0 | -16472 |
| release_queue | release | mechanism | 0.002 | 0.000 | 0.01 | 0.00 | -1.6 | 2661 |
| capacity_shortfall | capacity | mechanism | 0.001 | 0.000 | -0.01 | 0.00 | -0.8 | 2849 |
| api_lead_time | supply | mechanism | 0.001 | 0.000 | -0.04 | 0.00 | -1.7 | 1144 |
| deviation_rejection | quality | mechanism | 0.001 | 0.000 | -0.03 | 0.00 | -1.7 | -21063 |
| demand_covariance | demand | mechanism | 0.001 | 0.000 | -0.01 | 0.00 | -1.5 | -12059 |
| component_lead_time | supply | mechanism | 0.000 | 0.000 | -0.02 | 0.00 | -0.1 | 334 |
| horizon_10y | structure | structure | -0.000 | - | -0.14 | - | 1.3 | 95466 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| commissioning_delay | time | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -3119412 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -650982 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -6703202 |

**Attribution, norepinephrine_1mgml_4ml, S2** (base fill 0.993, P(meet) 0.84; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| inventory_timing | inventory | mechanism | 0.005 | 0.000 | 0.09 | 0.00 | -12.8 | 150083 |
| commissioning_delay | time | mechanism | 0.004 | 0.000 | 0.11 | 0.00 | -9.9 | 36301 |
| lost_sales_window | structure | structure | 0.004 | - | 0.11 | - | 11.0 | 30495 |
| horizon_10y | structure | structure | 0.003 | - | 0.07 | - | -5.4 | 114175 |
| sterility_delay | release | mechanism | 0.002 | 0.000 | 0.06 | 0.00 | -3.5 | 18691 |
| site_failures | capacity | mechanism | 0.002 | 0.000 | 0.08 | 0.00 | -3.4 | 9577 |
| common_cause | dependence | mechanism | 0.001 | 0.000 | 0.08 | 0.00 | -3.5 | 12869 |
| supplier_concentration | supply | mechanism | 0.001 | 0.001 | 0.04 | 0.01 | -1.4 | 3917 |
| capacity_shortfall | capacity | mechanism | 0.001 | 0.000 | 0.06 | 0.00 | -2.5 | 14664 |
| component_lead_time | supply | mechanism | -0.001 | 0.000 | -0.03 | 0.00 | 0.5 | -684 |
| api_lead_time | supply | mechanism | -0.001 | 0.000 | -0.03 | 0.00 | 0.6 | -2759 |
| demand_variance | demand | mechanism | -0.001 | 0.000 | 0.00 | 0.00 | -1.4 | -17732 |
| surge_headroom | demand | mechanism | 0.001 | 0.000 | 0.03 | 0.00 | -1.4 | -16904 |
| release_queue | release | mechanism | -0.000 | 0.000 | -0.01 | 0.00 | -0.6 | 2691 |
| demand_covariance | demand | mechanism | 0.000 | 0.000 | 0.01 | 0.00 | -0.7 | -11035 |
| deviation_rejection | quality | mechanism | -0.000 | 0.000 | 0.02 | 0.00 | -0.8 | -17701 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -4585325 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -1952945 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -9582734 |

**Attribution, norepinephrine_1mgml_4ml, S3** (base fill 0.993, P(meet) 0.86; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| lost_sales_window | structure | structure | 0.005 | - | 0.10 | - | 2.5 | 14286 |
| contract_insufficiency | contract | mechanism | 0.004 | 0.000 | 0.12 | 0.00 | -12.7 | 31842683 |
| inventory_timing | inventory | mechanism | 0.004 | 0.000 | 0.08 | 0.00 | -16.3 | 56395 |
| api_lead_time | supply | mechanism | -0.003 | 0.000 | -0.11 | 0.00 | 2.6 | -5341 |
| supplier_concentration | supply | mechanism | 0.002 | 0.002 | 0.03 | 0.01 | -1.8 | 5501 |
| component_lead_time | supply | mechanism | -0.002 | 0.000 | -0.05 | 0.00 | 1.8 | -5254 |
| site_failures | capacity | mechanism | 0.002 | 0.000 | 0.08 | 0.00 | -2.6 | 4517 |
| sterility_delay | release | mechanism | 0.002 | 0.000 | 0.04 | 0.00 | -4.1 | 7470 |
| demand_variance | demand | mechanism | 0.001 | 0.000 | 0.01 | 0.00 | -9.5 | -4403 |
| surge_headroom | demand | mechanism | 0.001 | 0.000 | 0.05 | 0.00 | -0.1 | -19054 |
| demand_covariance | demand | mechanism | 0.000 | 0.000 | 0.01 | 0.00 | -0.2 | -14778 |
| deviation_rejection | quality | mechanism | -0.000 | 0.000 | -0.01 | 0.00 | 0.9 | -25845 |
| release_queue | release | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.9 | 903 |
| common_cause | dependence | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.3 | 1701 |
| horizon_10y | structure | structure | -0.000 | - | 0.02 | - | 1.8 | 76750 |
| capacity_shortfall | capacity | mechanism | 0.000 | 0.000 | 0.02 | 0.00 | 0.0 | 650 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| commissioning_delay | time | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -7214389 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -1952945 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -13335932 |

**Attribution, norepinephrine_1mgml_4ml, S4** (base fill 0.993, P(meet) 0.86; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| inventory_timing | inventory | mechanism | 0.006 | 0.000 | 0.12 | 0.00 | -15.4 | 149040 |
| commissioning_delay | time | mechanism | 0.006 | 0.000 | 0.13 | 0.00 | -13.7 | 3812 |
| lost_sales_window | structure | structure | 0.005 | - | 0.06 | - | 1.5 | 18282 |
| sterility_delay | release | mechanism | 0.003 | 0.000 | 0.02 | 0.00 | -6.7 | 21931 |
| horizon_10y | structure | structure | 0.003 | - | 0.08 | - | -6.4 | 90420 |
| supplier_concentration | supply | mechanism | 0.002 | 0.001 | 0.05 | 0.01 | -1.6 | 4915 |
| site_failures | capacity | mechanism | 0.002 | 0.000 | 0.08 | 0.00 | -1.3 | 6547 |
| release_queue | release | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | -2.2 | 7225 |
| component_lead_time | supply | mechanism | -0.001 | 0.000 | -0.04 | 0.00 | 0.2 | -2862 |
| common_cause | dependence | mechanism | 0.001 | 0.000 | 0.01 | 0.00 | -0.8 | 900 |
| deviation_rejection | quality | mechanism | 0.001 | 0.000 | 0.02 | 0.00 | -1.0 | -23403 |
| api_lead_time | supply | mechanism | -0.000 | 0.000 | -0.03 | 0.00 | 0.2 | -2383 |
| capacity_shortfall | capacity | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.3 | -490 |
| demand_covariance | demand | mechanism | -0.000 | 0.000 | -0.01 | 0.00 | -0.3 | -12327 |
| demand_variance | demand | mechanism | 0.000 | 0.000 | -0.07 | 0.00 | -3.9 | -11624 |
| surge_headroom | demand | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.7 | -19672 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -9852152 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -1952945 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -17582842 |

**Attribution, norepinephrine_1mgml_4ml, S5** (base fill 0.990, P(meet) 0.72; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| api_lead_time | supply | mechanism | -0.036 | 0.000 | -0.49 | 0.00 | 41.1 | -550757 |
| component_lead_time | supply | mechanism | -0.036 | 0.000 | -0.50 | 0.00 | 40.9 | -548816 |
| commissioning_delay | time | mechanism | 0.009 | 0.000 | 0.27 | 0.00 | -11.6 | 247962 |
| site_failures | capacity | mechanism | 0.003 | 0.009 | 0.09 | 0.28 | -2.6 | 29374 |
| common_cause | dependence | mechanism | 0.002 | 0.007 | 0.06 | 0.25 | -2.3 | 5774 |
| supplier_concentration | supply | mechanism | 0.004 | 0.005 | 0.11 | 0.13 | -2.4 | 18709 |
| horizon_10y | structure | structure | 0.005 | - | 0.05 | - | -5.6 | 199807 |
| lost_sales_window | structure | structure | 0.003 | - | 0.08 | - | 10.0 | 28309 |
| sterility_delay | release | mechanism | 0.002 | 0.000 | 0.01 | 0.00 | -2.3 | 43760 |
| deviation_rejection | quality | mechanism | 0.001 | 0.000 | 0.03 | 0.00 | -1.9 | -16848 |
| capacity_shortfall | capacity | mechanism | 0.001 | 0.000 | 0.03 | 0.00 | -1.4 | 4875 |
| surge_headroom | demand | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -1.1 | -22372 |
| inventory_timing | inventory | mechanism | 0.000 | 0.000 | 0.01 | 0.00 | -6.0 | -11871 |
| release_queue | release | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.7 | 18883 |
| demand_covariance | demand | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.6 | -12529 |
| demand_variance | demand | mechanism | -0.000 | 0.000 | 0.00 | 0.00 | -3.4 | -18570 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -15140419 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -8137270 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -25386348 |

**Attribution, norepinephrine_1mgml_4ml, S6** (base fill 0.990, P(meet) 0.72; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| api_lead_time | supply | mechanism | -0.036 | 0.000 | -0.49 | 0.00 | 41.1 | -550757 |
| component_lead_time | supply | mechanism | -0.036 | 0.000 | -0.50 | 0.00 | 40.9 | -548816 |
| commissioning_delay | time | mechanism | 0.009 | 0.000 | 0.27 | 0.00 | -11.6 | 247962 |
| site_failures | capacity | mechanism | 0.003 | 0.009 | 0.09 | 0.28 | -2.6 | 29374 |
| common_cause | dependence | mechanism | 0.002 | 0.007 | 0.06 | 0.25 | -2.3 | 5774 |
| supplier_concentration | supply | mechanism | 0.004 | 0.005 | 0.11 | 0.13 | -2.4 | 18709 |
| horizon_10y | structure | structure | 0.005 | - | 0.05 | - | -5.6 | 199807 |
| lost_sales_window | structure | structure | 0.003 | - | 0.08 | - | 10.0 | 28309 |
| sterility_delay | release | mechanism | 0.002 | 0.000 | 0.01 | 0.00 | -2.3 | 43760 |
| deviation_rejection | quality | mechanism | 0.001 | 0.000 | 0.03 | 0.00 | -1.9 | -16848 |
| capacity_shortfall | capacity | mechanism | 0.001 | 0.000 | 0.03 | 0.00 | -1.4 | 4875 |
| surge_headroom | demand | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -1.1 | -22372 |
| inventory_timing | inventory | mechanism | 0.000 | 0.000 | 0.01 | 0.00 | -6.0 | -11871 |
| release_queue | release | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.7 | 18883 |
| demand_covariance | demand | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | -0.6 | -12529 |
| demand_variance | demand | mechanism | -0.000 | 0.000 | 0.00 | 0.00 | -3.4 | -18570 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| regulatory_unavailability | regulatory | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -16221878 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -9764724 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -25386348 |

**Attribution, norepinephrine_1mgml_4ml, S7** (base fill 0.957, P(meet) 0.21; quiet fill 1.000, P(meet) 1.00)

| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |
|---|---|---|---|---|---|---|---|---|
| regulatory_unavailability | regulatory | mechanism | 0.040 | 0.000 | 0.73 | 0.00 | -57.9 | 557476 |
| inventory_timing | inventory | mechanism | 0.019 | 0.000 | 0.26 | 0.00 | -48.5 | 111672 |
| lost_sales_window | structure | structure | 0.016 | - | 0.25 | - | 30.9 | 31590 |
| supplier_concentration | supply | mechanism | 0.014 | 0.002 | 0.13 | 0.03 | -11.7 | 39390 |
| site_failures | capacity | mechanism | 0.012 | 0.000 | 0.10 | 0.00 | -8.7 | 34564 |
| common_cause | dependence | mechanism | 0.010 | 0.000 | 0.07 | 0.00 | -9.7 | 27964 |
| sterility_delay | release | mechanism | 0.008 | 0.000 | 0.10 | 0.00 | -17.4 | 58823 |
| api_lead_time | supply | mechanism | -0.003 | 0.000 | -0.01 | 0.00 | -0.7 | -10133 |
| deviation_rejection | quality | mechanism | 0.003 | 0.000 | 0.00 | 0.00 | -4.2 | -16878 |
| component_lead_time | supply | mechanism | -0.002 | 0.000 | -0.01 | 0.00 | 0.7 | -8924 |
| release_queue | release | mechanism | 0.002 | 0.000 | 0.04 | 0.00 | -5.5 | 18307 |
| demand_variance | demand | mechanism | -0.002 | 0.000 | 0.00 | 0.00 | -9.7 | -25144 |
| surge_headroom | demand | mechanism | 0.002 | 0.000 | 0.02 | 0.00 | -2.4 | -12028 |
| horizon_10y | structure | structure | 0.001 | - | -0.14 | - | 1.9 | 104767 |
| demand_covariance | demand | mechanism | 0.001 | 0.000 | 0.00 | 0.00 | -1.2 | -8257 |
| capacity_shortfall | capacity | mechanism | 0.000 | 0.000 | 0.01 | 0.00 | 0.0 | 5398 |
| contract_insufficiency | contract | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| commissioning_delay | time | mechanism | 0.000 | 0.000 | 0.00 | 0.00 | 0.0 | 0 |
| fixed_quality_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -6664533 |
| replicated_validation_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -1301963 |
| capital_cost | cost | cost | 0.000 | - | 0.00 | - | 0.0 | -11883422 |

**Interaction study `abl_20260902_phaseA_pairs`: mean fill rate**

**Mean fill rate, factor combinations**

| configuration | sodium S0 | sodium S1 | sodium S2 | sodium S3 | sodium S4 | sodium S5 | sodium S6 | sodium S7 | norepinephrine S0 | norepinephrine S1 | norepinephrine S2 | norepinephrine S3 | norepinephrine S4 | norepinephrine S5 | norepinephrine S6 | norepinephrine S7 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 0.720 | 0.728 | 0.993 | 0.993 | 0.993 | 0.932 | 0.932 | 0.866 | 0.983 | 0.985 | 0.993 | 0.993 | 0.993 | 0.990 | 0.990 | 0.957 |
| pair:capacity_shortfall+inventory_timing | 0.984 | 0.999 | 1.000 | 0.999 | 0.999 | 0.994 | 0.994 | 0.991 | 0.995 | 0.997 | 0.998 | 0.997 | 0.999 | 0.992 | 0.992 | 0.977 |
| pair:capacity_shortfall+commissioning_delay | 0.973 | 0.982 | 0.999 | 0.993 | 1.000 | 0.999 | 0.999 | 0.972 | 0.985 | 0.986 | 0.998 | 0.993 | 0.999 | 0.999 | 0.999 | 0.958 |
| pair:inventory_timing+commissioning_delay | 0.721 | 0.797 | 0.999 | 0.997 | 1.000 | 1.000 | 1.000 | 0.891 | 0.995 | 0.997 | 0.999 | 0.997 | 1.000 | 0.999 | 0.999 | 0.976 |
| pair:capacity_shortfall+inventory_timing+commissioning_delay | 0.984 | 0.999 | 1.000 | 0.999 | 1.000 | 1.000 | 1.000 | 0.991 | 0.995 | 0.997 | 0.999 | 0.997 | 1.000 | 0.999 | 0.999 | 0.977 |

**P(fill >= 0.99), factor combinations**

| configuration | sodium S0 | sodium S1 | sodium S2 | sodium S3 | sodium S4 | sodium S5 | sodium S6 | sodium S7 | norepinephrine S0 | norepinephrine S1 | norepinephrine S2 | norepinephrine S3 | norepinephrine S4 | norepinephrine S5 | norepinephrine S6 | norepinephrine S7 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 0.00 | 0.00 | 0.89 | 0.86 | 0.79 | 0.00 | 0.00 | 0.19 | 0.56 | 0.65 | 0.84 | 0.86 | 0.86 | 0.72 | 0.72 | 0.21 |
| pair:capacity_shortfall+inventory_timing | 0.64 | 0.97 | 0.99 | 0.99 | 0.98 | 0.87 | 0.87 | 0.84 | 0.91 | 0.95 | 0.93 | 0.94 | 0.98 | 0.77 | 0.77 | 0.49 |
| pair:capacity_shortfall+commissioning_delay | 0.42 | 0.50 | 0.99 | 0.88 | 1.00 | 0.99 | 0.99 | 0.45 | 0.59 | 0.64 | 0.95 | 0.88 | 0.99 | 0.99 | 0.99 | 0.22 |
| pair:inventory_timing+commissioning_delay | 0.00 | 0.00 | 0.99 | 0.95 | 0.99 | 0.99 | 0.99 | 0.29 | 0.90 | 0.94 | 0.99 | 0.94 | 1.00 | 0.99 | 0.99 | 0.47 |
| pair:capacity_shortfall+inventory_timing+commissioning_delay | 0.64 | 0.97 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.84 | 0.91 | 0.95 | 0.99 | 0.94 | 1.00 | 0.99 | 0.99 | 0.49 |
