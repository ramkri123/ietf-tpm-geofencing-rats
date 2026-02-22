%%%
title = "Zero-Trust Sovereign AI: Verifiable Geofencing and Residency Proofs for Cybersecure Workloads"
abbrev = "GeoW"
category = "info"
docName = "draft-lkspa-wimse-verifiable-geo-fence-04"
ipr = "trust200902"
area = "Security"
workgroup = "Workload Identity in Multi System Environments"
keyword = ["geofencing", "attestation", "workload identity", "residency", "TPM", "GNSS"]

[seriesInfo]
name = "Internet-Draft"
value = "draft-lkspa-wimse-verifiable-geo-fence-04"
stream = "IETF"
status = "informational"

[[author]]
initials = "R."
surname = "Krishnan"
fullname = "Ram Krishnan"
organization = "JPMorgan Chase & Co."
  [author.address]
  email = "ramkri123@gmail.com"

[[author]]
initials = "N."
surname = "Smith"
fullname = "Ned Smith"
organization = "Intel"
  [author.address]
  email = "ned.smith@intel.com"

[[author]]
initials = "D."
surname = "Lopez"
fullname = "Diego R. Lopez"
organization = "Telefonica"
  [author.address]
  email = "diego.r.lopez@telefonica.com"

[[author]]
initials = "A."
surname = "Prasad"
fullname = "A Prasad"
organization = "Oracle"
  [author.address]
  email = "a.prasad@oracle.com"

[[author]]
initials = "S."
surname = "Addepalli"
fullname = "Srinivasa Addepalli"
organization = "Aryaka"
  [author.address]
  email = "srinivasa.addepalli@aryaka.com"

[[contributor]]
initials = "B."
surname = "Malepati"
fullname = "Bala Siva Sai Akhil Malepati"
organization = "Independent"
  [contributor.address]
  email = "saiakhil2012@yahoo.com"

[[contributor]]
initials = "G."
surname = "Arfaoui"
fullname = "Ghada Arfaoui"
organization = "Orange"
  [contributor.address]
  email = "ghada.arfaoui@orange.com"

[[contributor]]
initials = "M."
surname = "Epley"
fullname = "Michael Epley"
organization = "Red Hat"
  [contributor.address]
  email = "mepley@redhat.com"

[[contributor]]
initials = "V."
surname = "Masilamani"
fullname = "Vijay Masilamani"
organization = "Independent"
  [contributor.address]
  email = "saanvijay20@gmail.com"

%%%

.# Abstract

Modern cloud and distributed environments face significant risks from stolen bearer tokens, protocol replay, and trust gaps in transit. This document presents a framework for hardware-dependent Workload Identity Agent (WIA) attestation, covering both TPM-based platform attestation and geolocation hardware-based attestation.

By binding workload identity to both geographic and host attributes, and supplementing bearer tokens with verifiable, location- and host-bound claims, the framework addresses the challenges of bearer token theft, proof-of-possession and trust-in-transit for all networking protocols. Leveraging trusted hardware, attestation protocols, and geolocation services, this approach ensures that only authorized workloads in approved locations and environments can access sensitive data or services, even in the presence of advanced threats.

{mainmatter}

# Conventions and Definitions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [[RFC2119]] [[RFC8174]] when, and only when, they appear in all capitals, as shown here.

**Acronyms used in this document:**

- **TPM**: Trusted Platform Module
- **GNSS**: Global Navigation Satellite System
- **IMEI**: International Mobile Equipment Identity
- **IMSI**: International Mobile Subscriber Identity
- **PCR**: Platform Configuration Register
- **MDM**: Mobile Device Management
- **IPSEC**: Internet Protocol Security
- **BMC**: Baseboard Management Controller
- **WIA**: Workload Identity Agent
- **OOB**: Out-of-Band
- **EAT**: Entity Attestation Token
- **DAA**: Direct Anonymous Attestation
- **EPID**: Enhanced Privacy ID
- **DCAP**: Data Center Attestation Primitives
- **EK**: Endorsement Key
- **AK**: Attestation Key
- **IMA**: Integrity Measurement Architecture

**Key Terms:**

Data Residency:
: Technical and Legal Challenges Ensuring compliance with global and local data protection regulations and mandates (e.g., EU GDPR, US HIPAA, PCI DSS, and jurisdiction-specific laws; see Appendix for public references on strict data residency rules). Strict data residency rules require that specific categories of data must be stored and processed exclusively within designated geographic boundaries. Enforcing these mandates relies on a combination of trusted computing, host-affinity, geolocation-affinity, and geofencing--each defined below.

Data Residency Host-Affinity Requirement:
: Data must remain bound to explicitly trusted computing environments or hosts, governing where storage and processing occur.

Data Residency Geolocation-Affinity Requirement:
: Data must not be transferred beyond defined geographic regions. All storage and computation must remain within the specified boundaries.

Data Residency Host Geolocation Affinity (aka Geofencing):
: A compound enforcement mechanism requiring that data and workloads are executed only on authorized hosts located within the approved geographic regions.

Workload Identity Agent (WIA):
: SPIRE agent on each host, with TPM plugin to issue X.509 SVIDs and sign requests.

Location Anchor Host (LAH):
: Host with a trusted GNSS/5G modem attached to its TPM endorsement key.

Composite Geolocation:
: Fused location estimate from local GNSS plus mobile-API data.

Proof-Of-Residency (POR):
: Cryptographic proof that a workload is executing within approved geographic and host boundaries.

# Introduction

As organizations increasingly adopt cloud and distributed computing, the need to enforce data residency, geolocation affinity, and host affinity has become critical for regulatory compliance and risk management. Traditional approaches to geographic and host enforcement rely on trust in infrastructure providers or network-based controls, which are insufficient in adversarial or multi-tenant environments.

Modern workload security faces new challenges from stolen bearer tokens, protocol replay, and the lack of trust in transit. Attackers can exploit bearer tokens from unauthorized hosts or locations, bypassing traditional controls.

This document introduces a framework for hardware-dependent Workload Identity Agent (WIA) attestation, covering two distinct layers: TPM-based platform attestation and geolocation hardware-based attestation. The solution cryptographically binds workload identity to both platform and geographic attributes, supplementing bearer tokens with signed, verifiable claims about workload residency and location.

This enables enforcement of data residency, geolocation affinity, and host affinity policies, even in adversarial or multi-tenant environments, and directly addresses the limitations of bearer tokens, proof-of-possession, IPSEC, and trust-in-transit.

# Relationship to Transitive Attestation

This document is part of a layered attestation architecture that, together with the companion document [[I-D.mw-wimse-transitive-attestation]], provides an end-to-end chain of trust from hardware through to workload identity.

The three layers are:

- **Layer 1 -- Workload Identity Attestation (Hardware-Independent):** Covered by [[I-D.mw-wimse-transitive-attestation]]. Proves that a workload is co-located with a verified Workload Identity Agent (WIA) via a local mechanism such as a Unix Domain Socket. Defines the mTLS-based Proof of Residency (PoR) and DPoR protocol flows. This layer does NOT concern itself with how the WIA itself was verified—it treats the WIA as an already-attested trust anchor.

- **Layer 2 -- WIA Platform Attestation via TPM (Hardware-Dependent):** Covered by this document. Proves the WIA is running on an approved host via TPM-based measured boot, PCR verification, credential activation, and WIA identity issuance. This establishes the hardware root of trust that Layer 1 relies upon.

- **Layer 3 -- WIA Geolocation Attestation (Hardware-Dependent):** Covered by this document. Proves the attested host (from Layer 2) is within an approved geographic boundary, using GNSS sensors, mobile network modules, and composite geolocation services whose identities are cryptographically bound to the host TPM identity.

Together, the complete chain is:

  * TPM Hardware -> WIA (this draft, Layer 2) -> Workload (transitive attestation draft, Layer 1)
  * TPM/Geolocation Hardware -> WIA (this draft, Layers 2+3) -> Workload (transitive attestation draft, Layer 1)

This document focuses exclusively on Layers 2 and 3: the hardware-dependent attestation of the WIA itself. For how workloads prove they are co-located with an attested WIA, and for the data-plane protocol flows (mTLS PoR, DPoR), see [[I-D.mw-wimse-transitive-attestation]].

In the context of SPIFFE/SPIRE:

  * The **Workload Identity Manager** is represented by the SPIFFE/SPIRE server.
  * The **Workload Identity Agent** is represented by the SPIFFE/SPIRE agent.

# Use Cases

Data residency use cases can be divided into three categories: (1) server-centric location, (2) user-centric location, and (3) regulatory compliance.

## Category 1: Server-centric Location

Enterprises (e.g., healthcare, banking) need cryptographic proof of a trustworthy geographic boundary (i.e., region, zone, country, state, etc.) for cloud-facing workloads.

### Server workload to Server workload - General

Enterprises handling sensitive data rely on dedicated cloud hosts (e.g., EU sovereign cloud providers) that ensure compliance with data residency laws, while also ensuring appropriate levels of service (e.g., high availability). To meet data residency legal requirements, enterprises need to verify that workload data is processed by hosts within a geographic boundary and that workload data is only transmitted between specified geographic boundaries.

