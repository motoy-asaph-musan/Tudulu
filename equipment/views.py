# equipment/views.py

import json
from django.views.generic import View
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string, get_template
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.db.models import Q
from django.views import View
from django.conf import settings
from django.utils import timezone
import openpyxl
from xhtml2pdf import pisa
import stripe
import django_filters
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .filters import EquipmentFilter
from django.utils.dateparse import parse_date
from django.db.models import Q
from datetime import date, timedelta
from .models import CATEGORY_CHOICES
from .models import InstalledEquipment, Post, Like, Comment, Transaction, DueNotification
from .forms import EquipmentForm, PostForm, CommentForm, EquipmentForm
from users.models import CustomUser, UserProfile
from .models import Notification
from django.utils.timezone import now




# Create a directory for uploaded images if it doesn't exist
# This is a good practice to ensure the upload path is valid.
UPLOAD_DIR = 'uploaded_images'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@csrf_exempt
def upload_image(request):
    """
    A view to handle image uploads via a POST request.
    It saves the image file to a designated directory.
    """
    if request.method == 'POST':
        # Check if an image file is present in the request
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            # Create a file path to save the image
            file_path = os.path.join(UPLOAD_DIR, image_file.name)
            
            # Write the uploaded file to the specified path
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # Return a success message with the path to the uploaded file
            return JsonResponse({'message': 'Image uploaded successfully!', 'file_path': file_path})
        
        # If no image file is found, return an error
        return JsonResponse({'error': 'No image file found in the request.'}, status=400)
        
    # Handle non-POST requests with an error
    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


class CreateCheckoutSessionView(View):
    """
    Placeholder view for a checkout session.
    Your actual Stripe or payment integration logic would go here.
    """
    def get(self, request, *args, **kwargs):
        # This is a placeholder. You would implement your payment logic here.
        # For now, it just returns a simple JSON response.
        return JsonResponse({'message': 'This is a placeholder for CreateCheckoutSessionView.'})


def payment_success(request):
    """
    Placeholder view for handling a successful payment.
    This would typically render a success page or redirect the user.
    """
    return render(request, 'equipment/payment_success.html', {'message': 'Payment successful!'})


# ---------------- PAYMENTS ----------------
# Configure Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    """
    Creates a new Stripe Checkout session to handle payments.
    """
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Premium Plan'},
                    'unit_amount': 500, # $5.00 in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + '/equipment/payment-success/',
            cancel_url=YOUR_DOMAIN + '/equipment/payment-cancel/',
        )
        return JsonResponse({'id': checkout_session.id})

@csrf_exempt
def stripe_webhook(request):
    """
    Handles Stripe webhooks to update user subscription status after payment.
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # You can add logic here to identify the user and set their premium status
        # Example: user_id = session.get('client_reference_id')
        # user = CustomUser.objects.get(id=user_id)
        # user.profile.is_premium = True
        # user.profile.save()

    return HttpResponse(status=200)

@login_required
def payment_success(request):
    """
    View to display a success message after a payment is completed.
    This is the view linked to the Stripe success URL.
    """
    # Assuming the user's profile is updated via the webhook
    # For now, we can just show a success message
    messages.success(request, "Payment successful! You are now a premium user.")
    return render(request, 'equipment/payment_success.html')

@login_required
def upgrade(request):
    """
    Renders the upgrade page for premium membership.
    """
    return render(request, "equipment/upgrade.html", {"stripe_public_key": settings.STRIPE_PUBLIC_KEY})

@login_required
def upgrade_cancel(request):
    """
    Renders the page for a cancelled payment.
    """
    messages.info(request, "Your payment was cancelled.")
    return redirect('equipment:home')


# ---------------- EQUIPMENT VIEWS ----------------
# @login_required
# def equipment_add(request):
#     """
#     Adds new equipment to the database.
#     This view handles both GET (displaying the form) and POST (form submission).
#     """
#     if request.method == "POST":
#         form = EquipmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             equipment = form.save(commit=False)
#             equipment.created_by = request.user
#             equipment.save()
#             messages.success(request, "Equipment added successfully.")
#             return redirect("equipment:equipment_list")
#     else:
#         form = EquipmentForm()

#     return render(request, "equipment/add_equipment.html", {"form": form})

