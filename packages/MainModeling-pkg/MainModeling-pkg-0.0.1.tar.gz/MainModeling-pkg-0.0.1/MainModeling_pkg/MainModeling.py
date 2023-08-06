# -*- coding: utf-8 -*-
"""
Created on Tue May  5 00:06:30 2020

@author: David
"""
import numpy as np
def size(x):
    '''m=row n=column'''
    try:
        n=len(x[0][:])
        m=len(x)
#        if n!=len(x[1][:]):
#            print('error')
    except TypeError:
        try:
            n=len(x)
            m=1
        except:
            n=1
            m=1
    return m,n
def rnum(i,j,k):
    num=k
    mat=[[num for a in range(1,j+1)]for a in range(1,i+1)]
#    if i==1:
#        mat=mat[0]
    return mat    
def zeros(i,j):
    mat=rnum(i,j,0)
    return mat
def trans(x):
    try:
        c=max([len(x[i]) for i in range(len(x))])#len(x[0])
        xt=zeros(c,len(x))
        for i in range(0,len(x)):
            for j in range(0,c):
                if len(x[i])>j:
                    xt[j][i]=x[i][j]
                else:xt[j][i]=0
        if c==1:
            xt=xt[0]
    except TypeError:
        try:
            xt=zeros(len(x),1)
            for i in range(0,len(x)):
                xt[i][0]=x[i]
        except TypeError:
            xt=x
    return xt

###########################################################################################################################################################################
###########################################################################################################################################################################
########################################################                  GA                      #####################################################################
###########################################################################################################################################################################
###########################################################################################################################################################################
def walker(seqPoints,CoordPDra):
    #CoordP=[[1,2,5.5],[2,9,0],[3,9.7,4.2],[4,3.5,0.5],[5,5.3,2.8],[6,4,5],[7,1.6,1],[8,0,3.5]];CoordPDra=[CoordP,0]
    #seqPoints=[1,2,3,4,5,6,7,8]
    #Pob_floatelite,fxelite,Pob_floatMean=GA(functionanalysis,otherdata,lim,NumIndiv,MutationPorc,LengthChromosome,NGenerations,Nstop,elite,NumberCores,initialdata,Daughtercomputers)
    #Pob_floatelite,fxelite,Pob_floatMean=GA('MainModeling.walker',CoordPDra,[[1,8,'int']]*8,1000,5,6,1000,150,4,12,[],[])
    #dist,punish=walker(seqPoints,[CoordP,1])
    import numpy as np
    CoordP=CoordPDra[0];Dra=CoordPDra[1]
    seqPoints=seqPoints+[seqPoints[0]]
    ind=trans(CoordP)[0].index(seqPoints[0])
    dist=0;X=[CoordP[ind][1]];Y=[CoordP[ind][2]]
    for i in range(1,len(seqPoints)):
        ind=trans(CoordP)[0].index(seqPoints[i])
        X.append(CoordP[ind][1]);Y.append(CoordP[ind][2])
        disti=((X[i]-X[i-1])**2+(Y[i]-Y[i-1])**2)**0.5
        dist=dist+disti
    punish=len(seqPoints)-1-len(np.unique(seqPoints[0:len(seqPoints)-1]))
    if Dra==1:
        import matplotlib.pyplot as plt
        plt.plot(X,Y)
    return dist,punish

def fPobDec(Pob_2,ne,Nr):
    Pob_10=[0]*Nr*ne
    Pob_2N=[]
    for i in range(Nr*ne):
        Pob_2Ni='0b'
        for j in range(len(Pob_2[0])):
            Pob_2Ni=Pob_2Ni+str(Pob_2[i][j])
        Pob_2N.append(Pob_2Ni)
        
    for i in range(Nr*ne):
        Pob_10[i]=int(Pob_2N[i],2)
    return Pob_10
def fPobDecInv(Pob_10,ne,Nr,LC):
    Pob_2=zeros(Nr*ne,LC)
    Pob_2N=[bin(Pob_10[i]) for i in range(len(Pob_10))]
    for i in range(Nr*ne):
        bi=Pob_2N[i]
        cont=LC
        for j in range(len(bi)-1,2-1,-1):
            cont-=1
            Pob_2[i][cont]=int(bi[j])
    return Pob_2
def fScale(Pob_10,lim,ne,LC,Nr):
    Pob_float=[0]*Nr*ne
    for i in range(Nr):
        for j in range(ne):
            r=(i)*ne+j
            if lim[j][2]=='int':
                Pob_float[r]=int(round(Pob_10[r]/(2**LC-1)*(lim[j][1]-lim[j][0])+lim[j][0],0))
            elif lim[j][2]=='float':
                Pob_float[r]=float(round(Pob_10[r]/(2**LC-1)*(lim[j][1]*10000-lim[j][0]*10000)+lim[j][0]*10000,0)/10000)
    return Pob_float
def fScalInv(Pob_float,lim,ne,LC,Nr):
    Pob_10=[0]*Nr*ne
    for i in range(Nr):
        for j in range(ne):
            r=(i)*ne+j
            Pob_10[r]=int(round((Pob_float[r]-lim[j][0])*(2**LC-1)/(lim[j][1]-lim[j][0]),0))
    return Pob_10

def fSelectionRul(fxp,Nr):
    import math
    import numpy as np
    mean=sum(fxp)/len(fxp)
    if mean!=0:
        Ndecr=[fxp[i]/mean for i in range(len(fxp))]
        decr=[];resr0=[]
        for i in range(len(fxp)):
            decr.append(math.floor(Ndecr[i]))
            resr0.append(Ndecr[i]-decr[i])
        resr=[resr0[i]*360/sum(resr0) for i in range(len(resr0))]
        for i in range(1,len(resr)):
            resr[i]=resr[i]+resr[i-1] 
        while sum(decr)<Nr:
            roulette=360*np.random.rand()
            i=1
            while i<Nr-1:
                if roulette>=resr[i-1] and roulette<resr[i] and decr[i-1]<Nr/2:
                    decr[i-1]=decr[i-1]+1
                    i=Nr
                i+=1
    else:
        decr=[1]*len(fxp)
    return decr