### Server workload to Server workload - Agentic AI

Enterprises need to ensure that the AI agent is located within a specific geographic boundary when downloading sensitive data or performing other sensitive operations. A secure AI agent, running on a trusted host with TPM-backed attestation, interacts with geolocation and geofencing services to obtain verifiable proof of its geographic boundary. The agent periodically collects location data from trusted sensors, obtains attested composite location from a geolocation service, and enforces geofence policies via a geofencing service. The resulting attested geofence proof is used to bind workload identity to both the host and its geographic location, enabling secure, policy-driven execution of AI workloads and compliance with data residency requirements.

### Server workload to Server workload - Federated AI

In federated learning scenarios, multiple organizations collaborate to train machine learning models without sharing raw data. Each organization needs to ensure that its training data remains within a specific geographic boundary. This requires cryptographic proof that the training process is occurring on trusted hosts within the defined boundaries.

### User workload to Server workload

Enterprises ensure that they are communicating with a server (e.g., cloud services) located within a specific geographic boundary.

## Category 2: User-centric Location

Enterprises need cryptographic proof of trustworthy geographic boundary for user-facing workloads.

* A server (or proxy) authenticates to clients using different TLS certificates, each signed by a different Certificate Authority (CA), based on the geographic boundaries of user workloads.

* Enterprise Customer Premise Equipment (CPE) provides on-premises computing that is a basis for defining geolocation boundaries. A telco network provides a means for communication between premises.

* Construction and Engineering of SaaS workloads can benefit from attested geographic boundary data from end-user devices to restrict access within specific geopolitical regions (e.g., California). Enabling per-user or group-level geofencing helps prevent fraudulent access originating outside the authorized area.

* Healthcare providers need to ensure that the host is located in a specific geographic boundary when downloading patient data or performing other sensitive operations.

* U.S. Presidential Executive Order compliance directs Cloud Service Provider (CSP) support personnel be located in restricted geographies (e.g., Venezuela, Iran, China, North Korea). However, those personnel should not be allowed to support U.S. customers. Geolocation enforcement can ensure policy compliance.

## Category 3: Regulatory Compliance

Geographic boundary attestation helps satisfy data residency and data sovereignty requirements for regulatory compliance.

# Industry Gaps and Problem Statements

Modern cloud and distributed environments face significant risks from stolen bearer tokens, protocol replay, and trust gaps in transit. Current geofencing and location verification solutions face significant challenges across different data states, location sources, and authentication mechanisms. This section outlines the key gaps and problems that this specification aims to address.

## Data Generation/at-Rest Challenges

Textual Geotags:
: No standard for textual geotags (EXIF covers media only).

Attesting Geotags:
: Existing geotag formats are unsigned and forgeable via VPN/MITM attacks.

## Data-in-Use Challenges

### Authentication and Authorization Challenges

#### Bearer Token Vulnerabilities

Bearer tokens are typically generated via user MFA and used to establish HTTP sessions. A malicious actor can steal a bearer token (e.g., from a still-valid HAR file uploaded to a support portal, as seen in the Okta attack) and present it to a server workload. The attacker may be in a forbidden location and on an unauthorized host (e.g., their own laptop). Current solution options for addressing bearer token issue and their challenges:

* PoP Token: Not easy to establish trust between the presenter (client) and the token issuer.
* PoP via Mutual TLS: Client certificates are generally not supported in browsers. MITM entities such as API gateways often terminate TLS connections.
* Host TPMs for API call signature: Not scalable to sign every API call with a TPM key, as typical enterprise laptops/servers TPMs support only about 5 signatures per second.
* Non-HTTP protocols: No solution for IPSEC etc.

### Location and Geofencing Challenges

* **IP Address-Based Location:** This is the typical approach, but it has limitations: network providers can use geographic-region-based IANA-assigned IP addresses anywhere in the world, and enterprise VPNs can hide the user's real IP address.

* **Wi-Fi-Based Location:** For user laptop endpoints with agents (e.g., ZTNA), traditional geographic enforcement relies on trusting the Wi-Fi access point's location. However, Wi-Fi access points are mobile and can be moved, undermining this trust.

* **GNSS:** Certain GNSS, e.g., civilian GPS in smartphones and navigation systems, can be spoofed. A practical example is the Israel GPS spoofing attacks.

### Implicit Trust Challenges

* **Cloud Region Trust**: Implicit trust in cloud region assignment with no cryptographic proof of physical locality. There is no auditable link between stored blobs and actual geography.

* **Trust in Transit:** HTTP requests can be intercepted and modified by compromised intermediate proxies (e.g., API gateways, SASE firewalls).

# Approach Overview

This framework provides hardware-dependent attestation of Workload Identity Agents, organized into two layers:

- **Layer 2 -- TPM Platform Attestation:** Establishes that the WIA is running on an approved host with verified firmware, OS, and software integrity using TPM-based measured boot and remote attestation.

- **Layer 3 -- Geolocation HW-Based Attestation:** Layered on top of TPM attestation, establishes that the attested host is within an approved geographic boundary using hardware sensors (GNSS, mobile modems) whose identities are cryptographically bound to the host TPM.

Both layers support two deployment options:

- **Option A -- Host OS-Based (e.g., Keylime):** The attestation agent runs on the host operating system with direct TPM access. An external verifier (e.g., Keylime Verifier) queries the agent on-demand for TPM quotes and geolocation evidence.

- **Option B -- External Management Processor (e.g., HPE iLO family):** The management processor (BMC/iLO) has independent TPM access and sensor interfaces. An external management plane validates attestation evidence out-of-band, providing assurance even when the host OS is compromised.

For the workload-level attestation that builds on top of the WIA attestation described here (proving a workload is co-located with an attested WIA), see [[I-D.mw-wimse-transitive-attestation]].

## Server Hosts - Solution highlights

This section assumes that the maximum round-trip delay within a data center typically ranges from 500-1000 microseconds.

Scalable hierarchical approach -- enhancements to Workload Identity (SPIFFE/SPIRE) solution:

* Each of the hosts runs a workload identity agent (SPIFFE/SPIRE agent) with TPM plugin which connects to a workload identity manager (SPIFFE/SPIRE server).

* Location anchor hosts are directly attached to trusted location source - Mobile modem, GNSS Galileo receiver etc.
    * Use of multiple location anchor hosts can enhance security and trust.
    * For mobile sensors, the location can be tracked outside of host using a GSMA standards based mobile service provider API.

* Host geolocation sensor composition manager periodically verifies location anchor hosts device composition (primarily location sensors).
    * Use SPIFFE/SPIRE agent host geolocation plugin (new).

* Host proximity manager periodically verifies that location anchor hosts provide proof that application hosts are within the maximum data center round-trip delay from them.
    * SW-based Attested PTP - Modified Linux PTP daemon (SPIFFE/SPIRE workload) will sign PTP messages.
    * HW-based Attested PTP - Relevant for sub microsecond precision timing solutions.

* Workload identity agent provides proof that workloads run only on workload/location anchor hosts.
    * This is done using enhancements to existing SPIFFE/SPIRE agent and TPM plugin and addresses bearer token issue.

## End user/IoT hosts - Solution highlights

Browser solution -- new browser extension for proof residency and geofencing:

* Application proxy which intercepts every HTTP request; connects to workload identity agent to add geolocation; signs request using workload identity agent key which is attested by TPM attestation key.

Similar to the server hosts solution:

* Each of the hosts runs a workload identity agent (SPIFFE/SPIRE agent) which connects to a workload identity manager (SPIFFE/SPIRE server).

# TPM Platform Attestation (Layer 2)

This section describes how the Workload Identity Agent is attested to be running on an approved hardware platform. This forms the hardware root of trust on which all subsequent layers depend.

## Overview

TPM Platform Attestation establishes three properties:

1. **Hardware Identity:** The host contains an approved TPM with a valid, non-revoked Endorsement Key (EK) certificate.
2. **OS Integrity:** The host booted with approved firmware, bootloader, and operating system, as measured during the boot process and recorded in TPM Platform Configuration Registers (PCRs).
3. **WIA Integrity:** The Workload Identity Agent binary was measured (e.g., via Linux IMA) and matches approved values before execution.

## Measured Boot and OS Integrity Attestation

As part of the system boot/reboot process, a boot-loader-based measured system boot with remote Workload Identity Manager verification is used to ensure that only an approved OS is running on an approved hardware platform.

**Measurement Collection**: During the boot process, the boot loader collects measurements (hashes) of the boot components and configurations. The boot components are Firmware/BIOS/UEFI, bootloader, OS, drivers, location devices, and initial programs. All the location devices (e.g., GNSS sensor, mobile sensor) version/firmware in a platform are measured during each boot -- this is a boot loader enhancement. Any new location device which is hot-swapped in will be evaluated for inclusion only during next reboot.

**Log Creation**: These measurements are recorded in a log, often referred to as the TCGLog, and stored in the TPM's Platform Configuration Registers (PCRs).

