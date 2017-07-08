from django.contrib import admin
from vendemmia.models import *
#from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from string import upper
    	
class provenienza_dettaglioInline(admin.TabularInline):
    model = provenienza_dettaglio
    extra = 1
    class Meta:
		verbose_name_plural = "Dettaglio per provenienza"
	

class ListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Vendemmia'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'Vendemmia'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        a=[(str(i.anno),str(i.anno)) for i in ven.objects.all().order_by('-anno')]
        return tuple(a)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        return queryset.filter(Vendemmia__exact=self.value())
       

class bollaAdmin(admin.ModelAdmin):
    ordering = ['data', 'num']
    list_display = ('num','flagbio', 'Vendemmia', 'enop','Cultivar', 'Provenienza' ,'listaprovdettaglio',  'netto', 'grado','montegradi')
    inlines = (provenienza_dettaglioInline,)
    #list_filter = ('Vendemmia',)
    list_filter = (ListFilter,)
    search_fields = ['Cultivar__nome','Provenienza__nome']
    
    def changelist_view(self, request, extra_context=None):
        if not request.GET.has_key('Vendemmia'):
            q = request.GET.copy()
            q['Vendemmia'] = datetime.today().year  # default value for parameter
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(bollaAdmin,self).changelist_view(request, extra_context=extra_context)
    
    def montegradi(self, obj):
    	return ("%.4f" % (obj.grado*obj.netto)) 
    	
    def listaprovdettaglio(self, obj):
		return "%s" % (", ".join([topping.nome for topping in obj.Provenienza_eff.all()]))

    def flagbio(self, obj):
		if "BIO" in upper(obj.Qualita.tipo):
			return "BIO"
		else:
			return "" 

    def enop(self, obj):
        if obj.enopolio == "1":
            return "Petrosino"  	
        else:
            return "Mazara"

admin.site.register(ven)
admin.site.register(provenienza)
admin.site.register(qualita)
admin.site.register(cultivar)
admin.site.register(provenienza_eff)
admin.site.register(bolla, bollaAdmin)
