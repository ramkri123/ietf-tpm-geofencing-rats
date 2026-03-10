# Verifiable Geofencing and Residency Proofs for Cybersecure Workloads

[![IETF Draft](https://img.shields.io/badge/IETF-Internet--Draft-blue.svg)](https://datatracker.ietf.org/doc/draft-lkspa-rats-verifiable-geo-fence/)
[![RATS WG](https://img.shields.io/badge/WG-RATS-green.svg)](https://datatracker.ietf.org/wg/rats/about/)

This is the working area for the IETF Internet-Draft **"Zero-Trust Sovereign AI: Verifiable Geofencing and Residency Proofs for Cybersecure Workloads"** ([draft-lkspa-rats-verifiable-geo-fence](https://datatracker.ietf.org/doc/draft-lkspa-rats-verifiable-geo-fence/)).

## Overview

Modern cloud and distributed environments face significant risks from stolen bearer tokens, protocol replay, and trust gaps in transit. This document presents a framework for modernizing workload security through:

- **Cryptographically verifiable geofencing** — binding workload identity to geographic and host attributes using trusted hardware (TPM), GNSS, and mobile network attestation.
- **Proof-of-possession** — workload signing keys attested by a Workload Identity Manager for proof of residency on approved hosts.
- **Protocol-aware residency enforcement** — covering HTTP (enhanced DPoP), IPsec, and browser-based protocols.

The framework leverages SPIFFE/SPIRE for workload identity, TPM-backed attestation, and composite geolocation (GNSS + mobile network) to ensure that only authorized workloads in approved locations can access sensitive data or services.

## Authors

- Ram Krishnan (JPMorgan Chase & Co.)
- Ned Smith (Intel)
- Diego R. Lopez (Telefonica)
- A Prasad (Oracle)
- Srinivasa Addepalli (Aryaka)

## Building the Draft

The draft is written in [mmark](https://github.com/mmark-md/mmark) Markdown and compiled with `xml2rfc`.

### Prerequisites

- [mmark](https://github.com/mmark-md/mmark)
- [xml2rfc](https://pypi.org/project/xml2rfc/)

### Commands

```bash
# Build TXT and HTML outputs
make

# Clean build artifacts
make clean
```

## Contributing

Feedback is welcome via GitHub issues or the [RATS mailing list](https://www.ietf.org/mailman/listinfo/rats).