def freproduction(Pob_2,Nr,ne,decr,LC):
    import copy    
    import numpy as np
    dec=copy.deepcopy(decr)
    Parents=[0]*Nr
    cont=0
    while cont<Nr:
        v=max(dec)
        ind=dec.index(v)
        Parents[cont:cont+v]=[ind]*v
        dec[ind]=0
        cont+=v
    t1=np.random.permutation(Nr)
    if len(t1)%2!=0:print('The Number of Individuals must be even')
    t2=[[t1[i],t1[i+1]] for i in range(0,len(t1),2)]
    Couples=zeros(len(t2),2)
    for i in range(len(t2)):
        Couples[i][0]=Parents[t2[i][0]]
        Couples[i][1]=Parents[t2[i][1]]
    
    Pob_C=[0]*len(Pob_2)
    a1=[0]*len(t2)
    a2=[0]*len(t2)
    for t in range(len(t2)):
        a1[t]=Couples[t][0]
        a2[t]=Couples[t][1]
        for i in range(ne):
            pcross=np.random.randint(0,LC)
            r=(a1[t])*ne+i
            aux1=Pob_2[r][0:pcross]
            aux2=Pob_2[r][pcross:LC]
            r1=(a2[t])*ne+i
            aux3=Pob_2[r1][0:pcross]
            aux4=Pob_2[r1][pcross:LC]
            
            Pob_C[t*ne+i]=aux1+aux4
            Pob_C[int(len(Pob_2)/2)+t*ne+i]=aux3+aux2
    return Pob_C,Parents,Couples

def fMutation(Pob_2,LC,MutationPorc):
    import numpy as np
    R,C=size(Pob_2)
    Tgenes=R*C
    GenesMut=round(Tgenes*MutationPorc/100)
    for i in range(GenesMut):
        row=np.random.randint(0,R)
        column=np.random.randint(0,C)
        Pob_2[row][column]=1-Pob_2[row][column]
    return Pob_2
##https://blog.dominodatalab.com/simple-parallelization/
#from joblib import Parallel, delayed
#import multiprocessing
#     
## what are your inputs, and what operation do you want to 
## perform on each input. For example...
#inputs = range(10) 
#def processInput(i):
#    return i * i
# 
#num_cores = multiprocessing.cpu_count()
#     
#results = Parallel(n_jobs=num_cores)(delayed(processInput)(i) for i in inputs)

def fElite(fxp,fxpelite,elite,ne,Pob_2,punish,Pob_float,fx,Pob_2elite,fxelite,Pob_floatelite,multiobjectives):
    import copy
    import numpy as np
#    import sys
#    import statistics
    if max(fxp)>fxpelite[0]:
        fxpd=copy.deepcopy(fxp)
        Pob_2elite0=[0]*(elite*ne)
        fxpelite0=[0]*(elite)
        for i in range(elite):
            indelite=fxpd.index(max(fxpd))
    #        indworst=fxd.index(min(fxpd))
            fxpd[indelite]=0#statistics.mean(fxpd)
    #        fxpd[indeworst]=statistics.mean(fxpd)
            ri=(indelite)*ne
            rj=(indelite+1)*ne
            Pob_2elite0[i*ne:(i+1)*ne]=Pob_2[ri:rj]
            fxpelite0[i]=fxp[indelite]
            if i==0 and punish[indelite]==0:
                Pob_floatelite=Pob_float[ri:rj]
                fxelite=fx[indelite]
                global contGelite
                contGelite=contG
#                sys.stdout.write('\r'+'EndGeneration='+str(contG)+'    elite Generation '+str(contG))
#                sys.stdout.write('\r'+'Elite Generation '+str(contG))
#                sys.stdout.write(' elite fx '+str(round(fxelite,4))+ '  &  '+'elite Pob_float '+str(Pob_floatelite)+'                  ')
#                sys.stdout.flush()
        if multiobjectives==False or multiobjectives==[] or multiobjectives=='' or multiobjectives==0 or len(Pob_2elite)+1>=len(Pob_2)*0.3:
            Pob_2elite=copy.deepcopy(Pob_2elite0);fxpelite=copy.deepcopy(fxpelite0)#
#            Pob_2elite[0:len(Pob_2elite0)]=copy.deepcopy(Pob_2elite0)
        elif contG%2==0:Pob_2elite=copy.deepcopy(Pob_2elite0);fxpelite=copy.deepcopy(fxpelite0)
#        else:Pob_2elite=Pob_2elite+Pob_2elite0
#    fxpd=copy.deepcopy(fxp)
    for i in range(int(len(Pob_2elite)/ne)):
#        indemaxfxpd=fxpd.index(max(fxpd))
#        if multiobjectives==False or multiobjectives==[] or multiobjectives=='':indelite=indemaxfxpd
#        else:indelite=int(round(np.random.rand()*(len(fxpd)-1),0))
#        if multiobjectives!=False and multiobjectives!=[] and multiobjectives!='' and contG%2==0:
        indelite=int(round(np.random.rand()*(len(fxp)-1),0))
#        indelite=indemaxfxpd
        fxp[indelite]=fxpelite[i]
#        fxpd[indemaxfxpd]=statistics.mean(fxpd)
        ri=(indelite)*ne
        rj=(indelite+1)*ne
        Pob_2[ri:rj]=Pob_2elite[i*ne:(i+1)*ne]
