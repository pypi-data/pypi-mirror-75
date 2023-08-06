from isc_common.isc.data_binding.criterion import Criterion


class AdvancedCriteria(Criterion):
    _constructor = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, list):
                setattr(self, k, [AdvancedCriteria(**criterion) if criterion.get('_constructor') == 'AdvancedCriteria' else Criterion(**criterion) for criterion in v])
            else:
                setattr(self, k, v() if callable(v) else v)
