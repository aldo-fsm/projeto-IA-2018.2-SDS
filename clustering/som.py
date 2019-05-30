import numpy as np
import pandas as pd
import somoclu

"""
Essa função seleciona apenas algumas colunas dos Dados, utilizando o usecols nativo da biblioteca pandas

"""
def select_columns(dataset_path, columns):
  if(columns=='all'):
    dataset = pd.read_csv(dataset_path, keep_default_na=False, encoding="ISO-8859-1", sep=";")
  else:
    dataset = pd.read_csv(dataset_path, keep_default_na=False, usecols=columns, encoding="ISO-8859-1", sep=";")    
  return dataset

"""
Projeto da disciplina de Inteligência Artificial - POLI - UPE


Biblioteca utilizada: somoclu
Repositório original: https://github.com/peterwittek/somoclu

"""

"""
SOM como módulo para chamar num programa principal

nrows : número de linhas do mapa
ncolumns: número de colunas no mapa
maptype : default = planar
gridtype : default = hexagonal. Pode ser rectangular também
inicialization : default = "pca"

"""

def run_som(data, nrows, ncolumns, maptype="planar", gridtype="hexagonal", inicialization="pca"):
  
  labels = range(data.shape[0])

  n_rows, n_columns = nrows, ncolumns

  som = somoclu.Somoclu(n_columns, n_rows, maptype=maptype, gridtype=gridtype,
                        compactsupport=True, initialization=inicialization)
     
  """
  SOMOCLU: Classe para treino e visualização do SOM.

  """

  print("Training map...")
  som.train(data)
  print("Map trained!")

  """
  Treina o mapa usando os dados atuais no objeto Somoclu.

  """

  som.cluster()
  
  """ Classifica os neurônios, preenchendo a variável som.clusters, também seleciona
      as BMUs(neuônios que são exibidos no mapa) para cada entrada.
  """  
                        
  som.view_umatrix(bestmatches=True, labels=labels, filename='./mapa.png')
  print("Map image created at program's directory!")
  """
    Plota a U-Matrix do mapa treinado.
  """

  np.savetxt("./clusters.csv", som.clusters, delimiter=",")
  """ som.bmus possui as coordenadas das BMUs, que são as 
      células que conseguimos ver no mapa.
      
      som.clusters(arquivo cluster.csv) é o resultado do método som.cluster() e 
      possui a classificação de cada neurônio do mapa(ao total: (n_row * n_columns) 
      neurônios).
      
      Como a localização dos neurônios após o treinamento é fixa no mapa, através 
      das coordenadas das BMUs em som.bmus, é possível extrair as suas respectivas 
      classificações em som.clusters apenas em função de suas coordenadas.
      """

  clusters = pd.read_csv('./clusters.csv')
  id_classes = np.empty((len(data),2), dtype=int)
  id_class = pd.DataFrame()
  """ id_classes: array utilizado para armazenar as classes resultantes da cluesterização,
      será usado para salvar o arquivo classes.csv no formato:
          ID CLASSE 
          ..   ..
          ..   ..
          ..   ..
          ..   ..
  """
  i=-1
  for linha, coluna in som.bmus:
      i=i+1
      id_classes[i][0] = labels[i]                      #id
      id_classes[i][1] = som.clusters[linha][coluna]    #classe

  output = pd.DataFrame(id_classes, columns=['ID', 'Classe'])
  output.to_csv('./classes.csv', sep=',', index=False)
  print("Classification file succesfully created at program's directory!")

  f= open("./bmus.txt","w+")
  """escreve as coordenadas de cada bmu para arquivo "bmus.txt"""
  coordinates = []
  i=1
  j=0
  for x,y in som.bmus:
      print(("ID %d: (%d, %d)\n" % (i, x, y)), file=f)
      coordinates.append({'Id': i, 'x':x, 'y':y, 'cluster': som.clusters[x][y]})
      i=i+1
  f.close()
  return pd.DataFrame(coordinates)


# """ Carrega os dados """
# dataset = select_columns('./colunas-normalizadas.csv', 'all')
# dataset = dataset.drop([40, 41])



# """Seleciona os ID's, que serão os rótulos dos neurônios no mapa"""
# labels = range(len(dataset.iloc[:, 0]))

# print(list(labels))


# """Remove os ID's para não influenciarem no agrupamento"""              

# """ Quantidade de neurônios na rede.
#     Os valores das linhas e colunas podem ser alterados (valores muito grandes
#     exigirão muito processamento).
# """
# n_rows, n_columns = 40, 40




# som = somoclu.Somoclu(n_columns, n_rows, maptype="planar", gridtype="hexagonal",
#                       compactsupport=True, initialization="pca")
   
# """
# SOMOCLU: Classe para treino e visualização do SOM.

# """
# data = dataset.values

# som.train(data)

# """
# Treina o mapa usando os dados atuais no objeto Somoclu.

# """



# som.cluster()
# print(som.clusters)

# """ Classifica os neurônios, preenchendo a variável som.clusters, também seleciona
#     as BMUs(neuônios que são exibidos no mapa) para cada entrada.
# """  
        
              
# som.view_umatrix(bestmatches=True, labels=labels, filename='./mapa.png')
# """
#   Plota a U-Matrix do mapa treinado.
# """

# np.savetxt("./clusters.csv", som.clusters, delimiter=",")
# """ som.bmus possui as coordenadas das BMUs, que são as 
#     células que conseguimos ver no mapa.
    
#     som.clusters(arquivo cluster.csv) é o resultado do método som.cluster() e 
#     possui a classificação de cada neurônio do mapa(ao total: (n_row * n_columns) 
#     neurônios).
    
#     Como a localização dos neurônios após o treinamento é fixa no mapa, através 
#     das coordenadas das BMUs em som.bmus, é possível extrair as suas respectivas 
#     classificações em som.clusters apenas em função de suas coordenadas.
#     """
    
    

# clusters = pd.read_csv('./clusters.csv')
# id_classes = np.empty((len(data),2), dtype=int)
# id_class = pd.DataFrame()
# """ id_classes: array utilizado para armazenar as classes resultantes da cluesterização,
#     será usado para salvar o arquivo classes.csv no formato:
#         ID CLASSE 
#         ..   ..
#         ..   ..
#         ..   ..
#         ..   ..
# """
# i=-1
# for linha, coluna in som.bmus:
#     i=i+1
#     id_classes[i][0] = labels[i]                      #id
#     id_classes[i][1] = som.clusters[linha][coluna]    #classe

# #print(id_classes)

# output = pd.DataFrame(id_classes, columns=['ID', 'Classe'])
# output.to_csv('./classes.csv', sep=',', index=False)



# f= open("./bmus.txt","w+")
# """escreve as coordenadas de cada bmu para arquivo "bmus.txt"""
# coordinates = []
# i=1
# j=0
# for x,y in som.bmus:
#     print(("ID %d: (%d, %d)\n" % (i, x, y)), file=f)
#     coordinates.append({'Id': i, 'x':x, 'y':y})
#     i=i+1
