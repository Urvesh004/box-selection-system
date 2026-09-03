
# AI Usage Documentation

## 1. AI Tool Used

I used:

* ChatGPT

I used AI as a development assistant for understanding concepts, getting ideas, reviewing code, finding possible bugs, creating test cases, and improving documentation.

I reviewed and tested the suggestions before using them in the final project.

---

## 2. Prompt: Project Architecture

### Prompt Used

> I need to build a Django project for an e-commerce warehouse. The system should recommend a suitable shipping box based on product dimensions, weight, and box cost. Suggest a simple Django project structure and explain where the business logic should be placed.

### AI Output

The AI suggested separating the project into:

* Models
* Forms
* Views
* Services
* Tests
* Templates

It also suggested keeping the box recommendation logic in a separate service file.

### Accepted

I accepted the general project structure.

I used:

```text
models.py
forms.py
views.py
services.py
tests.py
```

I also kept the recommendation logic in:

```text
box_selector/services.py
```

This made the business logic separate from the Django views.

### Rejected / Modified

I did not add unnecessary technologies such as:

* Django REST Framework
* React
* Docker
* Redis
* Celery
* PostgreSQL

The assignment could be completed with normal Django, HTML, CSS, JavaScript and SQLite, so I kept the project simple.

---

## 3. Prompt: Box Recommendation Algorithm

### Prompt Used

> Create a simple algorithm to select the cheapest shipping box that can contain an order based on product dimensions and total weight.

### AI Output

The AI suggested:

1. Get all order items.
2. Calculate total weight.
3. Find the required dimensions.
4. Find boxes that can handle those requirements.
5. Sort suitable boxes by cost.
6. Select the cheapest box.

### Accepted

I accepted this approach because it matched the assignment requirements.

The final implementation checks:

```text
box length >= required length
box width >= required width
box height >= required height
box max weight >= total order weight
```

Then the suitable boxes are sorted by cost and the cheapest one is selected.

### Modified

The AI suggested more advanced packing approaches in some cases.

I did not implement a complex 3D packing algorithm because it was outside the scope of this small assignment.

The final project uses a simplified approach for multiple products.

---

## 4. Prompt: Django Formset

### Prompt Used

> How can I allow a user to add multiple products and quantities to one Django order form using a formset?

### AI Output

The AI suggested using a Django formset with JavaScript to dynamically add and remove product rows.

### Accepted

I used:

```text
OrderItemForm
OrderItemFormSet
```

The user can:

* Select a product.
* Enter quantity.
* Click the + button.
* Add another product.
* Submit multiple products in one order.

### Modified

The dynamically added rows required careful handling of Django form indexes.

I reviewed the JavaScript instead of directly accepting the generated solution.

---

## 5. Mistake Found: Dynamic Formset Row Removal

### Problem

One issue identified during development was related to removing dynamically added formset rows.

For example, a formset may contain:

```text
form-0
form-1
form-2
```

If `form-1` is removed directly, the remaining HTML can become:

```text
form-0
form-2
```

This can cause problems because Django expects the form indexes to be handled correctly.

### Action Taken

I reviewed the JavaScript responsible for adding and removing rows.

The formset indexes and `TOTAL_FORMS` value need to remain consistent after a row is removed.

### Verification

I manually tested:

1. Open Create Order.
2. Add a second product.
3. Add a third product.
4. Remove a product.
5. Submit the order.
6. Verify that the order is created correctly.

---

## 6. Prompt: Test Cases

### Prompt Used

> Suggest important test cases for a Django box recommendation system that checks product dimensions, weight, quantity, and box cost.

### AI Output

The AI suggested testing:

* Product fits in box.
* Product is too large.
* Product is too heavy.
* Exact dimensions.
* Cheapest suitable box.
* Empty order.
* Multiple products.
* Quantity.
* No suitable box.
* Invalid order.
* API responses.

### Accepted

I used these ideas to improve the test suite.

Important tests include:

