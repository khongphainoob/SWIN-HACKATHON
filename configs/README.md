# Configs Module

## Purpose
`configs/` stores configuration abstractions and future runtime settings.

Current state:
- `base_config.py` defines the abstract `load` contract.

## Recommended Config Scope
- Model settings (provider, model name, temperature, max tokens)
- Retrieval settings (`k`, thresholds, score cutoffs)
- Tool runtime settings (timeouts, retry policy)
- Environment-specific switches (dev/staging/prod)

## LangChain Fit
Keep configs explicit and injectable so chains, tools, and orchestrators remain testable and environment-agnostic.
