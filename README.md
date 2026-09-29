# SAEM MCP Server

**Research prototype.** In-silico tools only.

> **Status: in-silico research hypothesis. Not validated in cells, animals or patients.**
> Not a cure, not a therapy, not a medical device, not clinical decision support.
> Outputs are model results under stated assumptions and need wet-lab and clinical validation.

MCP server wrapping [Project Confluence](https://github.com/cloudynirvana/project-confluence) **simulations** as tools an agent can call.

This is a research prototype. It does not validate treatment protocols and it is not for clinical use.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/protocol-MCP-green.svg)](https://modelcontextprotocol.io)

## What Is This?

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that exposes Project Confluence SAEM research-simulation tools.

Run cancer **simulations**, query a research drug-class library, compare simulated resistance patterns, and inspect validation-gate **research checks** through the MCP protocol.

## Tools

| Tool | Description |
|------|-------------|
| `saem_run_simulation` | Run 3-phase Flatten→Heat→Push protocol for a specific cancer type (simulation) |
| `saem_run_all` | Run all 10 cancers, get comparison summary table |
| `saem_get_seriousness` | Composite seriousness breakdown (basin depth, eigenvalue analysis) |
| `saem_query_drug` | Search the 20-drug intervention library |
| `saem_list_drugs` | List drugs by category (curvature reducers, entropic drivers, etc.) |
| `saem_analyze_resistance` | Compare adaptive vs continuous therapy outcomes **in simulation** |
| `saem_get_validation_gates` | 6-gate pass/fail research check |
| `saem_get_generator` | Get the 10×10 generator matrix for any cancer type |

## Cancer Types Supported

TNBC, PDAC, NSCLC, GBM, Melanoma, Colorectal, HGSOC, mCRPC, AML, HCC

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

This MCP server is a research prototype in the [Project Confluence](https://github.com/cloudynirvana/project-confluence) ecosystem. Simulated scores are not protocols, doses, or clinical validation.

## License

MIT License. See [LICENSE](LICENSE).