```text
Suitable box selection
Product too large
Product too heavy
Exact dimensions
Cheapest suitable box
Empty order
Multiple products
Quantity calculation
Duplicate products
Invalid quantity
No suitable box
Invalid order ID
API success
API failure
Invalid HTTP method
```

### Rejected / Modified

I did not add tests for features that do not exist in the project, such as:

* Payment processing
* Customer authentication
* Email notifications
* Shipping providers
* Product inventory management

These features are outside the assignment scope.

---

## 7. Prompt: UI Improvement

### Prompt Used

> Review a simple Django HTML interface for a box selection system and suggest improvements while keeping the project simple.

### AI Output

The AI suggested improving:

* Navigation
* Tables
* Buttons
* Forms
* Recommendation cards
* Responsive layout
* Error messages
* Empty states

### Accepted

I improved the CSS and kept the interface based on:

```text
HTML
CSS
JavaScript
Django Templates
```

I did not introduce a frontend framework because it was not required.

---

## 8. Prompt: Code Review

### Prompt Used

> Review my Django box selection code and identify unused code, possible bugs, and unnecessary files.

### Problems / Improvements Found

The review identified several cleanup items:

### Unused import

`OrderItem` was imported in `views.py` but was not required there.

I removed the unused import.

### Unnecessary email configuration

The project contained an unused `MAILERS` configuration.

Since the application does not send emails, this configuration was unnecessary and was removed.

### Generated Python files

The project contained:

```text
__pycache__/
*.pyc
```

These are generated Python files and should not be committed to GitHub.

### Local database

The local:

```text
db.sqlite3
```

database should not be committed to the repository.

It was added to `.gitignore`.

---

## 9. Accepted vs Rejected AI Suggestions

### Accepted

I accepted AI suggestions for:

* Django project structure
* Separating business logic into `services.py`
* Formset concepts
* Additional test cases
* UI improvement ideas
* Code review ideas
* Documentation structure

### Rejected or Modified

I rejected or modified suggestions when they were:

* More complex than required.
* Not needed for the assignment.
* Not suitable for the current project.
* Not verified by running the application.
* Related to features that were not implemented.

I avoided adding unnecessary technologies just to make the project appear larger.

---

## 10. Verification Steps

I did not rely only on AI output.

I verified the project using the following steps.

### Step 1 — Run the Django application

```bash
python manage.py runserver
```

I manually checked the main pages:

```text
Dashboard
Products
Boxes
Orders
Create Order
Order Detail
Recommendation
Django Admin
```

### Step 2 — Test normal recommendation

I created an order with a product that fits an available box.

Expected result:

```text
A suitable box is recommended.
```

### Step 3 — Test no suitable box

I tested an order with a product that was too large or too heavy.

Expected result:

```text
No suitable box found.
```

### Step 4 — Test multiple products

I added multiple products to one order and verified that the total order weight was considered.

### Step 5 — Test quantity

I tested an order with quantity greater than one and verified that:

```text
total weight = product weight × quantity
```

### Step 6 — Run automated tests

```bash
python manage.py test
```

The actual test result is recorded in:

```text
TEST_OUTPUT.md
```

### Step 7 — Run Django system check

```bash
python manage.py check
```

This checks for Django configuration problems.

### Step 8 — Check migrations

```bash
python manage.py makemigrations --check --dry-run
```

This verifies that there are no unexpected model changes waiting for migrations.

---

## 11. Final Verification

Before submission, I verified:

* The project starts successfully.
* Products can be stored.
* Boxes can be stored.
* Orders can contain multiple products.
* Quantity validation works.
* Duplicate products are handled.
* Suitable boxes are selected.
* The cheapest suitable box is selected.
* No suitable box is handled.
* The recommendation API works.
* Invalid API methods are rejected.
* Automated tests pass.
* Django system checks pass.
* Unnecessary generated files are excluded from Git.
* The README explains how to run the project.

---

## 12. AI Responsibility Statement

AI was used as a development assistant, not as a replacement for understanding the project.

I reviewed, modified and tested the suggestions before including them in the final project.

I am responsible for the final code and the final implementation submitted for this assignment.
