from django.db import models

class Taxon(models.Model):
    scientific_name=models.CharField(max_length=100)
    common_name=models.CharField(max_length=100)
    cites=models.BooleanField()
    regulated_native=models.BooleanField()
    part1_live=models.BooleanField()
    part2_live=models.BooleanField()
    def __unicode__(self):
        return "%s (%s)" % (self.common_name, self.scientific_name)

