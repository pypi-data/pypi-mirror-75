from micromlgen.utils import jinja


def port_sefr(clf, classname=None, **kwargs):
    """Port SEFR classifier"""
    kwargs.update({
        'weights': clf.weights,
        'bias': clf.bias,
        'dimension': len(clf.weights),
        'classname': classname or 'SEFR'
    })
    return jinja('sefr/sefr.jinja', kwargs)