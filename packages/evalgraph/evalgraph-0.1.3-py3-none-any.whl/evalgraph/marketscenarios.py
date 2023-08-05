from evalgraph.core.scenarios import Scenario, BaseScenario
from evalgraph.core.scenariocontext import ScenarioContext
from evalgraph.option import Underlier, Option

class SpotShiftScenario(Scenario):
    def __init__(self, shift, source = None):
        super().__init__(source)
        self.shift = shift
        
    def __repr__(self):
        return f'SpotShiftScenario({self.shift})'
        
    def ProvidesFormula(self, node):
        return node.name == 'Spot'
    
    def Formula(self, node):
        def get_spot():
            return node.In(self.Source)() + self.shift
        return get_spot

if __name__ == "__main__":
    from evalgraph.option import NodeObject
    from evalgraph.nodes import node

    ScenarioContext.Stack.append(BaseScenario())

    und = Underlier(Ticker='SPY')
    opt = Option(OptionType='C')#,Underlier=und,Strike=und.Spot())
    scen = SpotShiftScenario(BaseScenario(),10)

    price = opt.Price()
    deps = opt.Price.Deps
    price2 = opt.Price.In(scen)()
    deps2 = opt.Price.In(scen).Deps
    diff = price2 - price
    print(diff)
    print(len(deps))
    print(len(deps2))
    a = 1
