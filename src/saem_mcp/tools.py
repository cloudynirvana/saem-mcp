"""MCP Tool definitions for the SAEM Cancer PoC server."""

from mcp.types import Tool

TOOLS = [
    Tool(
        name="saem_run_simulation",
        description=(
            "Run the full SAEM 3-phase Flatten→Heat→Push protocol simulation "
            "for a specific cancer type. Returns cure rate, escape distance, "
            "drug protocol, phase timing, and resistance comparison."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cancer_type": {
                    "type": "string",
                    "description": "Cancer type to simulate. One of: TNBC, PDAC, NSCLC, GBM, Melanoma, CML, Ovarian, AML, mCRPC, HCC",
                    "enum": ["TNBC", "PDAC", "NSCLC", "GBM", "Melanoma", "CML", "Ovarian", "AML", "mCRPC", "HCC"],
                },
            },
            "required": ["cancer_type"],
        },
    ),
    Tool(
        name="saem_run_all",
        description=(
            "Run simulation across all 10 cancer types and return a summary "
            "table with cure rates, seriousness rankings, and protocols."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    Tool(
        name="saem_get_seriousness",
        description=(
            "Get the composite seriousness breakdown for a cancer type. "
            "Shows coherence deficit, basin curvature, immune suppression, "
            "stress load, stromal barrier, and composite score."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cancer_type": {
                    "type": "string",
                    "description": "Cancer type to analyze.",
                    "enum": ["TNBC", "PDAC", "NSCLC", "GBM", "Melanoma", "CML", "Ovarian", "AML", "mCRPC", "HCC"],
                },
            },
            "required": ["cancer_type"],
        },
    ),
    Tool(
        name="saem_query_drug",
        description=(
            "Query details about a specific drug in the SAEM intervention library. "
            "Returns mechanism of action, target metabolites, evidence level, "
            "and which cancers it's most effective against."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "drug_name": {
                    "type": "string",
                    "description": "Name or partial name of the drug to search for.",
                },
            },
            "required": ["drug_name"],
        },
    ),
    Tool(
        name="saem_list_drugs",
        description=(
            "List all drugs in the SAEM intervention library, optionally "
            "filtered by category (curvature_reducer, entropic_driver, "
            "gradient_amplifier, immune_modulator, resistance_breaker)."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Optional category filter.",
                    "enum": [
                        "curvature_reducer",
                        "entropic_driver",
                        "gradient_amplifier",
                        "immune_modulator",
                        "resistance_breaker",
                    ],
                },
            },
        },
    ),
    Tool(
        name="saem_analyze_resistance",
        description=(
            "Compare adaptive (phased) vs continuous therapy for a cancer type. "
            "Shows escape distances and demonstrates adaptive superiority."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cancer_type": {
                    "type": "string",
                    "description": "Cancer type to analyze.",
                    "enum": ["TNBC", "PDAC", "NSCLC", "GBM", "Melanoma", "CML", "Ovarian", "AML", "mCRPC", "HCC"],
                },
            },
            "required": ["cancer_type"],
        },
    ),
    Tool(
        name="saem_get_validation_gates",
        description=(
            "Run all 6 validation gates and return pass/fail status for each: "
            "1) Escape distance, 2) Cure rate CI, 3) Drug diversity, "
            "4) Sensitivity robustness, 5) Adaptive superiority, 6) Coherence restoration."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    Tool(
        name="saem_get_generator",
        description=(
            "Get the 10×10 generator matrix for a specific cancer type. "
            "Returns the matrix values and metadata (confidence, tags, evidence)."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cancer_type": {
                    "type": "string",
                    "description": "Cancer type.",
                    "enum": ["TNBC", "PDAC", "NSCLC", "GBM", "Melanoma", "CML", "Ovarian", "AML", "mCRPC", "HCC"],
                },
            },
            "required": ["cancer_type"],
        },
    ),
]
