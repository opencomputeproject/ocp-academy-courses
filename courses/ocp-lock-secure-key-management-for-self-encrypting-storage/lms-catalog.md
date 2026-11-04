**Title**\
OCP L.O.C.K.: Secure Key Management for Self-Encrypting Storage

**Short Description**\
Trace L.O.C.K. trust boundaries, key lifecycles, controller interfaces, and secure retirement of self-encrypting storage.

**Long Description**

Explore the OCP L.O.C.K. Specification v1.1 for secure key management in self-encrypting storage. Follow the threat model and protected media-key path through a layered key hierarchy, lifecycle transitions, controller interfaces, and reset behavior. Knowledge checks help learners connect confidentiality, cryptographic retirement, and implementation requirements to an integration review.

**Overall duration: 51 minutes**

**Module 1: L.O.C.K.: Layered Open-source Cryptographic Key Management — 14 minutes.**\
Explain the storage retirement problem, firmware threat model, Key Management Block, and protected media-key path. Distinguish confidentiality and irreversible erasure from availability concerns.

**Module 2: Key Hierarchy and Lifecycle — 19 minutes.**\
Trace protection keys, multi-party authorization, epoch transitions, and persistence classes. Compare random and derived media keys and connect reset behavior to operational retirement boundaries.

**Module 3: Controller Integration and Compliance — 18 minutes.**\
Separate control-mailbox operations from protected key transfer. Sequence initialization and key operations, map host protocols, and review reset, timeout, cache-clearing, and mandatory compliance behavior.
