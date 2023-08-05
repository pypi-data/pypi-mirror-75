class ScenarioContext:
    Stack = []
    
    @staticmethod
    def CurrentScenario():
        if not len(ScenarioContext.Stack):
            raise Exception("No scenario in context")
        return ScenarioContext.Stack[-1]

    @staticmethod
    def Push(scenario):
        ScenarioContext.Stack.append(scenario)
    
    @staticmethod
    def Pop():
        ScenarioContext.Stack.pop()
