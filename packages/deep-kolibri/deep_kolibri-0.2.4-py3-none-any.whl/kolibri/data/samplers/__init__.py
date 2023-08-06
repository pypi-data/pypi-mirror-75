from imblearn.combine import (
    SMOTEENN, SMOTETomek,
)
from imblearn.over_sampling import (
    SMOTE, ADASYN, BorderlineSMOTE,
)
from imblearn.under_sampling import (
    ClusterCentroids,
    NearMiss,
    RandomUnderSampler,
    EditedNearestNeighbours,
    AllKNN,
    TomekLinks,
    OneSidedSelection,
    CondensedNearestNeighbour,
    NeighbourhoodCleaningRule,
)

from kolibri.data.samplers.auto_smpler import AutoSampler


def get_sampler(sampler, random_state=None):
    '''
    sampler: String
        The method used to perform re-sampling
        currently support: ['RUS', 'CNN', 'ENN', 'NCR', 'Tomek', 'ALLKNN', 'OSS',
            'NM', 'CC', 'SMOTE', 'ADASYN', 'BorderSMOTE', 'SMOTEENN', 'SMOTETomek',
            'ORG', AUTO']
    '''

    if sampler == 'RUS':
        return RandomUnderSampler(random_state=random_state)
    elif sampler == 'CNN':
        return CondensedNearestNeighbour(random_state=random_state)
    elif sampler == 'ENN':
        return EditedNearestNeighbours()
    elif sampler == 'NCR':
        return NeighbourhoodCleaningRule()
    elif sampler == 'Tomek':
        return TomekLinks()
    elif sampler == 'ALLKNN':
        return AllKNN()
    elif sampler == 'OSS':
        return OneSidedSelection(random_state=random_state)
    elif sampler == 'NM':
        return NearMiss()
    elif sampler == 'CC':
        return ClusterCentroids(random_state=random_state)
    elif sampler == 'SMOTE':
        return SMOTE(random_state=random_state)
    elif sampler == 'ADASYN':
        return ADASYN(random_state=random_state)
    elif sampler == 'BorderSMOTE':
        return BorderlineSMOTE(random_state=random_state)
    elif sampler == 'SMOTEENN':
        return SMOTEENN(random_state=random_state)
    elif sampler == 'SMOTETomek':
        return SMOTETomek(random_state=random_state)
    elif sampler == 'AUTO':
        return AutoSampler(random_state=random_state)
    else:
        raise Exception('Unexpected \'by\' type {}'.format(sampler))
