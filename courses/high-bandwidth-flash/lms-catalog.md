**Title**\
High Bandwidth Flash: Bridging SSD Capacity and HBM Performance

**Short Description**\
Explore HBF architecture, host interfaces, memory management, and placement of AI model weights and KV cache.

**Long Description**

Explore High Bandwidth Flash as a NAND-based memory tier between SSD capacity and HBM performance for AI systems. Follow the OCP HBF architecture from stacked dies and host channels to transaction rules, address interleaving, and software responsibilities. Evaluate how workload behavior, reliability, and memory placement affect its use for AI serving.

**Overall duration: 37 minutes**

**Module 1: Why AI Needs a New Memory Layer — 10 minutes.**\
Explain the AI memory bottleneck, position HBF alongside SSDs and HBM, and interpret the specification's capacity, bandwidth, and open integration boundaries.

**Module 2: How HBF Connects Capacity to the xPU — 14 minutes.**\
Trace base and core dies, UCIe channels, AXI transactions, page geometry, and address interleaving. Connect host access patterns to available parallel bandwidth.

**Module 3: Programming HBF for AI Serving — 13 minutes.**\
Review separate HBM and HBF management, NAND-aware writes, lifecycle and recovery responsibilities, and channel allocation. Compare placement strategies for model weights and KV cache.
