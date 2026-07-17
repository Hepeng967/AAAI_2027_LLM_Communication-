### Agent Type / Agent ID Group
All agents are Zealots (IDs 0-4). All share the same role.

**Role in this map:**
- All Zealots are both damage dealers and potential wounded baits.
- Priority: protect low-health allies by drawing enemy fire, focus-fire the Ultralisk when healthy, and retreat when wounded.

**WHO Rules:**
- Only communication from any Zealot to all other Zealots.
- Specifically, for each receiver r and sender s: if s != r, communication is allowed.
- No self-communication.
- (Sparse unidirectional broadcast from each agent to all others.)

**WHEN Rules:**
- Communication edge (r, s) is triggered if either of the following conditions is true for the sender s:
  1. `sender's own_health < 20` i.e. observation[s][33] < 20.0  (low health distress signal)
  2. `sender sees enemy_0_available == 1` i.e. observation[s][4] > 0.5  (enemy visible, so combat information is relevant)
- Default: no communication.

**WHAT Rules:**

*Note: All content selections refer to indices in the sender’s own observation vector of length 36.*

1. **Trigger: own_health < 20.0 (sender is wounded and retreating)**
   - Selected contents/features:
     - `own_health` (index 33)
     - `own_shield` (index 34)
     - `enemy_0_available` (index 4)
     - `enemy_0_distance` (index 5)
     - `enemy_0_rel_x` (index 6)
     - `enemy_0_rel_y` (index 7)
     - `enemy_0_health` (index 8)
   - Indices: [4, 5, 6, 7, 8, 33, 34]

2. **Trigger: enemy_0_available == 1 AND own_health >= 20.0 (sender is healthy and fighting)**
   - Selected contents/features:
     - `enemy_0_available` (index 4)
     - `enemy_0_distance` (index 5)
     - `enemy_0_rel_x` (index 6)
     - `enemy_0_rel_y` (index 7)
     - `enemy_0_health` (index 8)
     - `own_health` (index 33)
   - Indices: [4, 5, 6, 7, 8, 33]

**Default / no-trigger behavior:**
- When neither trigger is active, the sender sends nothing: a zero-mask (all zeros).