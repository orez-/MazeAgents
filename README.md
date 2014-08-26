MazeAgents
==========

## Abstract ##
From the jumping-off point of "have a guy navigate a maze," it would be neat to add "have a team of guys coordinate navigation of a maze" and furthermore "have multiple teams of guys competitively coordinate navigation of a maze, and have the teams try to sabotage each other". Early versions of this idea had one of the teams game-controlled, with the goal of getting a better time than other AIs, or just two AIs competing directly, with everyone unsure of who was friend and who was foe. Unfortunately, this would likely just lead to reclusive agents who spoke in a corrupted dialect of the communication API, only recognizable amongst themselves, defeating the entire point. By adding allied teams under the control of a game AI and predicating victory on their success through the maze, the agents have more incentive to speak in a universally accepted dialect. However, this puts the responsibility of victory in the intelligence of the game AI, potentially leading to over-design around its specific patterns. Teams of AI players seems to avoid this problem, but has more problems with agent identification mechanics. The agents need some way of identifying allies in a way that does not reveal the opponents as clearly untrustworthy.

By adding another team's completion of the maze as a condition for victory, we are able to add the question of trust to the mix. Agents are no longer sure if other teams are being helpful or unhelpful, and have to make judgements on what to do with the (potentially false) information provided to them.


## Game setup ##
- Generate a maze (maybe have a bunch of different styles to cycle through)
- n teams (n ≥ 4)
- m agents per team, distributed around the maze as defined by the maze style
  - Possibly want to avoid clumping, but leave it up to the maze gen.
- Each agent on a team has the same AI, written by the players (their interaction with the game)
- Goal is to have all agents escape the maze, as well as all the agents of one of the other teams, eg A needs A and B, B needs B and C, etc. No teams share a dependent, and each team is a dependent of exactly one team. Teams know which team is their dependent, but not which team they are a dependent for.
- In the not unlikely event of a tie (eg A and C are finished when B finishes), victory is awarded to the team who finished first. In the unlikely event that both finished at the same time, the result is a draw.


## Agent Senses ##
#### Sight ####
- An agent is fed information about the board state based on their line of sight. They know definitively which squares are in sight and which are not.
- If another agent is in an in-sight square, that agent is able to be identified by team.
  - VARIANT: can agents identify individuals? Probably.

#### Hearing ####
- Agents are able to communicate through a standardized API documented below. Agents hear any conversations in-range, and may act as they please with the heard (or overhead) information. If the speaking agent is in sight the voice is clearly associated with them.
- VARIANT: able to identify team by voice?
- VARIANT: able to identify individual by voice? (this would make the in-sight check moot but this should be a design choice)


## Communication API ##
- VARIANT: data limit
- DESIGN: sound travel mechanics
