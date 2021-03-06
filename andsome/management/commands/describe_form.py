# Copyright 2010 VPAC
#
# This file is part of django-andsom.
#
# django-andsome is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-andsome is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django-andsome  If not, see <http://www.gnu.org/licenses/>.


from django.core.management.base import LabelCommand

class Command(LabelCommand):
    help = "Outputs the specified model as a form definition to the shell."
    args = "[app.model]"
    label = 'application name and model name'
    
    requires_model_validation = True
    can_import_settings = True

    def handle_label(self, label, **options):    
        print describe_form(label)


def describe_form(label, fields=None):
    """
    Returns a string describing a form based on the model
    """
    from django.db.models.loading import get_model
    app_name = label.split('.')[-2]
    model = get_model(app_name, label.split('.')[-1])

    opts = model._meta
    field_list = []
    for f in opts.fields + opts.many_to_many:
        if not f.editable:
            continue
        if fields and not f.name in fields:
            continue
        formfield = f.formfield()
        if not '__dict__' in dir(formfield):
            continue
        attrs = {}
        valid_fields = ['required', 'initial', 'max_length', 'min_length', 'max_value', 'min_value', 'max_digits', 'decimal_places', 'choices', 'help_text', 'label']
        for k,v in formfield.__dict__.items():
            if k in valid_fields and v != None:
                # ignore defaults, to minimize verbosity
                if k == 'required' and v:
                    continue
                if k == 'help_text' and not v:
                    continue
                if k == 'widget':
                    attrs[k] = v.__class__
                else:
                    attrs[k] = v
        
        params = ', '.join(['%s=%r' % (k, v) for k, v in attrs.items()])
        field_list.append('    %(field_name)s = forms.%(field_type)s(%(params)s)' % { 'field_name': f.name, 
                                                                                  'field_type': formfield.__class__.__name__, 
                                                                                  'params': params })
                                                                               
    return '''
from django import forms
from %(app_name)s.models import %(object_name)s
    
class %(object_name)sForm(forms.Form):
%(field_list)s
''' % { 'app_name': app_name, 'object_name': opts.object_name,  'field_list': '\n'.join(field_list) }