#    with open('test','w') as ff: ff.write('len(Pob_2elite)/ne='+str(len(Pob_2elite)/ne)+' len(Pob_2)/ne='+str(len(Pob_2)/ne)+' Pob_2elite='+str(Pob_2elite)+' w='+str(weights))
    return Pob_2,Pob_2elite,fxelite,Pob_floatelite,fxpelite,fxp

#def fMainAnalysis(Pob_float,Nr,ne,functionanalysis,otherdata,i):
#    ri=(i)*ne
#    rj=(i+1)*ne
#    if otherdata==[]:
#        fxi,punishi=eval(str(functionanalysis)+'(Pob_float[ri:rj])')
#    else:
#        fxi,punishi=eval(str(functionanalysis)+'(Pob_float[ri:rj],otherdata)')
#    return fxi,punishi

def GA(functionanalysis,otherdata,lim,NumIndiv,MutationPorc,LengthChromosome,NGenerations,Nstopelite,elite,\
       NumberCores,initialdata,Daughtercomputers,tolbest,tolmean,multiobjectives):
    
    import sys
    import os
    if not 'numpy'in sys.modules.keys():
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
    import copy
    import statistics
    import time
#    if not 'joblib' in sys.modules.keys():
#        import subprocess
##        subprocess.check_call(['python', '-m', 'pip', 'install', 'joblib'])
#        os.system("start powershell python -m pip install joblib")
##        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'joblib'])
    try:
        from joblib import Parallel, delayed
    except:
        if not 'joblib' in sys.modules.keys():
            try:
                import subprocess
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'joblib'])
                from joblib import Parallel, delayed
            except:
                exitl=0
                while exitl<=12:
                    try:
                        exitl+=1
                        if exitl==1:os.system("start powershell python -m pip install joblib")
                        time.sleep(15)
                        from joblib import Parallel, delayed
                        exitl=1000
                    except:
                        exitl+=1
    import multiprocessing
#    from sklearn.neighbors import KNeighborsClassifier
    from sklearn import linear_model
    clffx = linear_model.BayesianRidge()
    clfpunish = linear_model.BayesianRidge()
    ML=0
    import importlib
    global contG,stop
#    import threading
#    global Pob_float,Nr,ne,functionanalysis,otherdata,i
    tstart = time.time()
    Nr=NumIndiv;MutationPorc0=MutationPorc
    lim=[copy.deepcopy(lim[i]) for i in range(len(lim))]
    LCmin=max(5,len(bin(int(round(max([lim[i][1]-lim[i][0] for i in range(len(lim))]),0)+1)))-1)
    if LengthChromosome==[] or LengthChromosome=='':LengthChromosome=0
    if LCmin>LengthChromosome:print('LengthChromosome less than LengthChromosome required. LengthChromosome='+str(LCmin)+' is taken.')
    LC=max(LengthChromosome,LCmin)
    ne=len(lim)
    

    num_cores = min(NumberCores,multiprocessing.cpu_count())
    
    
    functionanalysis.index('.');analysismodule='';aux=0;function=''
    for i in range(len(str(functionanalysis))):
        if functionanalysis[i]=='.':aux=1
        if aux==0:
            analysismodule=analysismodule+functionanalysis[i]
        elif functionanalysis[i]!='.':
           function=function+functionanalysis[i]
    if not os.path.exists("tempMultiComputer"):
        os.makedirs('tempMultiComputer')
    resultstotal='tempMultiComputer\\resultstotal'+str(int(round(np.random.rand()*100,0)))+time.strftime('_%d-%m-%y_%H-%M-%S')+'.out'
    with open(resultstotal,'w') as f0:
        f0.write('')
    
    
    resrand='Main'#str(int(round(np.random.rand()*100000,0)))
    if function!='py':
        Module = importlib.import_module(analysismodule)
        method=getattr(Module,function)
    else:
        from shutil import copyfile
        copyfile(functionanalysis, 'tempMultiComputer\\functionanalysiscopy1.py')
        with open('tempMultiComputer\\functionanalysiscopy1.py', 'a') as f:
            f.write('\r' + 'with open("tempMultiComputer\\'+'\\results'+resrand+'"+str(j0987654321)+".out", "a") as f:')
            f.write('\r' + '    res=str([x,fxi,punishi,individual0987654321]);res1=""')
            f.write('\r' + '    for i in range(len(res)):')
            f.write('\r' + '        if res[i]!=" ":res1=res1+res[i]')
            f.write('\r' + '    f.write("'+'\\'+'n"+res1)')
        data_list=open('tempMultiComputer\\functionanalysiscopy1.py', 'r').readlines()
#        if os.path.exists('MainModeling.py'):
#            copyfile('MainModeling.py','tempMultiComputer\\MainModeling.py')
#        if data_list.__contains__('adress=os.getcwd()\n'):
#            data_list[data_list.index('adress=os.getcwd()\n')]='adress=os.getcwd()[0:-18]\n'
        filessource=[arch.name for arch in os.scandir(os.getcwd()) if arch.is_file()]
        for j in range(len(filessource)):
            copyfile(filessource[j],'tempMultiComputer'+'\\'+filessource[j])
        
    num_coresall=[num_cores]
    createfun=[Nr]
    
    if function=='py':
        for j in range(0,num_coresall[0]):
            with open('tempMultiComputer\\functionanalysiscopy'+str(j)+'.py','w') as f:f.write('')
            
