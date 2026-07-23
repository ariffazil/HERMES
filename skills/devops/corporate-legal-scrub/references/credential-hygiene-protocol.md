# Credential hygiene protocol

Credentials must be resolved from `/root/.secrets/vault.env` or the approved
secret store at runtime. Repository files may contain environment-variable
names, but never credential values or prefixes.

For Brevo, reference only `BREVO_API_KEY`. For Brave Search, reference only
`BRAVE_SEARCH_API_KEY`. Verification may confirm presence, never print values.

If a credential is found in tracked history, remove it from the current tree,
disable the affected integration when possible, and request provider-side
rotation through the sovereign security workflow.
