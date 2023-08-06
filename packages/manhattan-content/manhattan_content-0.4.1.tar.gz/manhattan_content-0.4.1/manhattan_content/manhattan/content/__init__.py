import flask
import jinja2
from manhattan import forms, manage

from manhattan.content.snippets import GlobalRegion
from manhattan.content.views.update_global_contents import \
        update_global_contents_chains
from manhattan.content.utils.templates import (
    image_proxy,
    image_set_proxy,
    image_set_version,
    image_transform
)

__all__ = ['Content']


class ContentPublic:
    """
    The `ContentPublic` class provides initialization code for the package on
    public  applications.
    """

    def __init__(self,
        app,
        authenticate=None,
        base_url='',
        manage_app_tag='manage'
        ):
        self._app = app
        self._manage_app_tag = manage_app_tag

        # Register self with the app
        self._app._content = self

        # Jinja

        # Globals
        app.jinja_env.globals.update(dict(
            get_global_region=GlobalRegion.get_content,
            image_proxy=image_proxy,
            image_set_proxy=image_set_proxy,
            image_set_version=image_set_version,
            image_transform=image_transform
        ))

        # Context processors
        @app.context_processor
        def add_context():

            # Add a context processor to inject information required by the
            # frontend content editing environment into the Jinja environment.
            context = {
                'manhattan_content_init': False,
                'manhattan_content_base_url': None,
                'manhattan_content_var_name': None
            }

            # Check there's a blueprint associated with the URL
            if not flask.request.blueprint:
                return context

            # Find the manage app (there must be a manage app to support
            # content editing).
            manage_app = manage.utils.get_app(
                app._dispatcher,
                manage_app_tag
            )
            if not manage_app:
                return context

            # Ensure a user is logged in
            if authenticate and not authenticate():
                return context

            # The content editing environment should be initialized
            context['manhattan_content_init'] = True

            # Add CSRF token
            if manage_app.config.get('CSRF_SECRET_KEY'):
                context['manhattan_content_csrf_token'] = \
                    forms.CSRF.generate_token()

            # Find the manage blueprint associated with the request blueprint
            blueprint_name = 'manage_' + flask.request.blueprint
            manage_blueprint = manage_app.blueprints.get(blueprint_name)
            if manage_blueprint:

                # Look up the manage blueprint's config and see if it provides
                # a base URL.
                config = manage.utils.get_config(manage_app, blueprint_name)
                if hasattr(config, 'content_base_url'):
                    context['manhattan_content_base_url'] = \
                        config.content_base_url

                # Generate base params required to find the document
                context['manhattan_content_var_name'] = config.var_name

            return context


class ContentManage:
    """
    The `ContentManage` class provides initialization code for the package on
    manage applications.
    """

    def __init__(
        self,
        app,
        base_url='',
        update_global_contents_path='/update-global-contents'
        ):
        self._app = app

        # Views

        # Add view for updating global regions
        self._app.add_url_rule(
            base_url + update_global_contents_path,
            endpoint='update_global_contents',
            view_func=update_global_contents_chains.copy().flask_view(),
            methods=['POST']
            )
