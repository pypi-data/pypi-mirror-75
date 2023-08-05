import  copy

from django.forms.forms import BaseForm
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.forms.forms import DeclarativeFieldsMetaclass
from django.forms.models import construct_instance, model_to_dict, InlineForeignKeyField
from itertools import chain


def prepend_prefix(cls, data):
    d = {}
    prefix = f'{cls.__name__.lower()}'
    for k, v in data.items():
        d[f'{prefix}__{k}'] = v
    return d

def strip_prefix(cls, data):
    d = {}
    prefix = f'{cls.__name__.lower()}__'
    for k, v in data.items():
        if prefix in k:
            _, nk = k.split(prefix)
            d[nk] = v
    return d


class StaplerFormOptions:

    def __init__(self, options):
        self.modelforms = getattr(options, 'modelforms')
        self.auto_prefix = getattr(options, 'auto_prefix', True)
        self.required = getattr(options, 'required', self.modelforms)


class StaplerMetaclass(DeclarativeFieldsMetaclass):

    def __new__(mcs, name, bases, attrs):

        # gather the fields of the inner Meta class and add them to attrs
        meta = attrs.pop('Meta', None)
        if meta:
            options = StaplerFormOptions(meta)
            if not hasattr(meta, 'modelforms'):
                raise AttributeError('make sure that modelforms attribute is set in inner Meta class')
            base_fields = {}
            for form in meta.modelforms:
                # add class name prefix to fieldnames to prevent clashing between model fields
                if options.auto_prefix:
                    base_fields.update(prepend_prefix(form._meta.model, form.base_fields))
                else:
                    base_fields.update(form.base_fields)
            base_fields.update(attrs) # declared fields should override model fields
            attrs = base_fields

            # add options from meta class
            attrs['_meta'] = options

        else:
            pass

        return super().__new__(mcs, name, bases, attrs)


