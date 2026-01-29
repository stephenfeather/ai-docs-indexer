# ai-docs-indexer

Generate compressed documentation indexes for AI agent context files (AGENTS.md, CLAUDE.md, etc.).

## Why This Approach?

Based on [Vercel's research on AGENTS.md](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals), embedding a compressed documentation index directly in agent context dramatically outperforms other approaches:

| Approach | Pass Rate |
|----------|-----------|
| Baseline (no docs) | 53% |
| Skills (tool-based retrieval) | 53% |
| Skills with explicit instructions | 79% |
| **AGENTS.md (passive context)** | **100%** |

The key insight: rather than requiring agents to decide when to invoke documentation tools, embedding a compressed index (~8KB, 80% reduction from full docs) makes the information always available. This eliminates decision friction and sequencing problems that cause agents to skip retrieval.

## Installation

```bash
pip install ai-docs-indexer
```

Or with uv:

```bash
uv pip install ai-docs-indexer
```

## Usage

### Running with uv

If you have [uv](https://docs.astral.sh/uv/) installed, you can run the tool directly without manual environment setup:

```bash
uv run ai-docs-indexer scan ./docs --output AGENTS.md
```

This ensures the command runs in the expected Python environment with all dependencies.

### Basic usage

```bash
ai-docs-indexer scan ./docs --output AGENTS.md
```

### With options

```bash
ai-docs-indexer scan ./docs \
  --output CLAUDE.md \
  --format pipe \
  --name "Project Docs" \
  --root ./.docs \
  --extensions .md,.mdx,.rst \
  --instruction "Prefer retrieval-led reasoning"
```

### Multiple formats

```bash
ai-docs-indexer scan ./docs --format pipe --format json
```

### Output to stdout

```bash
ai-docs-indexer scan ./docs --format json --stdout
```

## Output Formats

### Pipe format (default)

Compact, AGENTS.md-style format:

```
[Project Docs Index]|root: ./.docs
|IMPORTANT: Prefer retrieval-led reasoning
|01-getting-started:{01-install.mdx,02-config.mdx}
```

### JSON format

```json
{
  "name": "Project Docs Index",
  "root": "./.docs",
  "instruction": "Prefer retrieval-led reasoning",
  "directories": {
    "01-getting-started": ["01-install.mdx", "02-config.mdx"]
  }
}
```

### YAML format

```yaml
name: Project Docs Index
root: ./.docs
instruction: Prefer retrieval-led reasoning
directories:
  01-getting-started:
    - 01-install.mdx
    - 02-config.mdx
```

## CLI Reference

```
ai-docs-indexer scan [OPTIONS] PATH

Arguments:
  PATH  Directory to scan for documentation files

Options:
  -o, --output PATH           Output file path
  -f, --format [pipe|json|yaml]  Output format (can specify multiple)
  -n, --name TEXT             Name for the index
  -r, --root TEXT             Root path in output
  -e, --extensions TEXT       Comma-separated extensions (.md,.mdx)
  -i, --instruction TEXT      Instruction for AI agents
  --include-hidden            Include hidden files/directories
  --follow-symlinks           Follow symbolic links
  --stdout                    Force output to stdout
  -q, --quiet                 Suppress status messages
```

## License

MIT
