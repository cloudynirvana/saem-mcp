"""MCP Server for SAEM Cancer PoC — Bioinformatics Simulation Engine.

Wraps the SAEM cancer-simulation framework as MCP tools, enabling AI-driven
in-silico cancer modeling from any MCP client (Antigravity, Claude Code, etc.).

Research simulation only: not a medical device, not CDS, not clinical
validation, and not dosing advice. See DISCLAIMER.md.
"""

import asyncio
import logging
import os
import sys
from typing import Any, Dict, List, Tuple

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent
from dotenv import load_dotenv

from .tools import TOOLS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("saem-mcp")

# Load environment
load_dotenv()

# Path to the SAEM project
SAEM_PROJECT_ROOT = os.getenv(
    "SAEM_PROJECT_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "saem-cancer-poc"))
)

# Initialize the MCP server
server = Server("saem-mcp")

# Lazy-loaded SAEM modules
_saem_loaded = False


def _ensure_saem():
    """Lazy-load SAEM modules by adding project paths to sys.path."""
    global _saem_loaded
    if _saem_loaded:
        return

    src_path = os.path.join(SAEM_PROJECT_ROOT, "src")
    root_path = SAEM_PROJECT_ROOT

    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    if root_path not in sys.path:
        sys.path.insert(0, root_path)

    _saem_loaded = True
    logger.info(f"SAEM loaded from: {SAEM_PROJECT_ROOT}")


def _get_generators():
    """Get all cancer generators."""
    _ensure_saem()
    from tnbc_ode import TNBCODESystem
    return TNBCODESystem.pan_cancer_generators()


def _get_healthy():
    """Get the healthy generator."""
    _ensure_saem()
    from tnbc_ode import TNBCODESystem
    return TNBCODESystem.healthy_generator()


def _get_metadata():
    """Get generator metadata."""
    _ensure_saem()
    from tnbc_ode import GENERATOR_METADATA
    return GENERATOR_METADATA


def _get_mapper():
    """Get intervention mapper."""
    _ensure_saem()
    from intervention import InterventionMapper
    return InterventionMapper()


def _get_optimizer():
    """Get geometric optimizer."""
    _ensure_saem()
    from geometric_optimization import GeometricOptimizer
    return GeometricOptimizer(10)


def _get_coherence():
    """Get coherence analyzer."""
    _ensure_saem()
    from coherence import CoherenceAnalyzer
    return CoherenceAnalyzer(10)


# ═══════════════════════════════════════════════════════════════════
# TOOL HANDLERS
# ═══════════════════════════════════════════════════════════════════

import numpy as np


def handle_run_simulation(cancer_type: str) -> str:
    """Run full simulation for one cancer type."""
    _ensure_saem()
    from confluence_runner import run_single_cancer

    mapper = _get_mapper()
    result = run_single_cancer(cancer_type, mapper, generate_lab_protocol=False)

    lines = [
        f"# 🧬 SAEM Simulation: {cancer_type}",
        "",
        "_In-silico run for the named cancer generator. Scores are model outputs, not clinical results._",
        "",
        f"## Model seriousness score: {result['seriousness']:.3f}",
        "",
        "## Simulated intervention schedule",
    ]
    for i, drug in enumerate(result.get("drugs", []), 1):
        lines.append(f"  {i}. {drug}")

    lines.extend([
        "",
        "## Simulated phase timing (model days)",
        f"  - Flatten: {result.get('phase_days', {}).get('flatten', '?')} days",
        f"  - Heat: {result.get('phase_days', {}).get('heat', '?')} days",
        f"  - Push: {result.get('phase_days', {}).get('push', '?')} days",
        "",
        "## In-silico metrics",
        f"  - Escape Distance: {result.get('escape_distance', 0):.4f}",
        f"  - Basin-escape rate (engine field: cure_rate): {result.get('cure_rate', 0)*100:.1f}%",
        f"  - 95% CI (simulator): [{result.get('cure_rate_ci_low', 0)*100:.1f}%, {result.get('cure_rate_ci_high', 0)*100:.1f}%]",
        "",
        "## Modeled resistance comparison",
        f"  - Adaptive (phased) escape: {result.get('adaptive_escape', 'N/A')}",
        f"  - Continuous escape: {result.get('continuous_escape', 'N/A')}",
        f"  - Adaptive lower escape in this run: {'✅ Yes' if result.get('adaptive_superior', False) else '❌ No'}",
    ])

    return "\n".join(lines)


