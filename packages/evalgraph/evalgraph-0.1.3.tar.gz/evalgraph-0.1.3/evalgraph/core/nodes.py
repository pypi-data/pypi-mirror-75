import inspect,json
from evalgraph.core.graphevaluator import GraphEvaluator, NodeState
from evalgraph.core.scenariocontext import ScenarioContext

def node_helper(fn):
    def node_fn(*args):
        self = args[0]
        if len(args)>1:
            others = json.dumps(args[1:])
            others = f"({others[1:-1]})"
        else:
            others = ""
        tag = f'{self}.{fn.__name__}{others}'
        return Node.create(tag,lambda: fn(*args), obj=self, name=fn.__name__)
    return node_fn

### decorators
def node(fn):
    return property(node_helper(fn))

def nodefn(fn):
    return node_helper(fn)

    
class Node:
    def __init__(self,tag,cb, obj=None, name=None, scenario = None):
        self.tag = tag
        self.cb = cb
        self.deps = set()
        self.precedents = set()
        self.state = NodeState.INVALID
        self.value = None
        self.obj = obj
        self.name = name
        self.scenario = scenario

    def invalidate(self):
        if self.state == NodeState.INVALID:
            return
        if GraphEvaluator.verbose:
            print(f"Invalidating {self}")
        self.state = NodeState.INVALID
        self.value = None
        for node in self.precedents:
            node.invalidate()

    @property
    def Deps(self):
        return list(self.deps)

    @property
    def Precedents(self):
        return list(self.precedents)

    def In(self,scenario):
        return Node.create(self.tag,self.cb,self.obj,self.name,scenario)
    
    @staticmethod
    def create(tag,cb,obj,name,scenario = None):
        if scenario is None:
            scenario = ScenarioContext.CurrentScenario()
        if tag not in scenario.cache:
            scenario.cache[tag] = Node(tag,cb,obj=obj,name=name, scenario=scenario)
        return scenario.cache[tag]
    
    def set(self,cb):
        self.invalidate()
        if type(cb) != type(lambda: None):
            self.cb = lambda: cb
        else:
            self.cb = cb

    def reset(self):
        self.invalidate()
        del self.scenario.cache[self.name]
        
    def recalculate(self):
        self.invalidate()
        return self()
    
    def __repr__(self):
        return f'Node[{self.state}|{self.scenario}|{self.name}={self.value}]'
    def evaluate(self):
        return GraphEvaluator.evaluate(self)
    def __call__(self):
        return self.scenario.Evaluate(self)

    

