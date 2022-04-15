from multiprocessing import _QueueType
from symtable import Symbol
from django.db import models

# Create your models here.


# Transaction line
#DATE	TRANSACTION ID	DESCRIPTION	QUANTITY	SYMBOL	PRICE	COMMISSION	AMOUNT	REG FEE

# routine to convert the RAW csv line into fields for the model Entry
def convertRawlineToEntry():
    pass

class Entry(models.Model):
    date        = models.DateField(db_index=True, blank=False)
    transid     = models.CharField(max_length=15, blank=False)
    description = models.CharField(max_length=100, blank=True)
    qty         = models.DecimalField(max_digits=10, decimal_places=4, blank=True)
    symbol      = models.CharField(max_length=50, blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=4, blank=True)
    commision   = models.DecimalField(max_digits=10, decimal_places=4, blank=True)
    amount      = models.DecimalField(max_digits=10, decimal_places=4, blank=True)

    rawline     = models.TextField(blank=True, null=True)
    converted   = models.BinaryField(blank=True, null=True)
    
    def __str__(self):
        return self.rawline


class Optiontrade(models.Model):
    Symbolline
    
    qty
    datetoexpire
    stikeprice
    price

    rawdescription 


    pass


