import os
import numpy

# paths:
path_vpcc= "/home/edfcosta/VPCC-HEVC-treinado-11b/"
path_encoder= "/home/edfcosta/VPCC-HEVC-treinado-11b/bin/PccAppEncoder"
path_results= "/home/edfcosta/out/"
#path_sequences= "/home/ghrehbein/V-PCC-Dataset/sequences/8i/8iVFBv2/"

# seleção de configurações:
geoms = ['1', '2', '3', '4', '5']
prediction = ['ctc-random-access.cfg']

## cfgDataset e datasetName precisam estar na mesma ordem

dataset_Name_8i = ["longdress",
                   "loot",
                   "redandblack",
                   "soldier"]

dataset_Name_technicolor = ["queen"]	

frames = '64'

modelo = 'eduardo'

invColSpace = ['yuv420torgb444.cfg']

def createDir(dataset):
    #cria o diretório dos resultados
    if os.path.exists(path_results):
        print(f"Directory: {path_results} exists.")
    else:
        os.mkdir(path_results)
        print(f"Directory: {path_results} has been created.")
        
    #cria o diretório do modelo treinado 
    if os.path.exists(path_results + modelo + '/'):
        print(f"Directory: {path_results}{modelo} exists.")
    else:
        os.mkdir(path_results + modelo + '/')
        print(f"Directory: {path_results}{modelo} has been created.")
        
    #cria o diretório do base 
    if os.path.exists(path_results + modelo + '/'):
        print(f"Directory: {path_results}{modelo} exists.")
    else:
        os.mkdir(path_results + modelo + '/')
        print(f"Directory: {path_results}{modelo} has been created.")
    
    #por sequência  
    for dts in dataset:
    
        #sequencia no treinado
        if os.path.exists(path_results + modelo + '/' + dts):
            print(f"Directory: {path_results}{modelo}/{dts} exists.")
        else:
            os.mkdir(path_results + modelo + '/' + dts)
            print(f"Directory: {path_results}{modelo}/{dts} has been created.")
            
        #sequencia no base
        if os.path.exists(path_results + modelo + '/' + dts):
            print(f"Directory: {path_results}modelo/{dts} exists.")
        else:
            os.mkdir(path_results + modelo + '/' + dts)
            print(f"Directory: {path_results}{modelo}/{dts} has been created.")
        
        #por modo
        for pred in prediction:
            #modo no treinado
            if os.path.exists(path_results + modelo + '/' + dts + "/" + pred):
                print(f"Directory: {path_results}{modelo}/{dts}/{pred} exists.")
            else:
                os.mkdir(path_results + modelo + '/' + dts + '/' + pred)
                print(f"Directory: {path_results}{modelo}/{dts}/{pred} has been created.")
                
            #modo no base
            if os.path.exists(path_results + modelo + '/' + dts + "/" + pred):
                print(f"Directory: {path_results}{modelo}/{dts}/{pred} exists.")
            else:
                os.mkdir(path_results + modelo + '/' + dts + '/' + pred)
                print(f"Directory: {path_results}{modelo}/{dts}/{pred} has been created.")
                
            #por quantização
            for g in geoms:
                #quantização no treinado
                if os.path.exists(path_results + modelo + '/' + dts + '/' + pred + '/r0' + g):
                    print(f"Directory: {path_results}{modelo}/{dts}/{pred}/r0{g} exists.")
                else:
                    os.mkdir(path_results + modelo + '/' + dts + '/' + pred + '/r0' + g)
                    print(f"Directory: {path_results}{modelo}/{dts}/{pred}/r0{g} has been created.")
                    
                #quantização no base
                if os.path.exists(path_results + modelo + '/' + dts + '/' + pred + '/r0' + g):
                    print(f"Directory: {path_results}{modelo}/{dts}/{pred}/r0{g} exists.")
                else:
                    os.mkdir(path_results + modelo + '/' + dts + '/' + pred + '/r0' + g)
                    print(f"Directory: {path_results}{modelo}/{dts}/{pred}/r0{g} has been created.")
                    
