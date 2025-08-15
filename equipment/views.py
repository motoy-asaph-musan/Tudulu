# equipment/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
import openpyxl
from xhtml2pdf import pisa

from .models import InstalledEquipment, Post, Like, Comment
from .forms import InstalledEquipmentForm, PostForm, CommentForm

# STRIPE FOR PAYMENT SYSTEM
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse



stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def upgrade(request):
    return render(request, "upgrade.html", {"stripe_public_key": settings.STRIPE_PUBLIC_KEY})

def upgrade_cancel(request):
    # Here you can handle cancelling premium subscription
    messages.info(request, "Your subscription has been cancelled.")
    return redirect("profile")  # Change 'profile' to your actual profile view name

@login_required
def process_payment(request):
    if request.method == "POST":
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Premium Membership'},
                    'unit_amount': 11,  # $5 in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/upgrade/success/'),
            cancel_url=request.build_absolute_uri('/upgrade/cancel/'),
        )
        return redirect(session.url, code=303)

# @login_required
# def cancel_subscription(request):
#     try:
#         customer = stripe.Customer.list(email=request.user.email).data[0]
#         subscriptions = stripe.Subscription.list(customer=customer.id, status="active")

#         if subscriptions.data:
#             sub_id = subscriptions.data[0].id
#             stripe.Subscription.delete(sub_id)
#             request.user.is_premium = False
#             request.user.save()
#             messages.success(request, "Your subscription has been cancelled.")
#         else:
#             messages.error(request, "No active subscription found.")
#     except Exception as e:
#         messages.error(request, f"Error: {str(e)}")

#     return redirect('profile')  # Or wherever your profile page is

@login_required
def cancel_subscription(request):
    profile = request.user.profile  # Assuming you have a profile model with subscription info

    if not profile.stripe_subscription_id:
        messages.error(request, "No active subscription found.")
        return redirect('profile')

    try:
        # Cancel at the end of the current billing cycle
        stripe.Subscription.modify(
            profile.stripe_subscription_id,
            cancel_at_period_end=True
        )
        profile.is_premium = False
        profile.save()
        messages.success(request, "Your subscription has been canceled. You will keep access until the end of the billing period.")
    except stripe.error.StripeError as e:
        messages.error(request, f"Error canceling subscription: {e.user_message}")

    return redirect('profile')

@login_required
def upgrade_success(request):
    profile = request.user.profile
    profile.is_premium = True
    profile.save()
    return render(request, "upgrade_success.html")

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Premium Plan',
                    },
                    'unit_amount': 500,  # $5.00
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + reverse('payment_success'),
            cancel_url=YOUR_DOMAIN + reverse('payment_cancel'),
        )
        return redirect(checkout_session.url)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.get('client_reference_id')
        # lookup user and set is_premium = True

    return HttpResponse(status=200)

@login_required
def payment_success(request):
    profile = request.user.profile
    profile.is_premium = True
    profile.save()
    return render(request, 'payment_success.html') 

@login_required
def upload_image(request):
    if not request.user.profile.is_premium:
        messages.error(request, "Upgrade to Premium to upload images!")
        return redirect('upgrade')

    # normal upload logic here...


# ----------- POSTS -----------
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'equipment/create_post.html', {'form': form})


@login_required
def post_list(request):
    query = request.GET.get('q')
    tag_filter = request.GET.get('tag')

    posts = Post.objects.all().order_by('-created_at')

    if query:
        posts = posts.filter(content__icontains=query)

    if tag_filter and tag_filter != 'all':
        posts = posts.filter(tags=tag_filter)

    comment_form = CommentForm()
    return render(request, 'equipment/home.html', {
        'posts': posts,
        'comment_form': comment_form,
        'query': query or '',
        'tag_filter': tag_filter or 'all'
    })


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('home')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('home')


# ----------- EQUIPMENT -----------
@login_required
def add_equipment(request):
    if request.method == 'POST':
        form = InstalledEquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.user = request.user  # Owner of the equipment
            equipment.added_by = request.user
            equipment.save()
            return redirect('equipment-list')
    else:
        form = InstalledEquipmentForm()
    return render(request, 'equipment/add_equipment.html', {'form': form})


@login_required
def equipment_list(request):
    # Filter by email from user profile
    user_email = request.user.email
    equipment = InstalledEquipment.objects.filter(user=request.user) #InstalledEquipment.objects.filter(user__email=user_email)
    

    today = date.today()

    for item in equipment:
        if item.next_service_date and item.next_service_date < today:
            item.status_display = "Overdue"
        elif item.next_service_date and (item.next_service_date - today).days <= 7:
            item.status_display = "Upcoming"
        else:
            item.status_display = "OK"

    # Search / Filter
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    if query:
        equipment = [e for e in equipment if query.lower() in e.name.lower() or query.lower() in e.location.lower()]

    if status_filter and status_filter != "All":
        equipment = [e for e in equipment if getattr(e, 'status_display', e.status) == status_filter]

    paginator = Paginator(equipment, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'equipment/equipment_list.html', {
        'page_obj': page_obj,
        'query': query or '',
        'status_filter': status_filter or 'All'
    })


# ----------- EXPORTS -----------
@login_required
def export_excel(request):
    equipment = InstalledEquipment.objects.filter(user__email=request.user.email)
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=equipment.xlsx'

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Installed Equipment'

    headers = ['Name', 'Serial Number', 'Location', 'Date Installed', 'Next Service Date']
    sheet.append(headers)

    for e in equipment:
        sheet.append([
            e.name,
            e.serial_number,
            e.location,
            str(e.date_installed or ''),
            str(e.next_service_date or '')
        ])

    workbook.save(response)
    return response


@login_required
def export_pdf(request):
    equipment = InstalledEquipment.objects.filter(user__email=request.user.email)
    template = get_template('equipment/pdf_template.html')
    html = template.render({'equipment': equipment})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="equipment.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response


# ----------- AUTH -----------
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'registration/login.html')


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


# ----------- STATIC HOME -----------
def home(request):
    return render(request, 'equipment/home.html')
