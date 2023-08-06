from sklearn.ensemble import RandomForestClassifier
from micromlgen.utils import jinja


def is_randomforest(clf):
    """Test if classifier can be ported"""
    return isinstance(clf, RandomForestClassifier)


def port_randomforest(clf, classname=None, **kwargs):
    """Port sklearn's RandomForestClassifier"""
    kwargs['classname'] = kwargs['classname'] or 'RandomForest'
    return jinja('randomforest/randomforest.jinja', {
        'classname': classname or 'RandomForestClassifier',
        'n_classes': clf.n_classes_,
        'trees': [{
            'left': clf.tree_.children_left,
            'right': clf.tree_.children_right,
            'features': clf.tree_.feature,
            'thresholds': clf.tree_.threshold,
            'classes': clf.tree_.value,
        } for clf in clf.estimators_]
    }, **locals())