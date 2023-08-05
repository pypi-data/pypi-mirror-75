class NodeState:
    INVALID = 'NODESTATE_INVALID'
    VALID = 'NODESTATE_VALID'
    CALCULATING = 'NODESTATE_CALCULATING'

class GraphEvaluator:
    verbose = True
    node_stack = []
    
    @staticmethod
    def evaluate(node):
        if node.state == NodeState.CALCULATING:
            nodes = " depends on\n".join([str(n) for n in GraphEvaluator.node_stack + [node]])
            raise Exception("Circular reference: \n%s" % nodes)
        if len(GraphEvaluator.node_stack):
            parent = GraphEvaluator.node_stack[-1]
            parent.deps.add(node)
            node.precedents.add(parent)
        GraphEvaluator.node_stack.append(node)
        if GraphEvaluator.verbose:
            arrows = "o" * (len(GraphEvaluator.node_stack) -1 ) * 3 + "> "
            print(f"{arrows} evaluating {node}")
        try:
            if node.state != NodeState.VALID:
                node.state = NodeState.CALCULATING
                node.value = node.cb()
                node.state = NodeState.VALID
            if GraphEvaluator.verbose:
                print(f"{arrows} calculated {node}")
            GraphEvaluator.node_stack.pop()
        #print(f"Children of {node}: {node.deps}")
        except Exception as e:
            node.value = e
            node.state = NodeState.INVALID
            GraphEvaluator.node_stack = []
            raise e
        return node.value
                