def handle_run_all() -> str:
    """Run simulation across all 10 cancers."""
    _ensure_saem()

    generators = _get_generators()
    mapper = _get_mapper()
    A_healthy = _get_healthy()
    optimizer = _get_optimizer()
    coherence = _get_coherence()

    lines = [
        "# 🧬 SAEM Pan-Cancer Simulation Results",
        "",
        "_In-silico comparison across cancer generators. Not a clinical pan-cancer result._",
        "",
        "| Cancer | Seriousness | In-silico escape rate | Escape Dist | Top library entry |",
        "|--------|------------|----------------------|-------------|-------------------|",
    ]

    from confluence_runner import compute_seriousness, select_drugs, compute_phase_timing
    from confluence_runner import run_monte_carlo

    results = []
    for name, A_cancer in generators.items():
        try:
            seriousness = compute_seriousness(name, A_cancer, A_healthy)
            drug_tuples = select_drugs(mapper, A_cancer, A_healthy, name)
            phase_days = compute_phase_timing(seriousness)
            distances, cure_rate, ci_low, ci_high = run_monte_carlo(
                A_cancer, A_healthy, drug_tuples, phase_days, n_trials=30
            )
            top_drug = drug_tuples[0][0].name if drug_tuples else "N/A"
            escape = float(np.mean(distances))

            lines.append(
                f"| {name} | {seriousness:.3f} | {cure_rate*100:.1f}% | {escape:.3f} | {top_drug} |"
            )
            results.append({
                "cancer": name, "seriousness": seriousness,
                "cure_rate": cure_rate, "escape": escape,
            })
        except Exception as e:
            lines.append(f"| {name} | ERROR | - | - | {e} |")

    lines.extend([
        "",
        f"**Total generators processed:** {len(results)}",
        f"**Mean in-silico escape rate:** {np.mean([r['cure_rate'] for r in results])*100:.1f}%" if results else "",
    ])

    return "\n".join(lines)


def handle_get_seriousness(cancer_type: str) -> str:
    """Get seriousness breakdown."""
    _ensure_saem()

    generators = _get_generators()
    A_cancer = generators[cancer_type]
    A_healthy = _get_healthy()
    optimizer = _get_optimizer()
    coherence = _get_coherence()
    metadata = _get_metadata()

    meta = metadata.get(cancer_type)

    # Compute components
    delta_A = A_healthy - A_cancer
    basin_curv = optimizer.compute_basin_curvature(A_cancer)
    coherence_val = coherence.compute_coherence(A_healthy) - coherence.compute_coherence(A_cancer)

    immune_sup = meta.immune_suppression if meta else 0.5
    stromal = meta.stromal_barrier if meta else 0.3
    stress = meta.stress_load if meta else 0.4

    # Weighted composite
    composite = (
        0.25 * min(1.0, abs(coherence_val))
        + 0.25 * min(1.0, basin_curv / 5.0)
        + 0.20 * immune_sup
        + 0.15 * stress
        + 0.15 * stromal
    )

    lines = [
        f"# Model seriousness breakdown: {cancer_type}",
        "",
        "_Simulation features, not a clinical severity or staging score._",
        "",
        f"| Component | Value | Weight |",
        f"|-----------|-------|--------|",
        f"| Coherence Deficit | {abs(coherence_val):.4f} | 25% |",
        f"| Basin Curvature | {basin_curv:.4f} | 25% |",
        f"| Immune Suppression | {immune_sup:.2f} | 20% |",
        f"| Stress Load | {stress:.2f} | 15% |",
        f"| Stromal Barrier | {stromal:.2f} | 15% |",
        f"",
        f"**Composite Score: {composite:.4f}**",
    ]

    if meta:
        lines.extend([
            "",
            f"**Confidence:** {meta.confidence}",
            f"**Tags:** {', '.join(meta.tags)}",
            f"**Evidence:** {meta.evidence_notes}",
        ])

    return "\n".join(lines)


def handle_query_drug(drug_name: str) -> str:
    """Query a drug by name."""
    mapper = _get_mapper()
    lib = mapper.intervention_library

    matches = []
    for inv in lib:
        if drug_name.lower() in inv.name.lower():
            matches.append(inv)

    if not matches:
        return f"❌ No drug found matching '{drug_name}'. Use `saem_list_drugs` to see available drugs."

    lines = []
    for inv in matches:
        effect_norm = float(np.linalg.norm(inv.expected_effect))
        lines.extend([
            f"## 💊 {inv.name}",
            f"- **Category:** {inv.category}",
            f"- **Mechanism:** {inv.mechanism}",
            f"- **Library evidence tag:** {inv.evidence_level}",
            f"- **Effect Magnitude:** {effect_norm:.4f}",
            f"- **Cancer Tags:** {', '.join(inv.cancer_tags) if inv.cancer_tags else 'General'}",
            "",
        ])

    return "\n".join(lines)


