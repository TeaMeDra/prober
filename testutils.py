import itertools

def print_test_pair(nodes, test_pairs, line):
    '''Prints test pairs required for device testing.'''    
    p1, p2 = test_pairs[line]
    id1, pin1 = p1
    id2, pin2 = p2
    print_vars = (nodes[id1]["name"], pin1, nodes[id2]["name"], pin2)
    return 'Test %s on pin %s against %s on pin %s:' % print_vars

def testing_pair_key(pair):
    '''Sorting utility for ordering nodes such that we test nodes in a
    convenient order.'''
    p1, p2 = pair
    id1, pin1 = p1
    id2, pin2 = p2
    return id1 + pin1

def remove_duplicates(test_pairs):
    '''Removes pair duplicates in pairs of nodes of an undirected graph,
    e.g. (a, b) is considered the same as (b, a).'''
    result = []
    seen = set()
    for pair in test_pairs:
        p1, p2 = pair
        if not ((p1, p2) in seen and (p2, p1) in seen):
            result.append((p1, p2))
            seen.add((p1, p2))
            seen.add((p2, p1))
    return result
    
def pairs_reverse(pair_list):
    '''Utility for adding pairs of type (a, b) for each (b, a) pair.'''
    result = []
    for p1, p2 in pair_list:
        result.append((p2, p1))
    return result   
    
def get_test_pairs(nodes):
    '''Obtain the test pairs for testing on the device.'''
    test_pairs = get_ordered_test_pairs(nodes)
    reverse_test_pairs = pairs_reverse(test_pairs)
    test_pairs = sorted(test_pairs + reverse_test_pairs, key = testing_pair_key) 
    test_pairs = remove_duplicates(test_pairs)
    return test_pairs

def get_ordered_test_pairs(nodes):
    '''Gets the testing pairs required for testing the circuit.'''
    nets = []
    result = []
    # Collect all the nets in the collapsed graph of the circuit
    for node in nodes:
        if nodes[node]["type"] in ["net", "spice"]:
            nets.append(node)

    for net in nets:
        # Collection of nodes attached to this net
        net_nodes = []
        for pin, node in nodes[net]["pins"].items():
            net_nodes.append((node["node"], node["pin"]))
        if net_nodes > 1:
            result += set(itertools.combinations(net_nodes, 2))
    return result