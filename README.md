# SAEM MCP Server 🧬

> **MCP server wrapping Project Confluence — the universal computational pathology framework.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/protocol-MCP-green.svg)](https://modelcontextprotocol.io)

## What Is This?

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that exposes [Project Confluence](https://github.com/cloudynirv/project-confluence)'s SAEM (System Aligned Equilibrium Medicine) framework as tools any AI agent can call.

Run cancer simulations, query drug libraries, analyze resistance patterns, and validate treatment protocols — all through the MCP protocol.

## Tools

| Tool | Description |
|------|-------------|
| `saem_run_simulation` | Run 3-phase Flatten→Heat→Push protocol for a specific cancer type |
| `saem_run_all` | Run all 10 cancers, get comparison summary table |
| `saem_get_seriousness` | Composite seriousness breakdown (basin depth, eigenvalue analysis) |
| `saem_query_drug` | Search the 20-drug intervention library |
| `saem_list_drugs` | List drugs by category (curvature reducers, entropic drivers, etc.) |
| `saem_analyze_resistance` | Compare adaptive vs continuous therapy outcomes |
| `saem_get_validation_gates` | 6-gate pass/fail validation check |
| `saem_get_generator` | Get the 10×10 generator matrix for any cancer type |

## Cancer Types Supported

TNBC, PDAC, NSCLC, GBM, Melanoma, Colorectal, HGSOC, mCRPC, AML, HCC

## Setup

```bash
git clone https://github.com/cloudynirv/saem-mcp.git
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
SAEM_CANCER_POC_PATH=/path/to/project-confluence
```

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

This MCP server is part of the [Project Confluence](https://github.com/cloudynirv/project-confluence) ecosystem — a universal computational framework for modeling and treating disease using geometric attractor escape theory (SAEM).

## License

MIT License.
