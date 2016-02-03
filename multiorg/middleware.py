import logging

from django.conf import settings
from django.db.models.loading import get_model

logger = logging.getLogger(__name__)


class MultiorgMiddleware(object):
    """
    Checks for the presence of 'multiorg_adopted_org' on the session. The value
    should be the ID of the organization currently adopted by the user. If no
    organization has been adopted, the user's default is used.

    In either case, an 'adopted_org' attr is put on `request.user`.
    """

    def process_request(self, request):
        adopted_org_attr = getattr(settings, 'MULTIORG_ADOPTED_ORG_ATTR',
                                   'adopted_org')
        org_model = get_model(settings.MULTIORG_ORGANIZATION_MODEL)

        try:
            org_id = request.session['multiorg_adopted_org']
            org_instance = org_model.objects.get(pk=org_id)
        except (KeyError, ValueError, org_model.DoesNotExist):
            # Just use default if this fails in any way.
            org_instance = getattr(request.user,
                                   settings.MULTIORG_ORGANIZATION_DEFAULT_ATTR,
                                   None)

        setattr(request.user, adopted_org_attr, org_instance)

        logger.debug("User's adopted org is %s, assigned to the '%s' attr.",
                     getattr(request.user, adopted_org_attr), adopted_org_attr)
