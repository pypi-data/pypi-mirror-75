# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Edit(Component):
    """An Edit component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- note (number; default 60)
- dyn (string; default 'mf')
- scale (number; default 1.5)
- accidental_margin (number; default 55)
- hide_toolbar (boolean; default True)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, note=Component.UNDEFINED, dyn=Component.UNDEFINED, scale=Component.UNDEFINED, accidental_margin=Component.UNDEFINED, hide_toolbar=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'note', 'dyn', 'scale', 'accidental_margin', 'hide_toolbar']
        self._type = 'Edit'
        self._namespace = 'score_component'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'note', 'dyn', 'scale', 'accidental_margin', 'hide_toolbar']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Edit, self).__init__(**args)
