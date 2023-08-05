# -*- coding: utf-8 -*-
"""
validator manager module.
"""

from pyrin.core.globals import _
from pyrin.core.structs import Manager, Context, DTO
from pyrin.utils.custom_print import print_warning
from pyrin.validator.interface import AbstractValidatorBase
from pyrin.validator.exceptions import InvalidValidatorTypeError, DuplicatedValidatorError, \
    ValidatorNotFoundError, ValidationError, InvalidEntityForValidationError, \
    InvalidDataForValidationError


class ValidatorManager(Manager):
    """
    validator manager class.
    """

    def __init__(self):
        """
        initializes an instance of ValidatorManager.
        """

        super().__init__()

        # a dictionary containing information of registered validators.
        # example: dict(type[BaseEntity] |
        #               str domain: dict(str name: AbstractValidatorBase instance))
        self._validators = Context()

    def register_validator(self, instance, **options):
        """
        registers a new validator or replaces the existing one.

        if `replace=True` is provided. otherwise, it raises an error
        on adding a validator which is already registered.

        :param AbstractValidatorBase instance: validator to be registered.
                                               it must be an instance of
                                               AbstractValidatorBase.

        :keyword bool replace: specifies that if there is another registered
                               validator with the same domain and name, replace
                               it with the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidValidatorTypeError: invalid validator type error.
        :raises DuplicatedValidatorError: duplicated validator error.
        """

        if not isinstance(instance, AbstractValidatorBase):
            raise InvalidValidatorTypeError('Input parameter [{instance}] is '
                                            'not an instance of [{base}].'
                                            .format(instance=instance,
                                                    base=AbstractValidatorBase))

        domain_validators = self.get_domain_validators(instance.domain)
        if domain_validators is not None:
            old_instance = domain_validators.get(instance.name, None)
            if old_instance is not None:
                replace = options.get('replace', False)
                if replace is not True:
                    raise DuplicatedValidatorError('There is another registered '
                                                   'validator [{old}] with name '
                                                   '[{name}] for domain [{domain}] '
                                                   'but "replace" option is not set, '
                                                   'so validator [{instance}] '
                                                   'could not be registered.'
                                                   .format(old=old_instance,
                                                           name=instance.name,
                                                           domain=instance.domain,
                                                           instance=instance))

                print_warning('Validator [{old_instance}] is going '
                              'to be replaced by [{new_instance}] '
                              'for domain [{domain}].'
                              .format(old_instance=old_instance,
                                      new_instance=instance,
                                      domain=instance.domain))

        if domain_validators is None:
            domain_validators = DTO()
            self._validators[instance.domain] = domain_validators
        domain_validators[instance.name] = instance
        self._validators[instance.domain] = domain_validators

    def get_domain_validators(self, domain):
        """
        gets all registered validators for given domain.

        it returns None if no validator found for given domain.

        :param type[BaseEntity] | str domain: the domain to get its validators.
                                              it could be a type of a BaseEntity
                                              subclass or a string name.

        :rtype: dict[type[BaseEntity] | str, AbstractValidatorBase]
        """

        return self._validators.get(domain, None)

    def get_validator(self, domain, name):
        """
        gets the registered validator for given domain and name.

        it returns None if no validator found for given name.

        :param type[BaseEntity] | str domain: the domain to get validator from.
                                              it could be a type of a BaseEntity
                                              subclass or a string name.

        :param str name: validator name to get.

        :rtype: AbstractValidatorBase
        """

        domain_validators = self.get_domain_validators(domain)
        if domain_validators is not None:
            return domain_validators.get(name, None)

        return None

    def validate_field(self, domain, name, value, **options):
        """
        validates the given value with given validator.

        it returns a value indicating that validator has been found.

        :param type[BaseEntity] | str domain: the domain to validate the value for.
                                              it could be a type of a BaseEntity
                                              subclass or a string name.

        :param str name: validator name to be used for validation.
        :param object value: value to be validated.

        :keyword bool force: specifies that if there is no validator
                             with specified domain and name, it should
                             raise an error. defaults to False if not provided.

        :keyword bool nullable: determines that provided value could be None.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool allow_blank: determines that empty strings should be
                                   considered valid. this argument will only
                                   be considered in string validators.

        :keyword bool allow_whitespace: determines that whitespace strings should be
                                        considered valid. this argument will only
                                        be considered in string validators.

        :raises ValidatorNotFoundError: validator not found error.
        :raises ValidationError: validation error.

        :returns: a value indicating that validator has been found.
        :rtype: bool
        """

        validator = self.get_validator(domain, name)
        force = options.get('force', None)
        if force is None:
            force = False

        if force is not False and validator is None:
            raise ValidatorNotFoundError('There is no validator with name '
                                         '[{name}] for domain [{domain}].'
                                         .format(name=name, domain=domain))

        if validator is not None:
            validator.validate(value, **options)

        return validator is not None

    def validate_dict(self, domain, data, **options):
        """
        validates available values of given dict.

        it uses the correct validator for each value based on its key name.

        :param type[BaseEntity] | str domain: the domain to validate the values for.
                                              it could be a type of a BaseEntity
                                              subclass or a string name.

        :param dict data: dictionary to validate its values.

        :keyword bool force: specifies that if there is no validator
                             for any of key names, it should raise an error.
                             defaults to False if not provided.

        :keyword bool lazy: specifies that all values must be validated first and
                            then a cumulative error must be raised containing a dict
                            of all keys and their corresponding error messages.
                            defaults to False if not provided.

        :keyword bool nullable: determines that provided values could be None.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool allow_blank: determines that empty strings should be
                                   considered valid. this argument will only
                                   be considered in string validators.

        :keyword bool allow_whitespace: determines that whitespace strings should be
                                        considered valid. this argument will only
                                        be considered in string validators.

        :raises InvalidDataForValidationError: invalid data for validation error.
        :raises ValidatorNotFoundError: validator not found error.
        :raises ValidationError: validation error.

        :returns: a dict containing all key/values that
                  no validator has been found for them.
        :rtype: dict
        """

        if data is None:
            raise InvalidDataForValidationError('Data for validation '
                                                'could not be None.')

        no_validator = DTO()
        cumulative_errors = DTO()
        lazy = options.get('lazy', None)
        if lazy is None:
            lazy = False

        for name, value in data.items():
            try:
                found = self.validate_field(domain, name, value, **options)
                if not found:
                    no_validator[name] = value
            except ValidationError as error:
                if lazy is not True:
                    raise error
                else:
                    cumulative_errors[name] = error.description

        if len(cumulative_errors) > 0:
            raise ValidationError(_('Validation failed with following errors.'),
                                  data=cumulative_errors)

        return no_validator

    def validate_entity(self, entity, **options):
        """
        validates available values of given entity.

        it uses the correct validator for each value based on its field name.

        :param BaseEntity entity: entity to validate its values.

        :keyword bool force: specifies that if there is no validator
                             for any of field names, it should raise an error.
                             defaults to False if not provided.

        :keyword bool lazy: specifies that all fields must be validated first and
                            then a cumulative error must be raised containing a dict
                            of all field names and their corresponding error messages.
                            defaults to False if not provided.

        :keyword bool nullable: determines that provided values could be None.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool allow_blank: determines that empty strings should be
                                   considered valid. this argument will only
                                   be considered in string validators.

        :keyword bool allow_whitespace: determines that whitespace strings should be
                                        considered valid. this argument will only
                                        be considered in string validators.

        :raises InvalidEntityForValidationError: invalid entity for validation error.
        :raises ValidatorNotFoundError: validator not found error.
        :raises ValidationError: validation error.

        :returns: a dict containing all field/values that
                  no validator has been found for them.
        :rtype: dict
        """

        if entity is None:
            raise InvalidEntityForValidationError('Entity for validation '
                                                  'could not be None.')

        return self.validate_dict(type(entity), entity.to_dict(), **options)
