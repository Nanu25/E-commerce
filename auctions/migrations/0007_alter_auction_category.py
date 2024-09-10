# Generated by Django 5.1rc1 on 2024-08-04 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auction_category_delete_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(choices=[('Fashion', 'Fashion'), ('Electronics', 'Electronics'), ('Toys', 'Toys'), ('Home', 'Home'), ('Books', 'Books'), ('Other', 'Other')], default='Other', max_length=50),
        ),
    ]
