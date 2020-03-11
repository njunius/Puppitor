#
# Animation_Structure contains nested dictionaries for storing frames of animation and where in the animation loop the simulation is
# the default arguments of Animation_Structure use theatrical terms for organization 
# 
# because of the way modifier_list and action_list are used in the construction of the nested dictionaries
# the order of the lists passed only determines the order of index arguments needed to access the values stored
# in either self.animation_frame_lists or self.current_frames
#
# NOTE: THE CURRENT DEFAULT OF final_frame_index IS A PLACEHOLDER MAKE SURE TO CHANGE IN PRODUCTION
# final_frame_index is strictly a bookkeeping variable and necessary for update_displayed_frame() to work properly
#
# frame_rate_delay is the number of frames to hold on before a new frame of animation is selected
# the default values assume a 60Hz rate of calling update_displayed_frame() and a desired animation rate of 10FPS
# 
class Animation_Structure:
    def __init__(self, frame_rate_delay = 5, frame_rate_map = {'tempo_up': 3, 'tempo_down': 5, 'neutral': 4}, modifier_list = ['tempo_up', 'tempo_down', 'neutral'], action_list = ['open_flow', 'closed_flow', 'projected_energy', 'resting'], affect_list = ['joy', 'anger', 'sadness', 'worry', 'love', 'fear']):
        
        # self.animation_frame_lists is a dictionary that uses modifiers to access actions to access individual frame lists
        self.animation_frame_lists = {}
        for modifier in modifier_list:
            self.animation_frame_lists[modifier] = {}
        for modifier in self.animation_frame_lists:
            for action in action_list:
                self.animation_frame_lists[modifier][action] = {}
        for modifier in self.animation_frame_lists:
            for action in action_list:
                for affect in affect_list:
                    self.animation_frame_lists[modifier][action][affect] = []
        
        # used to track the frame index of all animation lists
        self.current_frames = {}
        for modifier in modifier_list:
            self.current_frames[modifier] = {}        
        for modifier in self.current_frames:
            for action in action_list:
                self.current_frames[modifier][action] = 0
                
        # used to store the end points of each part of individual animation frame lists
        # to update the values to allow the update_displayed_frame() function to properly work:
        #
        # <Animation_Structure instance>.frame_index_delineators['<modifier>']['<action>']['startup'] = 6
        # <Animation_Structure instance>.frame_index_delineators['<modifier>']['<action>']['loop'] = 8
        # <Animation_Structure instance>.frame_index_delineators['<modifier>']['<action>']['final frame'] = len(<Animation_Structure instance>.animation_frame_lists['<modifier>']['<action>']['<affect>']) - 1
        #
        # the final frame line in the example assumes the desire is to have the final frame delineator as the last frame in the corresponding <Animation_Structure instance> animation_frame_list 
        # Animation_Structure assumes that 'startup' value < 'loop' value < 'final frame' value
        #
        self.frame_index_delineators = {}
        for modifier in modifier_list:
            self.frame_index_delineators[modifier] = {}
        for modifier in self.frame_index_delineators:
            for action in action_list:
                self.frame_index_delineators[modifier][action] = {'startup': 0, 'loop': 1, 'final frame': 2} # default values to be swapped out after the Animation_Structure is built (use load_animation_list() to add frames)
        
        self.current_displayed_frame = None
        self.current_animation_action = action_list[-1]
        
        # used for switching over to a new animation corresponding to the current action the player is taking once the previous animation has finished
        self.reached_end_of_frame_list = False
        
        # used for setting the frame rate of animations stored in this structure
        # default values assume an update rate of 60Hz creating an animation frame rate of 12FPS
        # needs to be set to have a default value (or if you do not want to use the variable frame rate options this is the only value you need to change)
        self.frame_rate_delay = frame_rate_delay
        
        # self.frame_rate_delay_map is an optional feature to allow for variable frame rates mapped to specific actions, modifiers, and affects that the Animation_Structure is tracking
        # passing frame_rate_map an empty dictionary will disable this feature
        self.frame_rate_delay_map = {}
        for act_mod in frame_rate_map:
            self.frame_rate_delay_map[act_mod] = frame_rate_map[act_mod]
        print(self.frame_rate_delay_map)
        
        # internal counter for advancing the frame rate delay
        self.frame_rate_delay_count = 0
        
    # used for putting full animations into the animation structure
    # frame_list is the set of animation frames to be added to the initialized animation_frame_lists
    # modifier, action, affect all correspond to where in the animation_frame_lists the animation frames will be stored (and by default should be strings)
    # startup_end_frame_index, loop_end_frame_index, final_frame_index are integer values used to mark off the different sections of the animation
    def load_animation_list(self, frame_list, modifier, action, affect, startup_end_frame_index, loop_end_frame_index, final_frame_index):
        for animation_frame in frame_list:
            self.animation_frame_lists[modifier][action][affect].append(animation_frame)
        self.frame_index_delineators[modifier][action]['startup'] = startup_end_frame_index
        self.frame_index_delineators[modifier][action]['loop'] = loop_end_frame_index
        self.frame_index_delineators[modifier][action]['final frame'] = final_frame_index
        return
    
    # should be used to access the currently displayed frame
    # should be returning a Sprite if used with RenPy
    def get_displayed_frame(self):
        return self.current_displayed_frame
        
    # returns the next frame in an animation sequence as well as the previous frame
    # this is primarily a book keeping function meant to allow a persistent
    # should be returning a Sprite if used with RenPy
    def update_displayed_frame(self, modifier, action, affect):
        # optional variable frame rate feature
        if self.frame_rate_delay_map:
            if modifier in self.frame_rate_delay_map:
                self.frame_rate_delay = self.frame_rate_delay_map[modifier]
            elif action in self.frame_rate_delay_map:
                self.frame_rate_delay = self.frame_rate_delay_map[action]
            elif affect in self.frame_rate_delay_map:
                self.frame_rate_delay = self.frame_rate_delay_map[affect]
        
        if self.frame_rate_delay_count < self.frame_rate_delay:
            self.frame_rate_delay_count += 1
        else:
            for mod in self.animation_frame_lists:
                # skip to returning to resting if the player has changed the energy state
                if self.current_animation_action != action:
                    if self.current_frames[mod][self.current_animation_action] < self.frame_index_delineators[mod][self.current_animation_action]['loop']:
                        self.current_frames[mod][self.current_animation_action] = self.frame_index_delineators[mod][self.current_animation_action]['loop'] + 1
                    else:
                        self.current_frames[mod][self.current_animation_action] += 1
                        if self.current_frames[mod][self.current_animation_action] > self.frame_index_delineators[mod][self.current_animation_action]['final frame']:
                            self.current_frames[mod][self.current_animation_action] = 0
                            self.reached_end_of_frame_list = True
                # startup animation
                elif self.current_frames[mod][self.current_animation_action] < self.frame_index_delineators[mod][self.current_animation_action]['startup']:
                    self.current_frames[mod][self.current_animation_action] += 1
                # loop animation 
                elif self.current_frames[mod][self.current_animation_action] <= self.frame_index_delineators[mod][self.current_animation_action]['loop']:
                    if self.current_animation_action != action:
                        self.current_frames[mod][self.current_animation_action] = self.frame_index_delineators[mod][self.current_animation_action]['loop'] + 1
                    else:
                        self.current_frames[mod][self.current_animation_action] += 1
                        if self.current_frames[mod][self.current_animation_action] > self.frame_index_delineators[mod][self.current_animation_action]['loop']:
                            self.current_frames[mod][self.current_animation_action] = self.frame_index_delineators[mod][self.current_animation_action]['startup'] + 1  # return to first frame of the loop
                # return to default animation
                elif self.current_frames[mod][self.current_animation_action] <= self.frame_index_delineators[mod][self.current_animation_action]['final frame']:
                    self.current_frames[mod][self.current_animation_action] += 1
                    if self.current_frames[mod][self.current_animation_action] > self.frame_index_delineators[mod][self.current_animation_action]['final frame']:
                        self.current_frames[mod][self.current_animation_action] = 0
                        self.reached_end_of_frame_list = True

            if self.reached_end_of_frame_list:
                self.current_animation_action = action
                self.reached_end_of_frame_list = False
            else:
                self.current_animation_action = self.current_animation_action
            self.frame_rate_delay_count = 0
        self.current_displayed_frame = self.animation_frame_lists[modifier][self.current_animation_action][affect][self.current_frames[modifier][self.current_animation_action]]
        return(self.animation_frame_lists[modifier][self.current_animation_action][affect][self.current_frames[modifier][self.current_animation_action]])
        