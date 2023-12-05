import common_advent as advent
terminal = advent.get_input(__file__)

class Folder():
    def __init__(self, name, parent = None, children = []) -> None:
        self.name = name
        self.parent = parent
        self.children = []
        self.size = 0
        for child in children:
            self.children.append(child)

    def find(self, childname):
        for child in self.children:
            if child.name == childname:
                return child
        return None
    
    def __str__(self) -> str:
        return f"{self.name} (dir, {self.size})"
    
    def __lt__(self, folder):
        return self.size < folder.size

    def __add__(self, o):
        return self.size + o
    
    def __radd__(self, other):
        if other == 0:
            return self.size
        else:
            return self.__add__(other)
    
    def update_size(self):
        size = 0
        for child in self.children:
            size += child.size
        self.size = size


class File():
    def __init__(self, size, name) -> None:
        self.size = int(size)
        self.name = name
    
    def __str__(self) -> str:
        return f"{self.name} (file, {self.size})"
    
#create dummy root to handle first line defining '/'
root_folder = Folder(name = 'root', children=[Folder(name = '/')])
current_folder = root_folder

for line in terminal:
    if '$' in line: # command
        if 'cd' in line:
            if '..' in line:
                current_folder = current_folder.parent
            else:
                next_folder = current_folder.find(line.split()[-1])
                current_folder = next_folder
        else:
            pass # $ ls needs no handling
    else: # return from system
        vals = line.split()
        if 'dir' in vals[0]: #avoid mistakes with files that have 'dir' as a substring of the name
            new_folder = Folder(name = vals[-1], parent = current_folder)
            current_folder.children.append(new_folder)
        else:
            new_file = File(*vals)
            current_folder.children.append(new_file)

root_folder = root_folder.children[0] # remove dummy folder

visited = set()
tree_view = ''

def search(folder, depth):
    global tree_view
    if folder not in visited:
        for child in folder.children:
            tree_view += f"{''.join([' ' for x in range(depth)])}-{child}\n"
            if 'Folder' in str(type(child)):
                search(child, depth + 1)
        folder.update_size()
        visited.add(folder)

search(root_folder, 0)

if False: # lazy toggle
    print(tree_view)

threshold = 100000
sum = sum(list(filter(lambda n: n.size <= threshold, visited)))
print(f"sum of folders lte threshold : {sum}")

max_size = 70000000
req_size = 30000000
dif_size = req_size - (max_size - root_folder.size)

min_req = min(list(filter(lambda n: n.size >= dif_size, visited)))
print(f"delete folder : {min_req}")



