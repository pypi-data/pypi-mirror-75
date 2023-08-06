from sklearn.linear_model import LogisticRegression
from micromlgen.utils import jinja


def is_logisticregression(clf):
    """Test if classifier can be ported"""
    return isinstance(clf, LogisticRegression)


def port_logisticregression(clf, **kwargs):
    """Port sklearn's DecisionTreeClassifier"""
    kwargs['classname'] = kwargs['classname'] or 'LogisticRegression'
    return jinja('logisticregression/logisticregression.jinja', {
        'weights': clf.coef_,
        'intercept': clf.intercept_,
        'classes': clf.classes_,
        'n_classes': len(clf.classes_)
    }, **kwargs)