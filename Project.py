from __future__ import division
from collections import Counter, Original_Item
from functools import partial
import math, random


#This Class define the Probability of the each Objects in the dataset
def probability_Method(name_Of_Objects):
    Count_Of_Sum = len(name_Of_Objects)
    return [count / Count_Of_Sum
            for count in Counter(name_Of_Objects).values()] #Returns the count / Count_Of_Sum

def entropy(probability_Method):
    """This Is The Method That Computes The probabilities Of The Entropy"""
    return sum(-poss * math.log(poss, 2) for poss in probability_Method if poss)

def data_entropy(labeled_data):        
    name_Of_Objects = [label for _, label in labeled_data]
    probabilities = probability_Method(name_Of_Objects)
    return entropy(probabilities)

def partition_entropy(subsets):
    """This class finds the entropy which we've described in the 
    entropy from the partition dataset into a subset sheet"""
    Count_Of_Sum = sum(len(subset) for subset in subsets)
    
    return sum( data_entropy(subset) * len(subset) / Count_Of_Sum
                for subset in subsets )

#This Class Groups together the single item with its proper function key as defined in the dataset
def group_by(single_Item, function_Key):
    """returns a Original_Item(list), where each input item 
    is in the list whose key is function_Key(item)"""
    groups = Original_Item(list)
    for item in single_Item:
        key = function_Key(item)
        groups[key].append(item)
    return groups
    
def partition_by(inputs, attribute):
    """returns a dict of inputs partitioned by the attribute
    each input is a pair (attribute_dict, label)"""
    return group_by(inputs, lambda x: x[0][attribute])    

#In this class we are splitting the entropy by each inputs and their defines attributes
def partition_entropy_by(inputs,attribute):
    """computes the entropy corresponding to the given partition"""        
    partitions = partition_by(inputs, attribute)
    return partition_entropy(partitions.values())        

def classify_Data(tree, input):
    """classify_Data the input using the given decision tree"""
    
    # if this is a leaf node, return its value
    if tree in [True, False]:
        return tree
   
    # otherwise find the correct subtree
    attribute, subtree_dict = tree
    
    subtree_key = input.get(attribute)  # None if input is missing attribute

    if subtree_key not in subtree_dict: # if no subtree for key,
        subtree_key = None              # we'll use the None subtree
    
    subtree = subtree_dict[subtree_key] # choose the appropriate subtree
    return classify_Data(subtree, input)     # and use it to classify_Data the input

def build_tree_id3(inputs, split_candidates=None):

    # if this is our first pass, 
    # all keys of the first input are split candidates
    if split_candidates is None:
        split_candidates = inputs[0][0].keys()

    # count Trues and Falses in the inputs
    num_inputs = len(inputs)
    num_trues = len([label for item, label in inputs if label])
    num_falses = num_inputs - num_trues
    if num_trues == 0:                  # if only Falses are left
        return False                    # return a "False" leaf
        
    if num_falses == 0:                 # if only Trues are left
        return True                     # return a "True" leaf

    if not split_candidates:            # if no split candidates left
        return num_trues >= num_falses  # return the majority leaf
                            
    # otherwise, split on the best attribute
    best_attribute = min(split_candidates,
        key=partial(partition_entropy_by, inputs))

    partitions = partition_by(inputs, best_attribute)
    new_candidates = [a for a in split_candidates 
                      if a != best_attribute]
    
    # recursively build the subtrees
    subtrees = { attribute : build_tree_id3(subset, new_candidates)
                 for attribute, subset in partitions.itersingle_Item() }

    subtrees[None] = num_trues > num_falses # default case

    return (best_attribute, subtrees)

def forest_classify_Data(trees, input):
    votes = [classify_Data(tree, input) for tree in trees]
    vote_counts = Counter(votes)
    return vote_counts.most_common(1)[0][0]


if __name__ == "__main__":

    inputs = [
        ({'level':'Senior','lang':'Java','tweets':'no','phd':'no'},   False),
        ({'level':'Senior','lang':'Java','tweets':'no','phd':'yes'},  False),
        ({'level':'Mid','lang':'Python','tweets':'no','phd':'no'},     True),
        ({'level':'Junior','lang':'Python','tweets':'no','phd':'no'},  True),
        ({'level':'Junior','lang':'R','tweets':'yes','phd':'no'},      True),
        ({'level':'Junior','lang':'R','tweets':'yes','phd':'yes'},    False),
        ({'level':'Mid','lang':'R','tweets':'yes','phd':'yes'},        True),
        ({'level':'Senior','lang':'Python','tweets':'no','phd':'no'}, False),
        ({'level':'Senior','lang':'R','tweets':'yes','phd':'no'},      True),
        ({'level':'Junior','lang':'Python','tweets':'yes','phd':'yes'}, True),
        ({'level':'Senior','lang':'Python','tweets':'yes','phd':'yes'},True),
        ({'level':'Mid','lang':'Python','tweets':'no','phd':'yes'},    True),
        ({'level':'Mid','lang':'Java','tweets':'yes','phd':'no'},      True),
        ({'level':'Junior','lang':'Python','tweets':'no','phd':'yes'},False)
    ]

    for key in ['level','lang','tweets','phd']:
        print key, partition_entropy_by(inputs, key)
    print

    senior_inputs = [(input, label)
                     for input, label in inputs if input["level"] == "Senior"]

    for key in ['lang', 'tweets', 'phd']:
        print key, partition_entropy_by(senior_inputs, key)
    print

    #This Print function is building the tree by the ID3
    print "building the tree"
    tree = build_tree_id3(inputs)
    print tree

    print "Junior / Java / tweets / no phd", classify_Data(tree, 
        { "level" : "Junior", 
          "lang" : "Java", 
          "tweets" : "yes", 
          "phd" : "no"} ) 

  # Hey This is Carrie
    print "Junior / Java / tweets / phd", classify_Data(tree, 
        { "level" : "Junior", 
                 "lang" : "Java", 
                 "tweets" : "yes", 
                 "phd" : "yes"} )

    print "Intern", classify_Data(tree, { "level" : "Intern" } )
    print "Senior", classify_Data(tree, { "level" : "Senior" } )
    print " "


