import os

# Sequences information
sequencias_8i = ['longdress', 'loot', 'redandblack', 'soldier']
sequencias_tech = ['queen']

sequencias_init_8i = ['1051', '1000', '1450', '0536']
sequencias_init_tech = ['0000']

tot_frames = 64

sequencias_n_8i = ['longdress_n', 'loot_n', 'redandblack_n', 'soldier_n']
sequencias_n_tech = ['queen_n']

modo = 'ctc-all-intra.cfg'

modelo = 'eduardo'
# Paths
path_dmetric = '/home/ghrehbein/Metricas/mpeg-pcc-dmetric-master/build/Release'

path_8i = '/home/ghrehbein/V-PCC-Dataset/sequences/8i/8iVFBv2/'
path_tech = '/home/ghrehbein/V-PCC-Dataset/sequences/Technicolor/queen/'

path_normals = '/home/ghrehbein/V-PCC-Dataset/normals/'
path_pcerror = '/home/ghrehbein/Metricas/mpeg-pcc-dmetric-master/build/Release/pc_error'

# ALTERAR:
path_coded = '/home/edfcosta/results_vpcc_base_treinado/' + modelo + '/'

def Montador(sequencias, sequencias_n, inicio, path, arquivo):
    init = 0
    for seq in sequencias:
        for quantizacao in range(1, 6, 1):
            for frame in range(tot_frames):
                if 'queen' in seq:
                    arquivo.write(
                        path_pcerror +
                        ' --fileA=' + path_tech + f"frame_{int(inicio[init]) + frame:04d}" + '.ply' +
                        ' --fileB=' + path_coded + seq + '/' + modo + '/r0' + str(quantizacao) + '/' + seq + '_' + modo + '_r' + str(quantizacao) + f'_{int(inicio[init]) + frame:04d}' + '.ply' +
                        ' --inputNorm=' + path_normals + sequencias_n[init] + f'/frame_{int(inicio[init]) + frame:04d}' + '_n.ply' + 
                        ' --color=1 --resolution=1023' +
                        ' > ' + path_coded + seq + '/' + modo + '/r0' + str(quantizacao) + '/' + seq + 'HEVC_AI_r' + str(quantizacao) + f'_{int(inicio[init]) + frame:04d}' + '_rec.txt 2>&1 &\n'
                    )
                else:
                    arquivo.write(
                        path_pcerror +
                        ' --fileA=' + path_8i + seq + '/Ply/' + seq + f'_vox10_{int(inicio[init]) + frame:04d}' + '.ply' +
                        ' --fileB=' + path_coded + seq + '/' + modo + '/r0' + str(quantizacao) + '/' + seq + '_' + modo + '_r' + str(quantizacao) + f'_{int(inicio[init]) + frame:04d}' + '.ply' +
                        ' --inputNorm=' + path_normals + sequencias_n[init] + '/' + seq + f'_vox10_{int(inicio[init]) + frame:04d}' + '_n.ply' + 
                        ' --color=1 --resolution=1023' +
                        ' > ' + path_coded + seq + '/' + modo + '/r0' + str(quantizacao) + '/' + seq + 'HEVC_AI_r' + str(quantizacao) + f'_{int(inicio[init]) + frame:04d}_rec.txt 2>&1 & \n'
                    )
        init += 1

with open(path_coded + 'pc_error_output_' + modelo + '.txt', 'w') as arquivo:
    Montador(sequencias_8i, sequencias_n_8i, sequencias_init_8i, path_8i, arquivo)
    Montador(sequencias_tech, sequencias_n_tech, sequencias_init_tech, path_tech, arquivo)
    #Montador(["soldier"], ["soldier_n"], ['0536'], path_8i, arquivo)