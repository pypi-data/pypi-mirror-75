from evalgraph.core.scenariocontext import ScenarioContext


class Scenario:
    _source = None
    def __init__(self,source = None):
        if source is None:
            source = ScenarioContext.CurrentScenario()
        self._source = source
        self.cache = {}

    def __enter__(self):
        ScenarioContext.Push(self)
    
    def __exit__(self, *_):
        ScenarioContext.Pop()
        
        
    @property
    def Source(self):
        return self._source

    def ProvidesFormula(self, node):
        raise NotImplementedError("Needs to be implemented in derived class")
    def Formula(self, node):
        raise NotImplementedError("Needs to be implemented in derived class")

    def Evaluate(self, node):
        ScenarioContext.Stack.append(self)
        if self.ProvidesFormula(node):
            value = self.Formula(node)()
        else:
            value = self.Source.Evaluate(node)
        ScenarioContext.Stack.pop()
        return value
    
class BaseScenario(Scenario):
    def __init__(self):
        self.cache = {}
    
    def Evaluate(self, node):
        return node.evaluate()
