from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product',
            new_name='PostLink',
        ),
    ]
