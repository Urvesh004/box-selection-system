from django import forms
from django.forms import formset_factory

from .models import Product


class OrderItemForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=False,
    )

    quantity = forms.IntegerField(
        min_value=1,
        required=False,
    )


class BaseOrderItemFormSet(forms.BaseFormSet):

    def clean(self):
        super().clean()

        if any(self.errors):
            return

        products = []
        has_items = False

        for form in self.forms:

            if not form.cleaned_data:
                continue

            product = form.cleaned_data.get("product")
            quantity = form.cleaned_data.get("quantity")

            if not product and not quantity:
                continue

            has_items = True

            if not product:
                form.add_error(
                    "product",
                    "Please select a product."
                )

            if not quantity:
                form.add_error(
                    "quantity",
                    "Please enter a quantity."
                )

            if product:

                if product in products:
                    form.add_error(
                        "product",
                        "This product is already added."
                    )
                else:
                    products.append(product)

        if not has_items:
            raise forms.ValidationError(
                "Please add at least one product."
            )


OrderItemFormSet = formset_factory(
    OrderItemForm,
    formset=BaseOrderItemFormSet,
    extra=1,
)