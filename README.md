# Box Selection System

A Django application for managing products, shipping boxes, and orders, then recommending the lowest-cost box that can accommodate an order.

## Features

- Manage products and boxes through the Django admin.
- Create orders with one or more products and quantities.
- View products, boxes, and orders in the web interface.
- Recommend the cheapest suitable box based on dimensions and total weight.
- Return recommendations as JSON through an API endpoint.

## Requirements

- Python 3.12 or newer
- Django 6.1.1
- SQLite (included with Python)

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv env
   ```

   Windows PowerShell:

   ```powershell
   .\env\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

4. Create an admin user:

   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

Open <http://127.0.0.1:8000/> in a browser.

## Usage

Use the admin site at <http://127.0.0.1:8000/admin/> to add products and boxes before creating an order.

The main application pages are:

| Page | URL |
| --- | --- |
| Home | `/` |
| Products | `/products/` |
| Boxes | `/boxes/` |
| Orders | `/orders/` |
| Create order | `/orders/create/` |
| Order details | `/orders/<order_id>/` |
| Recommendation page | `/orders/<order_id>/recommendation/` |

## Recommendation API

Send a `GET` request to:

```text
/orders/<order_id>/recommend/
```

Example successful response:

```json
{
  "success": true,
  "order_id": 1,
  "message": "Suitable box found.",
  "recommended_box": {
    "id": 2,
    "name": "Medium Box",
    "length": "35.00",
    "width": "25.00",
    "height": "10.00",
    "max_weight": "5.00",
    "cost": "20.00"
  }
}
```

A `404` response is returned when no box can accommodate the order. Other HTTP methods return `405`.

## How recommendations work

A box is suitable when:

- Its length, width, and height are each at least the largest corresponding product dimension in the order.
- Its maximum weight is at least the total weight of all ordered products.

Suitable boxes are ordered by cost, and the cheapest one is selected. Product rotation and physical packing of multiple products are not currently calculated.

## Testing

Run the test suite with:

```bash
python manage.py test
```

## Project Structure

- `box_selector/` - application models, views, forms, recommendation service, admin, and tests.
- `boxsystem/` - Django project settings and root URL configuration.
- `templates/` - HTML templates.
- `static/` - CSS assets.
- `db.sqlite3` - local SQLite database.