@login_required
def equipment_add(request):
    """
    Adds new equipment to the database.
    This view handles both GET (displaying the form) and POST (form submission).
    """
    if request.method == "POST":
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.user = request.user              # ✅ assign owner
            equipment.added_by = request.user          # optional: who added it
            equipment.save()
            messages.success(request, "Equipment added successfully.")
            return redirect("equipment:equipment_list")
    else:
        form = EquipmentForm()
    return render(request, "equipment/add_equipment.html", {"form": form})


# @login_required
# def equipment_list(request):
#     """
#     Displays a list of all equipment with filtering, searching, and date range.
#     """
#     query = request.GET.get("q")
#     status_filter = request.GET.get("status")
#     category_filter = request.GET.get("category")
#     start_date = request.GET.get("start_date")
#     end_date = request.GET.get("end_date")
#     date_range = request.GET.get("date_range")  # new dynamic range

#     equipments = InstalledEquipment.objects.all()

#     # Search filter
#     if query:
#         # equipments = equipments.filter(
#         #     Q(name__icontains=query) |
#         #     Q(serial_number__icontains=query) |
#         #     Q(description__icontains=query)
#         # )
#         equipments = equipments.filter(
#             Q(name__icontains=query) |
#             Q(location__icontains=query) |
#             Q(serial_number__icontains=query)
#         )


#     # Status filter
#     if status_filter:
#         equipments = equipments.filter(status=status_filter)

#     # Category filter
#     if category_filter:
#         equipments = equipments.filter(category=category_filter)

#     # Dynamic date ranges
#     if date_range:
#         today = date.today()
#         if date_range == "last_7_days":
#             equipments = equipments.filter(installed_date__gte=today - timedelta(days=7))
#         elif date_range == "last_30_days":
#             equipments = equipments.filter(installed_date__gte=today - timedelta(days=30))
#         elif date_range == "this_year":
#             equipments = equipments.filter(installed_date__year=today.year)

#     # Manual date range overrides dynamic range if provided
#     if start_date:
#         start = parse_date(start_date)
#         if start:
#             equipments = equipments.filter(installed_date__gte=start)

#     if end_date:
#         end = parse_date(end_date)
#         if end:
#             equipments = equipments.filter(installed_date__lte=end)

#     # Pagination
#     paginator = Paginator(equipments, 25)
#     page_obj = paginator.get_page(request.GET.get('page'))

#     context = {
#         "page_obj": page_obj,
#         "query": query or '',
#         "status_filter": status_filter or '',
#         "category_filter": category_filter or '',
#         "start_date": start_date or '',
#         "end_date": end_date or '',
#         "date_range": date_range or '',
#     }
#     return render(request, "equipment/equipment_list.html", context)

@login_required
def equipment_list(request):
    query = request.GET.get("q")
    status_filter = request.GET.get("status")
    category_filter = request.GET.get("category")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    date_range = request.GET.get("date_range")

    equipments = InstalledEquipment.objects.all()

    # 🔎 Search
    if query:
        equipments = equipments.filter(
            Q(name__icontains=query) |
            Q(serial_number__icontains=query) |
            Q(description__icontains=query)
        )

    # ✅ Status filter
    if status_filter:
        equipments = equipments.filter(status=status_filter)

    # ✅ Category filter
    if category_filter:
        equipments = equipments.filter(category=category_filter)

    # ✅ Handle predefined date ranges
    today = timezone.now().date()
    if date_range == "last_7_days":
        start_date = today - timedelta(days=7)
        end_date = today
    elif date_range == "last_30_days":
        start_date = today - timedelta(days=30)
        end_date = today
    elif date_range == "this_year":
        start_date = date(today.year, 1, 1)
        end_date = today

    # ✅ Apply manual/custom date range
    if start_date:
        equipments = equipments.filter(date_installed__gte=start_date)
    if end_date:
        equipments = equipments.filter(date_installed__lte=end_date)

    # 📊 Counts for dashboard
    total_equipment = equipments.count()
    active_equipment = equipments.filter(status="active").count()
    maintenance_equipment = equipments.filter(status="maintenance").count()
    retired_equipment = equipments.filter(status="retired").count()

    # 📂 Categories (assuming you use CATEGORY_CHOICES tuple)
    categories = CATEGORY_CHOICES

    # 📑 Pagination
    paginator = Paginator(equipments, 25)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "equipment_list": page_obj,
        "categories": categories,
        "query": query or "",
        "status_filter": status_filter or "",
        "category_filter": category_filter or "",
        "start_date": start_date if isinstance(start_date, str) else start_date.strftime("%Y-%m-%d") if start_date else "",
        "end_date": end_date if isinstance(end_date, str) else end_date.strftime("%Y-%m-%d") if end_date else "",
        "date_range": date_range or "",
        "total_equipment": total_equipment,
        "active_equipment": active_equipment,
        "maintenance_equipment": maintenance_equipment,
        "retired_equipment": retired_equipment,
    }
    return render(request, "equipment/equipment_list.html", context)

