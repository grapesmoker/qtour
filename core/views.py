from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.core.validators import EmailValidator, ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from core.models import *
from core.forms import *

from crispy_forms.layout import Button

import datetime as dt

def get_user(request):

    if request.user.is_authenticated():
        return QTourUser.objects.get(user=request.user)
    else:
        return request.user


def register(request):

    if request.method == 'GET':

        if request.user.is_authenticated():
            user = request.user
        else:
            user = None

        return render(request, 'register.html', {'user': user})

    elif request.method == 'POST':

        errors = []

        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        # affiliation = request.POST['affiliation']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        other_users = User.objects.filter(username=username)

        if other_users.exists():
            errors.append('A user with that username already exists.')

        if pass1 == '' or pass2 == '':
            errors.append('Password cannot be empty.')
        elif pass1 != pass2:
            errors.append('The two passwords you entered do not match.')

        if username is None or username.strip() == '':
            errors.append('Must enter a username.')

        emv = EmailValidator()

        try:
            res = emv(email)

        except ValidationError as ex:
            errors.append(ex.message)

        if first_name is None or first_name.strip() == '':
            errors.append('Enter a first name.')
        if last_name is None or last_name.strip() == '':
            errors.append('Enter a last name.')

        if errors:
            user_data = {'username': username,
                         'email': email,
                         'first_name': first_name,
                         'last_name': last_name}

            return render(request, 'register.html', {'errors': errors, 'user_data': user_data})

        else:
            user = User()
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.password = pass1
            user.save()

            qtour_user = QTourUser()
            qtour_user.user = user
            qtour_user.save()

            # user = authenticate(request, username=username, password=pass1)
            login(request, user)

            return render(request, 'landing.html', {'user': qtour_user})


def main(request):

    if request.method == 'GET':
        if request.user.is_authenticated():
            qtour_user = QTourUser.objects.get(user=request.user)
        else:
            qtour_user = None

        return render(request, 'landing.html', {'user': qtour_user})

def qlogin(request):

    if request.method == 'GET':
        if not request.user.is_authenticated():
            return render(request, 'login.html')
        else:
            print(request.user)
            qtour_user = QTourUser.objects.get(user=request.user)
            return render(request, 'landing.html', {'user': qtour_user})

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            qtour_user = QTourUser.objects.get(user=user)
            return render(request, 'landing.html', {'user': qtour_user})
        else:
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                message = 'Incorrect password for {}'.format(username)
            else:
                message = 'User {} not found'.format(username)

            return render(request, 'login.html', {'errors': [message],
                                                  'user': get_user(request)})

@login_required
def create_tournament(request):

    if request.method == 'GET':

        form = TournamentForm(mode='add')
        return render(request, 'tournament/tournament.html', {'form': form,
                                                              'user': get_user(request)})

    elif request.method == 'POST':

        form = TournamentForm(data=request.POST, mode='add')
        if form.is_valid():
            tour = form.save()
            tour.owner = get_user(request)
            tour.save()

            return HttpResponseRedirect('/tournament/{}'.format(tour.id))


@login_required
def tournament(request, tour_id):

    qtour_user = get_user(request)
    tournament = Tournament.objects.get(id=tour_id)

    if tournament.owner == qtour_user:
        if request.method == 'GET':
            tournament = Tournament.objects.get(id=tour_id)
            form = TournamentForm(instance=tournament, mode='edit')
            return render(request, 'tournament/tournament.html', {'form': form,
                                                                  'mode': 'edit',
                                                                  'tour_id': tour_id,
                                                                  'user': get_user(request)})

        elif request.method == 'POST':

            form = TournamentForm(data=request.POST, mode='edit', tour_id=tour_id)
            if form.is_valid():
                tournament.name = form.cleaned_data['name']
                tournament.date = form.cleaned_data['date']
                tournament.base_fee = form.cleaned_data['base_fee']
                tournament.save()

            return render(request, 'tournament/tournament.html', {'form': form,
                                                                  'tour_id': tour_id,
                                                                  'user': qtour_user})


    else:
        if request.method == 'GET':
            tournament = Tournament.objects.get(id=tour_id)
            form = TournamentForm(instance=tournament, mode='view')
            return render(request, 'tournament/site.html', {'form': form,
                                                            'tour_id': tour_id,
                                                            'user': qtour_user})


