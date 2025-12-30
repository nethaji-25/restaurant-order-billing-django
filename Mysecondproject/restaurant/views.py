from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required,permission_required
from .models import Table, Order, MenuItem, OrderItem,Bill,KitchenNotification
from decimal import Decimal
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table as PdfTable, TableStyle
from reportlab.lib import colors


# Create your views here.

@login_required
@permission_required('restaurant.add_order',raise_exception=True)
def create_order(request,table_id):
    table=get_object_or_404(Table,id=table_id)
    if table.status==Table.CLOSED:
        return render(request,template_name='Restaurant/error.html',context={'message': 'Table is closed'})
    if request.method=='POST':
        order=Order.objects.create(table=table)
        return redirect('add_order_items',order_id=order.id)
    return render(request,template_name='Restaurant/create_order.html',context={'table':table})


@login_required
@permission_required('restaurant.add_orderitem', raise_exception=True)
def add_order_items(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    menu_items = MenuItem.objects.filter(is_available=True)
    if request.method == 'POST':
        for item in menu_items:
            qty = request.POST.get(f'qty_{item.id}')
            if qty and int(qty) > 0:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=int(qty)
                )
        return redirect('order_summary', order_id=order.id)

    return render(request,template_name='Restaurant/add_order_items.html',context={'order': order,'menu_items': menu_items})

@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()

    return render(request,template_name='Restaurant/order_summary.html',context={'order': order,'items': items})

@login_required
@permission_required('restaurant.add_bill', raise_exception=True)
def generate_bill(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    total = Decimal('0.00')
    for item in order.items.all():
        total += item.menu_item.price * item.quantity

    tax = total * Decimal('0.10')

    bill, created = Bill.objects.get_or_create(
        order=order,
        defaults={
            'total_amount': total,
            'tax_amount': tax,
            'status': Bill.PENDING
        }
    )

    order.table.status = Table.BILL_REQUESTED
    order.table.save()

    return render(request,template_name='Restaurant/bill_summary.html',context={'bill': bill})



@login_required
@permission_required('restaurant.change_bill', raise_exception=True)
def mark_bill_paid(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill.status = Bill.PAID
    bill.save()
    return redirect('table_dashboard')


@login_required
def table_dashboard(request):
    tables = Table.objects.all().prefetch_related('orders')
    table_data = []
    for table in tables:
        latest_order = table.orders.order_by('-created_at').first()
        table_data.append({
            'table': table,
            'latest_order': latest_order
        })

    return render(request,template_name='Restaurant/table_dashboard.html',context={'table_data': table_data})



@login_required
def kitchen_dashboard(request):
    notifications = KitchenNotification.objects.filter(is_read=False).order_by('-created_at')
    return render(request,template_name='Restaurant/kitchen_dashboard.html',context={'notifications': notifications})

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(KitchenNotification,id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('kitchen')




@login_required
def export_bill_pdf(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    order = bill.order

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Bill_Table_{order.table.table_number}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>Restaurant Bill</b>", styles['Title']))
    elements.append(Paragraph(f"Table Number: {order.table.table_number}", styles['Normal']))
    elements.append(Paragraph(f"Bill Status: {bill.status}", styles['Normal']))
    elements.append(Paragraph(" ", styles['Normal']))

    data = [['Item', 'Quantity', 'Price']]

    for item in order.items.all():
        data.append([
            item.menu_item.name,
            str(item.quantity),
            f"{item.menu_item.price}"
        ])

    table = PdfTable(data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (1,1), (-1,-1), 'CENTER')
    ]))

    elements.append(table)
    elements.append(Paragraph(" ", styles['Normal']))
    elements.append(Paragraph(f"<b>Total:</b> {bill.total_amount}", styles['Normal']))
    elements.append(Paragraph(f"<b>Tax:</b> {bill.tax_amount}", styles['Normal']))

    doc.build(elements)
    return response
