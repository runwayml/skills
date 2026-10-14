# Runway Dev

Build AI video, image, audio, and real-time Character features into your applications with Runway's API. This plugin combines Runway Dev MCP with six integration skills for the official SDKs, models, Model Routers, Characters, Recipes, and published Workflows.

## Getting started

1. Install the plugin in your coding agent.
2. Ask: "Help me connect my Runway Dev account and choose a project."
3. Sign in or create a [Runway Dev account](https://dev.runway.com/) in your browser, finish Developer Portal setup, and authorize the bundled MCP connection.
4. Ask the agent to build the integration you need. When the application needs an API key, create one in Developer Portal and store it in your server environment as `RUNWAYML_API_SECRET`.

MCP uses OAuth; no API key is included in the plugin or MCP configuration. Your application uses its own server-side key for API requests. The agent can continue account-independent implementation using public documentation before MCP is connected.

## What MCP provides

- Live project access, model prices and constraints, and credit balances.
- Existing task status, failure diagnostics, and Model Router decisions.
- Model Router, Character, and knowledge-document management.
- Guidance for exposing published Runway app Workflows through the API.

The Dev MCP does not generate media, create application API keys, or change subscriptions. Generations run through your application's API integration and may consume credits.

## Examples

- "Add AI video generation to this app with the Runway API."
- "Help me integrate a Runway Character into this support app."
- "Why did my last Runway task fail, and how do I fix it?"

## Documentation and support

- [API and SDK documentation](https://docs.dev.runwayml.com/)
- [Connect Dev MCP](https://docs.dev.runwayml.com/guides/mcp/)
- [Runway support](https://help.runwayml.com/hc/en-us)
- [Privacy policy](https://runway.com/privacy-policy)
- [Terms of use](https://runway.com/terms-of-use)

Plugin source is [runwayml/skills](https://github.com/runwayml/skills). The package is licensed under [MIT](LICENSE).
