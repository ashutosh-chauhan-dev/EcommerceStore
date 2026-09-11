from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .models import Product, Category, Order, OrderItem
from .cart import Cart
from .forms import RegisterForm, LoginForm, CartAddProductForm, OrderCreateForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get("q")
    if query:
        products = products.filter(name__icontains=query)

    return render(request, "store/product_list.html", {
        "category": category,
        "categories": categories,
        "products": products,
        "query": query or "",
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_product_form = CartAddProductForm()
    return render(request, "store/product_detail.html", {
        "product": product,
        "cart_product_form": cart_product_form,
    })


def cart_detail(request):
    cart = Cart(request)
    return render(request, "store/cart_detail.html", {"cart": cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd["quantity"], update_quantity=False)
            messages.success(request, f"Added {product.name} to your cart.")
    return redirect("cart_detail")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"Removed {product.name} from your cart.")
    return redirect("cart_detail")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "store/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("product_list")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "store/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("product_list")


@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect("product_list")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                for item in cart:
                    product = item["product"]
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=item["price"],
                        quantity=item["quantity"],
                    )
                    if product.stock >= item["quantity"]:
                        product.stock -= item["quantity"]
                        product.save()
                cart.clear()
            return render(request, "store/order_created.html", {"order": order})
    else:
        form = OrderCreateForm()
    return render(request, "store/order_create.html", {"cart": cart, "form": form})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "store/order_history.html", {"orders": orders})
