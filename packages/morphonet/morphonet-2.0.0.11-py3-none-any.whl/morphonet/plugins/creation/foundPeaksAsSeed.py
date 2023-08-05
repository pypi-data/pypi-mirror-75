# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin

#  Perform the h-minima operation on a given image with  h-minima parameter value
def regionalext(input, h_min,MinOrMax): 
    from morphonet import vt_path
    import os
    path_regional_ext=os.path.join(vt_path,"build/bin/regionalext") 
    from morphonet.ImageHandling import SpatialImage,imsave,imread
    import numpy as np
    import os
    inputfile="temp_input.inr"
    outputfile="temp_output" + str(h_min) +".inr"
    imsave(inputfile,SpatialImage(input))
    os.system(path_regional_ext + " "+inputfile+" "+outputfile+" -h " + str(h_min) +" -"+MinOrMax+ " -parallel ")
    output=imread(outputfile)
    os.system('rm '+inputfile+' '+outputfile)
    return output


#Add an new seeds with hmin
class foundPeaksAsSeed(MorphoPlugin):
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_Name("Local Peaks")
        self.set_Parent("Create new Seeds")
        self.add_InputField("HMin",20)
        self.add_InputField("Volume",20)
        self.add_Dropdown("MinOrMax",["min","max"])

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if self.get_InputField("HMin") is None or self.get_InputField("Volume") is None:
            print("Please fill the parameters ")
        else:
            h_min=int(self.get_InputField("HMin"))
            volume=int(self.get_InputField("Volume"))
            MinOrMax=self.get_Dropdown("MinOrMax")
                   

            print(" ------>> Process "+self.name+" at "+ str(t) + " with "+str(h_min)+ " h "+MinOrMax+ " value upper "+str(volume) )
            from scipy import ndimage as ndi 
            import numpy as np
            data=dataset.get_seg(t)
            center=dataset.getCenter(data)
            rawdata=dataset.get_raw(t)
            rawdata[data!=dataset.background]=rawdata.max()
            print(" ---------->> Calcul Regional Ext  ")
            local_maxi=regionalext(rawdata,h_min,MinOrMax)
            print(" ---------->> Extrat Labels")
            labels = ndi.label(local_maxi)[0]
            binary_label=labels>1
            print(" ---------->> Remove small Labels")
            imerode=ndi.binary_erosion(binary_label,structure=np.ones((5,5,5)))#ERODE TO REMOVE VERY SMALL PEAKS
            labels[np.where(imerode==False)]=0
            peaks=np.unique(labels)
            peaks=peaks[peaks!=0]
            print(" ---------->> Found "+str(len(peaks))+" peaks with h "+MinOrMax+"="+str(h_min))
            for c in peaks:
                coord=np.where(labels==c)
                if len(coord[0])>volume:
                    bary=np.int32([coord[0].mean()-center[0],coord[1].mean()-center[1],coord[2].mean()-center[2]])
                    print('---------->> create a seed '+str(c)+" at "+str(np.int32([coord[0].mean(),coord[1].mean(),coord[2].mean()])) +" with volume "+str(len(coord[0])))
                    dataset.addSeed(bary)
                else:
                    print('---------->> remove seed '+str(c)+" with small volume "+str(len(coord[0])))
        dataset.restart(self.name)
