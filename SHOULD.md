## Token Optimization & Tool Usage Principles
- **Tool-First Approach**: To optimize token usage and evaluation efficiency, always prioritize using local Python tools/scripts or MCP servers for concrete tasks (e.g., log parsing, data processing, regex matching, firmware hardware status checks).
- **Avoid LLM Over-computation**: Do not use the LLM's reasoning capability to process raw, repetitive text or perform mathematical/bit-level calculations if a Python tool can achieve the same result.
- **Minimal Output**: When tools return data, only pass the summarized or essential key results back to the main LLM context to minimize token footprint.
- **Context-Aware Code Execution**:
  - When asked to "run a command," "check the code," or "verify something," you **MUST** first use the `ls` or `dir` tool (or a Python script if needed) to inspect the current directory context to determine which file or script is relevant to the user's request.
  - Do not assume which file to run; always verify the context programmatically before executing.