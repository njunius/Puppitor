#
# Scene_Parser is a simple parsing utility that assumes the format of a scene is as follows:
#       <Scene Title and/or number> 
#       character name: dialogue
#       (stage direction)
# NOTE: if there is any non-alphanumeric character THAT IS NOT A '(' in the first character of a line in the script IT WILL BE IGNORED BY THE PARSER
# 
class Scene_Parser:
    def __init__(self, scene_script, stage_directions = False):
        
        # flag for determining whether to include stage directions in the processed scene
        self.stage_directions = stage_directions
        
        # the scene with extra line breaks culled and turned into a list of tuples of format:
        # ('<character name>', '<character dialogue>')
        self.processed_scene = []
        self.num_lines_processed = 0
        
        # the scene as read directly from the file opened and passed in as scene_script
        # local variable since this information is not useful in future usage at this time and takes up memory
        scene_script_raw = scene_script.readlines()
        
        # the scene with all the empty line breaks removed and leading and trailing whitespace removed
        # local variable since this information is not useful in future usage at this time and takes up memory
        script_new_line_culled = []
        
        for line in scene_script_raw:
            if line != '\n':
                script_new_line_culled.append(line.strip())

        # process the stripped line into the ('<character name>', '<character dialogue>') tuple format
        for line in script_new_line_culled:
            # use '(' as a marker for stage directions and add it to the processed scene if the parser is processing stage directions
            # otherwise only add lines with the format '<character name>: <dialogue>'
            if line[0] == '(' and self.stage_directions:
                self.processed_scene.append(('',line))
            elif line[0].isalpha() or line[0].isdigit():
                split_line = line.split(': ')
                self.processed_scene.append((split_line[0], split_line[1]))
                
        self.num_lines_processed = len(self.processed_scene)
        
        print(self.processed_scene)
        print(self.num_lines_processed)
        
    # returns the tuple of ('<character name>', '<line of dialogue>') representing the line with the specified number in the scene
    def get_scene_line(self, line_num):
        if line_num < 0 or line_num > self.num_lines_processed:
            print('INVALID INDEX WHEN REQUESTING A LINE FROM A SCENE')
            return
        else:
            return self.processed_scene[line_num]