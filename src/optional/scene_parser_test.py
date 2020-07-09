import scene_parser

scene_dict = {}

scene_memory = open('smallscene.txt', 'r')

test_parser = scene_parser.Scene_Parser(scene_memory)
print()
scene_memory = open('smallscene.txt', 'r')
test_parser_stage_dir = scene_parser.Scene_Parser(scene_memory, True)

print()
print(test_parser.get_scene_line(0))
print(test_parser.get_scene_line(-1))
print(test_parser.get_scene_line(150))
print(test_parser.get_scene_line(50))