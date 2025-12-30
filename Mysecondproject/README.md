#  Restaurant Management System (Django)

A full-stack **Restaurant Management System** built using **Django**, implementing table management, order flow, billing, and kitchen notifications.
---

## Features(Includes Bonus Enhancements)

### 🪑 Table Management
- Predefined restaurant tables
- Table status tracking:
  - AVAILABLE
  - OCCUPIED
  - BILL_REQUESTED
  - CLOSED

###  Order Management
- Create orders per table
- Add multiple menu items with quantities
- Order lifecycle:
  - PLACED
  - IN_KITCHEN
  - SERVED

###  Billing System
- Bill generated **per order**
- Automatic calculation of:
  - Total amount
  - Tax (10%)
- Bill statuses:
  - NOT_GENERATED
  - PENDING
  - PAID
- On payment:
  - Table automatically becomes AVAILABLE
### 📄 PDF Bill Export (Bonus Feature)
- Bills can be exported as **downloadable PDF invoices**
- Implemented using **ReportLab**
- Includes:
  - Restaurant bill header
  - Table number
  - Ordered items with quantity & price
  - Total amount and tax
- Accessible from the **Bill Summary** screen



### Kitchen Notifications (In-App)
- Notification created when a new order is placed
- Kitchen dashboard shows unread notifications
- Notifications are marked as read once viewed

## UI
- Responsive and clean UI using **Tailwind CSS**
- Dashboards for:
  - Tables
  - Orders
  - Billing
  - Kitchen notifications

---

## Tech Stack

- Backend: Python, Django
- Frontend: HTML, Tailwind CSS
- Database: SQLite(default Django DB)
- Authentication: Django built-in auth
- ORM: Django ORM



Project Structure
restaurant/
├── models.py          # Tables, Orders, OrderItems, Bills, Notifications
├── views.py           # Business logic
├── urls.py            # App routing
├── templates/
│   └── Restaurant/    # HTML templates
└── migrations/

## Demo Login Credentials (For Evaluation)

## The application includes role-based access control.  
## You can use the following demo users to test each role:

### Waiter
- **Username:** waiter1
- **Password:** Accesstoorder
- **Access:** Create orders, add items, view order summary

### Cashier
- **Username:** cashier1
- **Password:** Accesstobill
- **Access:** Generate bills, mark bills as paid

### Manager
- **Username:** manager1
- **Password:** Accesstoall
- **Access:** Full access (tables, orders, billing, admin)



The application includes role-based access control.  
You can use the following demo users to test each role:

### Waiter
- **Username:** waiter1
- **Password:** Accesstoorder
- **Access:** Create orders, add items, view order summary

### Cashier
- **Username:** cashier1
- **Password:** Accesstobill
- **Access:** Generate bills, mark bills as paid

### Manager
- **Username:** manager1
- **Password:** Accesstoall
- **Access:** Full access (tables, orders, billing, admin)

- ## These credentials are for demo/testing purposes only.
