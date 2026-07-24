# Sovereign Identity Extension — Gateway Agent Card

> **Ratified:** 2026-07-13, CIV-33 close-the-loop

## Purpose

Bridge the A2A agent card layer (server-side Ed25519 signed, proves "this card was issued by the federation") with the sovereign identity layer (human private key, proves "Arif is commanding this session").

## Gateway Card Extension Block

Added to `agent-cards/pillars/aaa-gateway/agent-card.json`:

```json
{
  "extensions": [
    {
      "uri": "arif-fazil.com/ext/sovereign",
      "data": {
        "sovereign_anchor": "https://arif-fazil.com/000/",
        "sovereign_did": "https://arif-fazil.com/.well-known/did.json",
        "seal_anchor": "https://arif-fazil.com/999/",
        "seal_verification": "https://arif-fazil.com/999/seal.json",
        "authentication_protocol": "Ed25519-challenge-response",
        "nonce_flow": "arif_init(nonce) → sign(nonce) → verify(signature) → FULL authority"
      }
    }
  ]
}
```

## Verification Chain

```
agent card → signatures[].did → did:arif:aaa
              ↓
extensions[].sovereign_did → did:web:arif-fazil.com
              ↓
              /.well-known/did.json → Ed25519 public key
              ↓
              /000/ → sovereign anchor (human at position zero)
```

Any external agent reading the gateway card learns:
- Where to find the sovereign identity anchor (`/000/`)
- Where to verify seals (`/999/`)
- What protocol to use (Ed25519 nonce challenge)
- The correct nonce flow order

## Cross-Signing Pattern

Every agent card should carry BOTH:
- `signatures[]` — signed by federation key (`did:arif:aaa`), proves "federation issued this"
- `sovereignSignature` — signed by sovereign root (`did:web:arif-fazil.com`), proves "sovereign delegates to this"

If `sovereignSignature` is missing, the card can only reach OPERATOR authority.
