import requests
import logging

from celery import shared_task
from django.conf import settings
from minutes.models import Edition

headers = {
    "Authorization": "Token {}".format(settings.MINUTES_API_TOKEN),
    "Content-Type": "application/json",
}

logger = logging.getLogger("django")


@shared_task(acks_late=True)
def publish(epk, mode="STAGING"):
    edition = Edition.objects.get(id=epk)
    headers = {"Authorization": "Token " + settings.MINUTES_MAGNETO_TOKEN}
    data = {
        "action": "trigger",
        "build": "bakery-minutes",
        "environment": {
            "EDITION": edition.id.urn[9:],
            "EDITION_NAME": str(edition),
            "EDITION_LATEST": "Yes" if edition.is_latest_live() else "No",
            "VERTICAL_NAME": edition.vertical.name,
            "MODE": mode,
        },
    }

    resp = requests.post(
        "https://magneto.politicoapps.com", json=data, headers=headers
    )

    if mode == "PRODUCTION" and resp.status_code == 200:
        e = Edition.objects.get(id=edition)
        e.is_published = True
        e.save()

    return resp


@shared_task(acks_late=True)
def unpublish(edition):
    data = {"action": "unpublish", "data": edition}

    e = Edition.objects.get(id=edition)
    e.live = False
    e.save()

    if e == Edition.objects.latest_live(e.vertical):
        publish_latest(e.vertical.id.hex)

    requests.post(settings.MINUTES_BAKERY_URL, json=data, headers=headers)


@shared_task(acks_late=True)
def publish_latest(vertical):
    # change this to PRODUCTION when launching
    publish(Edition.objects.latest_live(vertical).id.hex, "STAGING")


@shared_task(acks_late=True)
def publish_if_ready(edition):
    e = Edition.objects.get(id=edition)
    if e.should_publish():
        # change this to PRODUCTION when launching
        publish(edition, "STAGING")


@shared_task(acks_late=True)
def autopublisher():
    logger.info("MINUTES: Starting autopublishing cycle...")
    for e in Edition.objects.all():
        logger.info('MINUTES: Publishing edition "{}"...'.format(e.id))
        publish_if_ready(e.id)
    logger.info("MINUTES: Autopublishing cycle complete.")
