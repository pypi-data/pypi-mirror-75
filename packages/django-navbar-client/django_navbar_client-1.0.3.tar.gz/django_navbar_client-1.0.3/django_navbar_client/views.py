from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django_navbar_client.models import AuthProfile
from urllib.parse import urlencode

import requests
import logging


logger = logging.getLogger(__name__)


def oauth_logout(request, **kwargs):
    user = request.user
    if user.is_anonymous:
        logger.warning("Anonymous logout attempted")
        return redirect(kwargs.get("next", reverse('home')))

    oauth_profile, created = AuthProfile.objects.get_or_create(user=user)
    if created:
        logger.warning("Profile Created during logout: %s", oauth_profile.user.username)
        return redirect(kwargs.get("next", reverse('home')))

    url = settings.OAUTH_SERVER_URL + "o/revoke_token/"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = "token={}&client_id={}&client_secret={}".format(
        oauth_profile.token,
        settings.OAUTH_CLIENT_ID,
        settings.OAUTH_CLIENT_SECRET
    )

    r = requests.post(url=url, headers=headers, data=data)
    if r.status_code == 200:
        logger.info("OAUTH token revoked server")
    else:
        logger.warning("OAuth Logout failed: %i", r.status_code)
        logger.warning("\tURL: %s", url)
        logger.warning("\tHEADERS: %s", headers)
        logger.warning("\tBODY: %s", data)
        logger.debug(r.json())

    # url = settings.OAUTH_SERVER_URL + "view/logout/"
    url = "{}accounts/logout/?{}".format(
        settings.OAUTH_SERVER_URL,
        urlencode({
            "next": request.build_absolute_uri('home')
           })
    )
    logout(request)
    return redirect(url)
    # headers = {"Authorization": oauth_profile.token}
    # # r = PM.request(method='GET', url=url, headers=headers)
    # r = requests.get(url=url, headers=headers)
    # if r.status_code == 200:
    #     logger.info("Logged out in OAUTH server")
    # else:
    #     logger.error("OAuth Logout failed: %i", r.status_code)
    #     logger.error("\tURL: %s", url)
    #     logger.error("\tHEADERS: %s", headers)
    #     logger.error(r.json())
    # logout(request)
    # logger.info("Logged out in local server")
    # return redirect(kwargs.get("next", reverse('home')))


def oauth_login(request):
    protocol = "https"
    logger.info("Redirect to login")
    login_url = "{0}o/authorize/?client_id={1}&response_type=code&redirect_uri={2}://{3}{4}".format(
            settings.OAUTH_SERVER_URL,
            settings.OAUTH_CLIENT_ID,
            protocol,
            request.META['HTTP_HOST'],
            reverse("django_navbar_client:callback"))
    status = request.GET.get("status", False)
    if status:
        login_url += "&status=" + status
    logging.debug("Redirect Oauth to %s", login_url)
    return redirect(login_url)


def oauth_navbar(request):
    caller = request.GET.get("caller")
    url = "{0}view/fullnav/?caller={1}".format(
        settings.OAUTH_SERVER_URL,
        caller)
    logger.info("Ask navbar for %s at %s", request.user, request.session.session_key)
    if request.user.is_authenticated:
        auth_profile, created = AuthProfile.objects.get_or_create(user=request.user)
        remote_response = ask_oauth(url, auth_profile.token)
    else:
        remote_response = ask_oauth(url, None)
    if remote_response.status_code != 200:
        logger.error("Auth server returned an error(%s):\n  %s\n heads:\n  %s  ",
                     remote_response.status_code,
                     remote_response.text,
                     remote_response.headers)
    return HttpResponse(content=remote_response.text, status=remote_response.status_code)


def oauth_callback(request, **kwargs):
    protocol = "https"
    logger.info("A Login callback received")
    logger.debug("data %s", request.GET)
    # Prepare request data
    url = settings.OAUTH_SERVER_URL + "o/token/"
    code = request.GET["code"]
    call_back_url = protocol + "://" + request.META['HTTP_HOST']+reverse('django_navbar_client:callback')
    fields = {
        "grant_type": "authorization_code",
        "client_id": settings.OAUTH_CLIENT_ID,
        "client_secret": settings.OAUTH_CLIENT_SECRET,
        "code": code,
        "redirect_uri": call_back_url,
    }
    logger.info("Asking Auth server for the Token")

    r = requests.post(url=url, data=fields)
    if r.status_code == 200:
        logger.debug("\tURL: %s", url)
        logger.debug("\tFIELDS: %s", fields)
        logger.debug("Response Obtained \n\t Data: %s", r.json())
        data = r.json()
        access_token = data["token_type"] + " " + data["access_token"]
        logger.info("Asking Auth server for ME")
        url = settings.OAUTH_SERVER_URL + "api/me"
        r = ask_oauth(url, token=access_token)
        if r.status_code == 200:
            logger.debug("Response Obtained \n\t Data: %s", r.json())
            me = r.json()
            try:
                user = User.objects.get_by_natural_key(me["user"])
            except ObjectDoesNotExist:
                logger.info("Local user created for %s", me["user"])
                user = User.objects.create_user(username=me["user"])
            try:
                if me.get("level", "unknown") == "admin":
                    user.is_staff = True
                    user.is_superuser = True
                user.authprofile.token = access_token
                logger.debug("Set profile token=%s", access_token)
                user.authprofile.uuid = me["uuid"]
                logger.debug("Set profile UUID=%s", me["uuid"])
            except AttributeError:
                logger.info("Local user created for %s", me["user"])
                AuthProfile.objects.create(user=user, token=access_token, uuid=me["uuid"])
            logger.debug("Saving user and profile")
            user.save()
            user.authprofile.save()
            logger.debug("Login user into system")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            logger.debug("Logged as s% in session %s ", request.user.id, request.session.session_key)
            return redirect(kwargs.get("next", reverse('home')))
        else:
            logger.warning("Something went wrong asking ME: %i", r.status_code)
            logger.warning("\tURL: %s", url)
            logger.debug(r.json())
    else:
        logger.warning("Something went wrong asking token: %i", r.status_code)
        logger.warning("\tURL: %s", url)
        logger.warning("\tFIELDS: %s", fields)
        logger.debug(r.json())
    logger.info("Unsuccessful login")
    response = HttpResponse(content=r.json(), status=r.status_code)
    return response


def ask_oauth(url, token, refesh=None):
    headers = None
    if token:
        headers = {"Authorization": token}
        logger.debug("\tHEADERS   : %s", headers)
    logger.debug("\tURL         : %s", url)
    print(not settings.DEBUG)
    response = requests.get(url=url, headers=headers, verify=not settings.DEBUG)
    return response
