# Puppitor
 A Python game interface, animation, and AI library designed to allow players to act out a character using physicality rather than dialogue

 Please note that this repository is currently being used to maintain a copy of Puppitor separate from its game development branch and 
 as such will not be updated frequently. The system is still in development and will not have documentation or examples created for 
 public use for some time.
 
# Directory Structure
 `core` contains the modules needed for basic functionality in Puppitor:
 * `affecter.py` (contains state tracking and rules application code housed in the `Affecter` class as well as `make_affect_vector()` which is used to format a python dictionary for use with `Affecter` features)
 * `action_key_map.py` (contains input mapping and state tracking in the `Action_Key_Map` class for use either with keyboard, and mouse button, input or AI behavior algorithms, can be used to drive changes in state to be applied to `affect_vectors` using rules stored in an `Affecter`)
 
 `secondary`contains potentially useful modules in either driving or reacting to state changes in Puppitor's core modules:
 * `animation_structure.py` (contains the `Animation_Structure` class designed for reactive sprite animation based on the states tracked by an `Affecter` and `Action_Key_Map`)
 * `npc_greedy.py` (contains the `think` function that performs a greedy search over a given affect_vector, the `current_emotional_state` argument, using a given `action_key_map` and `affecter` as the basis for actions to try and effects to evaluate)