@login_required
def delete_equipment(request, id):
    equipment = get_object_or_404(InstalledEquipment, id=id)
    if request.method == 'POST':
        equipment.delete()
        return redirect('equipment/equipment_list.html')
    return render(request, 'equipment/confirm_delete.html', {'equipment': equipment})


# def edit_equipment(request, id):
#     equipment = get_object_or_404(InstalledEquipment, id=id)
#     if request.method == 'POST':
#         form = EquipmentForm(request.POST, instance=equipment)
#         if form.is_valid():
#             form.save()
#             return redirect('equipment/equipment_list.html')  # Or wherever you want to go after saving
#     else:
#         form = EquipmentForm(instance=equipment)
#     return render(request, 'equipment/edit_equipment.html', {'form': form})

@login_required
def edit_equipment(request, id):
    equipment = InstalledEquipment.objects.get(id=id)

    if request.method == "POST":
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipment updated successfully!")
            return redirect('equipment:equipment_list')
       
    else:
        form = EquipmentForm(instance=equipment)

    context = {"form": form, "equipment": equipment}
    return render(request, "equipment/edit_equipment.html", context)


@login_required
def equipment_detail(request, pk):
    """
    Displays details of a single equipment item.
    """
    equipment = get_object_or_404(InstalledEquipment, pk=pk)
    return render(request, "equipment/equipment_detail.html", {"equipment": equipment})


@login_required
def equipment_edit(request, pk):
    """
    Edits existing equipment details.
    """
    equipment = get_object_or_404(InstalledEquipment, pk=pk)
    if request.method == "POST":
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipment updated successfully.")
            return redirect("equipment:equipment_detail", pk=pk)
    else:
        form = EquipmentForm(instance=equipment)

    return render(request, "equipment/equipment_form.html", {"form": form, "equipment": equipment})



@login_required
def delete_equipment(request, pk):
    try:
        equipment = InstalledEquipment.objects.get(pk=pk)
    except InstalledEquipment.DoesNotExist:
        return HttpResponse("Equipment not found", status=404)

    if request.method == "POST":
        equipment.delete()
        messages.success(request, "Equipment deleted successfully!")
        return redirect('equipment:equipment_list')

    return render(request, "equipment/equipment_confirm_delete.html", {"equipment": equipment})


# ---------------- EXPORTS ----------------
@login_required
def export_excel(request):
    """
    Exports all equipment data to an Excel file.
    """
    equipment = InstalledEquipment.objects.filter(user=request.user)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=equipment.xlsx'

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Installed Equipment'

    headers = ['Name', 'Serial Number', 'Category', 'Date Installed', 'Next Service Date']
    sheet.append(headers)

    for e in equipment:
        sheet.append([e.name, e.serial_number, e.category, str(e.date_installed or ''), str(e.next_service_date or '')])

    workbook.save(response)
    return response


@login_required
def export_pdf(request):
    """
    Exports all equipment data to a PDF file.
    """
    equipment = InstalledEquipment.objects.filter(user=request.user)
    template = get_template('equipment/pdf_template.html')
    html = template.render({'equipment': equipment})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="equipment.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response


# ---------------- POSTS AND COMMENTS ----------------

def home(request):
    """
    Render the home page with posts, equipment stats, 
    and optional search functionality for posts or people.
    """

    # Get query parameters
    query = request.GET.get("q")
    category = request.GET.get("category")
    filter_type = request.GET.get("filter", "posts")  # Default: search posts

    # Base queryset
    posts = Post.objects.all().order_by("-created_at")
    users = None

    # Apply search filters
    if query:
        if filter_type == "posts":
            posts = posts.filter(
                Q(content__icontains=query) |
                Q(tags__icontains=query) |   # ✅ fixed
                Q(author__username__icontains=query)
            ).distinct()
        elif filter_type == "people":
            users = User.objects.filter(
                Q(username__icontains=query) | Q(profile__bio__icontains=query)
            ).distinct()
    # Apply category filter if provided
    if category:
        posts = posts.filter(tags__iexact=category)  # ✅ no `.name`

    # Equipment stats
    total_equipment = InstalledEquipment.objects.count()
    recent_equipment = InstalledEquipment.objects.order_by("-date_installed")[:5]

    context = {
        "posts": posts,
        "users": users,
        "total_equipment": total_equipment,
        "recent_equipment": recent_equipment,
    }

    return render(request, "equipment/home.html", context)

