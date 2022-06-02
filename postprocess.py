from matplotlib import pyplot as plt
import numpy as np
import csv

#def load_results(loc):
def plot_main(loc):
    
    results_rb = np.zeros((525601,110))
    firstline = True

    with open('../reset_default_results/reset_'+loc+'/result_0_0_'+loc+'.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        a=0
        for row in plots:
            if firstline:
                firstline = False
            else:
                results_rb[a,:] = row[:]
                a=a+1
                
    results_base = np.zeros((525601,110))
    firstline = True
    
    with open('../baseline_results/baseline_'+loc+'/result_0_0_'+loc+'_baseline.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        a=0
        for row in plots:
            if firstline:
                firstline = False
            else:
                results_base[a,:] = row[:]
                a=a+1
    
    results = np.zeros((525601,110))
    firstline = True
    
    with open('./result_0_0_'+loc+'.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        a=0
        for row in plots:
            if firstline:
                firstline = False
            else:
                results[a,:] = row[:]
                a=a+1
    
    # with open('./reset_default_results_update/reset_'+loc+'/result_0_0_'+loc+'.csv', 'r') as csvfile:
    #     plots = csv.reader(csvfile, delimiter=',')
    #     a=0
    #     for row in plots:
    #         if firstline:
    #             firstline = False
    #         else:
    #             results[a,:] = row[:]
    #             a=a+1
                
#    return results, results_base, results_rb
                
    
    #=============================================================================
 
#def plot_main(loc, results, results_base, results_rb):
    
    if (loc=='seattle'):
        a = 2
    else:
        a = 0
        
    fan1 = results[:,32]
    fan2 = results[:,33]
    fan3 = results[:,34]
    
    fanTot = 60*(sum(fan1)+sum(fan2)+sum(fan3))
    fanTot = fanTot/1000000000
    fanCom = fan1+fan2+fan3
    
    fan1b = results_base[:,32]
    fan2b = results_base[:,33]
    fan3b = results_base[:,34]
    fanComb = fan1b+fan2b+fan3b
    
    fanTotb = 60*(sum(fan1b)+sum(fan2b)+sum(fan3b))
    fanTotb = fanTotb/1000000000
    
    fan1rb = results_rb[:,32]
    fan2rb = results_rb[:,33]
    fan3rb = results_rb[:,34]
    fanComrb = fan1rb+fan2rb+fan3rb
    
    fanTotrb = 60*(sum(fan1rb)+sum(fan2rb)+sum(fan3rb))
    fanTotrb = fanTotrb/1000000000
    
    #print(fanTot, fanTotb)
    
    chi1 = results[:,35]
    chi2 = results[:,36]
    
    chiCom = chi1+chi2
    
    chiTot = 60*(sum(chi1)+sum(chi2))
    chiTot = chiTot/1000000000
    
    chi1b = results_base[:,35]
    chi2b = results_base[:,36]
    
    chiComb = chi1b+chi2b
    
    chiTotb = 60*(sum(chi1b)+sum(chi2b))
    chiTotb = chiTotb/1000000000
    
    chi1rb = results_rb[:,35]
    chi2rb = results_rb[:,36]
    
    chiComrb = chi1rb+chi2rb
    
    chiTotrb = 60*(sum(chi1rb)+sum(chi2rb))
    chiTotrb = chiTotrb/1000000000
    
    #print(chiTot, chiTotb)
    
    boi = results[:,37]
    
    boiTot = 60*(sum(boi))
    boiTot = boiTot/1000000000
    
    boib = results_base[:,37]
    
    boiTotb = 60*(sum(boib))
    boiTotb = boiTotb/1000000000
    
    boirb = results_rb[:,37]
    
    boiTotrb = 60*(sum(boirb))
    boiTotrb = boiTotrb/1000000000
    
    #print(boiTot, boiTotb)
    
    if (loc=='seattle'):
        CHWP1 = results[:,53]
        CHWP2 = results[:,54]
        CHWP3 = results[:,55]
        
        CHWPTot = 60*(sum(CHWP1)+sum(CHWP2)+sum(CHWP3))
        
        CHWP1b = results[:,53]
        CHWP2b = results[:,54]
        CHWP3b = results[:,55]
        
        CHWPTotb = 60*(sum(CHWP1b)+sum(CHWP2b)+sum(CHWP3b))
    else:
    
        CHWP = results[:,53]
        CHWPTot = 60*(sum(CHWP))
        CHWPb = results_base[:,53]
        CHWPTotb = 60*(sum(CHWPb))
        CHWPrb = results_rb[:,53]
        CHWPTotrb = 60*(sum(CHWPrb))
        
    CHWPTot = CHWPTot/1000000000
    CHWPTotb = CHWPTotb/1000000000
    CHWPTotrb = CHWPTotrb/1000000000
    
    #print(CHWPTot, CHWPTotb)
    
    CWP = results[:,55+a]
    
    CWPTot = 60*(sum(CWP))
    CWPTot = CWPTot/1000000000
    
    CWPb = results_base[:,55+a]
    
    CWPTotb = 60*(sum(CWPb))
    CWPTotb = CWPTotb/1000000000
    
    CWPrb = results_rb[:,55+a]
    
    CWPTotrb = 60*(sum(CWPrb))
    CWPTotrb = CWPTotrb/1000000000
    
    #print(CWPTot, CWPTotb)
    
    HWP = results[:,54+a]
    
    HWPTot = 60*(sum(HWP))
    HWPTot = HWPTot/1000000000
    
    HWPb = results_base[:,54+a]
    
    HWPTotb = 60*(sum(HWPb))
    HWPTotb = HWPTotb/1000000000
    
    HWPrb = results_rb[:,54+a]
    
    HWPTotrb = 60*(sum(HWPrb))
    HWPTotrb = HWPTotrb/1000000000
    
    #print(HWPTot, HWPTotb)
    
    CT1 = results[:,56+a]
    CT2 = results[:,57+a]
    
    cooTowTot = 60*(sum(CT1)+sum(CT2))
    cooTowTot = cooTowTot/1000000000
    
    cooTowCom = CT1+CT2
    
    CT1b = results_base[:,56+a]
    CT2b = results_base[:,57+a]
    
    cooTowTotb = 60*(sum(CT1b)+sum(CT2b))
    cooTowTotb = cooTowTotb/1000000000
    
    cooTowComb = CT1b+CT2b
    
    CT1rb = results_rb[:,56+a]
    CT2rb = results_rb[:,57+a]
    
    cooTowTotrb = 60*(sum(CT1rb)+sum(CT2rb))
    cooTowTotrb = cooTowTotrb/1000000000
    
    cooTowComrb = CT1rb+CT2rb
    
    cooTot = cooTowTot+chiTot+CHWPTot+CWPTot
    heaTot = boiTot+HWPTot
    
    cooTotb = cooTowTotb+chiTotb+CHWPTotb+CWPTotb
    heaTotb = boiTotb+HWPTotb
    
    cooTotrb = cooTowTotrb+chiTotrb+CHWPTotrb+CWPTotrb
    heaTotrb = boiTotrb+HWPTotrb
    
    if (loc=='seattle'):
        cooCom = chiCom+CHWP1+CHWP2+CHWP3+CWP+cooTowCom
        cooComb = chiComb+CHWP1b+CHWP2b+CHWP3b+CWPb+cooTowComb
    else:
        cooCom = chiCom+CHWP+CWP+cooTowCom
        cooComb = chiComb+CHWPb+CWPb+cooTowComb
        cooComrb = chiComrb+CHWPrb+CWPrb+cooTowComrb
        
    heaCom = boi+HWP
    heaComb = boib+HWPb
    heaComrb = boirb+HWPrb
    
    #print(fanTot, cooTot, heaTot, fanTot+cooTot+heaTot)
    #print(fanTotb, cooTotb, heaTotb, fanTotb+cooTotb+heaTotb)
    
    TSupSet = results[:,68+a]
    TCHWSet = results[:,70+a]
    TOut = results[:,38]
    mSup = results[:,43]
    T5 = results[:,7]
    T1 = results[:,8]
    T2 = results[:,9]
    T3 = results[:,10]
    T4 = results[:,11]
    
    TSupSetb = results_base[:,68+a]
    TCHWSetb = results_base[:,70+a]
    TOutb = results_base[:,38]
    mSupb = results_base[:,43]
    T5b = results_base[:,7]
    T1b = results_base[:,8]
    T2b = results_base[:,9]
    T3b = results_base[:,10]
    T4b = results_base[:,11]
    
    TSupSetrb = results_rb[:,68+a]
    TCHWSetrb = results_rb[:,70+a]
    TOutrb = results_rb[:,38]
    mSuprb = results_rb[:,43]
    T5rb = results_rb[:,7]
    T1rb = results_rb[:,8]
    T2rb = results_rb[:,9]
    T3rb = results_rb[:,10]
    T4rb = results_rb[:,11]
    
    plt.figure(1)
    # plt.bar(1, fanTotb, edgecolor='k', color = 'g', label='fan')
    # plt.bar(2, fanTot, edgecolor='k', color = 'g', hatch='///')
    # plt.bar(3, fanTotrb, edgecolor='k', color = 'g', hatch='o')
    # plt.bar(5, cooTotb, edgecolor='k', color = 'b', label='cooling')
    # plt.bar(6, cooTot, edgecolor='k', color = 'b', hatch='///')
    # plt.bar(7, cooTotrb, edgecolor='k', color = 'b', hatch='o')
    # plt.bar(9, heaTotb, edgecolor='k', color = 'r', label='heating')
    # plt.bar(10, heaTot, edgecolor='k', color = 'r', hatch='///')
    # plt.bar(11, heaTotrb, edgecolor='k', color = 'r', hatch='o')
    plt.bar(1, fanTotb+cooTotb+heaTotb, edgecolor='k', color = 'w', label='baseline')
    plt.bar(2, fanTotrb+cooTotrb+heaTotrb, edgecolor='k', color = 'w', hatch='///', label='default reset')
    plt.bar(3, fanTot+cooTot+heaTot, edgecolor='k', color = 'w', hatch='o', label='tuned reset')
    plt.legend(loc='best')
    plt.ylabel('Energy (GJ)')
    plt.xticks([2], ['total energy'])
    plt.xlim([0,6])
    plt.savefig('total_energy.jpg', dpi = 300, bbox_inches='tight')
    plt.close()
    
    plt.figure(2)
    plt.bar(1, fanTotb, edgecolor='k', color = 'g', label='fan')
    plt.bar(2, fanTotrb, edgecolor='k', color = 'g', hatch='///')
    plt.bar(3, fanTot, edgecolor='k', color = 'g', hatch='o')
    plt.bar(5, cooTotb, edgecolor='k', color = 'b', label='cooling')
    plt.bar(6, cooTotrb, edgecolor='k', color = 'b', hatch='///')
    plt.bar(7, cooTot, edgecolor='k', color = 'b', hatch='o')
    plt.bar(9, heaTotb, edgecolor='k', color = 'r', label='heating')
    plt.bar(10, heaTotrb, edgecolor='k', color = 'r', hatch='///')
    plt.bar(11, heaTot, edgecolor='k', color = 'r', hatch='o')
    plt.bar(13, 0, edgecolor='k', color = 'w', label='baseline')
    plt.bar(14, 0, edgecolor='k', color = 'w', hatch='///', label='default reset')
    plt.bar(15, 0, edgecolor='k', color = 'w', hatch='o', label='tuned reset')
    plt.legend(loc='best')
    plt.ylabel('Energy (GJ)')
    plt.xticks([2, 6, 10], ['fan', 'cooling', 'heating'])
    plt.xlim([0,12])
    plt.savefig('energy_breakdown.jpg', dpi = 300, bbox_inches='tight')
    plt.close()
    
    # t = results[:,1]
    
    # def hravg(t,y,i1,i2):
        
    #     tc = 0
    #     sumy = 0
    #     avgy = np.zeros(24)
    #     hr = 1
    #     for i in range(24*60):
    #         if ((t[i+i1+1]-t[i1])/3600>hr):
    #             sumy = sumy/tc
    #             avgy[hr-1] = sumy
    #             sumy = 0
    #             tc = 0
    #             hr += 1
                
    #         else:
    #             sumy += y[i+i1]*(t[i+i1+1]-t[i1+i])
    #             tc += t[i+i1+1]-t[i1+i]
                
    #     return avgy
     
    # i1 = int(20*24*60)
    # i2 = int(21*24*60)   
    
    # avgFan = hravg(t,fanCom,i1,i2)
    # avgFanb = hravg(t,fanComb,i1,i2)
    
    # avgCoo = hravg(t,cooCom,i1,i2)
    # avgCoob = hravg(t,cooComb,i1,i2)
    
    # avgHea = hravg(t,heaCom,i1,i2)
    # avgHeab = hravg(t,heaComb,i1,i2)
    # plt.figure(3)
    # plt.plot(avgFan/1000, 'g', label='fan_reset')
    # plt.plot(avgFanb/1000, 'go', mfc='None', label='fan_base')
    # plt.plot(avgCoo/1000, 'b', label='cooling_reset')
    # plt.plot(avgCoob/1000, 'bo', mfc='None', label='cooling_base')
    # plt.plot(avgHea/1000, 'r', label='heating_reset')
    # plt.plot(avgHeab/1000, 'ro', mfc='None', label='heating_base')
    # plt.title('Winter Day')
    # plt.ylabel('Power (kW)')
    # #plt.ylim([0,500])
    # plt.legend(loc='best')
    # plt.xticks([0, 6, 12, 18, 24], ['12:00 am', '6:00 am', '12:00 pm', '6:00 pm', '12:00 am'])
    
    # plt.figure(4)
    # plt.plot((t[i1:i2]-t[i1])/3600, TSupSet[i1:i2], 'k', label='TSup')
    # plt.plot((t[i1:i2]-t[i1])/3600, TSupSetb[i1:i2], 'k--')
    # plt.plot((t[i1:i2]-t[i1])/3600, TOut[i1:i2], 'g', label='TOut')
    # plt.plot((t[i1:i2]-t[i1])/3600, TCHWSet[i1:i2], 'b', label='TCHW')
    # plt.plot((t[i1:i2]-t[i1])/3600, TCHWSetb[i1:i2], 'b--')
    # plt.plot((t[i1:i2]-t[i1])/3600, T1[i1:i2], 'y', label='TCore')
    # plt.plot((t[i1:i2]-t[i1])/3600, T1b[i1:i2], 'y--')
    # #plt.plot(np.linspace(0,24,24), np.zeros(24)+12.78, 'ko', mfc='None', label='TSup$_{base}$')
    # #plt.plot(np.linspace(0,24,24), np.zeros(24)+6.7, 'bo', mfc='None', label='TCHW$_{base}$')
    # plt.title('Winter Day')
    # plt.ylabel('Temperature ($^\circ$C)')
    # plt.ylim([0,30])
    # plt.legend(loc='best')
    # plt.xticks([0, 6, 12, 18, 24], ['12:00 am', '6:00 am', '12:00 pm', '6:00 pm', '12:00 am'])
    
    # plt.figure(5)
    # plt.plot((t[i1:i2]-t[i1])/3600, mSup[i1:i2], 'k', label='reset')
    # plt.plot((t[i1:i2]-t[i1])/3600, mSupb[i1:i2], 'k--', label='baseline')
    # plt.title('Winter Day')
    # plt.ylabel('Airflow rate (kg/s)')
    # #plt.ylim([0,30])
    # plt.legend(loc='best')
    # plt.xticks([0, 6, 12, 18, 24], ['12:00 am', '6:00 am', '12:00 pm', '6:00 pm', '12:00 am'])
    
    
    # i1 = int(232*24*60)
    # i2 = int(233*24*60)
    
    # avgFan = hravg(t,fanCom,i1,i2)
    # avgFanb = hravg(t,fanComb,i1,i2)
    
    # avgCoo = hravg(t,cooCom,i1,i2)
    # avgCoob = hravg(t,cooComb,i1,i2)
    
    # avgHea = hravg(t,heaCom,i1,i2)
    # avgHeab = hravg(t,heaComb,i1,i2)
    # plt.figure(6)
    # plt.plot(avgFan/1000, 'g', label='fan_reset')
    # plt.plot(avgFanb/1000, 'go', mfc='None', label='fan_base')
    # plt.plot(avgCoo/1000, 'b', label='cooling_reset')
    # plt.plot(avgCoob/1000, 'bo', mfc='None', label='cooling_base')
    # plt.plot(avgHea/1000, 'r', label='heating_reset')
    # plt.plot(avgHeab/1000, 'ro', mfc='None', label='heating_base')
    # plt.title('Summer Day')
    # plt.ylabel('Power (kW)')
    # #plt.ylim([0,500])
    # plt.legend(loc='best')
    # plt.xticks([0, 6, 12, 18, 24], ['12:00 am', '6:00 am', '12:00 pm', '6:00 pm', '12:00 am'])
    
    # plt.figure(7)
    # plt.plot((t[i1:i2]-t[i1])/3600, TSupSet[i1:i2], 'k', label='TSup')
    # plt.plot((t[i1:i2]-t[i1])/3600, TSupSetb[i1:i2], 'k--')
    # plt.plot((t[i1:i2]-t[i1])/3600, TOut[i1:i2], 'g', label='TOut')
    # plt.plot((t[i1:i2]-t[i1])/3600, TCHWSet[i1:i2], 'b', label='TCHW')
    # plt.plot((t[i1:i2]-t[i1])/3600, TCHWSetb[i1:i2], 'b--')
    # plt.plot((t[i1:i2]-t[i1])/3600, T1[i1:i2], 'y', label='TCore')
    # plt.plot((t[i1:i2]-t[i1])/3600, T1b[i1:i2], 'y--')
    # #plt.plot(np.linspace(0,24,24), np.zeros(24)+12.78, 'ko', mfc='None', label='TSup$_{base}$')
    # #plt.plot(np.linspace(0,24,24), np.zeros(24)+6.7, 'bo', mfc='None', label='TCHW$_{base}$')
    # plt.title('Summer Day')
    # plt.ylabel('Temperature ($^\circ$C)')
    # #plt.ylim([0,30])
    # plt.legend(loc='best')
    # plt.xticks([0, 6, 12, 18, 24], ['12:00 am', '6:00 am', '12:00 pm', '6:00 pm', '12:00 am'])
    
    # plt.figure(8)
    # plt.plot((t[i1:i2]-t[i1])/3600, mSup[i1:i2], 'k', label='reset')
    # plt.plot((t[i1:i2]-t[i1])/3600, mSupb[i1:i2], 'k--', label='baseline')
    # plt.title('Summer Day')
    # plt.ylabel('Airflow rate (kg/s)')
    # #plt.ylim([0,30])
    # plt.legend(loc='best')
    # plt.xticks([0, 6, 12, 18, 24], ['12:00 am', '6:00 am', '12:00 pm', '6:00 pm', '12:00 am'])
    
    # i1 = int(303*24*60)
    # i2 = int(304*24*60)
    
    # avgFan = hravg(t,fanCom,i1,i2)
    # avgFanb = hravg(t,fanComb,i1,i2)
    
    # avgCoo = hravg(t,cooCom,i1,i2)
    # avgCoob = hravg(t,cooComb,i1,i2)
    
    # avgHea = hravg(t,heaCom,i1,i2)
    # avgHeab = hravg(t,heaComb,i1,i2)
    # plt.figure(9)
    # plt.plot(avgFan/1000, 'g', label='fan_reset')
    # plt.plot(avgFanb/1000, 'go', mfc='None', label='fan_base')
    # plt.plot(avgCoo/1000, 'b', label='cooling_reset')
    # plt.plot(avgCoob/1000, 'bo', mfc='None', label='cooling_base')
    # plt.plot(avgHea/1000, 'r', label='heating_reset')
    # plt.plot(avgHeab/1000, 'ro', mfc='None', label='heating_base')
    # plt.title('Fall Day')
    # plt.ylabel('Power (kW)')
    # #plt.ylim([0,500])
    # plt.legend(loc='best')
    # plt.xticks([0, 6, 12, 18, 24], ['12:00 am', '6:00 am', '12:00 pm', '6:00 pm', '12:00 am'])
    
    # plt.figure(10)
    # plt.plot((t[i1:i2]-t[i1])/3600, TSupSet[i1:i2], 'k', label='TSup')
    # plt.plot((t[i1:i2]-t[i1])/3600, TSupSetb[i1:i2], 'k--')
    # plt.plot((t[i1:i2]-t[i1])/3600, TOut[i1:i2], 'g', label='TOut')
    # plt.plot((t[i1:i2]-t[i1])/3600, TCHWSet[i1:i2], 'b', label='TCHW')
    # plt.plot((t[i1:i2]-t[i1])/3600, TCHWSetb[i1:i2], 'b--')
    # plt.plot((t[i1:i2]-t[i1])/3600, T1[i1:i2], 'y', label='TCore')
    # plt.plot((t[i1:i2]-t[i1])/3600, T1b[i1:i2], 'y--')
    # #plt.plot(np.linspace(0,24,24), np.zeros(24)+12.78, 'ko', mfc='None', label='TSup$_{base}$')
    # #plt.plot(np.linspace(0,24,24), np.zeros(24)+6.7, 'bo', mfc='None', label='TCHW$_{base}$')
    # plt.title('Fall Day')
    # plt.ylabel('Temperature ($^\circ$C)')
    # plt.ylim([0,30])
    # plt.legend(loc='best')
    # plt.xticks([0, 6, 12, 18, 24], ['12:00 am', '6:00 am', '12:00 pm', '6:00 pm', '12:00 am'])
    
    # plt.figure(11)
    # plt.plot((t[i1:i2]-t[i1])/3600, mSup[i1:i2], 'k', label='reset')
    # plt.plot((t[i1:i2]-t[i1])/3600, mSupb[i1:i2], 'k--', label='baseline')
    # plt.title('Fall Day')
    # plt.ylabel('Airflow rate (kg/s)')
    # #plt.ylim([0,30])
    # plt.legend(loc='best')
    # plt.xticks([0, 6, 12, 18, 24], ['12:00 am', '6:00 am', '12:00 pm', '6:00 pm', '12:00 am'])
    
    # =============================================================================

    return

