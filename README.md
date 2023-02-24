# Puppitor
 A Python game interface, animation, and AI library designed to allow players to act out a character using physicality rather than dialogue

 Please note that this repository is currently being used to maintain a copy of Puppitor separate from its game development branch and 
 as such will not be updated frequently. The system is still in development and will not have documentation or examples created for 
 public use for some time.
 
# Directory Structure
`src`:
* `core` contains the modules needed for basic functionality in Puppitor:
    * `affecter.py` (contains state tracking and rules application code housed in the `Affecter` class as well as `make_affect_vector()` which is used to format a python dictionary for use with `Affecter` features)
    * `action_key_map.py` (contains input mapping and state tracking in the `Action_Key_Map` class for use either with keyboard, and mouse button, input or AI behavior algorithms, can be used to drive changes in state to be applied to `affect_vectors` using rules stored in an `Affecter`)

* `secondary`contains potentially useful modules in either driving or reacting to state changes in Puppitor's core modules:
    * `animation_structure.py` (contains the `Animation_Structure` class designed for reactive sprite animation based on the states tracked by an `Affecter` and `Action_Key_Map`)
    * `npc_greedy.py` (contains the `think` function that performs a greedy search over a given affect_vector, the `current_emotional_state` argument, using a given `action_key_map` and `affecter` as the basis for actions to try and effects to evaluate)
    * `npc_uct.py` (contains the `uct_think` function that performs Monte Carlo Tree Search based on given Puppitor inputs as well as the Node class for building trees)
    * `npc_a_star.py` (contains the `npc_a_star_think` function that performs A* search from a given `affect_vector` towards a `goal_emotion`)

`tools`:
* `a_star_unit_test.py` (tests a given rule file over each of its possible affects by starting an A* search from the least ideal state possible, the `goal_emotion` value at 0 and every other value in an affect vector at 1. Prints the results of each trial)
    * usage: `$ py a_star_unit_test.py ./affect_rules/test_passions_rules.json ./key_map.json resting neutral 180 F`
* `rule_file_validator.py` (tests a given rule file and affect vector to see if a particular affect is expressable using A* search)
    * usage: `$ py rule_file_validator.py ./affect_rules/test_passions_rules.json ./key_map.json ./affect_vector.json fear resting neutral 180 T <optional queue size limit argument>`

# Usage
To use Puppitor simply put `affecter.py` and `action_key_map.py` files in the desired directory and have `import affecter` and `import action_key_map` lines your project. Note that to use the components of `affecter.py` you will need to have JSON files formatted as Puppitor rules, examples can be found in `affect_rules`. Detailed API descriptions to come.

To run the validation files found in `tools` you will need to move them into a directory with `affecter.py`, `action_key_map.py`, and `npc_a_star.py` as well as a json rule file, json key map file and for `rule_file_validator.py` a json file with an affect vector in it