#core_count = 0
def encode_treinado(dataset, arquivo):
    #global core_count
    confFolder = ' --configurationFolder=' + path_vpcc + 'cfg/'
    confCompression = ' --config=' + path_vpcc + 'cfg/common/ctc-common.cfg'
    confPrediction = ' --config=' + path_vpcc + 'cfg/condition/' # ctc-all-intra.cfg
    confDataset = ' --config=' + path_vpcc + 'cfg/sequence/' # longdress_vox10.cfg
    confQuantization = ' --config=' + path_vpcc + 'cfg/rate/' # ctc-r3.cfg
    uncompressed = ' --uncompressedDataFolder=/home/edfcosta/vpcc/vpcc-dataset/V-PCC-Dataset/sequences/'     ##----NECESSARIO ALTERAR caso esteja em outra pasta de dataset----##
    numFrames = ' --frameCount=' + frames
    viEncAttributePath = ' --videoEncoderAttributePath=' + path_vpcc + 'dependencies/HM-master/bin/umake/gcc-11.3/x86_64/debug/TAppEncoder'
    colorConversion = ' --colorSpaceConversionPath=' + path_vpcc + 'dependencies/HDRTools/build/bin/HDRConvert'
    reconstructed = ' --reconstructedDataPath=' + path_results # longdress/r01/_enc_1.ply <arqu_saida>.ply
    compressedStream = ' --compressedStreamPath='  + path_results # longdress/r01/_enc_1.bin <arqu_saida>.bin

    for dts in dataset:
            for pred in prediction:
                for g in geoms:
                    #if core_count >= 31:
                        #core_count = 0
                
                    if dataset[0] == 'queen':
                        arquivo.write(
                            #'taskset -c ' + str(core_count) + ' ' +
                            path_encoder +
                            confFolder +
                            confCompression +
                            confPrediction + pred +
                            confDataset + str(dts) + ".cfg" +
                            confQuantization + 'ctc-r' + g + '.cfg' +
                            uncompressed +
                            numFrames +
                            viEncAttributePath +
                            colorConversion +
                            ' --keepIntermediateFiles=1' +
                            reconstructed + modelo + '/' + dts + "/" + pred + "/r0" + g + "/" + dts + "_" + pred + "_r" + str(g) + "_%04d.ply" +  # ident base ou treinado
                            compressedStream + modelo + '/' + dts + '/' + pred + '/r0' + g + '/' + dts + '.bin' +                                # ident base ou treinado
                            " > " + path_results + modelo + '/' + str(dts) + '/' + dts + "_" + pred + '_r' + g + '.log' +                         # ident base ou treinado
                            ' 2>&1 &' +
                            '\n'
                        )
                        #core_count += 1
                        
                    else:
                        arquivo.write(
                            #'taskset -c ' + str(core_count) + ' ' +
                            path_encoder +
                            confFolder +
                            confCompression +
                            confPrediction + pred +
                            confDataset + str(dts) + "_vox10.cfg" +
                            confQuantization + 'ctc-r' + g + '.cfg' +
                            uncompressed +
                            numFrames +
                            viEncAttributePath +
                            colorConversion +
                            ' --keepIntermediateFiles=1' +
                            reconstructed + modelo + '/' + dts + "/" + pred + "/r0" + g + "/" + dts + "_" + pred + "_r" + str(g) + "_%04d.ply" +  # ident base ou treinado
                            compressedStream + modelo + '/' + dts + '/' + pred + '/r0' + g + '/' + dts + '.bin' +                                # ident base ou treinado
                            " > " + path_results + modelo + '/' + str(dts) + '/' + dts + "_" + pred + '_r' + g + '.log' +                         # ident base ou treinado
                            ' 2>&1 &' +
                            '\n'
                        )
                        #core_count += 1
                    


createDir(dataset_Name_8i)
createDir(dataset_Name_technicolor)

# Abrir arquivo antes de chamar as funções
with open(path_results + 'codec_' + modelo + '_' + prediction[0] + '_log.txt', 'w') as arquivo:
    encode_treinado(dataset_Name_8i, arquivo)
    encode_treinado(dataset_Name_technicolor, arquivo)
    
    