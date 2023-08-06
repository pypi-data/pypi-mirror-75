from sklearn.naive_bayes import GaussianNB
from micromlgen.utils import jinja


def is_gaussiannb(clf):
    """Test if classifier can be ported"""
    return isinstance(clf, GaussianNB)


def port_gaussiannb(clf, **kwargs):
    """Port sklearn's DecisionTreeClassifier"""
    kwargs['classname'] = kwargs['classname'] or 'GaussianNB'
    return jinja('gaussiannb/gaussiannb.jinja', {
        'sigma': clf.sigma_,
        'theta': clf.theta_,
        'prior': clf.class_prior_,
        'classes': clf.classes_,
        'n_classes': len(clf.classes_)
    }, **kwargs)