**Attestation Report**: The TPM generates an attestation report, which includes the signed measurements and the boot configuration log. The signature of the attestation report (aka quote) is by a TPM Attestation Key (AK). This attestation includes data about the TPM's state and can be used to verify that the AK is indeed cryptographically backed by the TPM Endorsement Key (EK) certificate.

**Transmission**: The attestation report is then sent to an external verifier (Workload Identity Manager), through a secure TLS connection.

**Remote Verification**: The remote Workload Identity Manager checks the integrity of the attestation report and validates the measurements against known good values from the set of trusted hosts in the Host hardware identity datastore. The Workload Identity Manager also validates that the TPM EK certificate has not been revoked and is part of the approved list of TPM EK identifiers associated with the hardware platform. At this point, we can be sure that the hardware platform is approved for running workloads and is running an approved OS.

## WIA Attestation and Identity Issuance

The Workload Identity Agent TPM plugin is a process with elevated privileges that has access to TPM and location sensor hardware. Linux IMA measurement and Workload Identity Agent public/private key attestation are the changes compared to the original SPIFFE/SPIRE architecture with the TPM plugin.

**Measurement Collection**: For the Workload Identity Agent start case, the Agent executable is measured by Linux IMA, for example through cloud init and stored in TPM PCR through tools e.g., Linux ima-evm-utils before it is loaded. For the Workload Identity Agent restart case, it is not clear how the storage in TPM PCR will be accomplished - ideally this should be natively handled in the IMA measurement process with an ability to retrigger on restart or refresh cycles (OPEN ISSUES 1).

**Local Verification**: Enforce local validation of a measurement against an approved value stored in an extended attribute of the file.

**TPM attestation and remote Workload Identity Manager verification**:

Step 1 (Workload Identity Agent TPM APP ID issuance):

1. The Workload Identity Agent TPM plugin generates a TPM APP private key for proof of residency on the host for each start/restart.
2. The Workload Identity Agent TPM plugin sends the TPM APP public key, TPM AK public key and TPM EK certificate attestation parameters to the Workload Identity Manager.
3. The Workload Identity Manager verifies the attestation parameters. It then validates that the TPM EK certificate is in the trusted TPM EK certificate list with the Host Identity Manager (e.g. Keylime Verifier).
4. If validation passes, the Workload Identity Manager generates a credential activation challenge. The challenge's secret is encrypted using the Workload Identity Agent TPM APP public key.
5. The Workload Identity Manager sends the challenge to the Workload Identity Agent.
6. The Workload Identity Agent decrypts the challenge's secret using its TPM APP private key.
7. The Workload Identity Agent sends back the decrypted secret.
8. The Workload Identity Manager verifies that the decrypted secret matches the original secret used to build the challenge.
9. The Workload Identity Manager issues a Workload Identity Agent TPM APP ID using the TPM APP public key, TPM AK public key and TPM EK certificate.

Step 2 (Workload Identity Agent ID issuance):

1. The Workload Identity Agent generates a private/public key pair.
2. The Workload Identity Agent uses the TPM APP private key, stored in the TPM, to sign the public key.
3. The Workload Identity Agent sends the public key, signed by the TPM APP private key, to the Workload Identity Manager.
4. The Workload Identity Manager ensures the public key is associated with a Workload Identity Agent TPM APP ID.
5. If validation passes, the Workload Identity Manager generates a credential activation challenge. The challenge's secret is encrypted using the Workload Identity Agent public key.
6. The Workload Identity Manager sends the challenge to the Workload Identity Agent.
7. The Workload Identity Agent decrypts the challenge's secret using its private key.
8. The Workload Identity Agent sends back the decrypted secret.
9. The Workload Identity Manager verifies that the decrypted secret matches the original secret used to build the challenge.
10. The Workload Identity Manager issues the Workload Identity Agent ID using the Workload Identity Agent public key, the TPM APP signature of the Workload Identity Agent public key, and the Workload Identity Agent TPM APP ID.

## Deployment Option A: Host OS-Based (Keylime)

In this option, the TPM attestation agent runs on the host operating system with direct TPM access. An external Keylime Verifier performs remote verification.

### Architecture

1. **Keylime Agent (on host):** The rust-keylime agent starts on the host OS, registers with the Keylime Registrar, and stores the host's EK, AK, UUID, and mTLS certificate. The agent has direct access to the TPM 2.0 device.
2. **Keylime Registrar:** Stores agent registration data (UUID, IP, port, TPM keys, mTLS certificate) and serves as a lookup service for the Verifier.
3. **Keylime Verifier (external):** On attestation request, the Verifier queries the Registrar for the agent's AK public key, then contacts the agent directly to fetch a fresh TPM quote with a challenge nonce. The Verifier validates:
    - The TPM quote signature against the AK public key.
    - The PCR values against known-good reference values.
    - The nonce for freshness (anti-replay).
    - The App Key certificate (TPM2_Certify output) proving the App Key exists in the TPM and was certified by the AK.

### Integration with SPIRE

The SPIRE Agent TPM Plugin Server runs as an out-of-process sidecar (gRPC/HTTP via Unix socket). The plugin generates an App Key in the TPM, obtains an App Key certificate via the Keylime agent's delegated certification endpoint (TPM2_Certify), and assembles a SovereignAttestation message for the SPIRE Server. The SPIRE Server delegates verification to the external Keylime Verifier, which performs on-demand TPM quote fetching and validation.

### Advantages

- Mature open-source ecosystem (rust-keylime, SPIRE TPM plugin).
- Fine-grained PCR policy (per-PCR allowlists).
- Suitable for cloud and on-premises environments.

### Limitations

- Requires the host OS to be operational and the Keylime agent process to be running.
- Agent compromise could potentially affect attestation integrity (mitigated by TPM-bound keys).

## Deployment Option B: External Management Processor (e.g., HPE iLO)

In this option, the management processor (BMC) has independent access to the host TPM and performs attestation independently of the host operating system. This provides a higher-trust attestation path that solves the "compromised kernel" problem: if a hacker gains root access to the host OS, they can potentially blind in-band agents (e.g., Keylime agent, SPIRE agent) by feeding them fake data, but they cannot spoof the management processor's independent hardware path to the TPM.

### Dual TPM Access Paths

Both the Host CPU and the management processor can communicate with the TPM, but through different interfaces and with different levels of authority:

* **Host CPU Path (LPC/SPI Bus):** This is the standard "in-band" path. When the OS (Linux/ESXi/Windows) or the UEFI BIOS needs to extend a PCR (e.g., recording a hash of a workload binary), it talks to the TPM over the LPC or SPI bus.

* **Management Processor Path (I2C/Private Bus):** The management processor (e.g., HPE iLO) has a dedicated, private connection to the TPM chip that does not go through the Host CPU. This allows the management processor to query the TPM even if the Host CPU is powered off, crashed, or compromised by a rootkit. This is the "out-of-band" (OOB) path.

While both paths share the same physical TPM silicon, their roles are logically separated:

* The **Host CPU** sees the TPM as a local device (e.g., /dev/tpm0). It can extend PCRs (add new measurements) but cannot easily reset the TPM. It requires the OS network stack (SSH/gRPC) to report attestation status remotely.

* The **Management Processor** sees the TPM as a managed component via the Silicon Root of Trust. It can verify the TPM's Endorsement Key (EK) and Platform Certificate to ensure the TPM itself has not been tampered with. It uses the dedicated management NIC (via Redfish API) to report status independently of the OS network stack.

The end-to-end attestation paths are therefore:

* **In-band (Option A):** TPM --[LPC/SPI bus]--> Host CPU/OS --[host NIC, SSH/gRPC]--> Remote Verifier. The IMA event log and TPM Quote both travel through the host OS network stack. A compromised kernel sits on this path and can interfere with log delivery, though it cannot forge the hardware-signed TPM Quote.

* **Out-of-band (Option B):** TPM --[I2C/private bus]--> Management Processor --[dedicated mgmt NIC, Redfish API]--> Management Plane. The host OS has no visibility into this path. The management processor fetches the TPM Quote independently, so a compromised kernel cannot intercept, delay, or suppress the attestation evidence.

### Architecture

1. **Management Processor (e.g., HPE iLO):** Has direct access to the host TPM via a dedicated bus (I2C/private bus), independent of the host CPU and OS. The management processor collects TPM measurements and can perform attestation even when the host OS is not running or is compromised.
2. **External Management Plane (e.g., HPE OneView, HPE GreenLake):** Centralized management platform that receives attestation evidence from the management processor. Validates TPM quotes against golden measurements maintained in the management platform's database. Provides fleet-wide attestation visibility and policy enforcement.

### Silicon Root of Trust and IMA Integrity Protection

To ensure that the attestation measurements themselves are trustworthy, the management processor architecture provides multiple layers of protection against the "who watches the watcher" problem:

**Protection 1 -- Secure Boot / Silicon Root of Trust:** Before the OS starts, the management processor ASIC (e.g., HPE iLO) verifies the UEFI BIOS firmware. The BIOS then verifies the Bootloader (GRUB), and the Bootloader verifies the Linux Kernel signature. This ensures that the version of the Linux kernel -- and thus the IMA subsystem code -- being loaded is the authentic, signed version.

