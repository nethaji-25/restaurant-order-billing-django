from django.db import models

# Create your models here.

class Table(models.Model):
    AVAILABLE = 'AVAILABLE'
    OCCUPIED = 'OCCUPIED'
    BILL_REQUESTED = 'BILL_REQUESTED'
    CLOSED = 'CLOSED'

    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (OCCUPIED, 'Occupied'),
        (BILL_REQUESTED, 'Bill Requested'),
        (CLOSED, 'Closed'),
    ]

    table_number=models.PositiveIntegerField(unique=True)
    capacity=models.PositiveIntegerField()
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default=AVAILABLE)

    def __str__(self):
        return f"Table {self.table_number} ({self.status})"


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('STARTER', 'Starter'),
        ('MAIN', 'Main Course'),
        ('DRINK', 'Drink'),
        ('DESSERT', 'Dessert'),
    ]

    name=models.CharField(max_length=100)
    category=models.CharField(max_length=20,choices=CATEGORY_CHOICES)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Order(models.Model):
    PLACED = 'PLACED'
    IN_KITCHEN = 'IN_KITCHEN'
    SERVED = 'SERVED'

    STATUS_CHOICES = [
        (PLACED, 'Placed'),
        (IN_KITCHEN, 'In Kitchen'),
        (SERVED, 'Served'),
    ]

    table = models.ForeignKey(Table,on_delete=models.CASCADE,related_name='orders')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=PLACED)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None   #check if order is new

        if is_new:
            self.table.status = Table.OCCUPIED
            self.table.save()

        super().save(*args, **kwargs)

        # Create kitchen notification ONLY for new orders
        if is_new:
            from .models import KitchenNotification
            KitchenNotification.objects.create(
                order=self,
                message=f"New order placed for Table {self.table.table_number} (Order #{self.id})"
            )

    def __str__(self):
        return f"Order #{self.id} - Table {self.table.table_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

class Bill(models.Model):
    NOT_GENERATED = 'NOT_GENERATED'
    PENDING = 'PENDING'
    PAID = 'PAID'

    STATUS_CHOICES = [
        (NOT_GENERATED, 'Not Generated'),
        (PENDING, 'Pending Payment'),
        (PAID, 'Paid'),
    ]

    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name='bill')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_GENERATED)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == self.PAID:
            self.order.table.status = Table.AVAILABLE
            self.order.table.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill - Order {self.order.id} ({self.status})"



class KitchenNotification(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='kitchen_notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
