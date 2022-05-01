from statistics import mode
from django.db import models

from datetime import datetime

class TDSymbol(models.Model):
    symbol = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.symbol

    def transactions(self):
        qs = self.tdtransaction_set.all() 
        
        retstr = ""
        amt = 0
        for x in qs:
            retstr += f'{x.date}-->{x.amount} / '
            amt += x.amount

        if not amt == 0:
            retstr += f' Total = {amt}'

        return retstr

class TDTransaction(models.Model):
    parent      = models.ForeignKey(TDSymbol, on_delete=models.CASCADE, null=True)

    rawline     = models.TextField(blank=True, null=True)

    date        = models.DateField(db_index=True, blank=True, null=True)
    transid     = models.CharField(db_index=True, max_length=15, blank=False, unique=True)
    description = models.CharField(max_length=100, blank=True)
    qty         = models.DecimalField(max_digits=10, decimal_places=4, blank=True, default=0)
    symbol      = models.CharField(max_length=50, blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=4, blank=True, default=0)
    commision   = models.DecimalField(max_digits=10, decimal_places=4, blank=True, default=0)
    amount      = models.DecimalField(max_digits=10, decimal_places=4, blank=True, default=0)

    def __str__(self):
        return f'{self.date} - {self.symbol} - {self.amount}'


# routine to convert the RAW csv file into fields for the model Entry
def ingestfile(filename):
    ingestfile = open(filename)

    for line in ingestfile:
        # ignore stuff we don't want
        if ("DATE" in line) or ("***" in line):
            continue

        # break out our line into fields
        #DATE	TRANSACTION ID	DESCRIPTION	QUANTITY	SYMBOL	PRICE	COMMISSION	AMOUNT	REG FEE
        csvlineset = line.split(",")
        
        print(csvlineset)

        e, created = TDTransaction.objects.get_or_create(transid = csvlineset[1])
        if created:
            e.rawline = line
            e.date          = datetime.strptime(csvlineset[0], "%m/%d/%Y").date()
            e.description   = csvlineset[2]
            e.qty           = csvlineset[3] if not csvlineset[3] == "" else 0
            e.symbol        = csvlineset[4]
            e.price         = csvlineset[5] if not csvlineset[5] == "" else 0
            e.commision     = csvlineset[6] if not csvlineset[6] == "" else 0
            e.amount        = csvlineset[7] if not csvlineset[7] == "" else 0

            # check if there is already a parent TDSymbol to attach to, as long as we aren't blank :)
            if not e.symbol == "":
                tds, c = TDSymbol.objects.get_or_create(symbol=e.symbol)
                if c:
                    tds.save()
                e.parent = tds 

            e.save()

            print('created')
        else: 
            print('skipped')

        print()
