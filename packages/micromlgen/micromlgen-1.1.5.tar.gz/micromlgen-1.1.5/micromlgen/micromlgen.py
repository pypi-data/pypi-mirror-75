from sklearn.decomposition import PCA
from sklearn.svm import SVC, LinearSVC, OneClassSVM

try:
    from skbayes.rvm_ard_models import RVC
except ImportError:
    from micromlgen.patches import RVC
try:
    from sefr import SEFR
except ImportError:
    from micromlgen.patches import SEFR

from micromlgen import platforms
from micromlgen.svm import port_svm
from micromlgen.rvm import port_rvm
from micromlgen.sefr import port_sefr
from micromlgen.decisiontree import is_decisiontree, port_decisiontree
from micromlgen.randomforest import is_randomforest, port_randomforest
from micromlgen.logisticregression import is_logisticregression, port_logisticregression
from micromlgen.gaussiannb import is_gaussiannb, port_gaussiannb
from micromlgen.pca import port_pca


def port(
        clf,
        classname=None,
        classmap=None,
        platform=platforms.ARDUINO,
        precision=None):
    """Port a classifier to plain C++"""
    assert platform in platforms.ALL, 'Unknown platform %s. Use one of %s' % (platform, ', '.join(platforms.ALL))
    if isinstance(clf, (SVC, LinearSVC, OneClassSVM)):
        return port_svm(**locals())
    elif isinstance(clf, RVC):
        return port_rvm(**locals())
    elif isinstance(clf, PCA):
        return port_pca(pca=clf, **locals())
    elif isinstance(clf, SEFR):
        return port_sefr(**locals())
    elif is_decisiontree(clf):
        return port_decisiontree(**locals())
    elif is_randomforest(clf):
        return port_randomforest(**locals())
    elif is_logisticregression(clf):
        return port_logisticregression(**locals())
    elif is_gaussiannb(clf):
        return port_gaussiannb(**locals())
    raise TypeError('clf MUST be one of SVC, LinearSVC, OneClassSVC, RVC, DecisionTree, RandomForest, LogisticRegression, GaussianNB, SEFR, PCA')