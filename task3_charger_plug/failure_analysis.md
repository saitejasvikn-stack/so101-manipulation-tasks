# Task 3: Why Charger Plugging Is Hard — Failure Analysis

Charger insertion is a fundamentally harder problem than pick-and-place or
pouring. This is documented here deliberately, since understanding *why*
a task fails is a legitimate and valuable outcome in its own right.

## 1. Precision tolerance

Pick-and-place tolerates several millimeters of grasp error. Insertion
needs alignment within a couple millimeters and correct rotational
orientation, or the connector simply won't seat.

## 2. Self-occlusion at the critical moment

As the gripper approaches the socket, it physically blocks its own
camera's view of the target. An overhead camera loses the socket behind
the gripper; even a wrist camera can end up too close or badly angled
right before contact — the policy effectively "goes blind" exactly when
precision matters most.

## 3. Errors compound instead of averaging out

Imitation-learned policies (ACT, Diffusion Policy) are inherently a little
noisy/approximate. For pick-and-place, this noise averages out into
"good enough." For insertion, a few mm of error on one axis plus a slight
rotational offset compounds into an outright failure, not a "slightly
worse but still working" result.

## 4. Sparse training signal on the hardest part

Demonstrations naturally spend most of their time on the "easy" part
(moving to the general area) and only a couple of seconds on the
actual final-approach-and-insert moment — meaning the policy gets
proportionally little training signal on exactly the hardest few
centimeters of the task.

## 5. No force/contact feedback

Humans plug in chargers partly by feel — nudge, feel resistance, adjust
angle, push through. This setup is vision + position control only, with
no force/torque sensing at the gripper, so it can't detect "I'm in
contact but at a bad angle" the way a hand can.

## 6. Mechanical backlash

Low-cost servos (compared to industrial arms) have small amounts of
gear play/backlash. Negligible for pick-and-place, but can consume the
entire error margin for a task requiring millimeter precision.

## Mitigations attempted / worth trying

- [ ] Diffusion Policy instead of ACT (better suited to contact-rich tasks)
- [ ] Wrist camera mounted as close as possible to the gripper
- [ ] 80+ demonstrations with deliberately slow, precise final approach
- [ ] Staged evaluation (`staged_evaluate.py`) to isolate which sub-stage
      is actually failing, rather than treating it as one binary outcome
- [ ] (Future work) Force/torque sensing at the gripper — an active
      research direction, not something solved by vision-only imitation
      learning

## Framing for presentation

> "Here's the standard imitation-learning pipeline that got pick-and-place
> and pouring working. Charger insertion exposes a real, known limitation
> of vision-only imitation learning: no force feedback, camera occlusion
> at the critical moment, and near-zero tolerance for the small errors
> these policies inherently have. This is an active research problem —
> a lot of current manipulation research is specifically about adding
> tactile/force sensing or hybrid vision+force control to solve exactly
> this class of task."
