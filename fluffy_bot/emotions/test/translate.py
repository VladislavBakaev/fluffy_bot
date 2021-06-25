import json 
if __name__ == '__main__':
    file_name = "happy_1_109_sequence.json"
    new_name = "happy_1"
    translated = {'emotion': new_name, 'frame_list': []}
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
        frames = data["frame_list"]
        i = 0
        for position in frames:
            t_1 = position["positions"][0]['pos']
            t_2 = position["positions"][1]['pos']
            t_3 = position["positions"][2]['pos']
            b = position["positions"][3]['pos']
            t = position["millis"]/1000
            frame = {"num": i,
            "pos": [t_1, t_2, t_3, b, 0],
            "vel": [300,300,300,100,300],
            "slope": [255,255,255,100,255],
            "delay": t}
            i+=1
            translated['frame_list'].append(frame)
        with open("/home/rodion/PROJECTS/fluffy_bot/emotions/"+new_name+'.json', 'w') as outfile:
            json.dump(translated, outfile, sort_keys=True, indent=2)

            