**Protection 2 -- TPM PCR Extension (Hardware Enforcement):** Linux IMA extends measurement hashes into TPM PCR 10. PCR extension is a one-way operation -- data can be added (extended) to a PCR, but it cannot be overwritten or deleted without a full system reboot. Even if a compromised kernel stops IMA from recording a malicious binary, it cannot undo the previous clean measurements in the TPM. See Step 6 of the Periodic Attestation Cycle below for the full verification procedure.

**Protection 3 -- IMA Appraisal Mode:** By default, IMA only measures (logs). In IMA Appraisal mode, the kernel refuses to execute any binary or load any library that does not have a valid cryptographic signature (stored as an extended attribute on the file). IMA policies can themselves be digitally signed, preventing tampering.

**Protection 4 -- Out-of-Band (OOB) Attestation:** The management processor fetches the TPM Quote via its dedicated I2C/private bus, bypassing the Host CPU and OS entirely. The TPM signs the PCR values with its hardware-protected key. This ensures a compromised kernel cannot intercept, delay, or suppress the attestation evidence. See Step 3 of the Periodic Attestation Cycle for the detailed flow.

**Protection 5 -- Kernel Lockdown Mode:** Linux Kernel Lockdown (integrity or confidentiality mode) prevents even the root user from modifying kernel memory via /dev/mem, replacing the running kernel via kexec, or accessing sensitive debug interfaces that could be used to bypass IMA checks.

### Root Adversary and IMA Tampering

A key question is whether an adversary with root access to the host OS can tamper with IMA measurements themselves. The answer is that a root adversary has limited ability to interfere with IMA, but the protections above are specifically designed to detect such tampering:

* **What a root adversary CAN do:** A compromised kernel can disable or bypass the IMA subsystem, preventing future measurements from being recorded. The adversary can also tamper with the IMA event log in kernel memory to hide evidence of malicious binaries being loaded.

* **What a root adversary CANNOT do:** The adversary cannot roll back or modify TPM PCR 10, because PCR extension is a one-way cryptographic operation (PCR_new = Hash(PCR_old || measurement)). The adversary also cannot forge a TPM Quote, because the TPM signs PCR values with its hardware-protected Attestation Key, which is inaccessible to the host OS. Finally, the adversary cannot intercept or spoof the management processor's out-of-band attestation path (I2C/private bus).

* **How tampering is detected:** The verifier replays the IMA log against the hardware-signed TPM Quote obtained via the OOB path. Any mismatch triggers a trust failure. See Step 6 of the Periodic Attestation Cycle for the full detection procedure.

* **Residual risk (TOCTOU):** A root adversary could theoretically load a malicious binary between attestation cycles (time-of-check-time-of-use). This is mitigated by IMA Appraisal Mode (Protection 3) blocking unsigned binaries at load time, Kernel Lockdown (Protection 5) preventing kernel memory modification, and frequent attestation polling intervals.

### TPM Swap Attack Protection

In modern server implementations (e.g., HPE Gen11), the management processor acts as a gatekeeper during the boot process. It uses its independent path to verify that the TPM is authentic. If the management processor detects that the TPM has been physically replaced (a "TPM Swap" attack), it can prevent the Host CPU from starting, effectively blocking the server until an administrator intervenes.

### Periodic Attestation Cycle: Step-by-Step

The following describes what happens during each periodic attestation cycle (e.g., every 20-60 seconds) across the three components, and how each step detects IMA or kernel compromise. A challenge nonce is used end-to-end to guarantee freshness.

**Step 1 -- External Verifier: Initiate Attestation Challenge**

The external management plane verifier (e.g., HPE OneView/GreenLake) generates a cryptographically random nonce and sends it to the management processor (iLO) via the dedicated management NIC (Redfish API). This nonce will be embedded in the TPM Quote to prove that the attestation evidence is fresh and was produced in response to this specific request.

* _Compromise detection:_ The nonce originates outside the host entirely (at the management plane). The host OS never sees or handles this nonce because it travels over the dedicated management network to iLO.

**Step 2 -- Host OS: Normal Operation (Continuous)**

During normal operation, the Linux kernel's IMA subsystem continuously measures every binary, library, and kernel module loaded on the host. Each measurement is extended into TPM PCR 10 via the in-band LPC/SPI bus. The IMA event log accumulates in kernel memory at /sys/kernel/security/ima/ascii_runtime_measurements.

* _Compromise detection:_ If the kernel is compromised and IMA is disabled, measurements stop being extended into PCR 10. The PCR freezes at its last legitimate value. No new entries appear in the IMA log.

**Step 3 -- Management Processor (iLO): Fetch TPM Quote (OOB)**

The management processor passes the verifier's nonce to the TPM via the TPM2_Quote command over its dedicated I2C/private bus. The TPM constructs a Quote structure containing: (a) all PCR values (including PCR 10), (b) the verifier's nonce, and (c) the TPM's internal clock value (TPMS_CLOCK_INFO). The TPM signs this entire structure with its hardware-protected Attestation Key (AK). The management processor also reads the TCG Boot Event Log from firmware memory.

* _Compromise detection:_ This step is entirely independent of the host OS. A compromised kernel cannot intercept, delay, or modify the Quote because it has no access to the I2C/private bus or the management processor's execution environment. The nonce is embedded inside the TPM-signed Quote, so it cannot be stripped or replaced without invalidating the signature.

**Step 4 -- Host OS: Provide IMA Log (In-Band)**

The external management plane verifier (e.g., HPE OneView/GreenLake) requests the current IMA event log from the host OS via the host network stack. A lightweight log exporter runs on the host as a privileged systemd service (requiring root or CAP_SYS_ADMIN to read /sys/kernel/security/ima/ascii_runtime_measurements) and exposes the IMA runtime measurements over the network. The exporter is installed as a systemd unit file, started automatically at boot, and runs as a long-lived daemon listening for log retrieval requests (e.g., via gRPC or a REST endpoint). Its binary is itself measured by IMA at launch time and recorded in PCR 10, so any tampering with the exporter binary is captured in the TPM measurements. The log may also be retrieved via direct SSH access to the host. Regardless of the collection method, the IMA log is transmitted as untrusted input — the trust anchor is the OOB TPM Quote, not the log itself. Notably, the integrity of the log exporter does not affect the security model: even if both the kernel and the exporter are compromised and conspire to produce a falsified log, the verifier will detect the tampering via the PCR mismatch in Step 6.

* _Compromise detection:_ A compromised kernel can tamper with this log (remove entries, alter hashes, truncate). This is expected behavior and is why the log is treated as untrusted. The verifier will detect any tampering in Step 6.
* _Compromise detection:_ A compromised kernel may refuse to deliver the log entirely (e.g., kill the agent). In this case, the verifier has a TPM Quote (from Step 3) but no log to verify against it, which triggers a trust failure.

**Step 5 -- Management Processor (iLO): Forward Evidence to Management Plane**