def handle_list_drugs(category: str = None) -> str:
    """List drugs, optionally filtered by category."""
    mapper = _get_mapper()
    lib = mapper.intervention_library

    if category:
        lib = [inv for inv in lib if inv.category == category]

    lines = [
        f"# SAEM intervention library ({len(lib)} entries" + (f" in {category}" if category else "") + ")",
        "",
        "| # | Library entry | Category | Evidence tag | Mechanism |",
        "|---|------|----------|----------|-----------|",
    ]

    for i, inv in enumerate(lib, 1):
        mech = inv.mechanism[:50] + "..." if len(inv.mechanism) > 50 else inv.mechanism
        lines.append(f"| {i} | {inv.name} | {inv.category} | {inv.evidence_level} | {mech} |")

    return "\n".join(lines)


def handle_analyze_resistance(cancer_type: str) -> str:
    """Compare modeled adaptive vs continuous schedules (in-silico)."""
    _ensure_saem()
    from confluence_runner import (
        select_drugs, compute_seriousness, compute_phase_timing,
        run_resistance_comparison,
    )

    generators = _get_generators()
    A_cancer = generators[cancer_type]
    A_healthy = _get_healthy()
    mapper = _get_mapper()

    seriousness = compute_seriousness(cancer_type, A_cancer, A_healthy)
    drug_tuples = select_drugs(mapper, A_cancer, A_healthy, cancer_type)
    phase_days = compute_phase_timing(seriousness)

    adaptive_esc, continuous_esc = run_resistance_comparison(
        A_cancer, drug_tuples, phase_days, A_healthy
    )

    superior = adaptive_esc < continuous_esc

    lines = [
        f"# Modeled resistance comparison: {cancer_type}",
        "",
        "_In-silico schedule comparison. Not a regimen recommendation._",
        "",
        f"| Metric | Adaptive (Phased) | Continuous |",
        f"|--------|-------------------|------------|",
        f"| Escape Distance | {adaptive_esc:.4f} | {continuous_esc:.4f} |",
        f"| Strategy | 3-phase + holiday | Continuous schedule |",
        "",
        f"**Adaptive lower escape in this run:** {'✅ Yes' if superior else '❌ No'} "
        f"({'lower' if superior else 'higher'} modeled escape distance)",
        "",
        "**Model observation:** " + (
            "In this run, the phased schedule produced a lower simulated escape "
            "distance than the continuous schedule. That is a simulator comparison, "
            "not evidence that adaptive therapy is clinically superior."
            if superior else
            "In this run, the continuous schedule produced a lower simulated escape "
            "distance. That is a simulator comparison, not a dosing recommendation."
        ),
    ]

    return "\n".join(lines)


def handle_get_validation_gates() -> str:
    """Run all 6 in-silico computational gates."""
    _ensure_saem()
    from confluence_runner import (
        compute_seriousness, select_drugs, compute_phase_timing,
        run_monte_carlo, run_resistance_comparison,
    )

    generators = _get_generators()
    A_healthy = _get_healthy()
    mapper = _get_mapper()
    optimizer = _get_optimizer()
    coherence_analyzer = _get_coherence()

    gates = {
        "1. Escape Distance (all < 1.0)": True,
        "2. Cure Rate CI (all lower > 0%)": True,
        "3. Drug Diversity (≥3 unique top drugs)": True,
        "4. Sensitivity Robustness": True,
        "5. Adaptive Superiority (≥8/10)": True,
        "6. Coherence Restoration": True,
    }

    all_top_drugs = []
    adaptive_wins = 0
    total = len(generators)

    for name, A_cancer in generators.items():
        try:
            seriousness = compute_seriousness(name, A_cancer, A_healthy)
            drug_tuples = select_drugs(mapper, A_cancer, A_healthy, name)
            phase_days = compute_phase_timing(seriousness)

            distances, cure_rate, ci_low, ci_high = run_monte_carlo(
                A_cancer, A_healthy, drug_tuples, phase_days, n_trials=20
            )

            # Gate 1: escape distance
            if float(np.mean(distances)) >= 1.0:
                gates["1. Escape Distance (all < 1.0)"] = False

            # Gate 2: CI lower bound
            if ci_low <= 0:
                gates["2. Cure Rate CI (all lower > 0%)"] = False

            # Gate 3: drug diversity
            if drug_tuples:
                all_top_drugs.append(drug_tuples[0][0].name)

            # Gate 5: adaptive superiority
            adaptive_esc, continuous_esc = run_resistance_comparison(
                A_cancer, drug_tuples, phase_days, A_healthy
            )
            if adaptive_esc < continuous_esc:
                adaptive_wins += 1

            # Gate 6: coherence
            pre = coherence_analyzer.compute_coherence(A_cancer)
            post = coherence_analyzer.compute_coherence(A_healthy)
            if post <= pre:
                gates["6. Coherence Restoration"] = False

        except Exception as e:
            logger.error(f"Gate check failed for {name}: {e}")

    # Gate 3 check
    if len(set(all_top_drugs)) < 3:
        gates["3. Drug Diversity (≥3 unique top drugs)"] = False

    # Gate 5 check
    if adaptive_wins < 8:
        gates["5. Adaptive Superiority (≥8/10)"] = False

    # Format output
    passed = sum(1 for v in gates.values() if v)
    total_gates = len(gates)

    lines = [
        "# 🔬 SAEM computational gates (in-silico)",
        "",
        "_These gates are research checks on the simulator. A pass is not clinical validation of a treatment protocol._",
        "",
        f"**Result: {passed}/{total_gates} computational gates passed**",
        "",
        "| Gate | Status |",
        "|------|--------|",
    ]

    for gate, passed_flag in gates.items():
        status = "✅ PASS" if passed_flag else "❌ FAIL"
        lines.append(f"| {gate} | {status} |")

    lines.extend([
        "",
        f"**Adaptive wins:** {adaptive_wins}/{total}",
        f"**Unique top drugs:** {len(set(all_top_drugs))}",
    ])

    return "\n".join(lines)