@login_required
def add_site(request, tour_id):

    qtour_user = get_user(request)
    tournament = Tournament.objects.get(id=tour_id)

    if tournament.owner == qtour_user:
        if request.method == 'GET':
            form = TournamentSiteForm(tour_id=tour_id, mode='add')
            return render(request, 'tournament/site.html', {'form': form,
                                                            'tour_id': tour_id,
                                                            'user': qtour_user})

        if request.method == 'POST':
            form = TournamentSiteForm(data=request.POST, tour_id=tour_id, mode='add')
            if form.is_valid():
                site = TournamentSite()
                site.address = form.cleaned_data['address']
                site.city = form.cleaned_data['city']
                site.state = form.cleaned_data['state']
                site.site_name = form.cleaned_data['site_name']
                site.zip = form.cleaned_data['zip']
                site.country = form.cleaned_data['country']
                site.tournament = Tournament.objects.get(id=int(form.cleaned_data['tournament']))
                site.owner = qtour_user
                site.save()
                return HttpResponseRedirect('/tournament/{}/'.format(tour_id))
            else:
                return render(request, 'tournament/site.html', {'form': form,
                                                                'tour_id': tour_id,
                                                                'user': qtour_user})


@login_required
def site(request, site_id):

    qtour_user = get_user(request)
    site = TournamentSite.objects.get(id=site_id)
    tournament = site.tournament

    if tournament.owner == qtour_user or site.owner == qtour_user:
        if request.method == 'GET':
            form = TournamentSiteForm(instance=site, tour_id=tournament.id, mode='edit')
            return render(request, 'tournament/site.html', {'form': form,
                                                            'tour_id': tournament.id,
                                                            'user': qtour_user})
        elif request.method == 'POST':
            form = TournamentSiteForm(data=request.POST, tour_id=tournament.id, mode='edit')
            if form.is_valid():
                site.address = form.cleaned_data['address']
                site.city = form.cleaned_data['city']
                site.state = form.cleaned_data['state']
                site.site_name = form.cleaned_data['site_name']
                site.zip = form.cleaned_data['zip']
                site.country = form.cleaned_data['country']
                site.save()

            return render(request, 'tournament/site.html', {'form': form,
                                                            'tour_id': tournament.id,
                                                            'user': qtour_user})

    else:
        if request.method == 'GET':
            form = TournamentSiteForm(instance=site, tour_id=tournament.id, mode='view')
            return render(request, 'tournament/site.html', {'form': form,
                                                            'tour_id': tournament.id,
                                                            'user': qtour_user})


@login_required
def your_tournaments(request):

    if request.method == 'GET':
        qtour_user = get_user(request)
        tournaments = Tournament.objects.filter(owner=qtour_user)
        return render(request, 'tournament/tournaments.html', {'user': qtour_user,
                                                               'tournaments': tournaments,
                                                               'caption': 'Your tournaments'})


@login_required
def upcoming_tournaments(request):

    if request.method == 'GET':
        qtour_user = get_user(request)
        tournaments = Tournament.objects.filter(date__gt=dt.date.today())
        return render(request, 'tournament/tournaments.html', {'user': qtour_user,
                                                               'tournaments': tournaments,
                                                               'caption': 'Upcoming tournaments'})

@login_required
def past_tournaments(request):

    if request.method == 'GET':
        qtour_user = get_user(request)
        tournaments = Tournament.objects.filter(date__lt=dt.date.today())
        return render(request, 'tournament/tournaments.html', {'user': qtour_user,
                                                               'tournaments': tournaments,
                                                               'caption': 'Past tournaments'})