#    if function=='py' and Daughtercomputers!=[]:
#        for i in range(1,len(num_coresall)):
#            data_listDi=open(functionanalysis, 'r').readlines()
#            data_listDi.append('\rwith open("results'+Daughtercomputers[i-1][0]+'.out", "a") as f:\n')
#            data_listDi.append('    res=str([x,fxi,punishi]);res1=""\n')
#            data_listDi.append('    for i in range(len(res)):\n')
#            data_listDi.append('        if res[i]!=" ":res1=res1+res[i]\n')
#            data_listDi.append('    f.write("'+'\\'+'n"+res1)')
#            data_listD.append(data_listDi)
            
            
#            copyfile(functionanalysis, 'functionanalysiscopy'+Daughtercomputers[i-1][0]+'1.py')
#            with open('functionanalysiscopy'+Daughtercomputers[i-1][0]+'1.py', 'a') as f:
#                f.write('\r' + 'with open("results'+Daughtercomputers[i-1][0]+'.out", "a") as f:')
#                f.write('\r' + '    res=str([x,fxi,punishi]);res1=""')
#                f.write('\r' + '    for i in range(len(res)):')
#                f.write('\r' + '        if res[i]!=" ":res1=res1+res[i]')
#                f.write('\r' + '    f.write("'+'\\'+'n"+res1)')
#                f.close()
#                
#            for j in range(1,num_coresall[i]):
#    #            copyfile('functionanalysiscopy1.py', 'functionanalysiscopy'+str(j+1)+'.py')
#                with open('functionanalysiscopy'+Daughtercomputers[i-1][0]+str(j+1)+'.py','w') as f:f.write('')
#                

############Preparation of process
    Pob_2=zeros(Nr*ne,LC)
    #####################################################
    Pob_floati=[]
    if initialdata!=[]:
        for i in range(len(initialdata)):
            Pob_floati=Pob_floati+initialdata[i]
        Pob_10i=fScalInv(Pob_floati,lim,ne,LC,len(initialdata))
        Pob_2i=fPobDecInv(Pob_10i,ne,len(initialdata),LC)
        Pob_2[0:len(Pob_floati)]=Pob_2i
    #####################################################
    for i in range(len(Pob_floati),Nr*ne):
        for j in range(LC):
                Pob_2[i][j]=np.random.randint(2)
    Pob_10= fPobDec(Pob_2,ne,Nr)
    Pob_float = fScale(Pob_10,lim,ne,LC,Nr)
    fxpelite=[0]*(elite)
#    Inf=float('inf')
    Pob_2elite=[];fxelite=100;Pob_floatelite=0;Pob_floatelite0=0
    contG=0;stop=0#;stopmean=0;Nstopmean=10#contelite=0    
    if tolbest==[] or tolbest=='':tolbest=0
    if tolmean==[] or tolmean=='':tolmean=0
    Mfxp=tolmean+1;meanfxp=0;meanfxp0=100;keepdata=[]
    if Nstopelite==0 or Nstopelite==[]: Nstopelite=NGenerations
    Pob_floatMean=0;Pob_floatMean0=100
    train_accuracy_clf=0
    
    while contG<NGenerations and stop<Nstopelite and fxelite>tolbest and abs(Mfxp-meanfxp)>tolmean \
        and abs(meanfxp-meanfxp0)>tolmean:# and Pob_floatMean0!=Pob_floatMean:
        contG+=1
        fxp=[]
        fx=[]
        punish=[]
        if function=='py':
            for i in range(num_coresall[0]):
                with open("tempMultiComputer\\results"+resrand+str(i)+".out", "w") as f2:
                    f2.write('[[0],0,0,"na"]')
                    f2.write('\r[[0],0,0,"na"]')
        
        if isinstance(multiobjectives,int) and multiobjectives!=0:
            global weights
#            uk=[np.random.rand() for i in range(multiobjectives)];weights=[uk[i]/sum(uk) for i in range(len(uk))]
            if contG%2==0:  uk=[np.random.rand() for i in range(multiobjectives)];weights=[uk[i]/sum(uk) for i in range(len(uk))]
            else:           weights=[1/multiobjectives for i in range(multiobjectives)]
        else:weights=False
#        print(weights)
        

        def fMainAnalysis(i):
            import numpy as np
            import os
            import time
            j=i%num_cores
            ri=(i)*ne
            rj=(i+1)*ne
            x=Pob_float[ri:rj]
            if keepdata!=[] and trans(keepdata)[0].__contains__(x):
                indkeepdata=trans(keepdata)[0].index(x)
                fxi=keepdata[indkeepdata][1];punishi=keepdata[indkeepdata][2]
            else:
                if function=='py':
        #                randname=int(round(np.random.rand()*1000000000,0))
                        data_list1=['x='+str(x)+'\n']+['individual0987654321='+str(i)+'\n']+['j0987654321='+str(j)+'\n']+data_list
                        fout=open('tempMultiComputer\\functionanalysiscopy'+str(j)+'.py', 'w')
                        fout.writelines(data_list1)
                        fout.close()
                        os.system("start powershell python tempMultiComputer\\functionanalysiscopy"+str(j)+".py")
                        test=1
                        while test!=0:
                            try:
        #                        try:
                                y=list(np.loadtxt('tempMultiComputer\\results'+resrand+str(j)+'.out',dtype='str'))
        #                        except:
        #                            prob='\rproblems with Main Computer';print(prob)
                                y=[eval(y[j]) for j in range(len(y))]
                                indy=trans(y)[3].index(i)
                                test=0
                            except:
                                time.sleep(5)
                        fxi=y[indy][1]
                        punishi=y[indy][2]
                else:
                    fxi,punishi=method(x,otherdata)
            return fxi,punishi
        
        
        if contG>10 and ML!=0:
           for i in range(0,int(createfun[0])):
                ri=(i)*ne
                rj=(i+1)*ne
                x=Pob_float[ri:rj]
                fxi=clffx.predict(x)
                punishi=clfpunish.predict(x)
                results=[fxi,punishi]
        else:
            if num_cores==1:
                results=[]
                for i in range(Nr):
                    resultsi=fMainAnalysis(i)
                    results.append(resultsi)
            else:
                if createfun[0]!=0:
                    results=Parallel(n_jobs=num_cores, backend="threading")(delayed(fMainAnalysis)(i) for i in range(0,int(createfun[0])))
    #                for i in range(0,int(createfun[0])):results=threading.Thread(target=fMainAnalysis, args=(i,));results.start()
                else:
                    results=[]

        if function=='py':
            with open('tempMultiComputer\\resultstemp.txt','w') as f: f.write(str(results))
