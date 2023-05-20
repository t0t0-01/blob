from zss import simple_distance, Node, distance


A = (
    Node("f")
        .addkid(Node("a")
            .addkid(Node("h"))
            .addkid(Node("c")
                .addkid(Node("l"))))
        .addkid(Node("e"))
    )
B = (
    Node("f")
        .addkid(Node("a")
            .addkid(Node("d"))
            .addkid(Node("cvxvxcv")
                .addkid(Node("bdegsdfsdf"))))
        .addkid(Node("e"))
    )



def get_hierarchy(node, dic, count):
    children = Node.get_children(node)
    
    if children:
        for child in children:
            get_hierarchy(child, dic, count+1)
            
    
    dic[Node.get_label(node)] = 1 / count
    
    return dic
        
dic_A = get_hierarchy(A, {}, 1)
dic_B = get_hierarchy(B, {}, 1)

overall_dic = {}
for pos, x in enumerate([dic_A, dic_B]):
    new_dic = {f"{key}_{pos}" : value for key, value in x.items()}
    overall_dic.update(new_dic)
    
print(overall_dic)

"""
insert_cost = lambda node: overall_dic[Node.get_label(node)]
update_cost = insert_cost
remove_cost = insert_cost


# Assumption: same number of interests in both trees

print(distance(A, B, get_children=Node.get_children, insert_cost=insert_cost, remove_cost=remove_cost, update_cost=update_cost))

"""