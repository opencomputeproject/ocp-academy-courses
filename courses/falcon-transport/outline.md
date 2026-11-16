# Falcon Transport — 60-minute course outline

One narrated Slides course in one SCORM 1.2 package. Four tracked SCOs: Course Home, followed by the three modules below. Technical learners should know Ethernet, RDMA and basic congestion control.

Course Home introduces the course, the three modules, scope and estimated time.

## Module 1: Transaction Architecture — about 20 minutes

1. Transaction Architecture
2. Follow the work across a connection (p. 9, p. 10)
3. Two layers, four peer roles (p. 9, p. 10, p. 11, p. 14)
4. Connection, transaction, packet (p. 13, p. 14, p. 15, p. 19, p. 31, p. 32)
5. A push: receipt before acknowledgement — animated worked flow (p. 11, p. 12, p. 22, p. 63)
6. A pull: an ACK is not the response — animated worked flow (p. 12, p. 20, p. 21, p. 58, p. 59)
7. Reserve metadata. Allocate buffers on arrival. — animated worked flow (p. 47, p. 48, p. 49, p. 50, p. 51, p. 52, p. 53, p. 58, p. 59, p. 70, p. 114)
8. Negotiate behavior, not a revision number (p. 9, p. 31, p. 113, p. 114)
9. Keep the evidence separate (p. 11, p. 12, p. 14, p. 51, p. 58, p. 114)
10. Test the transaction model (p. 11, p. 12, p. 22, p. 51, p. 52, p. 53, p. 58, p. 59, p. 114)
11. Up next

## Module 2: Reliable Delivery and Loss Recovery — about 20 minutes

1. Reliable Delivery and Loss Recovery
2. Follow the recovery evidence
3. Capacity, receipt, and acknowledgement (p. 40, p. 41, p. 64, p. 65, p. 76, p. 77)
4. Repair the hole; preserve received packets — animated worked flow (p. 28, p. 29, p. 73, p. 74)
5. RACK tests time within known feedback — animated worked flow (p. 65, p. 74, p. 75)
6. A quiet-tail probe restarts feedback — animated worked flow (p. 75, p. 76, p. 77, p. 113, p. 114)
7. Retry ownership follows acknowledgement (p. 23, p. 24, p. 25, p. 26, p. 63, p. 64, p. 110)
8. Restore sequence progress; preserve the error (p. 26, p. 27, p. 64, p. 76, p. 78, p. 86, p. 110)
9. Name the evidence before choosing recovery
10. Check the recovery decisions (p. 26, p. 27, p. 63, p. 74, p. 75, p. 78, p. 113, p. 114)
11. Up next

## Module 3: Congestion Control and Multipathing — about 20 minutes

1. Congestion Control and Multipathing
2. Follow the feedback loop (p. 16, p. 88)
3. Measure fabric delay across two clocks — animated worked flow (p. 39, p. 45, p. 88, p. 89, p. 90)
4. Swift separates fabric and receiver pressure (p. 90, p. 91, p. 92, p. 93, p. 94, p. 95, p. 96)
5. CSIG reflects a signal, not an algorithm (p. 17, p. 18, p. 114)
6. One connection, up to four flows (p. 16, p. 69, p. 71, p. 72, p. 84)
7. An ACK reopens the original path — animated worked flow (p. 16, p. 17, p. 71, p. 72, p. 84, p. 94)
8. PLB changes routes after sustained congestion — animated worked flow (p. 96, p. 97, p. 98, p. 99, p. 114)
9. Four distinctions to keep (p. 88, p. 94, p. 97)
10. Check the feedback loop (p. 72, p. 84, p. 88, p. 89)
11. Course complete

## Boundaries and references

ULP mappings, application APIs, drivers, RTL, registers and NIC microarchitecture are excluded. Worked numbers illustrate protocol behavior, not deployment settings. Quizzes cite the actual specification pages; the table of contents contains stale page references.

The research and overlap audit is in references.md. Links to MRC, SUE-T and other networking courses provide context without equating their transport mechanisms. Summit recordings are optional further learning and excluded from the 60-minute estimate.
