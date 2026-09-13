"""MCP Tool definitions for the SAEM Cancer PoC server.

Tool text is research/simulation language only. These tools do not
validate clinical protocols or support treatment decisions.
"""

from mcp.types import Tool

TOOLS = [
    Tool(
        name="saem_run_simulation",
        description=(
            "Run the in-silico SAEM 3-phase Flatten→Heat→Push schedule "
            "for a cancer generator. Returns modeled escape distance, "
            "in-silico basin-escape rate (engine field: cure_rate), "
            "simulated intervention schedule, phase timing, and a "
            "resistance comparison. Research simulation only — not a "
            "clinical protocol or treatment recommendation."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cancer_type": {
                    "type": "string",
                    "description": "Cancer generator label to simulate. One of: TNBC, PDAC, NSCLC, GBM, Melanoma, CML, Ovarian, AML, mCRPC, HCC",
                    "enum": ["TNBC", "PDAC", "NSCLC", "GBM", "Melanoma", "CML", "Ovarian", "AML", "mCRPC", "HCC"],
                },
            },
            "required": ["cancer_type"],
        },
    ),
    Tool(
        name="saem_run_all",
        description=(
            "Run the simulation across all 10 cancer generators and return "
            "a summary table of in-silico scores (modeled basin-escape rates, "
            "seriousness rankings, and simulated schedules). Not a "
            "pan-cancer clinical result."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    Tool(
        name="saem_get_seriousness",
        description=(
            "Get the composite model seriousness breakdown for a cancer "
            "generator. Shows coherence deficit, basin curvature, immune "
            "suppression, stress load, stromal barrier, and composite score. "
            "These are simulation features, not a clinical severity or "
            "staging score."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cancer_type": {
                    "type": "string",
                    "description": "Cancer generator label to analyze.",
                    "enum": ["TNBC", "PDAC", "NSCLC", "GBM", "Melanoma", "CML", "Ovarian", "AML", "mCRPC", "HCC"],
                },
            },
            "required": ["cancer_type"],
        },
    ),
    Tool(
        name="saem_query_drug",
        description=(
            "Query a named entry in the SAEM intervention library. Returns "
            "mechanism notes, target metabolites, a literature evidence tag, "
            "and which cancer generators the entry is mapped to. Library "
            "entries are research annotations, not prescribing information "
            "and not a claim of clinical efficacy."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "drug_name": {
                    "type": "string",
                    "description": "Name or partial name of the library entry to search for.",
                },
            },
            "required": ["drug_name"],
        },
    ),
    Tool(
        name="saem_list_drugs",
        description=(
            "List entries in the SAEM intervention library, optionally "
            "filtered by category (curvature_reducer, entropic_driver, "
            "gradient_amplifier, immune_modulator, resistance_breaker). "
            "This is a simulation library listing, not a formulary."
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
            "Compare modeled adaptive (phased) vs continuous intervention "
            "schedules for a cancer generator. Reports in-silico escape "
            "distances. Does not claim clinical superiority or recommend "
            "a regimen."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cancer_type": {
                    "type": "string",
                    "description": "Cancer generator label to analyze.",
                    "enum": ["TNBC", "PDAC", "NSCLC", "GBM", "Melanoma", "CML", "Ovarian", "AML", "mCRPC", "HCC"],
                },
            },
            "required": ["cancer_type"],
        },
    ),
    Tool(
        name="saem_get_validation_gates",
        description=(
            "Run the six in-silico computational gates and return pass/fail "
            "for each: 1) Escape distance, 2) Simulated basin-escape-rate CI, "
            "3) Library diversity, 4) Sensitivity robustness, 5) Adaptive-"
            "schedule comparison, 6) Coherence restoration. These are "
            "research checks on the simulator, not clinical validation of "
            "a treatment protocol."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    Tool(
        name="saem_get_generator",
        description=(
            "Get the 10×10 generator matrix for a cancer generator. "
            "Returns the matrix values and metadata (confidence, tags, "
            "evidence notes). Model parameters only — not a clinical assay."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cancer_type": {
                    "type": "string",
                    "description": "Cancer generator label.",
                    "enum": ["TNBC", "PDAC", "NSCLC", "GBM", "Melanoma", "CML", "Ovarian", "AML", "mCRPC", "HCC"],
                },
            },
            "required": ["cancer_type"],
        },
    ),
]
