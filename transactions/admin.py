from django.contrib import admin

from .models import TDTransaction, TDSymbol

class TDSymbolAdmin(admin.ModelAdmin):
    list_display = ('pk','symbol','transactions')

class EntryAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'rawline',)

admin.site.register(TDTransaction, EntryAdmin)
admin.site.register(TDSymbol, TDSymbolAdmin)