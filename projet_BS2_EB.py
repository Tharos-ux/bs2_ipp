def read_interaction_file_dict(file):
    dico_interactions = dict()
    with open(file,"r") as f:
        next(f)
        for line in f:
            key, value = line.split()
            if value in dico_interactions.keys() and key in dico_interactions[value]:  
                pass                        
            else :
                dico_interactions.setdefault(key,[]).append(value)
    return dico_interactions
        
print(read_interaction_file_dict("toy_example.txt"))

def read_interaction_file_list(file):
    list_interactions = list()
    with open(file,"r") as f:
        next(f)
        for line in f:
            if tuple(line.split())[::-1] not in list_interactions:
                list_interactions.append(tuple(line.split())) 
    return list_interactions

print(read_interaction_file_list("toy_example.txt"))
    