from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = "Seed the database with sample categories and products"

    def handle(self, *args, **options):
        categories = {
            "apparel": "Apparel",
            "home": "Home & Living",
            "accessories": "Accessories",
        }
        cat_objs = {}
        for slug, name in categories.items():
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})
            cat_objs[slug] = cat

        products = [
            ("Linen Shirt", "apparel", 1499, 20, "A relaxed-fit linen shirt, breathable and perfect for warm days."),
            ("Cotton Tote Bag", "accessories", 499, 50, "A durable canvas tote bag for everyday errands."),
            ("Ceramic Mug", "home", 349, 40, "Hand-glazed ceramic mug, holds 300ml."),
            ("Wool Scarf", "apparel", 899, 15, "Soft wool scarf to keep you warm through winter."),
            ("Table Lamp", "home", 1999, 10, "Minimalist wooden table lamp with a fabric shade."),
            ("Leather Wallet", "accessories", 1299, 25, "Slim bifold wallet made from full-grain leather."),
        ]
        for name, cat_slug, price, stock, desc in products:
            slug = name.lower().replace(" ", "-")
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": cat_objs[cat_slug],
                    "price": price,
                    "stock": stock,
                    "description": desc,
                },
            )

        self.stdout.write(self.style.SUCCESS("Seeded categories and products."))
