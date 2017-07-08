# Create your views here.

from django.http import HttpResponse      
from vendemmia.models import ven,bolla,cultivar,provenienza_eff
from django.shortcuts import render_to_response  
from django.db.models import Sum, Count

#from django.utils import simplejson as json
import json

def index(request):
    
    query = bolla.objects.raw('SELECT idbolla, Vendemmia_id, SUM(netto) AS tot, SUM(netto*grado) AS monte from vendemmia_bolla GROUP BY Vendemmia_id ORDER BY Vendemmia_id DESC')
    #lista_bolla={}
    #for i in query:
    #	temp = lista_ven.get(pk=i.Vendemmia_id)
    #    lista_bolla[i.Vendemmia_id] = {
    #    								'anno' : temp.anno,
    #    								'inizio' :temp.inizio,
    #    								'fine' : temp.fine,
    #    								'note' : temp.note,
    #    								'quintali' : i.tot, 
    #    								'montegradi': i.monte 
    #    							}  
    
    prov_eff = provenienza_eff.objects.all()
            

    return render_to_response('index.html', {'query' : query, 'prov_eff' : prov_eff, })
    
    
def detail(request,anno):
        query = bolla.objects.raw('SELECT * , netto*grado AS monte FROM vendemmia_bolla WHERE Vendemmia_id = %s', [anno])
        sum_bolle = bolla.objects.raw('SELECT idbolla, Vendemmia_id, SUM(netto) AS tot, SUM(netto*grado) AS monte from vendemmia_bolla WHERE Vendemmia_id = %s', [anno])[0]
        cultivar_query = bolla.objects.raw('SELECT idbolla, Vendemmia_id, Cultivar_id, SUM(netto) AS tot, SUM(netto*grado) AS monte FROM vendemmia_bolla WHERE Vendemmia_id = %s GROUP BY Cultivar_id', [anno])
        provenienza_query = bolla.objects.raw('SELECT  idbolla, Vendemmia_id, Provenienza_id, Cultivar_id, SUM(netto) AS tot, SUM(netto*grado) AS monte FROM vendemmia_bolla WHERE Vendemmia_id = %s GROUP BY Provenienza_id, Cultivar_id', [anno])
        totali_qualita = bolla.calcoli.calc_per_qualita(anno)
        #totali_prov_eff = bolla.calcoli.calc_per_provenienzaeff(anno)
        totali_prov_eff = bolla.objects.raw('SELECT nome, lista.* FROM vendemmia_provenienza_eff JOIN (SELECT idbolla, vendemmia_id, provenienza_eff_id, Cultivar_eff_id, SUM(netto*percentuale/100) AS nettoass, SUM(netto*grado*percentuale/100) AS monteass FROM vendemmia_bolla JOIN vendemmia_provenienza_dettaglio ON idbolla = bolla_id WHERE vendemmia_id = %s GROUP BY provenienza_eff_id, Cultivar_eff_id) AS lista ON id = provenienza_eff_id ', [anno])

    	return render_to_response('detail.html',  {'query' : query, 'sum_bolle' : sum_bolle, 'cultivar_query': cultivar_query, 'provenienza_query' :  provenienza_query, 'totali_qualita' : totali_qualita, 'totali_prov_eff' : totali_prov_eff, })
    
    
 #------------------------------------------------------------------------------------------------------------------------   	   
