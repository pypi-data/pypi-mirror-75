# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 19:11:03 2020


This module takes a sklearn based DecisionTreeClassifier model object and returns a string
which is a sequence of SQL case-when statements that represents the 
Decison tree, and the resultant SQL snippet can be used to directly 
deploy the Decision Tree model on a SQL based database.

@author: Aditya Kumar
adityakumar3008@gmail.com
https://www.linkedin.com/in/nullp0inter/
"""

import pandas as pd
import numpy as np

__all__ = ["DecisionTreeClassifierConverter"]

class DecisionTreeClassifierConverter:
    
    """
    An implementation that can convert an SkLearn Decision Tree classifier 
    into a sequence of SQL case-when statements thereby making the model 
    directly deployable on a SQL based database.
    """
    def __init__(self, tree):
        """
        When initialising the converter, pass a valid Sklearn Decision tree classifier object

        Parameters
        ----------
        tree : Sklearn Decision Tree Classifier Object
            DESCRIPTION.
            Pass a valid Sklearn Decision Tree Classifier Object while initialising
        Returns
        -------
        Returns an obejct of the converter

        """
        self.tree = tree
        print("Classes of the tree are: ")
        print(tree.classes_)
        print("Choose class index accordingly if probability values are required. :)")
    
    def __value2prob__(self, value):
        """
        Takes the count of data-points in each leaf node and calculates
        the probability value associated with each class in that leaf node.

        """
        
        return value / value.sum(axis=1).reshape(-1, 1)
    
    
    def __indent__(self, depth):
        """
        Parameters
        ----------
        depth : number
            a number that requests the amount of indentation needed.

        Returns
        -------
        TYPE : String
            A string with proper that serves as indentation.

        """
        
        return "\n" + " " * 2 * depth
    
    def __indent_without_break__(self):
        """
        Returns
        -------
        str String
            a funtion used as a placeholder for case where no indentation is required.

        """
       
        return ""
    
    def __to_sql_recurse_classes__(self, left, right, conditions, features, targets, 
                               leaves, node_pos, depth, indent):
        """
        Returns
        -------
        sql : String
            Returns a string that is a sequence of SQL case-when statements
            with values as the resultant classes

        """
        sql = ""
        if conditions[node_pos] == -2:
            selected_feature = targets[np.argmax(leaves[node_pos])]
            if(indent == True):
                sql += self.__indent__(depth) + "'" + selected_feature + "'"
            else:
                sql += self.__indent_without_break__() + "'" + selected_feature + "'"
        else:
            if(indent == True):
                sql += self.__indent__(depth) + "CASE WHEN " + features[node_pos] + " <= " + str(conditions[node_pos]) + " THEN "
            else:
                sql += self.__indent_without_break__() + "CASE WHEN " + features[node_pos] + " <= " + str(conditions[node_pos]) + " THEN "
            if left[node_pos] != -1:
                sql += self.__to_sql_recurse_classes__(left, right, conditions, features, 
                                      targets, leaves, left[node_pos],
                                      depth + 1, indent)
            if(indent == True):
                sql += self.__indent__(depth) + "ELSE"
            else:
                sql += self.__indent_without_break__() + " ELSE "
            if right[node_pos] != -1:
                sql += self.__to_sql_recurse_classes__(left, right, conditions, features, 
                                      targets, leaves, right[node_pos],
                                      depth + 1, indent)
            if(indent == True):
                sql += self.__indent__(depth) + "END"
            else:
                sql += self.__indent_without_break__() + " END "
        return sql
    
    
    
    def __to_sql_recurse_prob__(self, left, right, conditions, features, targets, 
                            leaves, node_pos, depth, is_leaves, class_index, indent):
        """
        Returns
        -------
        sql : String
            Returns a string that is a sequence of SQL case-when statements
            with values as the resultant probability for selected class index

        """
        
        sql = ""
        if is_leaves[node_pos] == True:
            selected_feature = targets[np.argmax(leaves[node_pos])]
            proba = self.__value2prob__(leaves[node_pos])
            normalizer = proba.sum(axis=1)[:, np.newaxis]
            normalizer[normalizer == 0.0] = 1.0
            proba /= normalizer
            
            if(indent == True):
                sql += self.__indent__(depth) + "'" + str(proba[0][class_index]) + "'"
            else:
                sql += self.__indent_without_break__() + "'" + str(proba[0][class_index]) + "'"
        else:
            if(indent == True):
                sql += self.__indent__(depth) + "CASE WHEN " + features[node_pos] + " <= " + str(conditions[node_pos]) + " THEN "
            else:
                sql += self.__indent_without_break__() + "CASE WHEN " + features[node_pos] + " <= " + str(conditions[node_pos]) + " THEN "
            if left[node_pos] != -1:
                sql += self.__to_sql_recurse_prob__(left, right, conditions, features,
                                           targets, leaves, left[node_pos],
                                      depth + 1, is_leaves, class_index, indent)
            if(indent == True):
                sql += self.__indent__(depth) + "ELSE"
            else:
                sql += self.__indent_without_break__() + " ELSE "
            if right[node_pos] != -1:
                sql += self.__to_sql_recurse_prob__(left, right, conditions, features,
                                           targets, leaves, right[node_pos],
                                      depth + 1, is_leaves, class_index, indent)
            if(indent == True):
                sql += self.__indent__(depth) + "END"
            else:
                sql += self.__indent_without_break__() + " END "
        return sql
    
    def fit(self, cols, vbh_classes = True, class_index=0, indent = True):
        """
        This function takes the list of features used in training an
        Sklearn Decision Tree Classifier model object and returns a string
        which is a sequence of SQL case-when statements thatrepresents the 
        Decison tree and the resultant SQL snippet can be used to directly 
        deploy the Decision Tree model on a SQL based database.

        Parameters
        ----------
        cols : list
            A list of all the variable/feature names used to train the decision tree model.
        vbh_classes : Boolean, optional
            DESCRIPTION. The default is True.
                        If set to True, the resultant SQL statement will return in classes.
                        If set to False, the resultant SQL statement will return probability value for selected class.
        class_index : Int, optional
            DESCRIPTION. The default is 0.
                        The index of the class for which the probability values are needed.
        indent : Boolean, optional
            DESCRIPTION. The default is True.
                        If set to True, the resultant SQL query will have proper indentation.
                        If set to False, the resultant SQL query will not have indentation.(reduces query size)

        Returns
        -------
        TYPE : String
            DESCRIPTION.
                A SQL case-when statement is returned as a string
        """
        features = [cols[i] for i in self.tree.tree_.feature]
        is_leaves = self.__get_leaves_info__(self.tree)
        t = self.tree.tree_
        if vbh_classes == True:
            return self.__to_sql_recurse_classes__(t.children_left, t.children_right, 
                                   t.threshold, features, self.tree.classes_, 
                                   self.tree.tree_.value, 0, 0, indent)
        else:
            return self.__to_sql_recurse_prob__(t.children_left, t.children_right, 
                                   t.threshold, features, self.tree.classes_, 
                                   self.tree.tree_.value, 0, 0, is_leaves,
                                   class_index, indent)
        
    
    def __get_leaves_info__(self, clf):
        """
      
        Returns
        -------
        is_leaves : array
            Returns an array of booleans suggesting which of the nodes are leaf nodes.

        """
        n_nodes = clf.tree_.node_count
        children_left = clf.tree_.children_left
        children_right = clf.tree_.children_right
        feature = clf.tree_.feature
        threshold = clf.tree_.threshold
        
        node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
        is_leaves = np.zeros(shape=n_nodes, dtype=bool)
        stack = [(0, -1)]  # seed is the root node id and its parent depth
        while len(stack) > 0:
            node_id, parent_depth = stack.pop()
            node_depth[node_id] = parent_depth + 1
        
            # If we have a test node
            if (children_left[node_id] != children_right[node_id]):
                stack.append((children_left[node_id], parent_depth + 1))
                stack.append((children_right[node_id], parent_depth + 1))
            else:
                is_leaves[node_id] = True
                
        return is_leaves
    
    