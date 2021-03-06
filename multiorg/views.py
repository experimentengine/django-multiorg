import logging

from django.conf import settings
from django.db.models.loading import get_model
from django.http import HttpResponseBadRequest, HttpResponseForbidden, \
    HttpResponseRedirect
from django.views.generic import View


logger = logging.getLogger(__name__)

MULTIORG_REDIRECT_URL = getattr(settings, 'MULTIORG_REDIRECT_URL', '/')
NEXT_URL_PARAM_NAME = getattr(settings, 'MULTIORG_NEXT_PARAM_NAME', 'next_url')
ADMINS_ADOPT_ANY = getattr(settings, 'MULTIORG_ADMINS_ADOPT_ANY', False)


class MultiorgAdoptionView(View):
    """
    Sets a session variable for a user-adopted organization (e.g. Company).
    """
    def _adopt_org(self, organization_id, redirect_destination):
        if organization_id is None:
            return HttpResponseBadRequest()

        try:
            organization_id = int(organization_id)
        except ValueError:
            return HttpResponseBadRequest()

        org_model = get_model(settings.MULTIORG_ORGANIZATION_MODEL)
        try:
            organization = org_model.objects.get(id=organization_id)
        except org_model.DoesNotExist:
            return HttpResponseRedirect(redirect_destination)

        user_organizations = getattr(self.request.user,
                                     settings.MULTIORG_ORGANIZATION_ATTR)
        if organization not in user_organizations.all():
            logger.debug('Requested organization %s not in user orgs %s', organization_id, user_organizations.all())
            if not (ADMINS_ADOPT_ANY and self.request.user.is_staff):
                logger.debug('Admins can adopt any: %s, user is staff: %s', ADMINS_ADOPT_ANY, self.request.user.is_staff)
                return HttpResponseForbidden()

        # At this point, we know the user is allowed to adopt an existing organization.
        self.request.session['multiorg_adopted_org'] = organization_id
        return HttpResponseRedirect(redirect_destination)

    def post(self, request):
        logger.debug('Got POST: %s', self.request.POST)
        organization_id = self.request.POST.get('organization_id')
        redirect_destination = self.request.POST.get(NEXT_URL_PARAM_NAME,
                                                     MULTIORG_REDIRECT_URL)
        return self._adopt_org(organization_id, redirect_destination)

    def get(self, request):
        logger.debug('Got GET: %s', self.request.GET)
        organization_id = self.request.GET.get('organization_id')
        redirect_destination = self.request.GET.get(NEXT_URL_PARAM_NAME,
                                                    MULTIORG_REDIRECT_URL)
        return self._adopt_org(organization_id, redirect_destination)