#        if Daughtercomputers!=[]:
#            extd=0
#            while extd==0:
#                response=list(np.loadtxt(orderDaughters[i],dtype='str'))
#                if response[0]=='waiting':
#                    extd=1
#                else:
#                    time.sleep(5)
#            pool=multiprocessing.Pool(num_cores)
#            results=[pool.apply(fMainAnalysis, args=(i)) for i in range(Nr)]
#            results=pool.map(fMainAnalysis,[i for i in range(Nr)])
            
        fx=trans(results)[0]
        punish=trans(results)[1]
        
        
        
#        fx=fx+fxii;punish=punish+punishii
        fxp=[]
        for i in range(len(fx)):
            K=punish[i]#*ne
            fxp.append(1/((fx[i]+K)*(K+1)))
        decr=fSelectionRul(fxp,Nr)
        ##################################################################Elite
        if contG>0:
            Pob_2,Pob_2elite,fxelite,Pob_floatelite,fxpelite,fxp=\
            fElite(fxp,fxpelite,elite,ne,Pob_2,punish,Pob_float,fx,Pob_2elite,fxelite,Pob_floatelite,multiobjectives)
        Pob_floatMean0=Pob_floatMean;
        Pob_floatMean=[statistics.median(Pob_float[i:len(Pob_float):ne]) for i in range(ne)]
    #    if contG>1 and decr.count(1)<Nr/2 and Pob_floatMean==Pob_floatMean0:
    #        stop+=1
    #    else:
    #        stop=0
    #    Pob_floatMean0=copy.deepcopy(Pob_floatMean)
        printcont=1
#        if Daughtercomputers!=[]:printcont=1
        if function=='py':printcont=1
#    if function=='py':
#        deletelines(functionanalysis,5)
        meanfxp0=meanfxp
        meanfxp=statistics.mean(fxp);mfx=min(fx);Mfxp=max(fxp)
        indmax=fxp.index(Mfxp);ri=(indmax)*ne;rj=(indmax+1)*ne
        Pob_floatmax=Pob_float[ri:rj]
        if contG==1 or contG%printcont==0:
#            if Pob_floatelite!=0:
            sys.stdout.write('\r'+'elite Generation '+str(contGelite))
            sys.stdout.write(' elite fx '+str(round(fxelite,4))+ '  &  '+'elite Pob_float '+str(Pob_floatelite))
            sys.stdout.write('                                                                ')
            sys.stdout.write(' EndGeneration='+str(contG)+' minfx='+str(round(mfx,4))+' Pob_floatmax='+str(Pob_floatmax)+'               ')
            sys.stdout.flush()
         
        with open(resultstotal,'a') as f0:
            mpunish=min(punish);
            if contG==1:
                f0.write('\rGeneration0_meanfxp1_maxfxp2_minfx3_minpunish4_fxelite5_Pobfloatelite6_nameoffunctionanalized7=[')
            f0.write('\r['+str(contG)+','+str(meanfxp)+','+str(Mfxp)+','+str(mfx)+',')
            f0.write(str(mpunish)+','+str(fxelite)+','+str(Pob_floatelite))
            f0.write(',"'+functionanalysis+'"]')
        for jj in range(len(fx)):
            if keepdata!=[] and trans(keepdata)[0].__conatains__(Pob_float[(jj)*ne:(jj+1)*ne])==0 and ML!=0:
                keepdata.append([[[Pob_float[(jj)*ne:(jj+1)*ne]],fx[jj],punish[jj]]])
                if contG>5:
                    clffx.fit(trans(keepdata)[0],trans(keepdata)[1])
                    clfpunish.fit(trans(keepdata)[0],trans(keepdata)[2])
                    train_accuracy_clf = clffx.score(trans(keepdata)[0],trans(keepdata)[1])
                    if train_accuracy_clf>0.97:
                        ML+=1;print("train_accuracy_clf>",0.97)
                
        ##################################################################Selection
        Pob_2,Parents,Couples=freproduction( Pob_2,Nr,ne,decr,LC)
        Pob_2=fMutation(Pob_2,LC,MutationPorc)
    #    Pob_2=Pob_2elite+Pob_2[0:len(Pob_2)-elite*ne]
    #    Pob_2[len(Pob_2)-elite*ne:len(Pob_2)]=Pob_2elite
        Pob_10= fPobDec(Pob_2,ne,Nr)
        Pob_float = fScale(Pob_10,lim,ne,LC,Nr)
        if contG==1:rewrite='w'
        else:rewrite='a'
        with open('tempMultiComputer\\dataGA.txt',rewrite) as f0:
            f0.write('\rfxp='+str(fxp))
            f0.write('\rdecr='+str(decr))
            f0.write('\rParents='+str(Parents))
            f0.write('\rCouples='+str(Couples))
            f0.write('\rPob_floatMean='+str(Pob_floatMean)+'\n')
        if Pob_floatelite!=0 and Pob_floatelite0==Pob_floatelite:
            stop+=1
        else:
            stop=0;MutationPorc=MutationPorc0
        if stop==round(Nstopelite*0.7,0):
            MutationPorc=MutationPorc0*2
        Pob_floatelite0=copy.deepcopy(Pob_floatelite)

    if stop>=Nstopelite:print('stop>=Nstopelite')
    if fxelite<=tolbest:print('fxelite<=tolbest')
    if abs(Mfxp-meanfxp)<=tolmean:print('abs(Mfxp-meanfxp)<=tolmean')
    if abs(meanfxp-meanfxp0)<=tolmean:print('abs(meanfxp-meanfxp0)<=tolmean')
    if Pob_floatMean0==Pob_floatMean:print('Pob_floatMean0==Pob_floatMean')
    with open(resultstotal,'a') as f0:
        f0.write('\r]')
    if function=='py':
        for j in range(0,num_coresall[0]):
            os.remove('tempMultiComputer\\functionanalysiscopy'+str(j)+'.py')
            os.remove('tempMultiComputer\\results'+resrand+str(j)+'.out')

    elapsed = time.time() - tstart
    print('\n elapsed [s]=',elapsed)
    drawresultsGA(resultstotal)
    return Pob_floatelite,fxelite,Pob_floatMean,Pob_floatmax