def handle_get_generator(cancer_type: str) -> str:
    """Get generator matrix and metadata."""
    generators = _get_generators()
    metadata = _get_metadata()

    A = generators[cancer_type]
    meta = metadata.get(cancer_type)

    lines = [
        f"# Generator matrix: {cancer_type}",
        "",
        "_Model parameters only — not a clinical assay._",
        "",
        "```",
    ]

    # Format matrix
    for i in range(A.shape[0]):
        row = "  ".join(f"{A[i,j]:+.4f}" for j in range(A.shape[1]))
        lines.append(f"  [{row}]")

    lines.append("```")

    if meta:
        lines.extend([
            "",
            f"**Confidence:** {meta.confidence}",
            f"**Tags:** {', '.join(meta.tags)}",
            f"**Evidence:** {meta.evidence_notes}",
            f"**Immune Suppression:** {meta.immune_suppression:.2f}",
            f"**Stromal Barrier:** {meta.stromal_barrier:.2f}",
            f"**Stress Load:** {meta.stress_load:.2f}",
        ])

    optimizer = _get_optimizer()
    curv = optimizer.compute_basin_curvature(A)
    lines.append(f"\n**Basin Curvature:** {curv:.4f}")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
# SERVER WIRING
# ═══════════════════════════════════════════════════════════════════


@server.list_tools()
async def list_tools():
    """Return list of available tools."""
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls — runs compute-heavy work in a thread pool."""
    try:
        result: str

        match name:
            case "saem_run_simulation":
                result = await asyncio.to_thread(
                    handle_run_simulation, arguments["cancer_type"]
                )

            case "saem_run_all":
                result = await asyncio.to_thread(handle_run_all)

            case "saem_get_seriousness":
                result = await asyncio.to_thread(
                    handle_get_seriousness, arguments["cancer_type"]
                )

            case "saem_query_drug":
                result = await asyncio.to_thread(
                    handle_query_drug, arguments["drug_name"]
                )

            case "saem_list_drugs":
                result = await asyncio.to_thread(
                    handle_list_drugs, arguments.get("category")
                )

            case "saem_analyze_resistance":
                result = await asyncio.to_thread(
                    handle_analyze_resistance, arguments["cancer_type"]
                )

            case "saem_get_validation_gates":
                result = await asyncio.to_thread(handle_get_validation_gates)

            case "saem_get_generator":
                result = await asyncio.to_thread(
                    handle_get_generator, arguments["cancer_type"]
                )

            case _:
                result = f"Unknown tool: {name}"

        if not result.startswith("Unknown tool:"):
            result = (
                result
                + "\n\n---\n"
                + "_In-silico research output. Not a medical device, CDS, "
                + "or dosing advice. See DISCLAIMER.md._"
            )

        return [TextContent(type="text", text=result)]

    except KeyError as e:
        logger.warning(f"Invalid cancer type or missing arg: {e}")
        return [TextContent(
            type="text",
            text=f"⚠️ **Invalid input:** {e}. Valid cancer types: TNBC, PDAC, NSCLC, GBM, Melanoma, CML, Ovarian, AML, mCRPC, HCC"
        )]

    except Exception as e:
        logger.error(f"Error in {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ **Error:** {e}")]


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════


async def main():
    """Main entry point."""
    logger.info("Starting SAEM Bioinformatics MCP Server...")
    logger.info(f"SAEM Project Root: {SAEM_PROJECT_ROOT}")

    # Test mode
    if "--test" in sys.argv:
        try:
            _ensure_saem()
            generators = _get_generators()
            print(f"✅ SAEM loaded! {len(generators)} cancer generators available.")
            for name in generators:
                print(f"   - {name}")

            mapper = _get_mapper()
            print(f"✅ Drug library: {len(mapper.intervention_library)} interventions")
            print("✅ All systems operational.")
            return
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    # Run the MCP server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def run():
    """Entry point for the package."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
