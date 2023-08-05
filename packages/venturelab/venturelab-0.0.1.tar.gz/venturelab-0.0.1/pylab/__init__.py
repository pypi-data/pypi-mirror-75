class Unit():
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.groups = []
        self.things = []
        
    def create_node(self, name, group, content=None):
        self.nodes.append({"name":name})
        self.things.append({"name":name})
        group['content'].append({'node':{"name":name, 'content':content}})
        node = {
            'name':name,
            'content':content 
        }
        return node

    def create_root(self, name):
        self.things.append({"name":name, 'content':[]})
        self.root = {
            'name':name,
            'content': []
        }
        
        return self.root

    def create_group(self, name, group, content=[]):
        self.groups.append({'name':name, 'content':content})
        self.things.append({"name":name, 'content':content})
        group['content'].append({'group':{'name':name, 'content':content}})
        group = {
            'name':name,
            'content': content
        }
        return group
    
    def view(self, vp):
        vl = {}
        vol = self.construct(vp, True)
        for thing in self.things:
            vl = {
                'conts': thing
            }
        
    def construct(vself, vp, vin):
        def col():
            if type(vp['name']) != str:
                return False
            else:
                return True
        vol = {
            'content':vp['content'],
            'structure':col()
        }
        if vin == True:
            if vol['structure'] == False:
                vol['structure'] = True
        return vol

def create_unit(name):
    unit = Unit(name)
    return unit

create_unit('nono')