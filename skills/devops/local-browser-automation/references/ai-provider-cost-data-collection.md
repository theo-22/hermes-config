# AI Provider Cost Data Collection via Browser Extension

How to pull granular AI spend/usage data from provider consoles using Hermes browser tools.

## Discovered 2026-06-29

The Hermes Browser Extension (v0.1) can actively navigate and interact with authenticated provider consoles — not just read pages Ted has open.

## Providers and URLs

### OpenRouter
- **Profile**: `https://openrouter.ai/settings/profile` — shows token usage, top models by tokens
- **Spend tab**: Click "Spend" tab on Profile page to see dollar amounts by model
- **Credits page**: `https://openrouter.ai/settings/credits` — shows transaction history and month-to-date credits spent
- **Key data**: Spend by model (7d), credits month-to-date, daily trend, all-time total

### OpenAI Platform
- **Usage**: `https://platform.openai.com/usage` — shows total spend, tokens, requests by model
- **Home**: `https://platform.openai.com` — shows credit balance, June spend summary
- **Note**: ChatGPT Pro subscription is billed via Apple App Store, NOT in API usage page. API usage is separate and often $0 if only using ChatGPT Plus.

### Google AI Studio
- **Spend**: `https://aistudio.google.com` → click "Spend" in nav — shows model-level cost breakdown
- **Usage**: `https://aistudio.google.com` → click "Usage" — shows request counts
- **Note**: Very low cost for Ted ($0.26/mo) — mostly free tier

### Anthropic Console
- **URL**: `https://console.anthropic.com` → redirects to `https://platform.claude.com`
- **Status**: Requires login (Google OAuth or email) — NOT pre-authenticated in Ted's browser
- **Action**: Stop and ask Ted to log in before proceeding

## Data Points to Extract Per Provider

For each provider, collect:
1. **Total spend** (current period / month-to-date)
2. **Spend by model** (which models cost what)
3. **Request count by model** (how many calls)
4. **Token count** (input/output)
5. **Cost per request** (average)
6. **Daily trend** (spike detection)
7. **All-time total** (since account start)

## Example Data (June 2026)

| Provider | Period | Spend | Requests | Tokens | Top Model |
|----------|--------|-------|----------|--------|-----------|
| OpenRouter | 7d | $32.10 | — | 1.31B | GPT-5.5 $15.67 |
| OpenRouter | MTD | $82.36 | — | — | — |
| OpenAI API | Jun 15-30 | $0.00 | 173 | 20.557M | — |
| Google Gemini | Jun 2-29 | $0.26 | — | — | — |
| Anthropic | — | — | — | — | Needs login |

## Dashboard Mapping

Ted's Budget dashboard (theos-mini.tail19cc07.ts.net/budget) shows:
- AI Cost section with "ACTUAL vs UNKNOWN" status
- Currently shows $196.69 total (mix of subscriptions + API)
- OpenRouter: $82.36 (matches credits MTD)
- ChatGPT Pro 5x: $94.05 (subscription, not API)
- Claude Pro: $20.00 (subscription)
- Gemini API: $0.26
- Anthropic API: $0.02

Subscriptions (ChatGPT Pro, Claude Pro) are billed through Apple App Store or directly, not visible in API consoles. Only API usage shows in provider consoles.
