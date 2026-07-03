import json
import random

inject_wave_timing=30
competition_duration=360
max_num_of_injects=36
min_injects_per_drop=1
max_injects_per_drop=5
num_of_drops=competition_duration // inject_wave_timing # should this be calculated in the function?

def random_gen_injects(inject_wave_timing,competition_duration,max_num_of_injects,min_injects_per_drop,max_injects_per_drop,num_of_drops,pre_chosen_inject_ids=[]):
    injects_to_use=[]

    with open('injects.json', 'r') as f:
        injects = json.load(f)

    for drop_num in range(num_of_drops):
        drops = []
        num_injects_this_drop = random.randint(min_injects_per_drop,max_injects_per_drop)

        for inject_num in range(num_injects_this_drop):
            if len(injects) <= 0:
                continue
            if len(pre_chosen_inject_ids) == 0:
                inject_id = random.choice(list(injects.keys()))
            else:
                inject_id = random.choice(pre_chosen_inject_ids)
                pre_chosen_inject_ids.remove(inject_id)
            inject = injects[inject_id]
            inject["drop_time_from_start"] = inject_wave_timing * drop_num
            drops.append(inject)
            injects.pop(inject_id)
        injects_to_use.append(drops)
    return injects_to_use

injects_to_use = random_gen_injects(inject_wave_timing,competition_duration,max_num_of_injects,min_injects_per_drop,max_injects_per_drop,num_of_drops)
# injects_to_use = random_gen_injects(inject_wave_timing,competition_duration,max_num_of_injects,min_injects_per_drop,max_injects_per_drop,num_of_drops, ["1", "7", "3", "4"])

print(injects_to_use[0])