def grafici(request):

        #query = bolla.objects.raw('SELECT * , netto*grado AS monte FROM vendemmia_bolla')
        
        #average_query = bolla.objects.raw('SELECT Vendemmia_id, Cultivar_id, AVG(netto) as media FROM vendemmia_bolla GROUP BY Cultivar_id, Vendemmia_id ORDER BY Vendemmia_id')
        #cultivar_query = bolla.objects.values('Cultivar_id').annotate(tot=Sum('netto')) 
        #cultivar_query = bolla.objects.extra(select={'tot' :  'SELECT SUM(netto) FROM vendemmia_bolla GROUP BY Cultivar_id', 'monte' :  'SELECT SUM(netto*grado) FROM vendemmia_bolla GROUP BY Cultivar_id'})
        #cultivar_query=bolla.calcoli
        cultivar_elenco = cultivar.objects.all()
        ven_elenco = bolla.objects.values('Vendemmia_id').distinct()
        
        tic=[]
        for row in cultivar_elenco:
        	tic = tic + [[str(row.id), str(row.nome)]]
        	
        
			
	#data = [
	#	{'label': 'Day 1',
    	#	'data': [[1, 4], [2,8], [9, 8]],
    	#	'color': '#454d7d',
   	#	},
   	#	{'label': 'Day 2',
    	#	'data': [[16, 4], [18,5], [19, 8]],
    	#	'color': '#720',
    	#	},
   	#]

   	
	data = []
   		
	for year in ven_elenco:
    		single_data={}
    		single_data['label'] = year['Vendemmia_id']
    		single_data['data'] = bolla.calcoli.totali(year['Vendemmia_id'])
    		data = data + [single_data]

    	#aggiungiamo le medie per confronto	
    	single_data={}
	single_data['label'] = 'media'
	single_data['data'] = bolla.calcoli.media_per_cultivar()
	data = data + [single_data]
   		
    	return render_to_response('graf.html',  { 'data' : json.dumps(data), 'tic': tic})
    	
    	
    	
 #------------------------------------------------------------------------------------------------------------------------   	
def grafici_prov(request):

        provenienza_elenco = provenienza_eff.objects.all().order_by('nome')
        ven_elenco = bolla.objects.values('Vendemmia_id').distinct()
        
        tic=[]
        for row in provenienza_elenco:
        	tic = tic + [[str(row.id), str(row.nome)]]
        	
        #tic.sort(key=lambda tup: tup[1]) ordina le tuple considerando il secondo (indice =1) elemento della coppia
        
        i=0
        t=[]
        
        #Occorre ordinare alfabeticamente le etichette (ovvero, le provenienze) dell'asse x
        #per far questo, visto che il grafico ha bisogno di numeri, occorre ordinare i dati secondo
        #un ordine prestabilito. La lista di coppie t successiva permette lo scambio biunivoco 
        #tra l'id memorizzato ne db e l'ordine che dobbiamo attuare
	for coppia in tic:
		t=t+[[coppia[0],str(i)]]
		coppia[0]=str(i)
		i=i+1

	coppia_dict = dict(t)
	
	data = []
   		
	for year in ven_elenco:
    		single_data={}
    		single_data['label'] = year['Vendemmia_id']
    		single_data['data'] = bolla.calcoli.totale_per_provenienzaeff(year['Vendemmia_id'])
    		single_data['data'] = [[coppia_dict.get(str(s[0]),s[0]), s[1]] for s in single_data['data']]
    		data = data + [single_data]

    	#aggiungiamo le medie per confronto	
    	single_data={}
	single_data['label'] = 'media'
	single_data['data'] = bolla.calcoli.media_per_provenienzaeff()
	single_data['data'] = [[coppia_dict.get(str(s[0]),s[0]), s[1]] for s in single_data['data']]
	data = data + [single_data]
	
	
   		
    	return render_to_response('graf_prov.html',  { 'data' : json.dumps(data), 'tic': tic})

#------------------------------------------------------------------------------------------------------------------------   	
def grafici_singoli(request,provenienza):
	titolo = provenienza_eff.objects.get(pk=provenienza).nome
	prov = int(provenienza)
	ven_elenco = bolla.objects.values('Vendemmia_id').distinct()
	data = []
   		
	for year in ven_elenco:
		calcolo = bolla.calcoli.totale_per_provenienzaeff(year['Vendemmia_id'])
    		data = data + [[year['Vendemmia_id'], calcolo[[x[0] for x in calcolo].index(prov)][1] ]]

    	#aggiungiamo le medie per confronto
	calcolo = bolla.calcoli.media_per_provenienzaeff()
    	data = data + [['media', calcolo[[x[0] for x in calcolo].index(prov)][1] ]]
	
    	return render_to_response('graf_singoli.html',  { 'data' : json.dumps(data), 'titolo' : titolo })
