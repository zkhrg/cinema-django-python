from django.shortcuts import render, redirect
from .models import Movie, Hall, Seance, Ticket, Order
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def start_page(request):
    movies_list = Movie.objects.all()
    hall_list = Hall.objects.all()
    context = {'movies_list': movies_list}
    context['hall_list'] = hall_list
    if request.user.is_authenticated:
        context['auth'] = True

    return render(request, 'index.html', context)


def movies_page(request):
    movies_list = Movie.objects.all()
    context = {'movies_list': movies_list}

    if request.user.is_authenticated:
        context['auth'] = True

    return render(request, 'movies.html', context)


def movie_page(request, movie_slug):
    context = {}
    if request.user.is_authenticated:
        context['auth'] = True

    movie = Movie.objects.get(movie_slug=movie_slug)
    seance_list = list(Seance.objects.filter(movie=movie))
    print(f"\n\n\n{seance_list}\n\n\n")
    context['movie'] = movie
    context['seance_list'] = seance_list

    return render(request, 'movie.html', context)


def seance_page(request, movie_slug, seance_slug):
    """необходимо использовать movie_slug для использования поиска нужного фильма, чтобы к нему отрендерить сеанс"""
    context = dict()

    if request.user.is_authenticated:
        context['auth'] = True
    seance = Seance.objects.get(seance_slug=seance_slug)
    context['seance'] = seance
    tickets_list = Ticket.objects.filter(seance=seance)
    context['tickets_list'] = tickets_list
    context['row_count'] = ([1] * seance.hall_id.row_count).copy()
    context['place_count'] = ([1] * seance.hall_id.place_count).copy()

    if request.method == "POST":
        if 'info2' in request.POST:
            z = request.POST.get('info2', '')
            z = z.split(" ")
            # если список билетов не пустой был, когда нажималась кнопка, то выбранные билеты становятся неактивными
            # для выбора и закрепляются в заказе за юзером.
            success_message = "Были куплены билеты "
            if z[0] != '':
                for ticket in z:
                    ticket = ticket.split("_")
                    print(ticket)
                    t = Ticket.objects.get(row_number=ticket[0], place_number=ticket[1], seance=seance)
                    t.status = False
                    t.save()
                    success_message += f"| Ряд {int(ticket[0])+1}   Место {int(ticket[1])+1} "

                    usr = User.objects.get(username=request.user.username)
                    order = Order(ticket=t, customer=usr)
                    order.save()
            else:
                success_message = "Билеты не были куплены"
            messages.success(request, success_message)

            return redirect(request.path_info)

    return render(request, 'seance.html', context)


def halls_page(request):
    halls_list = Hall.objects.all()
    context = {'halls_list': halls_list}

    if request.user.is_authenticated:
        context['auth'] = True

    return render(request, 'halls.html', context)


def order_page(request):
    context = {}

    if request.user.is_authenticated:
        context['auth'] = True

    return render(request, 'buy.html', context)


@login_required(login_url='login')
def profile_page(request):
    context = {}

    if request.user.is_authenticated:
        context['auth'] = True

    orders_list = Order.objects.filter(customer=request.user)
    context['orders_list'] = orders_list

    return render(request, 'profile.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('start')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('start')
        messages.error(request, "Email или пароль введены неправильно")

    context = {}
    return render(request, 'login.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('start')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except form.ValidationError as ve:
                context = {'form': form, 'validation_errors': ve}
                return render(request, 'register.html', context)
            user = form.cleaned_data.get('email')
            messages.success(request, f"Аккаунт успешно зарегистрирован на почту {user}")

            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('start')
