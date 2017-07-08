from django.db import models
# coding: latin-1

# Create your models here.
from datetime import datetime

class ven(models.Model):
	anno = models.PositiveSmallIntegerField(primary_key=True, default=datetime.today().year)
	inizio = models.DateField()
	fine = models.DateField(blank=True)
	note = models.TextField(blank=True)
	def __unicode__(self):
		return u"%d" % (self.anno)
		
	class Meta:
		verbose_name_plural = "Vendemmie"
	
	
	
#come da catastino soci
class provenienza(models.Model):
	nome = models.CharField(max_length=50)
	def __unicode__(self):
		return self.nome
		
	class Meta:
		verbose_name_plural = "Provenienza"
		ordering = ['nome']
	
	
	
class qualita(models.Model):
	tipo = models.CharField(max_length=30)
	def __unicode__(self):
		return self.tipo
		
	class Meta:
		verbose_name_plural = "Qualità"
	
	
	
class cultivar(models.Model):
	nome = models.CharField(max_length=30)
	def __unicode__(self):
		return self.nome
		
	class Meta:
		verbose_name_plural = "Cultivar"

#reale provenienza, a volte differente da quella in bolletta, con prevista indicazione 
#della percentuale in modo da garantire una statistica effettiva
#i fondi dettagliati inclusi cioe' i sopra sotto, pozzo, doppi nomi su singoli fondi
#non sono previsti in quanto non si ha tutta la statistica completa	
#il campo biologico si riferisce alla classificazione fatta secondo il fascicolo aziendale per              
#l'agricoltura biologica
class provenienza_eff(models.Model):
	nome = models.CharField(max_length=50)
	biologico = models.CharField(max_length=50)
	def __unicode__(self):
		return self.nome
		
	class Meta:
		verbose_name_plural = "Provenienze dettagliate"
		ordering = ['nome']
	#dati_catastali = #collegamento a separata tabella magari in un'altra applicazione, per adesso null
	

class calcoli(models.Manager):
	def totali(self,anno):
        	from django.db import connection
        	cursor = connection.cursor()
        	cursor.execute("""
            		SELECT id, nome, tot 
            		FROM vendemmia_cultivar 
            		LEFT OUTER JOIN (SELECT Cultivar_id, Vendemmia_id, SUM(netto) AS tot FROM vendemmia_bolla WHERE vendemmia_id=%s GROUP BY Cultivar_id) 
            		ON id=Cultivar_id;
            		""", [anno])
            	
        	a=[]
		for row in cursor.fetchall():
    			if row[2] is None:
				a= a+ [[row[0],0]]
			else:
				a= a+ [[row[0],row[2]]]
        	#p = dict([(cultivar.objects.filter(id=row[0])[0].nome, row[2]) for row in cursor.fetchall()])	
       		return a
       		
       	def montegradi(self,anno):
        	from django.db import connection
        	cursor = connection.cursor()
        	cursor.execute("""
            		SELECT id, nome, monte 
            		FROM vendemmia_cultivar 
            		LEFT OUTER JOIN (SELECT Cultivar_id, Vendemmia_id, SUM(netto*grado) AS monte FROM vendemmia_bolla WHERE vendemmia_id=%s GROUP BY Cultivar_id) 
            		ON id=Cultivar_id;
            		""", [anno])           	
        	a=[]
		for row in cursor.fetchall():
    			if row[2] is None:
				a= a+ [[row[0],0]]
			else:
				a= a+ [[row[0],row[2]]]   		
       		return a
       		
       	def media_per_cultivar(self):
        	from django.db import connection
        	cursor = connection.cursor()
        	cursor.execute("""
        		SELECT cultivar_id, AVG(tot) as media 
        		FROM (SELECT cultivar_id, vendemmia_id, SUM(netto) as tot FROM vendemmia_bolla GROUP BY Cultivar_id, vendemmia_id) 
        		GROUP BY cultivar_id;
        		""")
        	a=[]
		for row in cursor.fetchall():
			if row[1] is None:
				a= a+ [[row[0],0]]
			else:
				a= a+ [[row[0],row[1]]]
    		
    		return a
    	
    	def calc_per_qualita(self, anno):
    		from django.db import connection
        	cursor = connection.cursor()
        	cursor.execute("""
        		SELECT  Vendemmia_id, vendemmia_qualita.tipo, SUM(netto) AS tot, SUM(netto*grado) AS monte 
        		FROM vendemmia_bolla 
        		LEFT OUTER JOIN vendemmia_qualita
        		ON Qualita_id = vendemmia_qualita.id
        		WHERE Vendemmia_id = %s 
        		GROUP BY Qualita_id
       			""", [anno])
       		a=[]
		for row in cursor.fetchall():
			a= a+ [[str(row[1]),row[2],row[3]]]

    		return a
    		
    	def totale_per_provenienzaeff(self, anno):
    		from django.db import connection
        	cursor = connection.cursor()
        	cursor.execute("""
        		SELECT id, nome, nettoass, monteass
			FROM vendemmia_provenienza_eff 
			LEFT OUTER JOIN (SELECT idbolla, vendemmia_id, provenienza_eff_id, SUM(netto*percentuale/100) AS nettoass, SUM(netto*grado*percentuale/100) AS monteass
    					FROM vendemmia_bolla 
    					JOIN vendemmia_provenienza_dettaglio 
    					ON idbolla = bolla_id 
    					WHERE vendemmia_id = %s 
    					GROUP BY provenienza_eff_id) AS lista 
			ON id = provenienza_eff_id
			ORDER BY nome
       			""", [anno])
       		a=[]
		for row in cursor.fetchall():
			if row[2] is None:
				a= a+ [[row[0],0]]
			else:
				a= a+ [[row[0],row[2]]]
    		
    		return a
    		
    		
    	def monte_per_provenienzaeff(self, anno):
    		from django.db import connection
        	cursor = connection.cursor()
        	cursor.execute("""
        		SELECT id, nome, nettoass, monteass
			FROM vendemmia_provenienza_eff 
			LEFT OUTER JOIN (SELECT idbolla, vendemmia_id, provenienza_eff_id, SUM(netto*percentuale/100) AS nettoass, SUM(netto*grado*percentuale/100) AS monteass
    					FROM vendemmia_bolla 
    					JOIN vendemmia_provenienza_dettaglio 
    					ON idbolla = bolla_id 
    					WHERE vendemmia_id = %s 
    					GROUP BY provenienza_eff_id) AS lista 
			ON id = provenienza_eff_id
       			""", [anno])
       		a=[]
		for row in cursor.fetchall():
			if row[3] is None:
				a= a+ [[row[0],0]]
			else:
				a= a+ [[row[0],row[3]]]
    		
    		return a
    		
    	
    	def media_per_provenienzaeff(self):
        	from django.db import connection
        	cursor = connection.cursor()
        	cursor.execute("""
        		SELECT provenienza_eff_id,  AVG(tot) as media 
			FROM (SELECT provenienza_eff_id, vendemmia_id, SUM((netto*percentuale/100)) as tot 
        			FROM vendemmia_bolla 
        			JOIN vendemmia_provenienza_dettaglio 
    				ON idbolla = bolla_id
        			GROUP BY provenienza_eff_id, vendemmia_id)
			GROUP BY provenienza_eff_id
        		""")
        	a=[]
		for row in cursor.fetchall():
			if row[1] is None:
				a= a+ [[row[0],0]]
			else:
				a= a+ [[row[0],row[1]]]
    		
    		return a
    		
    		