def drawresultsGA(resultstotal):
    f=open(resultstotal,'r')
    resultstotal_list0=f.readlines()
    resultstotal_list=[]
    for i in range(2,len(resultstotal_list0)):
        try:resultstotal_list.append(eval(resultstotal_list0[i]))
        except:pass
    fxmeandraw=[];fxMaxdraw=[]
    for i in range(len(resultstotal_list)):
        fxmeandraw.append(1/resultstotal_list[i][1])
        fxMaxdraw.append(1/resultstotal_list[i][2])
    import matplotlib.pyplot as plt
    steps=list(range(len(resultstotal_list)))
    plt.plot(steps,fxmeandraw,c='silver',label='f(x) mean')
    plt.plot(steps,fxMaxdraw,c='black',label='f(x) best')
    plt.ylabel('f(x)');plt.xlabel('step')
    plt.legend()
########################################################              ETABS GA                   #####################################################################
###########################################################################################################################################################################

def etabselem(KeNew,Element,units,ModelDirectory,ProgramPath,ModelName0,ETABSversion,*remove):
#    from MainModeling import *
    import numpy as np
    import comtypes.client
    import sys
    from shutil import copyfile
    import os
#    import psutil
    
    Periods=[];Ux=[];Uy=[];Rz=[];contp=0
    while Periods==[] and Ux==[] and Uy==[] and Rz==[] and contp<3:
            contp+=1
            #try:
            #set the following flag to True to manually specify the path to ETABS.exe
            #this allows for a connection to a version of ETABS other than the latest installation
            #otherwise the latest installed version of ETABS will be launched
            if ProgramPath==[]:SpecifyPath=False
            else:SpecifyPath=True
            ModelName=ModelName0+str(round(np.random.rand()*10e14))
            ModelPath0=ModelDirectory+ModelName0+'.EDB'
            ModelPath=ModelDirectory+ModelName+'.EDB'
            copyfile(ModelPath0, ModelPath)
            #set the following flag to True to attach to an existing instance of the program
            #otherwise a new instance of the program will be started
            AttachToInstance = False
            if AttachToInstance:
            #attach to a running instance of ETABS
                try:
                    #get the active ETABS object
                    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject") 
                except (OSError, comtypes.COMError):
                    print("No running instance of the program found or failed to attach.")
                    sys.exit(-1)
            else:
                #create API helper object
        #        helper = comtypes.client.CreateObject('ETABS2017.Helper')
        #        helper = helper.QueryInterface(comtypes.gen.ETABS2017.cHelper)
                contdel=0
                while contdel<3:
                    try:
                        helper = eval("comtypes.client.CreateObject('ETABS"+ETABSversion+".Helper')")
                        helper = eval("helper.QueryInterface(comtypes.gen.ETABS"+ETABSversion+".cHelper)")
                        contdel=3
                        if SpecifyPath:
                            try:
                                #'create an instance of the ETABS object from the specified path
                                myETABSObject = helper.CreateObject(ProgramPath)
                            except (OSError, comtypes.COMError):
                                print("Cannot start a new instance of the program from " + ProgramPath)
                                sys.exit(-1)
                        else:
                    
                            try: 
                                #create an instance of the ETABS object from the latest installed ETABS
                                myETABSObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject") 
                            except (OSError, comtypes.COMError):
                                print("Cannot start a new instance of the program.")
                                sys.exit(-1)  
                    except:contdel+=1
            try:
                #start ETABS application
                myETABSObject.ApplicationStart()
            #create SapModel object
                SapModel=myETABSObject.SapModel
            
            #initialize model 
                SapModel.InitializeNewModel()
                #create file
                assert SapModel.File.OpenFile(ModelPath)==0,'error '+ModelPath
                ret = SapModel.File.OpenFile(ModelPath)
#                print(ModelPath,ret)
                assert SapModel.SetModelIsLocked(False)==0,'error '+ModelPath
                ret = SapModel.SetModelIsLocked(False)
#                print(ModelPath,ret)
                # switch to N-m units
                if units=='N_mm_C':unit=1
                elif units=='kip_ft_F':unit=3
                assert SapModel.SetPresentUnits(unit)==0,'error '+ModelPath
                ret = SapModel.SetPresentUnits(unit)
#                print(ModelPath,ret)
                #add link property
                for j in range(len(Element)):
                    for k in range(len(Element[j])-1):
                        if Element[j][0]=='Link1':
                            Name=str(Element[j][k+1])
                            DOF=[1, 0, 0, 0, 0, 0]
                            Fixed=[0, 0, 0, 0, 0, 0]
                            Ke=[KeNew[(j+1)*k], 0, 0, 0, 0, 0]
                            Ce=[0, 0, 0, 0, 0, 0]
                            ret = SapModel.PropLink.SetLinear(Name, DOF, Fixed, Ke, Ce,0,0)     
                assert SapModel.Analyze.RunAnalysis()==0,'error '+ModelPath
                Analyze=SapModel.Analyze.RunAnalysis()
#                print(ModelPath,Analyze)
                assert SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")==0,'error '+ModelPath
                ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")
