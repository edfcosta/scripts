# -*- coding: utf-8 -*-
import pandas as pd
import statistics

#path = '/home/edfcosta/results-d1-d2-bdr/ +ALTERAR (ex:hevc-base) + /results/'

modelo = 'eduardo'

path = '/home/edfcosta/results_vpcc_base_treinado/' + modelo + '/results/'
sequencias = ['longdress', 'loot', 'redandblack', 'soldier', 'queen']
ranges = ['1051', '1000', '1450', '0536', '0000']

with open (path + 'medias_seq.txt', 'w') as dataMedias:
  for s, init in zip(sequencias, ranges):
      for r_num in range(1, 6):
          arquivoLido = path + s + '/' + s + '_r' + str(r_num) + '.txt'
          dados = []  # Limpar a lista de dados para cada iteração
          
          seq, r, frame, mseF_p2point, mseF_p2plane, c0_PSNRF, c1_PSNRF, c2_PSNRF = "", "", "", "", "", "", "", ""
          
          with open(arquivoLido, 'r') as arquivo_txt:
              linhas = arquivo_txt.readlines()
              count = False
              for linha in linhas:
                  if linha.startswith('Sequencia'):
                      dados_linha = linha.split()
                      seq = dados_linha[1]
                      r = dados_linha[2]
                      frame = dados_linha[3]
                      print(f'\n{frame} \n\t{seq} \n\t{r} \n\t{frame}')
                      
                  elif 'mseF,PSNR (p2point):' in linha:
                      dados_linha = linha.split()
                      mseF_p2point = float(dados_linha[2])
                      
                  elif 'mseF,PSNR (p2plane):' in linha:
                      dados_linha = linha.split()
                      mseF_p2plane = float(dados_linha[2])
                  
                  elif 'c[0],PSNRF' in linha:
                      dados_linha = linha.split()
                      c0_PSNRF = float(dados_linha[2])
                      
                      
                  elif 'c[1],PSNRF' in linha:
                      dados_linha = linha.split()
                      c1_PSNRF = float(dados_linha[2])
                      
                  elif 'c[2],PSNRF' in linha:
                      dados_linha = linha.split()
                      c2_PSNRF = float(dados_linha[2])
                      count = True
     
                  elif count == True:  
                      dados.append([seq, r, frame, mseF_p2point, mseF_p2plane, c0_PSNRF, c1_PSNRF, c2_PSNRF])
                      count = False
                      
              dados.append([seq, r, frame, mseF_p2point, mseF_p2plane, c0_PSNRF, c1_PSNRF, c2_PSNRF])
              
             
              # Criando um DataFrame do Pandas com os dados
              df = pd.DataFrame(dados, columns=['Sequencia', 'r', 'Frame', 'mseF,PSNR (p2point)', 'mseF,PSNR (p2plane)', 'c[0],PSNRF', 'c[1],PSNRF',  'c[2],PSNRF'])
              
              #media das colunas
              media = [["Media", "", "", 
              statistics.mean(df['mseF,PSNR (p2point)']),
              statistics.mean(df['mseF,PSNR (p2plane)']),
              statistics.mean(df['c[0],PSNRF']),
              statistics.mean(df['c[1],PSNRF']),
              statistics.mean(df['c[2],PSNRF'])]]
              
              # Adicionar a nova linha ao DataFrame
              df.loc[len(df)] = media[0]
              
              #escreve no txt das medias
              dataMedias.write(s + '_' + r + '\n')
              
              dataMedias.write('p2point: ' + str(media[0][3]) + '\n')  # Valor de p2point
              dataMedias.write('p2plane: ' + str(media[0][4]) + '\n')  # Valor de p2plane
              dataMedias.write('c0: ' + str(media[0][5]) + '\n')  # Valor de c0
              dataMedias.write('c1: ' + str(media[0][6]) + '\n')  # Valor de c1
              dataMedias.write('c2: ' + str(media[0][7]) + '\n\n')  # Valor de c2
              
              # Salvando o DataFrame em um arquivo CSV
              df.to_excel(path + s + '/' + s + '_r' + str(r_num) + '.xlsx', index=False)
              
              
              
              print(f"Arquivo CSV {s}_r{r_num}.csv criado com sucesso!")
