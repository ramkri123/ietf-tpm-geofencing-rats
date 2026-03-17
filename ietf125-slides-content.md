# IETF 125 — RATS WG Presentation
## draft-lkspa-rats-verifiable-geo-fence-00
Draft co-authors: R. Krishnan, N. Smith, D. R. Lopez, A. Prasad, S. Addepalli, B. S. S. A. Malepati, G. Arfaoui, M. Epley, V. Masilamani

---

## Slide 1: Problem Statement

**Title:** Why Workload Geofencing Needs Hardware Roots

- Software-only identities (bearer tokens, SVIDs) are **stolen, replayed, or proxied** — no binding to physical hardware
- IP-based geolocation is **trivially spoofed** — VPNs, proxies, cloud region labels provide zero cryptographic assurance
- Regulations (RBI India, South Korea Spatial Data Act etc.) **require provable data residency** — but today's tooling can't prove it
- Location metadata is **unsigned** — no integrity, no audit trail, no verifiable provenance
- Result: **no cryptographic link** between a workload's identity, its platform integrity, and its physical location

> **Speaker note:** "The core gap is: today, nothing binds WHERE a workload runs to WHO it claims to be, with hardware-rooted proof."

---

## Slide 2: Solution — V-GAP

**Title:** Verifiable Geofencing Attestation Profile (V-GAP)

- **RATS Architecture profile** (RFC 9334) — not a new framework, builds on existing RATS plumbing
- Binds workload identity issuance to two hardware-rooted proofs:
  1. **Platform integrity** — TPM quote seals all evidence fields into a single hardware statement
  2. **Geographic residency** — "in-zone" proof, optionally privacy-preserving via transparent ZKPs
- **Three-layer trust chain** (silicon → agent → workload):

| Layer | What | How |
|:------|:-----|:----|
| Layer 1 | Workload ↔ Agent binding | Transitive Attestation (draft-mw-wimse) |
| Layer 2 | Platform integrity | TPM quote + PCR validation (this document) |
| Layer 3 | Residency verification | Geolocation proof + location endorsement (this document) |

- Credential issued **only when both layers pass** — fail-closed via X.509 CRITICAL extension

> **Speaker note:** "V-GAP is Layer 2 + Layer 3. Layer 1 is handled by transitive attestation. Together they give you silicon-to-workload trust."

---

## Slide 3: V-GAP Profile — RATS Mapping

**Title:** How V-GAP Maps to RATS Roles

| RATS Role | V-GAP Entity | What It Does |
|:----------|:-------------|:-------------|
| **Attester** | Location Anchor Host (LAH) | Produces `lah-bundle` — TPM quote + geo proof |
| **Verifier** | Host Identity Mgmt Plane | Validates TPM, PCRs, geo proofs → Attestation Result |
| **Endorser** | Location Endorser (e.g., MNO) | Signs location claim; MAY be an MNO, satellite operator, or other trusted location authority |
| **Relying Party + CA** | Workload Identity Mgmt Plane | Issues X.509-SVID only if attestation passes |
| **Downstream RP** | mTLS peer | Trusts CA signature as proxy for verified residency |

**Evidence flow** (background-check model, RFC 9334 §3.2):

```
LAH (Attester) → lah-bundle → Verifier ← Location Endorsement
                                  ↓
                          Attestation Result
                                  ↓
                    RP + CA → X.509-SVID (CRITICAL ext)
                                  ↓
                         Downstream RP (mTLS)
```

**Key design choice:** RP acts as "trust translator" — embeds attestation result into standard X.509, so downstream consumers don't need to understand RATS or V-GAP.

> **Speaker note:** "This is the background-check model from RFC 9334. The Attester never sees the result — it goes straight from Verifier to RP. The RP then bakes it into a standard cert. Note that the Endorser role is not limited to MNOs — our PoC uses an MNO via the CAMARA interface, but the architecture accommodates any trusted location authority: satellite operators, fixed infrastructure providers, or other parties with authoritative location visibility."

---

## Slide 4: Next Steps

**Title:** Path to WG Adoption

1. **Merge opportunity** with [draft-richardson-rats-geographic-results-01](https://datatracker.ietf.org/doc/draft-richardson-rats-geographic-results/01/)
   - Richardson defines **geographic claim encoding** in EAR (Attestation Results)
   - V-GAP defines the **Evidence profile and verification flow** that produces those results
   - Complementary scope — V-GAP is "how you get the evidence," Richardson is "how you encode the result"

2. **Seeking WG adoption** as a Standards Track document
   - Draft restructured to normative (category: std)
   - Core V-GAP profile is normative; operational/deployment guidance in informative appendices
   - Reference implementation: [github.com/lfedgeai/AegisSovereignAI](https://github.com/lfedgeai/AegisSovereignAI)

3. **Feedback requested on:**
   - RATS role mapping — is the "trust translator" (RP + CA) pattern the right fit?
   - Privacy technique extensibility — currently `none` and `zkp`, should we define a registry?
   - Proximity profiles — deferred to future docs, any interest in co-authoring?

> **Speaker note:** "We'd like to merge with Michael's draft — our scopes are complementary. We're asking the WG if there's interest in adoption and what the right next step is."