#                print(ModelPath,ret)
                ResModal= SapModel.Results.ModalPeriod()
                Periods=ResModal[4]
                ResModalParticipation=SapModel.Results.ModalParticipatingMassRatios()
                Ux=ResModalParticipation[5]
                Uy=ResModalParticipation[6]
                Rz=ResModalParticipation[13]
                # Unlock model
                if remove!=():
                    rem=remove[0]
                else:rem='ok'
                if min(rem!='no',rem!='No',rem!='NO'):
                    assert SapModel.SetModelIsLocked(False)==0
                    ret = SapModel.SetModelIsLocked(False)
                    assert myETABSObject.ApplicationExit(False)==0
                    ret = myETABSObject.ApplicationExit(False)
                    os.remove(ModelPath)
                    os.remove(ModelDirectory+ModelName+'.ico')
                    os.remove(ModelDirectory+ModelName+'.$et')
                    os.remove(ModelDirectory+ModelName+'.ebk')
            #    if ret1!=1: Periods=1000;Ux=1000;Uy=1000;Rz=1000
            #    print(ret1)
            except:
                os.remove(ModelPath)
                try:os.remove(ModelDirectory+ModelName+'.ico')
                except:pass
                try:os.remove(ModelDirectory+ModelName+'.$et')
                except:pass
                try:os.remove(ModelDirectory+ModelName+'.ebk')
                except:pass
#        ret = myETABSObject.ApplicationExit(False)

#        if Periods==[] and Ux==[] and Uy==[] and Rz==[]:
#            pidetabs=[]
#            for proc in psutil.process_iter(attrs=['pid', 'name']):
#                if proc.info['name']=='ETABS.exe':pidetabs.append(proc.info['pid'])
    return Periods,Ux,Uy,Rz
#except:
#    pass
def etabsIterations(KeNew,otherdata):
#    from MainModeling import *
#    import numpy as np
    import time
    Element=otherdata[0];units=otherdata[1];StructuralWeigthObj=otherdata[2];StructureDemand_CapacityObj=otherdata[3]
    ModelDirectory=otherdata[4];ProgramPath=otherdata[5];ModelName0=otherdata[6]
    PerObj=otherdata[7];ModalMassObj=otherdata[8];ETABSversion=otherdata[9]
    ob=len(PerObj)
    
#    intcont=0
#    while error==2 and punish==1 and intcont<2:
#        intcont+=1
#        try:
    Periods,Ux,Uy,Rz=etabselem(KeNew,Element,units,ModelDirectory,ProgramPath,ModelName0,ETABSversion)
    while ob>len(Periods):
        try:
            time.sleep(3)
            Periods,Ux,Uy,Rz=etabselem(KeNew,Element,units,ModelDirectory,ProgramPath,ModelName0,ETABSversion)
        except:pass
    if ob>len(Periods):
        print('the number of objectives is greater than the number of results')
        error=2 ; punish=1 ; Periods=[100 for i in range(ob)]
    else:
        vectOp=PerObj[:ob]
        vectOm=[]
        if ModalMassObj!=[]:
            for i in range(len(ModalMassObj)):vectOm=vectOm+trans(ModalMassObj)[i]
            Wp=0.8;Wm=0.2
        else:Wp=1;errorm=0
#        vectOm=trans(ModalMassObj)[0]+trans(ModalMassObj)[1]+trans(ModalMassObj)[2]
#                vectO=vectOp+vectOm
        vectp=Periods[:ob]
        vectm=Ux[:ob]+Uy[:ob]+Rz[:ob]
#        vect=vectp+vectm
        if weights!=False or weights!=[]:ukp=weights[:ob]
        else:ukp=list(range(len(vectp),0,-1))
        wkp=[ukp[i]/sum(ukp) for i in range(len(ukp))]
#        ukm=[np.random.rand() for i in range(len(vectm))]
        if weights!=False or weights!=[]:ukm=weights[ob:]
        else:ukm=list(range(len(vectm),0,-1))
        wkm=[ukm[i]/sum(ukm) for i in range(len(ukm))]
#        with open('test','w') as ff: ff.write(str(wkp)+'           '+str(wkm))
        
        errorp=sum([abs((vectp[i]-vectOp[i])/vectOp[i])*wkp[i] if vectOp[i]!=0 else vectp[i]*wkp[i] for i in range(len(vectp))])*Wp
        if ModalMassObj!=[]:errorm=sum([max(0,abs((vectm[i]-vectOm[i])/vectOm[i])-0.25)*wkm[i] if vectOm[i]!=0 else max(0,vectm[i]-0.25)*wkm[i] for i in range(len(vectm))])*Wm
        error=errorp+errorm
        punish=0
        with open('test','w') as ff: ff.write('weights='+str(weights)+'\rwkp='+str(wkp)+' wkm='+str(wkm)+'\r vectOp='+str(vectOp)+' vectp='+str(vectp)+'\rvectOm='+str(vectOm)+' vectm='+str(vectm)+'\rerrorp='+str(errorp)+' errorm='+str(errorm))
#                Refp=sum([vectOp[i]**2 for i in range(len(vectOp))])**0.5
#                Refm=sum([vectOm[i]**2 for i in range(len(vectOm))])**0.5
#        #            Ref=sum([vectO[i]**2 for i in range(len(vectO))])**0.5            
#                vectRp=[(vectOp[i]-vectp[i])**2 for i in range(len(vectOp))]
#                vectRm=[(vectOm[i]-vectm[i])**2 for i in range(len(vectOm))]
#        #            vectR=[(vectO[i]-vect[i])**2 for i in range(len(vectO))]
#        #            error=sum(vectR)**0.5/Ref
#        #            error=sum(vectRp)**0.5/Refp
##                error=sum(vectRp)**0.5/Refp*.75+max(0,sum(vectRm)**0.5/Refm-0.2)*.25# It is allawed until 20% of difference from the modal mass
##                punish=0#max(0,sum(vectRm)**0.5/Refm-0.2) # It is allawed until 20% of difference in the modal mass
#                error=sum(vectRp)**0.5/Refp
#                punish=max(0,sum(vectRm)**0.5/Refm-0.2)
#        except:pass
#            import os
#            name='etabs.exe';os.system("taskkill /f /im " + name)
#    print(error)
    return error,punish
