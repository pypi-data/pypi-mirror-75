from sklearn.svm import OneClassSVM

from micromlgen.utils import jinja


def port_svm(clf, classname=None, **kwargs):
    """Port a SVC / LinearSVC classifier"""
    assert isinstance(clf.gamma, float), 'You probably didn\'t set an explicit value for gamma: 0.001 is a good default'
    assert classname is None or len(classname) > 0, 'Invalid class name'
    if classname is None:
        classname = 'OneClassSVM' if isinstance(clf, OneClassSVM) else 'SVM'
    support_v = clf.support_vectors_
    n_classes = len(clf.n_support_)
    template_data = {
        **kwargs,
        'kernel': {
            'type': clf.kernel,
            'gamma': clf.gamma,
            'coef0': clf.coef0,
            'degree': clf.degree
        },
        'sizes': {
            'features': len(support_v[0]),
            'vectors': len(support_v),
            'classes': n_classes,
            'decisions': n_classes * (n_classes - 1) // 2,
            'supports': clf.n_support_
        },
        'arrays': {
            'supports': support_v,
            'intercepts': clf.intercept_,
            'coefs': clf.dual_coef_
        },
        'classname': classname
    }
    return jinja('svm/svm.jinja', template_data)