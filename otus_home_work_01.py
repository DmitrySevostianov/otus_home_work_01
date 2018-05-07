import ast
import os
import collections

from nltk import pos_tag

# rename !
def merge_to_flat_list(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


### see to Rasswet / otus-web / dz01 ...
def is_verb(word):
    if not word:
        return False
    
    tagged_word = pos_tag([word])
    word, tag = tagged_word[0]
    standard_tag_for_verb = 'VB'
    return tag == standard_tag_for_verb


def get_file_names_from_directories(path):
    filenames = []
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                filenames.append(os.path.join(dirname, file))
                if len(filenames) == 100:
                    break
    #print('total %s files' % len(filenames))
    return filenames


def generate_trees(_path, with_filenames=False, with_file_content=False):
    filenames = []
    trees = []
    filenames = get_file_names_from_directories(_path)
    
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            tree = None
        if with_filenames:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
            
    filtered_trees = [tree for tree in trees if tree]    
    return filtered_trees


def get_verbs_from_function_name(function_name):
    verbs = [word for word in function_name.split('_') if is_verb(word)]
    return verbs



###### next refactoring :
## see Rasswet / otus-web
## def is_system_name():
## def extract functions_from_trees


def is_system_name(func):
    return func.startswith('__') and func.endswith('__')

def get_function_names_from_tree(tree):
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def get_not_system_function_names(path):
    trees = generate_trees(path)    
    
    list_of_all_function_names = [get_function_names_from_tree(tree) for tree in trees]
    #print(list_of_all_functions)
    flat_list_of_function_names = merge_to_flat_list(list_of_all_function_names)
    #print(flat_list_of_function_names)
    not_system_function_names = [func for func in flat_list_of_function_names if not is_system_name(func)]
    return not_system_function_names


def get_top_verbs_in_path(path, top_size=10):  
    function_names = get_not_system_function_names(path)
    
    list_of_verbs = [get_verbs_from_function_name(function_name) for function_name in function_names]
    
    flat_list_of_verbs = merge_to_flat_list(list_of_verbs)
    return collections.Counter(flat_list_of_verbs).most_common(top_size)


def collect_verbs():
    wds = []
    projects = [
        'django',
        'flask',
        #'pyramid',
        #'reddit',
        #'requests',
        #'sqlalchemy',
    ]
    for project in projects:
        path = os.path.join('.', project)
        wds += get_top_verbs_in_path(path)
        
    return wds

'''
top_size = 200
print('total %s words, %s unique' % (len(wds), len(set(wds))))
for word, occurence in collections.Counter(wds).most_common(top_size):
    print(word, occurence)
'''

def print_amount_of_verbs(verbs_wds):
    print('total %s words, %s unique' % (len(verbs_wds), len(set(verbs_wds))))
    pass


def print_word_occurence_paires(verbs_wds, _top_size):
    word_occurance_pairs = collections.Counter(verbs_wds).most_common(_top_size)
    for word, occurence in word_occurance_pairs:
        print(word, occurence)
    pass    


if __name__ == '__main__':
    top_size = 200
    verbs = collect_verbs()
    print_amount_of_verbs(verbs)
    print_word_occurence_paires(verbs,top_size)