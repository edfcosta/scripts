'''
sequencias:
  longdress    1051-1114
  loot         1000-1063
  queen        0000-0063
  redandblack  1450-1513
  soldier      0536-0599
pred:
  RA  
r:
  1-5
'''

import os

modelo ='eduardo'

path = '/home/edfcosta/results_vpcc_base_treinado/' + modelo + '/'

sequencias = ['longdress', 'loot', 'redandblack', 'soldier', 'queen']
ranges = ['1051', '1000', '1450', '0536', '0000']
hevcra = 'HEVC_AI_'
totFrames = 64

modo = 'ctc-all-intra.cfg'

aPartirDaLinha = '3. Final (symmetric).'
encontraSizes = 'Point cloud sizes for org version, dec version, and the scaling ratio:'


def dirs():
    if os.path.exists(path + 'results'):
        print(path + 'results/ EXISTS.')
    else:
        os.mkdir(path + 'results')
    for seq in sequencias:
        if os.path.exists(path + 'results/' + seq ):
            print(path + f'results/{seq} EXISTS.')
        else:
            os.mkdir(path + 'results/' + seq)    
   

def separa_txt():
    for s, init in zip(sequencias, ranges):
        for r_num in range(1, 6):
            arquivo = path + 'results/' + s + '/' + s + '_r' + str(r_num) + '.txt'
            with open(arquivo, 'w') as new:
                for num in range(0, totFrames):
                    arquivoLido = path + s + '/' + modo + '/r0' + str(r_num) + '/' + s + hevcra + 'r' + str(r_num) + '_' +str(f'{int(init) + int(num):04d}') + '_rec.txt'
                    new.write(f"\nSequencia: {s} \tr{r_num} \t{int(init) + int(num):04d}\n")
                    with open(arquivoLido, 'r') as data:
                        linhas = data.readlines()
                        for idx, line in enumerate(linhas):
                            if encontraSizes in line:
                                new.write(line)
                            if(aPartirDaLinha in line):
                                new.write(line + '\n')
                                for next_line in linhas[idx + 1:idx + 11]:
                                    new.write(next_line)
                                
                                
dirs()
separa_txt()
