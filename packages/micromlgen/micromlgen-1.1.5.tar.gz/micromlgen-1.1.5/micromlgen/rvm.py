from micromlgen.utils import jinja


def port_rvm(clf, classname, **kwargs):
    """Port a RVM classifier"""
    assert classname is None or len(classname) > 0, 'Invalid class name'
    template_data = {
        **kwargs,
        'kernel': {
            'type': clf.kernel,
            'gamma': clf.gamma,
            'coef0': clf.coef0,
            'degree': clf.degree
        },
        'sizes': {
            'features': len(clf.relevant_vectors_[0]),
        },
        'arrays': {
            'vectors': clf.relevant_vectors_,
            'coefs': clf.coef_,
            'actives': clf.active_,
            'intercepts': clf.intercept_,
            'mean': clf._x_mean,
            'std': clf._x_std
        },
        'classname': classname if classname is not None else 'RVM',
    }
    return jinja('rvm/rvm.jinja', template_data)
