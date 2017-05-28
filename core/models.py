from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import us


class QTourUser(models.Model):

    user = models.OneToOneField(User)


class Tournament(models.Model):

    name = models.CharField(max_length=500)
    date = models.DateField()
    location = models.CharField(max_length=500, null=True)
    base_fee = models.PositiveIntegerField()

    acf = models.BooleanField(default=False)

    description = models.TextField(null=True)
    announcement_url = models.URLField(null=True)

    adjustments = models.ManyToManyField('DiscountOrPenalty',
                                         related_name='tournament_adjustments')
    packet_adjustments = models.ManyToManyField('PacketDiscountOrPenalty',
                                                related_name='tournament_packet_adjustments')

    owner = models.ForeignKey(QTourUser)


class TournamentSite(models.Model):

    tournament = models.ForeignKey(Tournament)

    site_name = models.CharField(max_length=500)

    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=4, choices=[(state.abbr, state.name) for state in us.STATES], null=True)
    zip = models.CharField(max_length=5)
    country = models.CharField(max_length=100)

    owner = models.ForeignKey(QTourUser)


class School(models.Model):

    name = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=4, choices=[(state.abbr, state.name) for state in us.STATES])
    country = models.CharField(max_length=100)

    manager = models.ForeignKey(QTourUser, null=True)

    def __str__(self):
        return self.name + ', ' + self.city


class Player(models.Model):

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, null=True)


# discounts and penalties

class DiscountOrPenalty(models.Model):

    name = models.CharField(max_length=100)
    tournament = models.ForeignKey(Tournament, null=True)
    site = models.ForeignKey(TournamentSite, null=True)


class StaffDiscount(DiscountOrPenalty):

    discount_per_staffer = models.IntegerField()


class BuzzerDiscount(DiscountOrPenalty):

    discount_per_buzzer = models.IntegerField()


class TravelDiscount(DiscountOrPenalty):

    miles = models.IntegerField()
    discount_per_miles = models.IntegerField()


class PacketDiscountOrPenalty(DiscountOrPenalty):

    submission_date = models.DateField()
    amount = models.IntegerField()


class RegistrationEntry(models.Model):

    school = models.ForeignKey(School)
    tournament = models.ForeignKey(Tournament)
    site = models.ForeignKey(TournamentSite)
    buzzers = models.IntegerField()
    staff = models.IntegerField()
    travel_distance = models.IntegerField()
    packet_submitted_on = models.DateField()


class Team(models.Model):

    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, null=True)
    tournament = models.ForeignKey(Tournament)
    tournament_site = models.ForeignKey(TournamentSite)
    registration = models.ForeignKey(RegistrationEntry)