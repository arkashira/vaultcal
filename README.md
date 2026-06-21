# vaultcal

`vaultcal` provides a minimal “one‑click” setup wizard for a self‑hosted
[Radicale](https://radicale.org/) server. The wizard:

* Generates a TLS certificate (simulated – no external network calls).
* Produces a default Radicale configuration that blocks the insecure
  `XML‑RPC` and `DAV` methods.
* Emits simple firewall rules that only allow traffic to the Radicale
  port (default 5232).

All logic lives in the standard library – no third‑party runtime
dependencies.

## Quick start