@login_required
def create_post(request):
    """
    Creates a new post.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('equipment:home')
    else:
        form = PostForm()
    return render(request, 'equipment/create_post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    """
    Displays a single post and its comments. Handles comment submission.
    """
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(is_approved=True)
    # comments = post.comment_set.filter(is_approved=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, "Your comment is awaiting moderation.")
            # return redirect('equipment:post_detail', post_id=post_id)
            return redirect(reverse('equipment:post_detail', args=[post_id]) + '#comments')
        
    else:
        comment_form = CommentForm()
    comments = post.comments.filter(is_approved=True)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'equipment/post_detail.html', context)

@login_required
def edit_post(request, post_id):
    """
    Edits an existing post.
    """
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('equipment:post_detail', post_id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('equipment:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'equipment/edit_post.html', context)

@login_required
def delete_post(request, post_id):
    """
    Deletes a post.
    """
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this post.")
    return redirect('equipment:home')

@login_required
@require_POST
def add_comment(request, post_id):
    """
    Adds a comment to a post and notifies the post author.
    """
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

        # Success feedback
        messages.success(request, "Comment submitted successfully!")

        # Create notification (only if commenter is not the author)
        if request.user != post.author:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                notification_type="comment",
                post=post,
                message=f"{request.user.username} commented on your post."
            )
    else:
        messages.error(request, "There was an error submitting your comment.")

    return redirect("equipment:post_detail", post_id=post_id)

@login_required
def like_post(request, pk):
    """
    Handles liking and un-liking a post.
    It checks for the existence of a Like object and either creates or deletes it.
    """
    post = get_object_or_404(Post, id=pk)

    # Check if the user has already liked the post
    existing_like = post.likes.filter(user=request.user)

    if existing_like.exists():
        # If the user already liked the post, remove the like
        existing_like.delete()
    else:
        # If the user hasn't liked the post, create a new like
        Like.objects.create(user=request.user, post=post)

        # ✅ Create a notification only when a like is added
        if request.user != post.author:  # prevent self-notifications
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                notification_type="like",
                post=post,
                message=f"{request.user.username} liked your post."
            )

    # Redirect back
    return HttpResponseRedirect(
        request.META.get("HTTP_REFERER", reverse("equipment:post_detail", args=[pk]))
    )

@login_required
def rent_equipment(request, equipment_id):
    """
    Handles the renting of equipment.
    """
    equipment = get_object_or_404(InstalledEquipment, id=equipment_id)
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        try:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            
            # Check for existing transactions to avoid double-booking
            existing_transactions = Transaction.objects.filter(
                equipment=equipment,
                end_date__gte=start_date,
                start_date__lte=end_date
            )
            
            if existing_transactions.exists():
                messages.error(request, 'This equipment is already booked for the selected dates.')
                return redirect('equipment:home')
            
            if not equipment.is_available:
                messages.error(request, 'This equipment is currently unavailable.')
                return redirect('equipment:home')
            
            # Create a new transaction
            Transaction.objects.create(
                equipment=equipment,
                user=request.user,
                start_date=start_date,
                end_date=end_date,
                status='pending'
            )
            
            equipment.is_available = False
            equipment.save()
            
            messages.success(request, 'Your rental request has been submitted!')
            
        except (ValueError, TypeError) as e:
            messages.error(request, f'Invalid date format: {e}')
    
    return redirect('equipment:home')


# -------------------------------
# 1. Maintenance check (can be run manually or via cron/celery)
# -------------------------------
def check_due_maintenance():
    today = now().date()
    due_equipments = InstalledEquipment.objects.filter(next_service_date__lte=today)

    for equipment in due_equipments:
        Notification.objects.get_or_create(
            recipient=equipment.user,  # equipment owner
            notification_type="maintenance",
            equipment=equipment,
            message=f"Your equipment {equipment.name} is due for maintenance!"
        )

@login_required
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by("-created_at")

    return render(request, "equipment/notifications.html", {"notifications": notifications})


@login_required
def mark_notification_as_read(request, pk):
    notification = Notification.objects.get(pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect("notifications")