The management processor transmits the hardware-signed TPM Quote (which contains the verifier's nonce and the TPM clock value inside the signed payload) and the TCG Boot Event Log to the external management plane (e.g., HPE OneView/GreenLake) via the dedicated management NIC using the Redfish API. The management processor signs this transmission with its own OEM CA-chained identity key.

* _Compromise detection:_ The management processor's identity is verified by the OEM CA chain. A spoofed or tampered management processor would fail certificate validation.

**Step 6 -- External Verifier: Validate Evidence**

The external verifier (management plane) performs the following validation:

1. **Verify TPM Quote signature** using the TPM's AK public key. If invalid, the TPM or Quote has been tampered with.
2. **Verify nonce** embedded in the signed Quote matches the nonce sent in Step 1. If mismatched, the Quote is a replay of an older attestation or was generated in response to a different challenge.
3. **Verify TPM clock** monotonicity: the clock value embedded in the signed Quote must be greater than the previous attestation cycle's clock value. A rollback indicates tampering.
4. **Replay the IMA log** entry by entry, recomputing PCR 10: for each log entry, compute Hash(entry) and extend it into a running PCR accumulator starting from the initial PCR value (all zeros after reset).
5. **Compare the recomputed PCR 10** against the hardware-signed PCR 10 from the TPM Quote:
    * **Match:** The IMA log is consistent with the TPM's measurements. The system is running approved software.
    * **Mismatch:** The IMA log has been tampered with (entries removed, altered, or fabricated). The verifier raises a trust failure alert.
6. **Compare PCR 10 against golden reference values** to detect unexpected binaries (even if the log is consistent, a new/unknown binary triggers a policy violation).
7. **Check for log staleness:** Compare the number of IMA log entries and the TPM clock against the previous cycle. If the system is active (network traffic, CPU load) but the log has not grown, IMA may have been disabled by a compromised kernel.

* _Compromise detection summary:_
    * **Tampered IMA log** → detected at Step 6 sub-step 5 (log-vs-PCR mismatch).
    * **Disabled IMA** → detected at Step 6 sub-step 7 (stale log with active system).
    * **Replayed old Quote** → detected at Step 6 sub-steps 2-3 (nonce from Step 1 / clock mismatch).
    * **Unauthorized binary loaded** → detected at Step 6 sub-step 6 (policy violation).
    * **Log delivery suppressed** → detected by absence of log at Step 4 (trust failure due to missing evidence).



### Advantages

- Out-of-band attestation: works even when the host OS is compromised, rebooting, or offline.
- Hardware-isolated attestation path: the management processor is physically separate from the host CPU.
- Detects compromised kernel / IMA subversion through hardware-signed TPM quotes.
- TPM Swap attack protection at boot time.
- Enterprise fleet management integration (HPE OneView, Dell iDRAC, Lenovo XClarity, etc.).

### Limitations

- Vendor-specific management processor implementations.
- Requires enterprise management plane infrastructure.
- Management processor firmware must itself be trusted and kept up to date.

## Workload Identity Fusion: Periodic SPIRE Re-Attestation

Both deployment options (A and B) can integrate periodic SPIRE Agent re-attestation with host platform attestation to fuse workload identity with hardware-verified host integrity. The core pattern is: the SPIRE Server's challenge nonce is forwarded to the host attestation verifier, which uses it to fetch a fresh TPM Quote, creating a cryptographic binding between the workload SVID and the host's hardware-attested state.

**In-band implementation (Option A):** In the reference implementation [[AegisSovereignAI]], the SPIRE Server sends a challenge nonce to the SPIRE Agent, which assembles a SovereignAttestation message. The SPIRE Server delegates verification to the Keylime Verifier, which contacts the in-band Keylime agent to fetch a fresh TPM Quote using the same nonce. The verifier validates the Quote, IMA log, and geolocation, then returns attested claims to the SPIRE Server for SVID issuance. This flow is entirely in-band: the TPM Quote travels through the host OS network stack.

**OOB upgrade (Option B):** When a management processor is available, the verification step is upgraded to use the OOB path. The SPIRE Server still sends a challenge nonce to the SPIRE Agent, and the SPIRE Agent still assembles a SovereignAttestation message. However, the management plane verifier (e.g., HPE OneView/GreenLake) forwards the nonce to the management processor (iLO) instead of the in-band agent. The management processor fetches the TPM Quote via its dedicated I2C/private bus (Step 3 of the Periodic Attestation Cycle), and the IMA log is collected separately as untrusted input from the host (Step 4). The verifier performs the full validation (Step 6), and the attested claims -- including platform integrity, IMA status, and geolocation -- are returned to the SPIRE Server for SVID issuance.

**Periodic re-attestation:** The SPIRE Agent's SVID has a short TTL (e.g., 60 seconds) and is periodically re-issued. Each re-attestation cycle triggers the full OOB verification flow, meaning the workload identity is continuously re-bound to the host's current hardware-attested state. If the host platform fails attestation (e.g., IMA log tampering detected, unauthorized binary loaded), the SPIRE Server refuses to re-issue the SVID, effectively revoking the workload's identity and blocking it from communicating with other services.

This fusion achieves several properties:

1. **Single nonce, dual binding:** The same cryptographic nonce binds both the workload identity proof (TPM App Key certification) and the host platform integrity proof (TPM Quote via OOB path), preventing an attacker from combining a valid workload credential with a compromised host.
2. **Continuous assurance:** Unlike one-time boot attestation, the short SVID TTL forces re-attestation every 20-60 seconds, ensuring that host compromise is detected within one attestation cycle.
3. **Automatic revocation:** SVID non-renewal on attestation failure is an implicit revocation mechanism that requires no revocation lists or OCSP infrastructure.
4. **Defense in depth:** The OOB path ensures that even if the in-band SPIRE Agent and Keylime Agent are both compromised, the management processor's independent TPM Quote reveals the true platform state.

## Privacy Options for TPM-Based Attestation

From a privacy standpoint, sharing TPM details--especially the EK certificate--across organizational boundaries can be problematic. Below are two approaches that let you attest workload identities without exposing raw EK data.

* Option 1 -- Pseudonymity:
    - Only the Workload Identity Agent's TPM APP public key and Host identity agent's (e.g. Keylime agent) TPM AK public key are shared outside the host-owner organization.
    - The consuming organization's Workload Identity Manager verifies that AK against its own list of trusted AK public keys.
    - A unique TPM AK is generated and attested per tenant, so no single AK maps across tenants.
    - Supported by all TPM 2.0+ devices, this gives you per-tenant pseudonymity without ever revealing the EK.
* Option 2 -- Full Anonymity:
    - Leverage TPM 2.0+ Direct Anonymous Attestation (DAA) or EPID. Note that this requires TPM 2.0+ devices with DAA support.
    - Each host's TPM runs the DAA Join protocol with a Privacy CA to obtain a group credential.
    - The Workload Identity Agent signs its public key with that DAA credential (using a session-specific basename).
    - The Workload Identity Manager verifies the signature against the DAA group public key--proving membership without exposing or linking any device identity.
* Both options remove direct TPM EK exposure. Pseudonymity uses the standard TPM AK model, while TPM DAA offers unlinkable, anonymous proofs of TPM possession.

# Geolocation HW-Based Attestation (Layer 3)

This section describes how the geolocation of an attested host is verified using hardware sensors. Geolocation attestation is layered on top of TPM Platform Attestation (Layer 2)--a successful TPM platform attestation is a prerequisite for geolocation attestation, because the geolocation sensor identities are cryptographically bound to the host TPM identity.

## Overview

Geolocation HW-Based Attestation establishes two additional properties beyond TPM Platform Attestation:

1. **Sensor Integrity:** The geolocation sensors (GNSS, mobile modem) attached to the host are genuine, their firmware is measured, and their identities (sensor hardware ID, IMEI, IMSI) are bound to the host TPM EK.
2. **Geographic Location:** The host is located within an approved geographic boundary, as determined by cryptographically attested sensor readings cross-verified with independent sources (e.g., mobile network operator location services).

## Sensor Composition and Binding to TPM EK

The Host geolocation sensor composition manager runs outside of the host. In addition to obtaining location from device location sources (e.g., GNSS), it connects to mobile location service providers (e.g., Telefonica) using the GSMA Location API. The process described below is run periodically (e.g., every 5 minutes) to check if the host hardware composition has changed. Host hardware composition comprises TPM EK, GNSS sensor hardware ID, mobile sensor hardware ID (IMEI), and mobile-SIM IMSI. Note that this workflow is feasible only in enterprise environments where the host hardware is owned and managed by the enterprise.

1. The Workload Identity Agent periodically gathers host composition details (e.g., mobile sensor hardware ID (IMEI), mobile-SIM IMSI) and sends them to the Host geolocation sensor composition manager.
2. The Host geolocation sensor composition manager cross-verifies that the components of the host are still intact or detects if anything has been removed. Plugging out components can decrease the quality of location. Note that e-SIM does not have the plugging out problem like standard SIM but could be subject to e-SIM swap attack.

## Geolocation Gathering Workflow

The process described below is run periodically (e.g., every 30 seconds for frequently mobile hosts such as smartphones; every 5 minutes for less frequently mobile hosts such as laptops; every 50 minutes for stationary hosts) to check if the host's location has changed and to obtain an attested location.

1. The Workload Identity Agent gathers the location using the geolocation plugin (a) directly from host-local location sensors (e.g., GNSS), which provide a hardware-attested location, and/or (b) using existing Operating System (OS) APIs, which gather a composite location from location providers (e.g., Google, Apple). Location has a quality associated with it. For example, IP address-based or Wi-Fi-based location is of lower quality compared to other sources.
2. For each of the registered workload IDs (or website URL), based on the configured location policy (precise, approximated within a fixed radius, geographic region-based indicating city/state/country - see OPEN ISSUES 2), the location is converted appropriately to a workload ID-specific location. For thin clients (browser clients), the workload ID is the website URL. This ensures that the privacy of the workload is preserved while still allowing for geolocation enforcement.
3. All the above details are captured in the Geolocation Information Cache which contains the following fields:
    1. Time of collection (timestamp)
    2. Workload ID specific location details for each client workload where each entry contains:
        1. client workload ID - relevant for thick clients (e.g. Microsoft Teams client)
        2. server workload ID (or website URL) - relevant for thin clients (e.g. Microsoft Teams browser version)
        3. client location type (e.g. precise, approximated, geographic region based)
        4. client location (e.g. latitude/longitude, city/state/country)
        5. client location quality (e.g. GNSS, mobile network, Wi-Fi, IP address)

It is important to note that the Geolocation Information Cache is kept in the Workload Identity Agent memory and is not stored on disk. The information is refreshed periodically to ensure that the location is up-to-date. This information is used only by workloads in the host and never leaves the host.

If the location is gathered only using existing OS APIs, it may be done in the workload (thick client) or browser extension (thin client). The Geolocation Information Cache is stored in thick client memory (relevant only to specific client) or browser extension memory (relevant to all thin clients and indexed using user in OAuth bearer token/server website URL).

## Deployment Option A: Host OS-Based (Keylime)

In this option, the Keylime agent collects geolocation sensor data on the host OS and extends TPM PCR 15 with a hash of the geolocation evidence, binding the location to the TPM attestation.

### Architecture

1. **Keylime Agent (on host):** In addition to its TPM attestation role (Layer 2), the agent interfaces with GNSS sensors and mobile modems attached to the host. It collects:
    - **TPM-Attested Data (Mobile):** sensor_id, sensor_imei, sim_imsi.
    - **TPM-Attested Data (Location):** sensor_id, sensor_serial_number, latitude, longitude, accuracy.
    - **NOT TPM-Attested:** sim_msisdn (looked up from sidecar database using IMEI+IMSI composite key).
2. **PCR 15 Extension:** The agent generates a geolocation response where the hash of (geolocation data + challenge nonce) is extended into TPM PCR 15, cryptographically binding the location reading to the TPM identity.
3. **Keylime Verifier (external):** On attestation request, the Verifier:
    - Contacts the Keylime agent to fetch geolocation with the challenge nonce.
    - Validates that the nonce matches (freshness/TOCTOU protection).
    - Validates the PCR 15 value against the expected hash.
    - Cross-verifies the claimed location against the mobile network operator's location service (GSMA/CAMARA API) using the IMEI/IMSI from the TPM-attested data.

### Mobile Location Verification

A mobile location verification microservice acts as a thin CAMARA API wrapper. It receives the MSISDN (from SVID claims or Keylime DB lookup via IMEI+IMSI) and queries the mobile network operator's location service to obtain an independent location fix and cross-verify the GNSS-reported location.

### Advantages

- Reuses the same Keylime infrastructure as Layer 2. 
- PCR 15 binding provides cryptographic linkage between geolocation and TPM identity.
- Mobile network cross-verification mitigates GNSS spoofing.

### Limitations

- Requires GNSS sensor and/or mobile modem to be physically attached to the host.
- Host OS compromise could potentially affect sensor readings before they are extended into the PCR (mitigated by TPM binding and cross-verification).

## Deployment Option B: External Management Processor (e.g., HPE iLO)

In this option, geolocation sensors are connected to or accessible from the management processor, providing out-of-band geolocation attestation independent of the host OS. This leverages the same dual-path architecture described in the Layer 2 Option B: the management processor uses its dedicated hardware bus (I2C/private bus) to access both the TPM and the geolocation sensors, completely bypassing the Host CPU and OS.

This architecture is critical for geolocation integrity because a compromised Host OS could feed spoofed GNSS coordinates to an in-band Keylime agent. By routing sensor readings through the management processor's isolated hardware path, the geolocation data is collected and attested without any Host OS involvement.

### Architecture

1. **Management Processor Sensor Interface:** The management processor (BMC/iLO) interfaces with geolocation sensors (GNSS receivers, mobile modems) through dedicated I/O channels separate from the host CPU bus. Sensor readings are collected by the management processor independently of the host OS. The management processor can verify sensor firmware integrity as part of its Silicon Root of Trust chain.
2. **Management Processor Attestation:** The management processor reads sensor data, signs it with its own identity key (OEM CA chain), and associates the geolocation evidence with the host TPM EK identity. The geolocation hash can be extended into the TPM via the management processor's dedicated TPM bus, providing the same PCR binding as the Keylime option but through the out-of-band path.
3. **External Management Plane:** The management plane receives geolocation evidence from the management processor via the dedicated management NIC (Redfish API) and validates:
    - Sensor identity against registered sensor inventory.
    - Location reading against geofence policies.
    - Cross-verification with mobile network operator location services.
    - Association with the TPM EK identity from the Layer 2 attestation.
    - Consistency between the hardware-signed TPM Quote (obtained OOB) and the geolocation PCR value.

### Advantages

- Geolocation readings are hardware-isolated from the host OS -- immune to host-level malware and GNSS spoofing at the OS layer.
- Integrated with enterprise fleet management (same management plane as Layer 2 Option B).
- Suitable for high-security environments (defense, critical infrastructure).
- The same out-of-band TPM Quote that detects IMA/kernel subversion also verifies the geolocation PCR, providing a single hardware-attested evidence bundle.

### Limitations

- Requires management processor with geolocation sensor I/O capability.
- Vendor-specific sensor integration.
- Management processor firmware must be trusted.

## Composite Geolocation and Policy Enforcement

Regardless of the deployment option, the composite geolocation process combines multiple location sources to produce a quality-scored, verifiable location claim:

1. **GNSS Location:** Direct hardware-attested location from GNSS sensors (e.g., GPS, Galileo). Subject to spoofing risk but provides precise coordinates.
2. **Mobile Network Location:** Location from mobile network operator via GSMA/CAMARA API using device IMEI/IMSI. More resistant to spoofing than GNSS alone, as the mobile network independently verifies device location through cell tower triangulation.
3. **Auditor-Mediated Proof of Position (Fallback):** When no geolocation sensor is available, the sensor is offline, or the GNSS signal is weak (e.g., data center hosts deep inside a building), an auditor-mediated endorsement can provide a cryptographically verifiable physical position claim. As described in [[I-D.richardson-rats-pop-endorsement]], a human auditor physically visits the device, connects via a USB or serial console cable, and collects a signed Entity Attestation Token (EAT) from the device's TPM Attestation Key. The auditor then creates a signed Endorsement binding the device identity to its physical position (e.g., "Building 4, Aisle 37, Cabinet 9, Rack Unit 2-3"). This endorsement is periodically renewed through re-audit and provides a level of position precision (rack-level) that GPS cannot achieve indoors. The endorsement can be loaded directly into the device and passed along with Evidence to a Verifier.
4. **Composite Location:** The system fuses available location sources (GNSS, mobile network, and/or auditor endorsement), producing a composite location with a quality score. Discrepancies between sources trigger alerts.

Policy enforcement can then use the composite location to verify that the host is within the approved geographic boundary defined by the geofence policy.

# Scaling the Solution

Having a geolocation sensor on every host is not scalable from a deployment and management perspective and can be cost prohibitive. In the case of end user hosts, the geolocation sensor can be on a mobile host (e.g., smartphone with Mobile network capabilities and optionally GNSS capabilities) which can be leveraged by a laptop/desktop host which is proximal to the mobile host. The mobile host serves as the location anchor host. In the case of data center hosts, the geolocation sensor can be on a host with Mobile network and/or GNSS capabilities which can be leveraged by other data center hosts. This host serves as the location anchor host.

## End user location anchor host

The goal is to provide an easy-to-use wireless solution that can be used by end users without requiring them to install a geolocation sensor on their laptop/desktop host.

The smartphone can be used as a location anchor host for the laptop/desktop host. The smartphone connects to the laptop/desktop host using Bluetooth Low Energy (BLE) or Ultra-Wideband (UWB) technology and continuously measures the following:

  * signal strength of the laptop/desktop host
  * round-trip time (RTT) between the smartphone and laptop/desktop host

Host proximity manager periodically verifies that the smartphone provides proof that the laptop/desktop host is in proximity using the measured signal strength and RTT.

## Data center location anchor host

The goal is to provide an easy-to-use solution that can be used by data center operators without requiring them to install a geolocation sensor on every data center host.

PTP is a network protocol that enables precise synchronization of clocks across a computer network and can be used to measure the round-trip time (RTT) between the location anchor host and other data center hosts with sub-microsecond accuracy. To provide cryptographically verifiable proof of residency on the host -- referred to as "attested PTP" -- the PTP software/hardware can be enhanced so that all PTP messages are signed with a private key.

This signing can be done in two ways:

* Software-based: PTP software (e.g. Linux PTP daemon), after adding timestamp to PTP message, signs the PTP message with its private key -- Linux PTP daemon is a workload managed by workload identity manager. This approach may not provide sub-microsecond accuracy due to inherent software jitter, but it can still provide a reasonable approximation of the proximity of the other data center hosts to the location anchor host.
* Hardware-based: PTP hardware (e.g., SmartNIC), after adding timestamp to PTP message, signs the PTP message with its private key (e.g., SmartNIC DPU). The corresponding public key, used to verify the signatures, can be attested by the Host TPM Attestation Key (AK). This approach provides sub-microsecond accuracy and the perfect proximity measure of the other data center hosts to the location anchor host, and is suitable for data center environments where precise timing is critical.

Host proximity manager periodically verifies that the PTP daemon in the location anchor hosts provide proof that the PTP daemon in the application hosts are within the maximum DC round-trip delay from them. The PTP daemon is another workload managed by the workload identity manager.

Note that attested PTP is a proposed enhancement to the existing PTP hardware and software. For a detailed specification of hardware-rooted attestation for PTP, including verifiable residency and proximity proofs, see [[I-D.ramki-ptp-hardware-rooted-attestation]].

# Data Plane Geolocation Extensions

This section describes how geolocation information from Layer 3 attestation is conveyed in data plane protocols. For the underlying Proof of Residency (PoR) and DPoR mechanisms that bind workload identity to the WIA, see [[I-D.mw-wimse-transitive-attestation]].

## HTTP: Workload-Geo-ID Header

A new HTTP header field 'Workload-Geo-ID' is proposed for conveying the workload geolocation information from the Geolocation Information Cache. The header contains the following fields:

- The latest Geolocation Information Cache relevant to the client workload ID (thick clients) or user in OAuth bearer token/server website URL (thin clients) which has the following details: client workload location, client workload location type (e.g. precise, approximated, geographic region based), client workload location quality (e.g. GNSS, mobile network, Wi-Fi, IP address).
- Thick or Thin client flag: Indicates whether the client workload is a thick client (e.g., Microsoft Teams thick client app) or a thin client (e.g., Microsoft Teams thin client browser app).
- Type flag: Request signing with geolocation information or SVID with geolocation information.

The HTTP request is signed as described in [[I-D.mw-wimse-transitive-attestation]] using the workload or WIA private key. Intermediate proxies (e.g., API gateways, SASE firewalls) or server workloads can verify the Workload-Geo-ID and enforce geolocation policies.

Intermediate proxies or server workloads connect to the Composite Geolocation Manager to supply GNSS geolocation/workload identity agent ID and get attested composite location. The Composite Geolocation Manager can use the host TPM EK certificate in the Workload Identity Agent ID to retrieve the mobile geolocation sensor IMEI/IMSI from the Host hardware identity datastore. Using the IMEI/IMSI, they can retrieve the location of the host from the mobile network operator's location service.

Policy enforcement can be based on:

- Workload Identity Agent ID (running on the same host as the client workload),
- user in OAuth bearer token,
- server website URL,
- client workload ID (relevant only for thick clients),
- client workload location,
- client workload location type (e.g. precise, approximated, geographic region based),
- client workload location quality (e.g. GNSS, mobile network, Wi-Fi, IP address).

Besides native HTTP protocols, this solution also addresses browser-based Secure Shell (ssh) terminals and Remote Desktop Protocol (RDP) terminals which tunnel traffic over HTTP/TLS.

## HTTP: Geolocation in SVID

The workload SVID can be used to convey the geolocation information to the workload. The SVID is signed by the Workload Identity Manager and contains the workload's public key, the Workload Identity Agent ID, and the workload geolocation information.

The workload SVID can be conveyed in the 'Workload-Geo-ID' header field.

## IPSEC: Geolocation in IKEv2

In the IPSEC key exchange protocol (IKE), the following geolocation extensions are proposed:

* The IPSEC client includes the Geolocation Information from the Workload Identity Agent Geolocation Information Cache in the IPSEC IKEv2 notification payload.
* The IPSEC server extracts the Geolocation Information from the IKEv2 notification payload and connects to the Composite Geolocation Manager to get attested composite location.
* The IPSEC server can use the composite Geolocation Information to verify that the host is within the allowed geographic boundary.

For the Proof of Residency binding within the IPSEC IKEv2 key exchange (using the WIA public key as the ephemeral ECDHE key), see [[I-D.mw-wimse-transitive-attestation]].

Since IPSEC tunnel can encapsulate any IP traffic, geolocation attestation at the IPSEC level provides geographic verification for all traffic tunneled through it (e.g., RDP, SCTP, NFS, SSH). However, location information granularity is at the IPSEC client host level and not at the individual workload level.

# Confidential Computing Considerations

In confidential computing, the host operating system cannot be trusted. Instead, the platform owner must maintain and verify the relationships between three hardware identifiers:

* Hardware-rooted certification key -- Vendor-issued, CPU-bound asymmetric key pair used to either sign attestation evidence directly (AMD VCEK) or certify an attestation signing key (Intel PCK). Always anchored in the vendor's root CA.
    * AMD SEV-SNP "Versioned Chip Endorsement Key -- VCEK" is defined in the AMD SEV-SNP ABI specification (Chapter 1, Glossary, Table 2).
    * Intel TDX, "Provisioning Certification Key -- PCK" is defined in the Intel TDX DCAP Quoting Library API documentation (Page 6, Table 1-1: Terminology). Role: Certifies the Attestation Key inside the TDX Quoting Enclave, which signs the quote.
* TPM Endorsement Key (EK)
* Geolocation Sensor ID + public key

Proof of Residency:

* The confidential workload generates a hardware attestation that includes its hardware-rooted certification key.
* The platform owner receives this attestation and binds the reported hardware-rooted certification key to the TPM EK.
* This binding produces a cryptographic proof that the workload is running on the expected physical CPU.

Proof of Geolocation:

* The geolocation sensor creates a signed location report using its private key. This is supported in popular GNSS sensors such as u-blox.
* An agent on the bare-metal host periodically polls the sensor and collects these signed reports.
* The platform owner maps each sensor's ID and its signed geolocation to the corresponding CPU ID and TPM EK.
* This mapping yields a verifiable proof that the workload is executing at the claimed physical location.

Note: The Intel SGX Attestation Service utilizing the Enhanced Privacy ID (EPID) group-signature mechanism is a legacy, privacy-preserving attestation path. Intel has announced that this service will reach end-of-life on April 2 2025, after which EPID-based attestation will no longer be supported. This discussion focuses on current attestation models (e.g., ECDSA-based DCAP for SGX and PCK-based attestation for TDX) and excludes EPID/DAA from scope. ECDSA-based DCAP for SGX and PCK-based attestation for TDX are closely related in structure and trust model -- both are part of Intel's Data Center Attestation Primitives (DCAP).

# Solution Mapping to Industry Gaps

This section maps the layered attestation framework to the industry gaps identified in the Industry Gaps section.

* **Host TPMs for Signature** challenges are addressed by Layer 2 (TPM Platform Attestation): The WIA private key is used for signing, and the WIA public key is signed by the Host TPM APP private key providing a cryptographically verifiable proof of residency of the WIA on the host. Workloads use the WIA to sign requests, avoiding the TPM performance bottleneck (approximately 5 signatures/second).

* **Bearer Tokens**, **PoP Token**, **PoP via Mutual TLS** challenges are addressed by combining Layer 2 (this draft) with [[I-D.mw-wimse-transitive-attestation]]: HTTP request signature with the WIA private key provides a scalable and cryptographically verifiable proof of residency on host and workload identity. The transitive attestation draft defines the mTLS PoR and DPoR protocol flows that consume the WIA attestation established here.

* **IP Address-Based Location** and **Wi-Fi-Based Location** challenges are addressed by Layer 3 (Geolocation HW-Based Attestation): Combination of host-local location sensors (e.g., GNSS) with direct hardware-based attestation and mobile network location services provides a more reliable and cryptographically verifiable location than IP address, Wi-Fi-based methods or existing Host OS location services.

* **Trust in Transit** challenges are addressed by combining Layer 2 (this draft) with [[I-D.mw-wimse-transitive-attestation]]: the WIA-signed HTTP requests provide tamper-evident proof of origin, verified by intermediate proxies.

* **IPSEC** challenges are addressed via the geolocation extensions described in the Data Plane Geolocation Extensions section combined with the PoR mechanism in [[I-D.mw-wimse-transitive-attestation]].

# Authorization Policy Implementers

Policy implementers use attested geographic boundary from Workload to make decisions. Example implementers:

* Intermediate proxies (e.g., API gateway, Firewall)
* SaaS application.
* K8s node agent.
* OS process scheduler.

If the policy implementer is at the SaaS application level, things are simpler. However, if it is pushed down to, say, K8s or OS process scheduler or JVM class loader/deserializer, then malware can be prevented (similar to a code-signed application).

# Security Considerations

The proposed framework introduces several security considerations that must be addressed to ensure the integrity and trustworthiness of geofencing:

- **TPM and Hardware Trust**: The security of the solution depends on the integrity of the TPM and other hardware roots of trust. Physical attacks, firmware vulnerabilities, or supply chain compromises could undermine attestation. Regular updates, secure provisioning, and monitoring are required.

- **Geolocation Spoofing**: Location sensors (e.g., GPS) are susceptible to spoofing or replay attacks. Use of cryptographically authenticated signals (e.g., Galileo GNSS, mobile network) and cross-verification with multiple sources can mitigate this risk.

- **SIM and e-SIM Attacks**: Physical SIM removal or e-SIM swap attacks can break the binding between device and location. Continuous monitoring of device composition and periodic re-attestation are recommended.

- **Software Integrity**: The geolocation agent and supporting software must be protected against tampering. Use of Linux IMA, secure boot, and measured launch environments helps ensure only approved software is executed.

- **Communication Security**: All attestation and geolocation data must be transmitted over secure, authenticated channels (e.g., TLS) to prevent interception or manipulation.

- **Policy Enforcement**: The enforcement of geofence policies must be robust against attempts by malicious workloads or agents to bypass controls. Policy decisions should be based on verifiable, signed attestation evidence.

- **Time Source Integrity**: Trusted time sources are necessary to prevent replay attacks and ensure the freshness of attestation data.

- **Datastore Security**: The Host hardware identity datastore containing trusted host compositions and location sensor details must be protected against unauthorized access and tampering, using encryption and access controls.

- **Management Processor Security** (Option B): The management processor firmware and its communication channels to the management plane must be secured against tampering. OEM firmware signing and secure boot of the management processor are essential.

By addressing these considerations, the framework aims to provide a secure and reliable foundation for verifiable geofencing in diverse deployment environments.

# IANA Considerations

This document has no IANA actions.

# Appendix - Items to follow up

## OPEN ISSUES 1: Restart time attestation/remote verification of workload identity agent for integrity and proof of residency on Host

For the workload identity agent restart case, it is not clear how the storage in TPM PCR will be accomplished - ideally this should be natively handled in the IMA measurement process with an ability to retrigger on restart or refresh cycles.

## OPEN ISSUES 2: Location privacy options

The current approach includes some location privacy options for the geolocation in the Geolocation Information Cache. This may need to be expanded further in the future.

## OPEN ISSUES 3: Attested PTP (Partially Addressed)

Attested PTP is a software/hardware-based solution using Precision Time Protocol (PTP) for measuring proximity between hosts in a data center. For a detailed specification, see [[I-D.ramki-ptp-hardware-rooted-attestation]]. Standardization of the attested PTP mechanism is ongoing.

## OPEN ISSUES 4: Geotagging textual data

Popular standard for geotagging photos/videos is EXIF. There is no standard for geotagging textual data. If there is no geolocation tag, data can be stored/processed in non-compliant locations.

## OPEN ISSUES 5: Attesting Geotags

There is no standard for attesting (signing) geolocation tag. If geolocation tag is not signed, it can be manipulated through techniques such as VPNs.

# Appendix - Public References for Strict Data Residency Rules

India -- Reserve Bank of India (RBI): Payment System Data Localization (2018): From RBI Circular RBI/2017-18/153 (April 6, 2018): "All system providers shall ensure that the entire data relating to payment systems operated by them are stored in a system only in India. This data should include the full end-to-end transaction details / information collected / carried / processed as part of the message / payment instruction."

South Korea's Data Localization Regulations -- Geospatial Information Management Act (Spatial Data Act): Article 16, Paragraph 1: Prohibits the export of state-led survey data.

{backmatter}

<reference anchor="RFC9449" target="https://www.rfc-editor.org/rfc/rfc9449">
  <front>
    <title>OAuth 2.0 Demonstrating Proof of Possession (DPoP)</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett"/>
    <author initials="B." surname="Campbell" fullname="Brian Campbell"/>
    <author initials="J." surname="Bradley" fullname="John Bradley"/>
    <author initials="T." surname="Lodderstedt" fullname="Torsten Lodderstedt"/>
    <author initials="M." surname="Jones" fullname="Michael Jones"/>
    <author initials="D." surname="Waite" fullname="David Waite"/>
    <date month="September" year="2023"/>
  </front>
</reference>

<reference anchor="I-D.ietf-wimse-arch" target="https://datatracker.ietf.org/doc/html/draft-ietf-wimse-arch">
  <front>
    <title>Workload Identity in a Multi System Environment (WIMSE) Architecture</title>
    <author initials="Y." surname="Sheffer" fullname="Yaron Sheffer"/>
    <date month="October" day="21" year="2024"/>
  </front>
</reference>

<reference anchor="I-D.mw-wimse-transitive-attestation" target="https://datatracker.ietf.org/doc/html/draft-mw-wimse-transitive-attestation-00">
  <front>
    <title>Transitive Attestation for Workload Proof of Residency</title>
    <author initials="R." surname="Krishnan" fullname="Ram Krishnan"/>
    <author initials="A." surname="Prasad" fullname="A Prasad"/>
    <author initials="D." surname="Lopez" fullname="Diego R. Lopez"/>
    <author initials="S." surname="Addepalli" fullname="Srinivasa Addepalli"/>
    <date year="2025"/>
  </front>
</reference>

<reference anchor="galileo" target="https://defence-industry-space.ec.europa.eu/eu-space/galileo-satellite-navigation_en">
  <front>
    <title>Galileo Satellite Navigation</title>
    <author>
      <organization>European Commission, EU Space</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="doj-cisa" target="https://www.justice.gov/opa/pr/justice-department-implements-critical-national-security-program-protect-americans-sensitive">
  <front>
    <title>DOJ and CISA Issue New National Security Program to Regulate Foreign Access to Sensitive Data</title>
    <author>
      <organization>DOJ and CISA</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="tcg-geo-loc" target="https://trustedcomputinggroup.org/resource/trusted-computing-future-emerging-use-cases-and-solutions/">
  <front>
    <title>TCG keynote and whitepaper-Trusted Computing Future-Emerging Use Cases and Solutions</title>
    <author>
      <organization>TCG</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="tcg-tpm" target="https://trustedcomputinggroup.org/resource/trusted-platform-module-2-0-a-brief-introduction/">
  <front>
    <title>Trusted Platform Module 2.0-A Brief Introduction</title>
    <author>
      <organization>TCG</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="spire" target="https://spiffe.io/">
  <front>
    <title>SPIFFE/SPIRE workload identity</title>
    <author>
      <organization>Spire open source project</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="spire-tpm" target="https://github.com/bloomberg/spire-tpm-plugin">
  <front>
    <title>SPIFFE/SPIRE TPM plugin</title>
    <author>
      <organization>Spire open source project plugin</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="linux-ima" target="https://linux-ima.sourceforge.net/">
  <front>
    <title>Linux Integrity Measurement Architecture</title>
    <author>
      <organization>Sourceforge Linux IMA documentation</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="gsma-loc" target="https://www.gsma.com/solutions-and-impact/gsma-open-gateway/gsma-open-gateway-api-descriptions/">
  <front>
    <title>GSMA location API</title>
    <author>
      <organization>GSMA open gateway documentation</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="spiffe-x509-svid" target="https://github.com/spiffe/spiffe/blob/main/standards/X509-SVID.md">
  <front>
    <title>SPIFFE X.509-SVID Standard</title>
    <author>
      <organization>SPIFFE Project</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="spiffe-jwt-svid" target="https://github.com/spiffe/spiffe/blob/main/standards/JWT-SVID.md">
  <front>
    <title>SPIFFE JWT-SVID Standard</title>
    <author>
      <organization>SPIFFE Project</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="RFC7800" target="https://www.rfc-editor.org/rfc/rfc7800">
  <front>
    <title>Proof-of-Possession Key Semantics for JSON Web Tokens (JWT)</title>
    <author initials="M." surname="Jones" fullname="Michael B. Jones"/>
    <author initials="J." surname="Bradley" fullname="John Bradley"/>
    <author initials="H." surname="Tschofenig" fullname="Hannes Tschofenig"/>
    <date month="April" year="2016"/>
  </front>
</reference>

<reference anchor="RFC8705" target="https://www.rfc-editor.org/rfc/rfc8705">
  <front>
    <title>OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens</title>
    <author initials="B." surname="Campbell" fullname="Brian Campbell"/>
    <author initials="J." surname="Bradley" fullname="John Bradley"/>
    <author initials="N." surname="Sakimura" fullname="Nat Sakimura"/>
    <author initials="T." surname="Lodderstedt" fullname="Torsten Lodderstedt"/>
    <date month="February" year="2020"/>
  </front>
</reference>

<reference anchor="tpm-performance" target="https://stiankri.substack.com/p/tpm-performance">
  <front>
    <title>TPM Performance - How Fast is Your TPM?</title>
    <author>
      <organization>Stian Kristoffersen (Substack)</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="keylime" target="https://keylime.org/">
  <front>
    <title>Keylime</title>
    <author>
      <organization>Keylime open source project</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="hpe-ilo" target="https://www.hpe.com/us/en/servers/integrated-lights-out-ilo.html">
  <front>
    <title>HPE Integrated Lights-Out (iLO)</title>
    <author>
      <organization>Hewlett Packard Enterprise</organization>
    </author>
    <date/>
  </front>
</reference>

<reference anchor="I-D.richardson-rats-pop-endorsement" target="https://datatracker.ietf.org/doc/html/draft-richardson-rats-pop-endorsement-00">
  <front>
    <title>Proof of Position for Auditor managed Endorsements</title>
    <author initials="M." surname="Richardson" fullname="Michael Richardson"/>
    <date year="2024"/>
  </front>
</reference>

<reference anchor="I-D.ramki-ptp-hardware-rooted-attestation" target="https://github.com/ramkri123/ptp-asymmetric-authentication">
  <front>
    <title>Hardware-Rooted Attestation for Precision Time Protocol: Verifiable Residency and Proximity Proofs</title>
    <author initials="R." surname="Krishnan" fullname="Ram Krishnan"/>
    <date year="2025"/>
  </front>
</reference>

<reference anchor="AegisSovereignAI" target="https://github.com/lfedgeai/AegisSovereignAI/blob/main/hybrid-cloud-poc/README-arch-sovereign-unified-identity.md">
  <front>
    <title>Aegis Sovereign AI: End-to-End Sovereign Unified Identity and Trust Framework</title>
    <author initials="R." surname="Krishnan" fullname="Ram Krishnan"/>
    <date year="2025"/>
  </front>
</reference>
