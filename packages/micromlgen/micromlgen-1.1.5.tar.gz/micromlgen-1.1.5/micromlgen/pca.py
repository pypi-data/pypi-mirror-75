from micromlgen.utils import jinja


def port_pca(pca, classname=None, **kwargs):
    """Port a PCA"""
    template_data = {
        'arrays': {
            'components': pca.components_,
            'mean': pca.mean_
        },
        'classname': classname if classname is not None else 'PCA'
    }
    return jinja('pca/pca.jinja', template_data)