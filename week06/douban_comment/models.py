from django.db import models


class T1(models.Model):
    id = models.BigAutoField(primary_key=True)
    n_star = models.IntegerField()
    short = models.CharField(max_length=400)
    sentiment = models.FloatField()

    # 元数据，不属于任何一个字段的数据
    class Meta:
        managed = False
        db_table = 't1'

