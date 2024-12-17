### Generates a conversation tree

# Step 1: Generate child
def generate_child(user, expert, parent_conversation, path):
    expert_question = expert.generate_response(parent_conversation)
    parent_conversation += f"\nExpert: {expert_question}\n"
    user_response = user.generate_response(parent_conversation)
    parent_conversation += f"User: {user_response}\n"
    return {
        "expert_question": expert_question,
        "user_response": user_response,
        "conversation": parent_conversation,
        "path": path
    }

# Step 2: Generate children
def generate_children(user, expert, parent_conversation, branches_per_node, parent_path):
    children = {}
    for current_branch in range(branches_per_node):
        path = parent_path + (current_branch,)
        child_node = generate_child(user, expert, parent_conversation, path)
        children[current_branch] = child_node
    return children

# Step 3: Generate level
def generate_level(user, expert, parent_conversations, branches_per_node):
    level = {}
    node_idx = 0
    nodes_to_process = []
    # Flatten parent_conversations
    def collect_nodes(conversations):
        nodes = []
        for node in conversations.values():
            # If the current node is a leaf
            if 'conversation' in node and 'path' in node:
                nodes.append(node)
            # Else the current node is not a leaf, run the function to collect its children
            else:
                nodes.extend(collect_nodes(node))
        return nodes
    nodes_to_process = collect_nodes(parent_conversations)
    for node in nodes_to_process:
        parent_conversation = node['conversation']
        parent_path = node['path']
        children = generate_children(user, expert, parent_conversation, branches_per_node, parent_path)
        level[node_idx] = children
        node_idx += 1
    return level

# Step 4: Generate tree
def generate_tree(user, expert, branches_per_node, num_levels, root_conversation):
    tree = {0: {0: {"conversation": root_conversation, "path": (0,)}}}
    for level_idx in range(num_levels):
        # Get conversations from the previous level
        parent_level = tree[level_idx]
        # Generate new level
        tree[level_idx + 1] = generate_level(user, expert, parent_level, branches_per_node)
    return tree

# Step 5: Flatten the tree
def flatten_tree(tree):
    flat_tree = {}
    def recurse(node):
        if 'conversation' in node and 'path' in node:
            flat_tree[node['path']] = node['conversation']
        for key, child in node.items():
            if isinstance(child, dict) and key not in ['conversation', 'expert_question', 'user_response', 'path']:
                recurse(child)
    # Start from the root node
    root_nodes = tree
    for root_node in root_nodes.values():
        recurse(root_node)
    return flat_tree

# Step 6: Generate & Flatten
def generate_flat_tree(user, expert, branches_per_node, num_levels, root_conversation):
    tree = generate_tree(user, expert, branches_per_node, num_levels, root_conversation)
    flat_tree = flatten_tree(tree)
    return flat_tree

# Step 7: Pick one path
def pick_one_path(flat_tree):
    return {key: flat_tree[key] for key in flat_tree.keys() if sum(key) == 0} # path of all 0s