def etabsGA(Ke1Init,Element,ETABSversion,units,StructuralWeigthObj,StructureDemand_CapacityObj,ModelDirectory,
            ProgramPath,ModelName0,PerObj,ModalMassObj,NumIndiv,MutationPorc,LengthChromosome,NGenerations,
            Nstopelite,elite,NumberCores,Daughtercomputers,tolbest,tolmean):
    lim=[]
    initialdata=[]
    for i in range(len(Element)):
        if Element[i][0]=='Link1':
            for j in range(0,len(Element[i])-1):
                if Ke1Init!=[]:
                    lim.append([Ke1Init[i][j]/9,Ke1Init[i][j]*9,'float'])
                    initialdata.append(Ke1Init[i][j])
                else:
                    lim.append([0,1e7,'float'])
    otherdata=[Element,units,StructuralWeigthObj,StructureDemand_CapacityObj,ModelDirectory,ProgramPath,ModelName0,PerObj,ModalMassObj,ETABSversion]#optional
    functionanalysis='MainModeling.etabsIterations'
    initialdata=[initialdata]
    if NumberCores>1:controlPowershell('ETABS',NumberCores)
    multiobjectives=len(PerObj)+sum([len(ModalMassObj[jj]) for jj in range(len(ModalMassObj))])
#    multiobjectives=False
    Pob_floatelite,fxelite,Pob_floatMean,Pob_floatmax=GA(functionanalysis,otherdata,lim,NumIndiv,\
            MutationPorc,LengthChromosome,NGenerations,Nstopelite,elite,NumberCores,initialdata,Daughtercomputers,tolbest,tolmean,multiobjectives)
    return Pob_floatelite,fxelite,Pob_floatMean,Pob_floatmax

def controlPowershell(program,NumberCores):
    text=[]
    text.append("import os")
    text.append("\rimport psutil")
    text.append("\rimport time")
    text.append("\rimport copy")
    text.append("\rimport numpy as np")
    text.append("\rprint('Etabs Monitoring')")
    text.append("\rtol=5")
    text.append("\rcontdel=0;maxcontsaved=0")
    text.append("\rif '"+program+"'=='ETABS' or '"+program+"'=='Etabs' or '"+program+"'=='etabs':program1='ETABS.exe';program2='etabs.exe'")
    text.append("\rreppid=[];cont1=0;maxcont=0;pidetabs0=[];switch=0;cont=0")
    text.append("\rwhile True:")
    text.append("\r    pidetabs=[]")
    text.append("\r    for proc in psutil.process_iter(attrs=['pid', 'name']):")
    text.append("\r        if proc.info['name']==program1:")
    text.append("\r            pidetabs.append(proc.info['pid'])")
    text.append("\r            if reppid==[] or list(np.transpose(reppid)[0]).__contains__(proc.info['pid'])==0:")
    text.append("\r                reppid.append([proc.info['pid'],0]);cont1=0;switch=0;contdel=0")
    text.append("\r    if cont1==0:cont+=1;maxcontsaved=max(maxcontsaved,maxcont)")
    text.append("\r    cont1+=1")
    text.append("\r    if pidetabs0!=[] and pidetabs!=[]:")
    text.append("\r        for i in range(len(pidetabs)):")
    text.append("\r            for j in range(len(pidetabs0)):")
    text.append("\r                ind=list(np.transpose(reppid)[0]).index(pidetabs[i])")
    text.append("\r                if (pidetabs[i]==pidetabs0[j] and len(pidetabs)<=max(2,"+str(NumberCores)+"/1.5)) or (cont>"+str(NumberCores)+"*1.5 and cont1/3>maxcontsaved):")
    text.append("\r                    reppid[ind][1]=reppid[ind][1]+1.0")#+1")print(cont,maxcontsaved,reppid[ind]);
    text.append("\r                    if (min(list(np.transpose(reppid)[1]))>tol and cont1>maxcont) or cont1/3>maxcontsaved:")
    text.append("\r                        if switch==0:switch=1;cont1=0;reppid=[[reppid[j][0],0] for j in range(len(reppid))]")
    text.append("\r                        if (switch==1 and cont1>maxcont) or cont1/3>maxcontsaved:")
    text.append("\r                            os.system('taskkill /f /im ' + program2)")
    text.append("\r                            reppid[ind][1]=0;cont1=0;switch=0;cont=0;maxcont=maxcont/1.5;maxcontsaved=maxcontsaved/1.5")
    text.append("\r        for i in range(len(reppid)-1,-1,-1):")
    text.append("\r            if pidetabs.__contains__(reppid[i][0])==0:")
    text.append("\r                reppid.remove(reppid[i])")
    text.append("\r    pidetabs0=copy.deepcopy(pidetabs)")
    text.append("\r    print(reppid,cont1)")
    text.append("\r    time.sleep(5);maxcont=max(cont1,maxcont)")
    text.append("\r    if len(pidetabs)==0:")
    text.append("\r        contdel+=1")
    text.append("\r    if contdel==5:")
    text.append("\r       break")
    import os
    Daughtercomputers=os.getcwd()
    with open(Daughtercomputers+'\\tempMultiComputer\\controlGAprocess.py','w+') as f:f.writelines(text)
    os.system("start powershell python tempMultiComputer\\controlGAprocess.py")
