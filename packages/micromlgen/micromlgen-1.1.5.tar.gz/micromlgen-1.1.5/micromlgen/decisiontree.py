from sklearn.tree import DecisionTreeClassifier
from micromlgen.utils import jinja


def is_decisiontree(clf):
    """Test if classifier can be ported"""
    return isinstance(clf, DecisionTreeClassifier)


def port_decisiontree(clf, **kwargs):
    """Port sklearn's DecisionTreeClassifier"""
    kwargs['classname'] = kwargs['classname'] or 'DecisionTree'
    return jinja('decisiontree/decisiontree.jinja', {
        'left': clf.tree_.children_left,
        'right': clf.tree_.children_right,
        'features': clf.tree_.feature,
        'thresholds': clf.tree_.threshold,
        'classes': clf.tree_.value,
        'i': 0
    }, **kwargs)