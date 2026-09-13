# SAEM MCP Server 🧬

> **MCP server wrapping Project Confluence — a computational pathology / cancer-simulation framework.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/protocol-MCP-green.svg)](https://modelcontextprotocol.io)

## What Is This?

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that exposes [Project Confluence](https://github.com/cloudynirvana/project-confluence)'s SAEM (System Aligned Equilibrium Medicine) framework as tools any AI agent can call.

Run in-silico cancer simulations, query the intervention library, analyze modeled resistance patterns, and check computational protocol gates — all through the MCP protocol.

**Research simulation only.** This is not a medical device, not CDS, and not clinical validation. See [DISCLAIMER.md](DISCLAIMER.md).

## Tools

| Tool | Description |
|------|-------------|
| `saem_run_simulation` | Run the in-silico 3-phase Flatten→Heat→Push schedule for a cancer generator |
| `saem_run_all` | Run all 10 cancer generators; return a comparison summary table |
| `saem_get_seriousness` | Composite model seriousness breakdown (basin depth, eigenvalue analysis) |
| `saem_query_drug` | Search the 20-entry intervention library |
| `saem_list_drugs` | List library entries by category (curvature reducers, entropic drivers, etc.) |
| `saem_analyze_resistance` | Compare modeled adaptive vs continuous intervention schedules |
| `saem_get_validation_gates` | 6-gate in-silico / computational pass-fail check |
| `saem_get_generator` | Get the 10×10 generator matrix for any supported cancer type |

## Cancer Types Supported

The MCP tool schemas currently accept: TNBC, PDAC, NSCLC, GBM, Melanoma, CML, Ovarian, AML, mCRPC, HCC.

These are **model generator labels**, not a claim of clinical coverage or validated treatment indications.

## Setup

```bash
git clone https://github.com/cloudynirvana/saem-mcp.git
cd saem-mcp
python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate

pip install -e .
```

## Configuration

Copy `.env.example` to `.env` and configure:

```
SAEM_PROJECT_ROOT=/path/to/project-confluence
```

(`SAEM_PROJECT_ROOT` is the variable the server reads. Point it at the SAEM / Project Confluence checkout that provides the simulation engine.)

## Test

```bash
python -m saem_mcp.server --test
```

## Run

```bash
python -m saem_mcp.server
```

## Use with Any MCP Client

Add to your MCP client configuration:

```json
{
  "mcp": {
    "servers": {
      "saem": {
        "command": "python",
        "args": ["-m", "saem_mcp.server"],
        "cwd": "/path/to/saem-mcp"
      }
    }
  }
}
```

## Part of Project Confluence

This MCP server is part of the [Project Confluence](https://github.com/cloudynirvana/project-confluence) ecosystem — a computational framework for **modeling** disease dynamics with geometric attractor-escape theory (SAEM). It does not treat disease and does not replace clinical judgment.

## Disclaimer

See [DISCLAIMER.md](DISCLAIMER.md). In short: not a medical device, not CDS, not clinically validated, and not dosing advice.

## License

MIT License.
