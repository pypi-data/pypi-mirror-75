class Unit():
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.groups = []
        
    def create_node(self, name, group, content=None):
        self.nodes.append({"name":name, "root":group})
        group['content'].append({'node':{"name":name, "root":group}})
        node = {
            'name':name,
            'root':group,
            'content':content 
        }
        return node

    def create_root(self, name):
        self.root = {
            'name':name,
            'content': []
        }
        
        return self.root

    def create_group(self, name, group, content=[]):
        self.groups.append({'name':name, 'root':group})
        group['content'].append({'group':{'name':name, 'root':group, 'content':content}})
        group = {
            'name':name,
            'root':group,
            'content': content
        }
        return group