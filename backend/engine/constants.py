"""Shared engine constants."""

CLINICAL_FIREWALL = (
    "Population outreach prioritization only — diagnostic orders require "
    "clinician confirmation under DoH guidelines."
)

DATA_SOURCES_NOT_USED = [
    "Insurance claims",
    "Non-health records",
    "Unauthorized genomic reports",
]

WELL_CHILD_OVERDUE_DAYS = 30
IFHAS_OVERDUE_DAYS = 30
SPARSE_EHR_MONTHS = 6
HBA1C_TREND_THRESHOLD = 0.05
BP_TREND_THRESHOLD = 0.05
GROWTH_DRIFT_THRESHOLD = 5.0
