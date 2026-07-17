### Agent Type / Agent ID Group
**All agents: Zealot (IDs 0-4, all identical type)**

**Role in this map:**
- **Low-health Zealot (own_health < 20%):** Retreat and kite; needs to inform others of its wounded state so they can protect it.
- **Healthy Zealot (own_health >= 20%):** Engage the Ultralisk, focus fire, and protect wounded allies by drawing aggro.

---

### WHO Rules
- Each agent sends to all other agents (broadcast), but only the **sender’s identity** and **critical status** are relevant.
- The receiver uses the received message update its understanding of which ally is wounded or healthy.
- **Sender→Receiver:** All-to-all (every agent to every other agent), but with strong **WHEN** gating to avoid constant chatter.

---

### WHEN Rules (per sender-receiver edge, both directions)
- **Trigger condition:** The sender’s **own_health** (index 33) is less than 0.20 **OR** the sender’s **ally_0_visible** (index 9) is 1 and the corresponding ally has health < 0.20 (for a wounded ally that is visible).
- More precisely, the sender triggers **only** when:
  - `own_health < 0.20` (sender is wounded), OR
  - any ally that is visible (`ally_i_visible` == 1) has `ally_i_health < 0.20` (sender sees a wounded ally).
- **Else:** No communication (all-zero message).

---

### WHAT Rules (sender contents)

#### 1. Trigger: `own_health < 0.20` (sender is wounded)
The wounded Zealot broadcasts its **own health** and **own shield** so others know its exact low status.
- **Selected contents/features:**
  - `own_health` (index 33)
  - `own_shield` (index 34)

#### 2. Trigger: any `ally_i_visible` == 1 and `ally_i_health < 0.20` (sender sees a wounded ally)
The healthy Zealot broadcasts the **relative position** of the wounded ally and the **ally’s health** so others can locate and protect that ally.
- **Selected contents/features:**
  - For the first visible wounded ally (iterate order 0,1,2,3):
    - `ally_i_rel_x` (index 11 + 3*i)
    - `ally_i_rel_y` (index 12 + 3*i)
    - `ally_i_health` (index 13 + 3*i)

#### 3. Trigger: no wounded ally visible and own health >= 0.20 (normal state)
- **Selected contents/features:**
  - No information sent (all zeros).

---

### Default / No-Trigger Behavior
When no trigger condition is met (no wounded ally visible and own health >= 0.20), the sender transmits an all-zero message of length 35. This keeps the communication sparse and avoids unnecessary bandwidth.

---

### Implementation Notes for Code Generation
- **communication_who(o):** Always return a tensor of shape `[batch, 5, 5]` with all entries = 1 (all-to-all edges). The sparsity is enforced by **WHEN**.
- **communication_when(o):** Return a mask of shape `[batch, 5, 5]`, where each entry is 1 if the sender's trigger is active, else 0.
- **communication_what(o):** Return a tensor of shape `[batch, 5, 35]`. For each sender agent i:
  - If `o[batch, i, 33] < 0.20`: set indices 33 and 34 to 1, all else 0.
  - Else if any `o[batch, i, 9 + 3*j] == 1` and `o[batch, i, 13 + 6*j] < 0.20` (for j=0..3): set indices 11+3*j, 12+3*j, 13+6*j to 1 for the first such j; all else 0.
  - Else: send all zeros.