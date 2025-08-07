from django.shortcuts import render, redirect
from .forms import InstalledEquipmentForm
from django.core.paginator import Paginator
from datetime import date
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import InstalledEquipment
from .forms import InstalledEquipmentForm
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('home')  # Change this to your homepage or dashboard
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'registration/login.html')

# @login_required
def home(request):
    return render(request, 'equipment/home.html')

# @login_required
# def equipment_list(request):
#     equipment = InstalledEquipment.objects.all()
#     return render(request, 'equipment/equipment_list.html', {'equipment': equipment})



@login_required
def add_equipment(request):
    if request.method == 'POST':
        form = InstalledEquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.added_by = request.user
            equipment.save()
            return redirect('equipment-list')  # We'll define this next
    else:
        form = InstalledEquipmentForm()
    return render(request, 'equipment/add_equipment.html', {'form': form})



@login_required
def equipment_list(request):
    equipment = InstalledEquipment.objects.filter(added_by=request.user)
    today = date.today()

    # Determine status
    for item in equipment:
        if item.next_service_date < today:
            item.status = "Overdue"
        elif (item.next_service_date - today).days <= 7:
            item.status = "Upcoming"
        else:
            item.status = "OK"

    # Filter/Search
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    if query:
        equipment = [e for e in equipment if query.lower() in e.name.lower() or query.lower() in e.location.lower()]

    if status_filter and status_filter != "All":
        equipment = [e for e in equipment if e.status == status_filter]

    paginator = Paginator(equipment, 25)  # 25 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'equipment/equipment_list.html', {
        'page_obj': page_obj,
        'equipment': equipment,
        'query': query or '',
        'status_filter': status_filter or 'All'
    })
import openpyxl
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template

@login_required
def export_excel(request):
    equipment = InstalledEquipment.objects.filter(added_by=request.user)
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
        sheet.append([e.name, e.serial_number, e.location, str(e.date_installed), str(e.next_service_date)])

    workbook.save(response)
    return response

@login_required
def export_pdf(request):
    equipment = InstalledEquipment.objects.filter(added_by=request.user)
    template = get_template('equipment/pdf_template.html')
    html = template.render({'equipment': equipment})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="equipment.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

@login_required
def post_list(request):
    posts = EquipmentPost.objects.all().order_by('-created_at')
    return render(request, 'equipment/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = EquipmentPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = EquipmentPostForm()
    return render(request, 'equipment/create_post.html', {'form': form})

def post_list(request):
    query = request.GET.get('q')
    tag_filter = request.GET.get('tag')
    posts = EquipmentPost.objects.all().order_by('-created_at')

    if query:
        posts = posts.filter(title__icontains=query)

    if tag_filter and tag_filter != 'all':
        posts = posts.filter(tag=tag_filter)

    return render(request, 'equipment/home.html', {
        'posts': posts,
        'query': query,
        'tag_filter': tag_filter,
    })

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(EquipmentPost, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('home')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(EquipmentPost, id=post_id)
    if request.method == 'POST':
        Comment.objects.create(post=post, user=request.user, content=request.POST['comment'])
    return redirect('home')


def home(request):
    return render(request, 'equipment/home.html')

def add_equipment(request):
    return render(request, 'equipment/add_equipment.html')

def equipment_list(request):
    equipments = InstalledEquipment.objects.all()
    return render(request, 'equipment/list.html', {'equipments': equipments})