def ultimovalore():
	return bolla.objects.latest('idbolla').data
		
def ultimavendemmia():
	return bolla.objects.latest('idbolla').Vendemmia.anno


    		    		
	
class bolla(models.Model):
	CHOICES = (
		("1", "Enopolio di Petrosino"),
		("2", "Enopolio di Mazara"),
	)
	
	idbolla = models.AutoField(primary_key=True)
	Vendemmia = models.ForeignKey(ven, default = ultimavendemmia)
	num = models.PositiveIntegerField()
	enopolio = models.CharField(max_length=25, choices = CHOICES, default="1")
	data = models.DateField(default = ultimovalore)
	diraspata = models.BooleanField(default=False) #se vero, allora raccolta meccanicamente
	

	
	# campi da bolletta
	Cultivar = models.ForeignKey(cultivar, related_name='Cultivar')
	Provenienza = models.ForeignKey(provenienza)
	Qualita = models.ForeignKey(qualita)
	
	# campi effettivi
	# inserire una funzione che generi un valore default pari a quelli piu' sopra di bolletta
	Cultivar_eff = models.ForeignKey(cultivar, related_name='Cultivar_eff')
	Provenienza_eff = models.ManyToManyField(provenienza_eff, through='provenienza_dettaglio', related_name='Provenienza_eff')
	
	grado = models.DecimalField(max_digits=4, decimal_places=2)
	netto = models.DecimalField(max_digits=5, decimal_places=2)
	
	note = models.TextField(blank=True)
	objects = models.Manager() #default manager
	calcoli = calcoli()
	
	def __unicode__(self):
		return u"Bolla n. %d del %s " % (self.num, self.data.strftime('%d/%m/%Y'))
		
	class Meta:
		verbose_name_plural = "Bollette"
		
	def montegradi(self, obj):
	    return ("%.4f" % (obj.grado*obj.netto))
	    



class provenienza_dettaglio(models.Model):
	provenienza_eff = models.ForeignKey(provenienza_eff)
	bolla = models.ForeignKey(bolla)
	percentuale = models.PositiveSmallIntegerField(default=100)
	
	class Meta:
		verbose_name_plural = "Provenienze dettagliate"	
