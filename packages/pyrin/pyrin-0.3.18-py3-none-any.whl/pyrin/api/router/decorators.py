# -*- coding: utf-8 -*-
"""
router decorators module.
"""

import pyrin.api.router.services as router_services


def api(url, methods=None, authenticated=True, permissions=None, **options):
    """
    decorator to register an api handler for application.

    this decorator could take all the options that are used in route initialization.

    :param str url: the url rule as string.

    :param str | tuple[str] methods: http methods that this rule should handle.
                                     if not provided, defaults to `GET`.

    :param bool authenticated: specifies that this route could not be accessed
                               if the requester has not been authenticated.
                               defaults to True if not provided.

    :param PermissionBase | tuple[PermissionBase] permissions: all required permissions
                                                               for accessing this route.

    :keyword bool fresh_auth: specifies that this route could not be accessed
                              if the requester has not a fresh authentication.
                              fresh authentication means an authentication that
                              has been done by providing user credentials to
                              server. defaults to False if not provided.

    :keyword bool replace: specifies that this route must replace any existing
                           route with the same url and http methods or raise
                           an error if not provided. defaults to False.

    :keyword int max_content_length: max content length that this route could handle,
                                     in bytes. if not provided, it will be set to
                                     `restricted_max_content_length` api config key.
                                     note that this value should be lesser than or equal
                                     to `max_content_length` api config key, otherwise
                                     it will cause an error.

    :keyword int status_code: status code to be returned on successful responses.
                              defaults to corresponding status code of request's
                              http method if not provided.

    :note status_code: it could be a value from `InformationResponseCodeEnum`
                       or `SuccessfulResponseCodeEnum` or `RedirectionResponseCodeEnum`.

    :keyword bool strict_status: specifies that it should only consider
                                 the status code as processed if it is from
                                 `InformationResponseCodeEnum` or
                                 `SuccessfulResponseCodeEnum` or
                                 `RedirectionResponseCodeEnum` values. otherwise
                                 all codes from `INFORMATION_CODE_MIN`
                                 to `INFORMATION_CODE_MAX` or from
                                 `SUCCESS_CODE_MIN` to `SUCCESS_CODE_MAX`
                                 or from `REDIRECTION_CODE_MIN` to
                                 `REDIRECTION_CODE_MAX` will be considered
                                 as processed. defaults to True if not provided.

    :keyword str | list[str] environments: a list of all environments that this
                                           route must be exposed on them.
                                           the values could be from all available
                                           environments in environments config store.
                                           for example: `production`, `development`.
                                           if not provided, the route will be exposed
                                           on all environments.

    :keyword ResultSchema result_schema: result schema to be used to filter results.

    :keyword bool exposed_only: if set to False, it returns all
                                columns of the entity as dict.
                                it will be used only for entity conversion.
                                if not provided, defaults to True.
                                this value will override the corresponding
                                value of `result_schema` if provided.

    :keyword int depth: a value indicating the depth for conversion.
                        for example if entity A has a relationship with
                        entity B and there is a list of B in A, if `depth=0`
                        is provided, then just columns of A will be available
                        in result dict, but if `depth=1` is provided, then all
                        B entities in A will also be included in the result dict.
                        actually, `depth` specifies that relationships in an
                        entity should be followed by how much depth.
                        note that, if `columns` is also provided, it is required to
                        specify relationship property names in provided columns.
                        otherwise they won't be included even if `depth` is provided.
                        defaults to `default_depth` value of database config store.
                        please be careful on increasing `depth`, it could fail
                        application if set to higher values. choose it wisely.
                        normally the maximum acceptable `depth` would be 2 or 3.
                        there is a hard limit for max valid `depth` which is set
                        in `ConverterMixin.MAX_DEPTH` class variable. providing higher
                        `depth` value than this limit, will cause an error.
                        it will be used only for entity conversion.
                        this value will override the corresponding value of
                        `result_schema` if provided.

    :keyword bool provide_automatic_options: controls whether the `OPTIONS` method should be
                                             added automatically.
                                             this can also be controlled by setting the
                                             `view_func.provide_automatic_options = False`
                                             before adding the rule.

    :keyword dict defaults: an optional dict with defaults for other rules with the
                            same endpoint. this is a bit tricky but useful if you
                            want to have unique urls.

    :keyword str subdomain: the subdomain rule string for this rule. If not specified the
                            rule only matches for the `default_subdomain` of the map. if
                            the map is not bound to a subdomain this feature is disabled.

    :keyword bool strict_slashes: override the `Map` setting for `strict_slashes` only for
                                  this rule. if not specified the `Map` setting is used.

    :keyword bool merge_slashes: override `Map.merge_slashes` for this rule.

    :keyword bool build_only: set this to True and the rule will never match but will
                              create a url that can be build. this is useful if you have
                              resources on a subdomain or folder that are not handled by
                              the WSGI application (like static data)

    :keyword str | callable redirect_to: if given this must be either a string
                                         or callable. in case of a callable it's
                                         called with the url adapter that
                                         triggered the match and the values
                                         of the url as keyword arguments and has
                                         to return the target for the redirect,
                                         otherwise it has to be a string with
                                         placeholders in rule syntax.

    :keyword bool alias: if enabled this rule serves as an alias for another rule with
                         the same endpoint and arguments.

    :keyword str host: if provided and the url map has host matching enabled this can be
                       used to provide a match rule for the whole host. this also means
                       that the subdomain feature is disabled.

    :keyword bool websocket: if set to True, this rule is only matches for
                             websocket (`ws://`, `wss://`) requests. by default,
                             rules will only match for http requests.
                             defaults to False if not provided.

    :raises DuplicateRouteURLError: duplicate route url error.
    :raises OverwritingEndpointIsNotAllowedError: overwriting endpoint is not allowed error.
    :raises MaxContentLengthLimitMismatchError: max content length limit mismatch error.
    :raises InvalidViewFunctionTypeError: invalid view function type error.
    :raises InvalidResultSchemaTypeError: invalid result schema type error.
    :raises InvalidResponseStatusCodeError: invalid response status code error.

    :rtype: function
    """

    def decorator(func):
        """
        decorates the given function and registers it as an api handler.

        :param function func: function to register it as an api handler.

        :rtype: function
        """

        router_services.add_route(url, view_func=func, methods=methods,
                                  authenticated=authenticated,
                                  permissions=permissions, **options)

        return func

    return decorator
