# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Pianoinput(Component):
    """A Pianoinput component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- note (number; default 60)
- scale (number; default 0.7)
- keywidth (number; default 40)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, note=Component.UNDEFINED, scale=Component.UNDEFINED, keywidth=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'note', 'scale', 'keywidth']
        self._type = 'Pianoinput'
        self._namespace = 'score_component'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'note', 'scale', 'keywidth']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Pianoinput, self).__init__(**args)
