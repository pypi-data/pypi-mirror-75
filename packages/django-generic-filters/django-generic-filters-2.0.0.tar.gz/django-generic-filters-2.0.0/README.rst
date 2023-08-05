######################
django-generic-filters
######################

`django-generic-filters` is a toolkit to filter results of Django's
``ListView``, using forms.

Main use cases are obviously search forms and filtered lists.

As a developer, given you have a ``ListView``, in order to let the user
filter the results:

* use a form to easily render the filters as HTML;
* the user typically sends the filters via GET;
* validate the user's input using a Django form;
* filter the Django view's queryset using form's cleaned data.

.. image:: https://secure.travis-ci.org/peopledoc/django-generic-filters.png?branch=master
   :alt: Build Status
   :target: https://secure.travis-ci.org/peopledoc/django-generic-filters


*******
Example
*******

**views.py**

.. code-block:: python

    from django_genericfilters.views import FilteredListView


    class UserListView(FilteredListView):
        # ListView options. FilteredListView inherits from ListView.
        model = User
        template_name = 'user/user_list.html'
        paginate_by = 10
        context_object_name = 'users'

        # FormMixin options. FilteredListView inherits from FormMixin.
        form_class = UserListForm

        # FilteredListView options.
        search_fields = ['first_name', 'last_name', 'username', 'email']
        filter_fields = ['is_active', 'is_staff', 'is_superuser']
        default_order = 'last_name'

        def form_valid(self, form):
            """Return the queryset when form has been submitted."""
            queryset = super(UserListView, self).form_valid(form)

            # Handle specific fields of the custom ListForm
            # Others are automatically handled by FilteredListView.

            if form.cleaned_data['is_active'] == 'yes':
                queryset = queryset.filter(is_active=True)
            elif form.cleaned_data['is_active'] == 'no':
                queryset = queryset.filter(is_active=False)

            if form.cleaned_data['is_staff'] == 'yes':
                queryset = queryset.filter(is_staff=True)
            elif form.cleaned_data['is_staff'] == 'no':
                queryset = queryset.filter(is_staff=False)

            if form.cleaned_data['is_superuser'] == 'yes':
                queryset = queryset.filter(is_superuser=True)
            elif form.cleaned_data['is_superuser'] == 'no':
                queryset = queryset.filter(is_superuser=False)

            return queryset


**forms.py**

.. code-block:: python

    from django import forms
    from django.utils.translation import ugettext_lazy as _
    from django_genericfilters import forms as gf


    class UserListForm(gf.QueryFormMixin, gf.OrderFormMixin, gf.FilteredForm):
        is_active = gf.ChoiceField(label=_('Status'),
                                   choices=(('yes', _('Active')),
                                            ('no', _('Unactive'))))

        is_staff = gf.ChoiceField(label=_('Staff'))

        is_superuser = gf.ChoiceField(label=_('Superuser'))

        def get_order_by_choices(self):
            return [('date_joined', _(u'date joined')),
                    ('last_login', _(u'last login')),
                    ('last_name', _(u'Name'))]


*****
Forms
*****

Several form mixins are provided to cover frequent use cases:

* ``OrderFormMixin`` with order_by and order_reverse fields.
* ``QueryFormMixin`` for little full-text search using icontains.

See "mixin" documentation for details.

*******
Release
*******

To prepare a new version:

* Create a branch named ``release/<version>``
* In a commit, change the ``CHANGELOG`` and ``VERSION`` file to remove the ``.dev0`` and set the date of the release
* In a second commit, change the ``VERSION`` to the next version number + ``.dev0``
* Create a PR for your branch
* When the PR is merged, tag the first commit with the version number, and create a github release using the ``CHANGELOG``

To release a new version (including the wheel)::

    pip install twine
    python setup.py sdist bdist_wheel
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

And after testing everything works fine on the testing repository::

    twine upload dist/*

**********
Ressources
**********

* Documentation: https://django-generic-filters.readthedocs.io
* PyPI page: http://pypi.python.org/pypi/django-generic-filters
* Code repository: https://github.com/novapost/django-generic-filters
* Bugtracker: https://github.com/novapost/django-generic-filters/issues
* Continuous integration: https://travis-ci.org/novapost/django-generic-filters
