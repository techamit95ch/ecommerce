# To backup Product data in json

python manage.py dumpdata products --format json --indent 4 products/fixtures/products.json

# To load Product data

 python manage.py loaddata products/fixtures/products.json
