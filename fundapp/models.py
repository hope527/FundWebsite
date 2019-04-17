from django.db import models


class BasicInformation(models.Model):
    fund_id = models.TextField(unique=True, primary_key=True)
    chinese_name = models.TextField()
    english_name = models.TextField()
    isin_code = models.TextField()
    entry_day = models.TextField()
    manager_fee = models.FloatField()
    custody_fee = models.FloatField()
    sales_fee = models.FloatField()
    area = models.TextField()
    investment_target = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'basic_information'


class DomesticInformation(models.Model):
    fund_id = models.TextField(unique=True, primary_key=True)
    classfication = models.TextField(blank=True, null=True)
    redemption_fee = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'domestic_information'


class Interest(models.Model):
    fund_id = models.TextField()
    date = models.IntegerField()
    interest = models.FloatField()

    class Meta:
        managed = False
        db_table = 'interest'
        unique_together = (('fund_id', 'date'),)


class OverseasInformation(models.Model):
    fund_id = models.TextField(unique=True, primary_key=True)
    market = models.TextField(blank=True, null=True)
    regional = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'overseas_information'


class Price(models.Model):
    fund_id = models.TextField()
    date = models.IntegerField()
    nav = models.FloatField()

    class Meta:
        managed = False
        db_table = 'price'
        unique_together = (('fund_id', 'date'),)
