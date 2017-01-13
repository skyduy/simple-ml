# coding: utf-8


class TreeNode(object):
    def __init__(self, name_value, num_occur, parent_node):
        self.name = name_value
        self.count = num_occur
        self.node_link = None
        self.parent = parent_node
        self.children = {}

    def inc(self, num_occur):
        self.count += num_occur

    def display(self, ind=1):
        print '  '*ind, self.name, ' ', self.count
        for child in self.children.values():
            child.display(ind+1)


def create_tree(data_set, min_sup=1):
    header_table = {}       # 保存所有的频繁项集合
    for trans in data_set:
        for item in trans:
            header_table[item] = header_table.get(item, 0) + data_set[trans]
    for k in header_table.keys():
        if header_table[k] < min_sup:
            del(header_table[k])
    freq_item_set = set(header_table.keys())
    if len(freq_item_set) == 0:
        return None, None
    for k in header_table:
        header_table[k] = [header_table[k], None]
    rest_tree = TreeNode('Null set', 1, None)
    for tran_set, count in data_set.items():
        local_data = {}     # 仅保存在data_set的某个单元里面的频繁项，并用词来更新树
        for item in tran_set:
            if item in freq_item_set:
                local_data[item] = header_table[item][0]
        if len(local_data) > 0:
            ordered_items = [
                v[0] for v in sorted(local_data.items(), key=lambda p: p[1], reverse=True)
            ]
            update_tree(ordered_items, rest_tree, header_table, count)
    return rest_tree, header_table


def update_tree(items, in_tree, header_table, count):
    """
    更新树
    :param items: 需要添加的单元频繁项， 顺序为总的频繁度
    :param in_tree: 添加在该树下
    :param header_table: 保存了所有频繁项以及一个None的字典
    :param count: 单元出现次数
    :return:
    """
    if items[0] in in_tree.children:
        in_tree.children[items[0]].inc(count)
    else:
        in_tree.children[items[0]] = TreeNode(items[0], count, in_tree)
        if header_table[items[0]][1] is None:
            header_table[items[0]][1] = in_tree.children[items[0]]
        else:
            update_header(header_table[items[0]][1], in_tree.children[items[0]])

    if len(items) > 1:
        update_tree(items[1::], in_tree.children[items[0]], header_table, count)


def update_header(node_to_test, target_node):
    while node_to_test.node_link is not None:
        node_to_test = node_to_test.node_link
    node_to_test.node_link = target_node


def load_simple_data():
    simple_data = [
        ['r', 'z', 'h', 'j', 'p'],
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
        ['z'],
        ['r', 'x', 'n', 'o', 's'],
        ['y', 'r', 'x', 'z', 'q', 't', 'p'],
        ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']
    ]

    return [
        [1, 3, 4],
        [2, 3, 5],
        [1, 2, 3, 5],
        [2, 5],
    ]
    #return simple_data


def create_init_set(data_set):
    ret_dict = {}
    for trans in data_set:
        ret_dict[frozenset(trans)] = 1
    return ret_dict


def ascent_tree(leaf_node, prefix_path):
    if leaf_node.parent is not None:
        prefix_path.append(leaf_node.name)
        ascent_tree(leaf_node.parent, prefix_path)


def find_prefix_path(tree_node):
    cond_patterns = {}
    while tree_node is not None:
        prefix_path = []
        ascent_tree(tree_node, prefix_path)
        if len(prefix_path) > 1:
            cond_patterns[frozenset(prefix_path[1:])] = tree_node.count
        tree_node = tree_node.node_link
    return cond_patterns


def mine_tree(limit_set, header_table, min_sup, prefix, freq_item_list):
    big_list = [v[0] for v in sorted(header_table.items(), key=lambda p:p[1])]
    for base_pattern in big_list:
        new_prefix = prefix.copy()
        new_prefix.add(base_pattern)
        if new_prefix >= limit_set:
            freq_item_list.append(new_prefix)
        cond_pattern_bases = find_prefix_path(header_table[base_pattern][1])
        # cond_tree condition-tree 条件树
        my_cond_tree, my_head = create_tree(cond_pattern_bases, min_sup)
        if my_head is not None:
            # print 'conditional tree for: ', new_prefix
            # my_cond_tree.display()
            mine_tree(limit_set, my_head, min_sup, new_prefix, freq_item_list)

if __name__ == '__main__':
    simple_data = load_simple_data()
    init_set = create_init_set(simple_data)
    tree, table = create_tree(init_set, 3)
    limit = {5}
    freq_item_set = []
    mine_tree(limit, table, 3, {2}, freq_item_set)

    def unique(unhashable_list):
        from itertools import groupby
        return [k for k, v in groupby(unhashable_list)]

    print freq_item_set
    print unique(freq_item_set)
