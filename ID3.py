from math import log
from readData import *
import logging
import sys

def label(feature):
    return feature[len(feature) - 1]

def elog(num):
    try:
        return log(num)
    except:
        return 0

def cond_entropy(feature_dist):
    total = sum(feature_dist.itervalues())
    if total == 0:
        return sys.float_info.max
    condent = 0
    for count in feature_dist.itervalues():
        probability = (float(count))/total
        condent -= probability*elog(probability)
    #if condent < 0:
        #logging.debug(feature_dist)
        #sys.exit(0)
    return condent
    
def find_split(matrix):
    min_ent = sys.float_info.max
    split_feat = 0
    split_thresh = float(0)
    prev = 0
    curr = 0
    feat_dist_init = {}
    rem_dist_init = {}
    point_count = len(matrix)
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    for row in matrix:
        logging.debug('storing points in rem dict')
        try:
            rem_dist_init[label(row)] += 1
        except:
            rem_dist_init[label(row)] = 1
    for feat in range(0, len(matrix[0]) - 2):
        logging.debug('analyzing new feat')
        feat_dist = feat_dist_init
        rem_dist = rem_dist_init
        matrix = sorted(matrix, key = lambda m_entry: m_entry[feat])
        logging.debug('pts sorted')
        for count, point in enumerate(matrix):
            prev = curr
            curr = point[feat]
            if curr != prev and count:
                logging.debug('calc info gain')
                ent = (float(count)/point_count)*cond_entropy(feat_dist) + \
                (float(count)/point_count)*cond_entropy(rem_dist)
                logging.debug('ent is ')
                logging.debug(ent)
                if (ent < min_ent):
                    logging.debug('update split to ')
                    logging.debug(ent)
                    min_ent = ent
                    split_feat = feat
                    split_thresh = point[feat]

            try:
                feat_dist[label(point)] += 1
            except:
                feat_dist[label(point)] = 1
            rem_dist[label(point)] -= 1
            logging.debug('move on')
    return (split_feat, split_thresh)

def test_purity(pointset):
    prev_label = 0
    curr_label = label(pointset[0])
    for row in pointset:
        prev_label = curr_label
        curr_label = label(row)
        if curr_label != prev_label:
            return (False, None)
    return (True, curr_label)

class Tree():
    def __init__(self):
        self.threshold = 0
        self.feature = 0
        self.isLeaf = False
        self.label = -1
        self.left = None
        self.right = None

def make_decision_tree(pointset):
    (isClean, nodeLabel) = test_purity(pointset)
    node = Tree()
    if isClean:
        node.isLeaf = True
        node.label = nodeLabel
        logging.debug('made leaf!')
        return node
    else:
        (feature, threshold) = find_split(pointset)
        left_branch = [row for row in pointset if row[feature] <= threshold]
        right_branch = [row for row in pointset if row[feature] > threshold]
        print left_branch
        print right_branch
        sys.exit(0)
        node.left = make_decision_tree(left_branch)
        node.right = make_decision_tree(right_branch)


if __name__ == "__main__":
    data = read_to_list(sys.argv[1])
    root = make_decision_tree(data)

