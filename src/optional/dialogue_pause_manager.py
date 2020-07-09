#
# Dialogue_Pause_Manager is a small helper class used to track state information if dynamic pausing of dialogue printout is part of the game loop
#
class Dialogue_Pause_Manager:
    def __init__(self, defined_afm_time, in_line_afm_time = 2):
        # should be Ren'Py auto forward time stored in the preferences
        self.user_afm_time = defined_afm_time
        
        # auto forward time used in the middle of printing a line of dialouge to
        # maintain a relatively smooth printout (should be a low number
        self.in_line_afm_time = in_line_afm_time
        
        # used to pause the printout of a line at the next wait tag in Ren'Py
        self.afm_pause_time = 0
        
        # flag to determine when player controlled pausing of lines should happen
        self.speaking = False
        
        # counter for tracking where in a line the player has gotten to
        self.num_words_said = 0
        
        # dictionary to store character name colors for use with dialogue
        self.character_colors = {}
