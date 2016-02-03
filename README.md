django-multiorg
===============
Allow users to view a Django application as a member of different organizations.


Using django-multiorg
---------------------
django-multiorg is agnostic about your current user/organization makeup. In fact, it was developed in an architecture where users were initially members of only one organization.

All that's required is that the user model (per Django's `get_user_model`) have an M2M relationship with the organization model.

However, since we don't make any assumptions about your project's architecture, some configuration is required. All settings should be placed in your Django project's settings. 

Required configurations:

* `MULTIORG_ORGANIZATION_MODEL`: the model your User model has an M2M relationship with. Example: `'companies.Company'`.
* `MULTIORG_ORGANIZATION_ATTR`: the name of the attribute on the User model for this M2M relationship. Example: `'companies'`.
* `MULTIORG_ORGANIZATION_DEFAULT_ATTR`: the name of the attribute on the User model to use as a default, if no organization has been adopted. Example: `company`.  

Optional configurations:

* `MULTIORG_REDIRECT_URL`: the path the user should be redirected to after adopting an organization. Default: `'/'`.
* `MULTIORG_NEXT_PARAM_NAME`: the name of a GET/POST param that contains a destination for redirects after organization adoption. Default: `'next_url'`.


Example use
-----------
In some cases, we determine what to show users based on their `company` attribute:
 
    class CompanyUserView(View):
        ...
        def get_context_data(self):
            ctx = {}
            ctx['company_users'] = User.objects.filter(company=self.request.user.company)
            ...
            return ctx
    
With django-multiorg, the user can *adopt* a new company, allowing them to see the users for any company they're associated with. 


Release status
--------------
Although we are just now releasing django-multiorg, it has been in production use for nearly a year at [Experiment Engine](https://www.experimentengine.com/).

Acknowledgements
----------------
django-multiorg's implementation is modeled on [django-masquerade](https://bitbucket.org/technivore/django-masquerade/), which allows
staff users to view a Django-powered site as though they were another user.
