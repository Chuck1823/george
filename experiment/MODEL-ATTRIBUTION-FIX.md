# Model Attribution Fix

## Problem
Traces store `openrouter/auto` as the model ID, but we need the **actual resolved model** (e.g., `anthropic/claude-sonnet-4-20240620`, `qwen/qwen-2.5-32b`).

## Root Cause
OpenClaw stores the **configured model alias** (`modelId`) from `resolveModelAgentRuntimeMetadata`, not the **actual model** returned by the API. OpenRouter's `/chat/completions` response includes:

```json
{
  "model": "anthropic/claude-sonnet-4-20240620",  ← actual model used
  "id": "gen-..."
}
```

But OpenClaw captures `params.model` (`openrouter/auto`) and never updates it with the response's `model` field.

## Fix Going Forward

### Option A: Patch OpenClaw LLM Client
In the file handling the LLM API response (likely `runtime-BzlxAzli.js` or the LLM client), after parsing the OpenRouter response:

```javascript
// Current behavior (broken):
trajectoryEntry.modelId = config.modelId;  // "openrouter/auto"

// Should be:
trajectoryEntry.modelId = config.modelId;  // Keep alias for reference
trajectoryEntry.actualModel = response.model;  // Add actual model from response
```

This requires a PR to OpenClaw or using a patch file in `patches/`.

### Option B: Switch away from `openrouter/auto`
Use specific models in config:
```yaml
# openclaw config
model: openrouter/anthropic/claude-sonnet-4-20240620
```

Then `modelId` will always be the actual model. You lose auto-routing, but gain certainty.

### Option C: Use OpenRouter Router Hints
Set provider routing hints to narrow which model gets selected, while still tracking it:
```yaml
model: openrouter/auto
provider:
  openrouter:
    route: "anthropic/claude-sonnet-4"  # Force route to specific model
```

## What We Need to Change

1. **In `export-all.py`**: Add `actual_model` field extraction if available in trajectory data
2. **In `openclaw` node_modules**: Patch the LLM response handler to capture `response.model`
3. **In trace metadata**: Store both `generation_model` (alias) and `actual_model` (resolved)

## Backfill Note
Old traces **cannot** be backfilled because the resolved model wasn't stored anywhere. We need to fix this going forward and accept that old traces are stuck with `openrouter/auto`.
