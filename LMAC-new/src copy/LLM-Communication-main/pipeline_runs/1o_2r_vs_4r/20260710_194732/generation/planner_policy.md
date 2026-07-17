### Agent Type / Agent ID Group
**Agent 0 (Overseer)**
**Role in this map:**
Vision / scout / relay agent. Overseer can see across the pit from the start and is the only agent that can spot the four Reapers. It must communicate enemy positions to its allied Roaches (agents 1, 2) so they can path around the pit and attack.

**Agent 1, 2 (Roaches)**
**Role in this map:**
Damage dealers. They start blocked from the enemy by terrain and rely on the Overseer’s messages to locate the Reapers. They should not send large messages back to the Overseer (Overseer already sees everything it can see), but they can send a simple alive/reachability signal.

---

## WHO Rules

| receiver | sender  | reason |
|----------|---------|--------|
| 1 (roach) | 0 (overseer) | Roach needs enemy locations from Overseer. |
| 2 (roach) | 0 (overseer) | Roach needs enemy locations from Overseer. |
| 0 (overseer) | 1 (roach) | Optional: roach reports its own status. |
| 0 (overseer) | 2 (roach) | Optional: roach reports its own status. |

All other edges (e.g. roach→roach, overseer→overseer, or roach→different roach) are always **off**.

---

## WHEN Rules

**(1) Edge overseer→roach1 (sender 0, receiver 1)**
**Trigger condition:** (any enemy_available == 1)  
- Check sender observation: `obs[sender, 4] == 1 or obs[sender, 11] == 1 or obs[sender, 18] == 1 or obs[sender, 25] == 1`.  
- If Overseer sees at least one enemy, it should communicate. This always true for Overseer at start, but handles case where enemies die.

**(2) Edge overseer→roach2 (sender 0, receiver 2)**
**Trigger condition:** Same as above: `obs[sender, 4] == 1 or obs[sender, 11] == 1 or obs[sender, 18] == 1 or obs[sender, 25] == 1`.

**(3) Edge roach1→overseer (sender 1, receiver 0)**
**Trigger condition:** `obs[sender, 46] > 0` (own health > 0, i.e., roach is alive). Always true unless dead.  
Rationale: Only send when alive.

**(4) Edge roach2→overseer (sender 2, receiver 0)**
**Trigger condition:** Same: `obs[sender, 46] > 0`.

---

## WHAT Rules

### Sender: Overseer (agent 0)

**Trigger 1: At least one enemy is available.**  
*(This is the same condition as the WHEN trigger. Execution in code: if WHEN is true for the edge, send these contents.)*  
**Selected contents/features (from sender’s own observation):**

- For **enemy 0**: indices 4,5,6,7,8,9,10  (available, distance, rel_x, rel_y, health, type_0, type_1) — 7 values  
- For **enemy 1**: indices 11,12,13,14,15,16,17 — 7 values  
- For **enemy 2**: indices 18,19,20,21,22,23,24 — 7 values  
- For **enemy 3**: indices 25,26,27,28,29,30,31 — 7 values  

Total message: **28 floats** (7 × 4 enemies).  
If some enemy is not available (available flag = 0), the remaining fields are still sent but less meaningful; that’s fine.

---

### Sender: Roach (agent 1 or 2)

**Trigger 1: Roach is alive (own_health > 0).**  
**Selected contents/features (from sender’s own observation):**

- own_health: index 46  (1 value)  
- own_type_0, own_type_1: indices 47,48  (2 values)  
- ally_0_visible: index 32 (indicates if roach can see the Overseer) (1 value)  

Total message: **4 floats**.

Rationale: roach does not have enemy info; only small status is useful to Overseer.

---

### Default / no-trigger behavior
- For any edge where WHEN condition is false, the sender transmits a zero vector of length equal to the described message dimension for that sender type.
- For edges not listed in WHO rules (e.g., roach→roach), the communication matrix entry is always 0.

---

## Summary for code generation

**communication_who(o):**  
Shape: [batch, 3, 3] (receiver, sender).  
Edges set to 1: (1,0), (2,0), (0,1), (0,2). All other edges 0.

**communication_when(o):**  
- For (1,0): (o[:,0,4]==1 | o[:,0,11]==1 | o[:,0,18]==1 | o[:,0,25]==1).float()  
- For (2,0): same.  
- For (0,1): (o[:,1,46] > 0).float()  
- For (0,2): (o[:,2,46] > 0).float()  

**communication_what(o):**  
- Agent 0 message dim = 28  
- Agent 1 message dim = 4  
- Agent 2 message dim = 4  

Extract:  
msg_0 = o[:,0, 4:32]   # 28 values (all enemy slots)  
msg_1 = torch.stack([o[:,1,46], o[:,1,47], o[:,1,48], o[:,1,32]], dim=-1)  
msg_2 = torch.stack([o[:,2,46], o[:,2,47], o[:,2,48], o[:,2,32]], dim=-1)  

If when condition is False for an edge, zero out the message for that receiver-sender pair in the communication matrix (mask).  

**communication_matrix(o):** = communication_who(o) * communication_when(o).  

**communication(o):** concatenate original obs [batch,3,49] with gathered WHAT messages according to the communication matrix. See LMAC base code for gather logic.