class StaplerBaseForm(BaseForm):

    def __init__(self, data=None, **kwargs):

        self._validated_instances = None # stores the instance validation results after clean has been called
        instances = kwargs.pop('instances', [])
        instance = kwargs.pop('instance', None)
        if instance:
            instances.append(instance)
            instances = list(set(instances))

        initial = kwargs.get('initial')
        ac_object_data = {}

        # get all ModelForms
        for mf in self._meta.modelforms:
            opts = mf._meta
            mc = opts.model
            instance = self._get_instance(mc, instances)

            if instance is None:
                # if we didn't get an instance, instantiate a new one
                current_instance = mc()
                object_data = {}
            else:
                current_instance = instance
                object_data = model_to_dict(instance, opts.fields, opts.exclude)

            ac_object_data.update(prepend_prefix(mc, object_data))

            # set attribute for instance
            setattr(self, f'{mc.__name__.lower()}_instance', current_instance)

        # if initial was provided, it should override the values from instance
        if initial is not None:
            ac_object_data.update(initial)

        kwargs['initial'] = ac_object_data
        super().__init__(data, **kwargs)


    @property
    def validated_instances(self):
        if self._validated_instances == None:
            self._is_valid()
        return self._validated_instances

    @property
    def valid_instances(self):
        return self._get_valid_instances()

    @property
    def invalid_instances(self):
        return self._get_invalid_instances()

    def _get_instance(self, mc, instances):
        for instance in instances:
            if type(instance) == mc:
                return instance

    def _get_instances(self):
        mcs = [m._meta.model.__name__.lower() for m in self._meta.modelforms]
        attr_names = [f'{m}_instance' for m in mcs]
        instances = [getattr(self, attr_name) for attr_name in attr_names]
        return instances

    def _get_valid_instances(self):
        return [getattr(self, f'{instance}') for instance, valid in self.validated_instances.items() if valid]

    def _get_invalid_instances(self):
        return [getattr(self, f'{instance}') for instance, valid in self.validated_instances.items() if not valid]

    def _mc_to_mfc(self, mc):
        mfcs = self._meta.modelforms
        for mfc in mfcs:
            if mfc._meta.model == mc:
                return mfc

    def _get_validation_exclusions(self, mfc, mc):
        """
        For backwards-compatibility, exclude several types of fields from model
        validation. See tickets #12507, #12521, #12553.
        """
        exclude = []
        # Build up a list of fields that should be excluded from model field
        # validation and unique checks.
        for f in mc._meta.fields:  # self.instance._meta.fields:
            field = f.name

            # Exclude fields that aren't on the form. The developer may be
            # adding these values to the model after form validation.
            if field not in self.fields:
                exclude.append(f.name)

            # Don't perform model validation on fields that were defined
            # manually on the form and excluded via the ModelForm's Meta
            # class. See #12901.
            elif mfc._meta.fields and field not in mfc._meta.fields:
                exclude.append(f.name)

            elif mfc._meta.exclude and field in self._meta.exclude:
                exclude.append(f.name)

            # Exclude fields that failed form validation. There's no need for
            # the model fields to validate them as well.
            elif field in self._errors:
                exclude.append(f.name)

            # Exclude empty fields that are not required by the form, if the
            # underlying model field is required. This keeps the model field
            # from raising a required error. Note: don't exclude the field from
            # validation if the model field allows blanks. If it does, the blank
            # value may be included in a unique check, so cannot be excluded
            # from validation.
            else:
                form_field = self.fields[field]
                field_value = self.cleaned_data.get(field)
                if not f.blank and not form_field.required and field_value in form_field.empty_values:
                    exclude.append(f.name)
        return exclude

    def _post_clean(self):

        opts = self._meta
        mfcs = opts.modelforms

        # keep original cleaned data, required for workaround so we can keep using the construct_instance() function
        _cleaned_data = self.cleaned_data
        _fields = self.fields

        for mfc in mfcs:
            mc = mfc._meta.model
            current_instance = getattr(self, f'{mc.__name__.lower()}_instance')
            exclude = self._get_validation_exclusions(mfc, mc)

            # if opts.auto_prefix is true, modify the cleaned data, it should only contain cleaned data for the current modelclass (mc)
            # in addition, the prefix should be removed so that the construct_instance function can be used
            # do so for fields attr to
            if opts.auto_prefix:
                self.cleaned_data = strip_prefix(mc, _cleaned_data)
                self.fields = strip_prefix(mc,  _fields)

            # Foreign Keys being used to represent inline relationships
            # are excluded from basic field value validation. This is for two
            # reasons: firstly, the value may not be supplied (#12507; the
            # case of providing new values to the admin); secondly the
            # object being referred to may not yet fully exist (#12749).
            # However, these fields *must* be included in uniqueness checks,
            # so this can't be part of _get_validation_exclusions().
            #
            # create a instance to get acces to the fields attr
            #
            mfc_instance = mfc()
            for name, field in mfc_instance.fields.items():
                if isinstance(field, InlineForeignKeyField):
                    exclude.append(name)

            try:
                exclude_f = mfc._meta.exclude
            except AttributeError:
                exclude = None

            try:
                current_instance = construct_instance(self, current_instance, self.fields, exclude_f)
                setattr(self, f'{mc.__name__.lower()}_instance', current_instance)
            except ValidationError as e:
                self._update_errors(e)

            try:
                current_instance.full_clean(exclude=exclude, validate_unique=False)
            except ValidationError as e:
                self._update_errors(e)

            # Validate uniqueness if needed.
            if mfc_instance._validate_unique:
                self.validate_unique(mc, self._get_validation_exclusions(mfc, mc))

        # restore cleaned data if necessary
        if opts.auto_prefix:
            self.cleaned_data = _cleaned_data
            self.fields = _fields

    def validate_unique(self, mc, exclude):
        """
        Call the instance's validate_unique() method and update the form's
        validation errors if any were raised.
        """
        instance = getattr(f'{mc.__name__.lower()}_instance')
        try:
            instance.validate_unique(exclude=exclude)
        except ValidationError as e:
            self._update_errors(e)

    def _update_errors(self, errors):
        # Override any validation error messages defined at the model level
        # with those defined at the form level.
        opts = self._meta

        # Allow the model generated by construct_instance() to raise
        # ValidationError and have them handled in the same way as others.
        if hasattr(errors, 'error_dict'):
            error_dict = errors.error_dict
        else:
            error_dict = {NON_FIELD_ERRORS: errors}

        for field, messages in error_dict.items():
            if (field == NON_FIELD_ERRORS and opts.error_messages and
                    NON_FIELD_ERRORS in opts.error_messages):
                error_messages = opts.error_messages[NON_FIELD_ERRORS]
            elif field in self.fields:
                error_messages = self.fields[field].error_messages
            else:
                continue

            for message in messages:
                if (isinstance(message, ValidationError) and
                        message.code in error_messages):
                    message.message = error_messages[message.code]

        self.add_error(None, errors)

    def _save_m2m(self):
        """
        Save the many-to-many fields and generic relations for this form.
        """
        for instance in self.valid_instances:
            mc = type(instance)
            mfc = self._mc_to_mfc(mc)
            exclude = mfc._meta.exclude
            fields = self.fields
            opts = instance._meta

            # update cleaned_data if necessary
            if self._meta.auto_prefix:
                cleaned_data = strip_prefix(type(instance), self.cleaned_data)
                field_prefix = f"{mc.__name__.lower()}__"
            else:
                cleaned_data = self.cleaned_data
                field_prefix = ""

            # Note that for historical reasons we want to include also
            # private_fields here. (GenericRelation was previously a fake
            # m2m field).
            for f in chain(opts.many_to_many, opts.private_fields):
                if not hasattr(f, 'save_form_data'):
                    continue
                if fields and f"{field_prefix}{f.name}" not in fields:
                    continue
                if exclude and f"{field_prefix}{f.name}" in exclude:
                    continue
                if f.name in cleaned_data:
                    f.save_form_data(instance, cleaned_data[f.name])

    def _save(self, commit):
        """
        Save this form's self.instance object if commit=True. Otherwise, add
        a save_m2m() method to the form which can be called after the instance
        is saved manually at a later time. Return the model instance.
        """

        # if any errors, make sure that the belong to non required instances
        if self.errors:
            errors = copy.deepcopy(self.errors)
            for instance in self.invalid_instances:
                for f in instance._meta.fields:
                    errors.pop(f.name, None)
                for f in instance._meta.many_to_many:
                    errors.pop(f.name, None)
            if errors:
                raise ValueError(
                    "At least one of the instances could not be created/changed because the data didn't validate. %s" % self.invalid_instances)

        if commit:
            # If committing, save the instance and the m2m data immediately.
            for instance in self.valid_instances:
                instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        saved_instances = {f'{type(instance).__name__.lower()}_instance': instance for instance in self.valid_instances}
        failed_instances = {f'{type(instance).__name__.lower()}_instance': None for instance in self.invalid_instances}
        saved_instances.update(failed_instances)
        return saved_instances

    def _is_valid_instance(self, instance, errors):
        if self._meta.auto_prefix:
            field_prefix = f'{type(instance).__name__.lower()}__'
        else:
            field_prefix = ''
        for f in chain(instance._meta.fields, instance._meta.many_to_many):
            if f'{field_prefix}{f.name}' in errors:
                return False
        return True

    def _is_valid(self):
        instance_attrs = {f'{mfc._meta.model.__name__.lower()}_instance': True for mfc in self._meta.modelforms}

        # if one of the originally required fields was not valid, check which per instance which is valid or not
        if not super().is_valid():
            errors = [fn for fn in self.errors.keys()]
            for instance_attr in instance_attrs.keys():
                instance = getattr(self, instance_attr)
                instance_attrs[instance_attr] = self._is_valid_instance(instance, errors)
        self._validated_instances = instance_attrs

    def is_valid(self):
        self._is_valid()
        required_instances = set([f'{mfc._meta.model.__name__.lower()}_instance' for mfc in self._meta.required])
        valid_instances = set([instance for instance, valid in self.validated_instances.items() if valid])
        return not(required_instances - valid_instances)

    def pre_save(self):
        pass

    def post_save(self):
        pass

    def save(self, commit=True):
        self.pre_save()
        instances = self._save(commit)
        self.post_save()
        return instances


class StaplerForm(StaplerBaseForm, metaclass=StaplerMetaclass):
    pass


