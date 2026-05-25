from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_add_card_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardrequest',
            name='cvv',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
