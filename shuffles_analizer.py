import json

filename = "shuffles_to_4_abc"
filename_counter = filename+"_counterexamples"
counterexamples = []

with open(filename,'r') as file:
    json_data = json.load(file)

n = len(json_data)

for thing in json_data:
    if not thing["commuting_is_enough"]:
        counterexamples.append(thing)

counterexamples.insert(0,str(len(counterexamples))+" counterexamples out of "+str(n)+" tuples.")

json_str = json.dumps(counterexamples,indent=2)

with open(filename_counter, 'w') as file:
    file.write(json_str)
        
