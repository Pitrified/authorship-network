#!python2

from timeit import default_timer as timer

# import EstraiIDAutoriDEIampi as eaID
# import EstraiPapAutAffDEI as ePAAD
# import CreaEdgeCollab as cec
# import EstraiAutoriCollab as eac
# import CollassaNodiAmpi as cna
# from Verifiche_Test import PreparaPerGephi as ppg

import AnalisiMSR as amsr

celaborati = 'Versione3_Single\\'
cfileRAW   = 'C:\Users\Test\Documents\Tesi\FileRAW\\'
pfAuthorRAW = cfileRAW + 'Authors10.txt'
# pfAuthorRAW = cfileRAW + 'AuthorsDA0A1000000.txt'
# pfAuthorRAW = cfileRAW + 'Authors.txt'
pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations500.txt'
# pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations.txt'

pfPersone    = celaborati + 'PersoneDEI.txt'
pfAutoriID   = celaborati + 'AutoriDEIMacro.txt'
pfPapAutAff  = celaborati + 'PapAutAffDEIMacro.txt'
pfEdgeCollab = celaborati + 'EdgeCollabMacro.txt'
pfAutCollab  = celaborati + 'AutoriCollabMacro.txt'
pfEdgeCollabUnificati = celaborati + 'EdgeCollabUnificatiMacro.txt'
pfAutCollabUnificati  = celaborati + 'AutoriCollabUnificatiMacro.txt'
pfEdgeGephi  = celaborati + 'EdgeCollabUnificatiMacroGephi.tsv'
pfAutGephi   = celaborati + 'AutoriCollabUnificatiMacroGephi.tsv'


##in pfPersone ho una lista di nomi del dipartimento
start = timer()
##estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
sIDautDEI = amsr.estraiIDautori(pfPersone, pfAuthorRAW, pfAutoriID)
#print 'setlen:{} set:{}'.format(len(sIDautDEI), sIDautDEI)
lap1 = timer()
print 'completato estraiIDautori in {}'.format(lap1 - start)

##estraggo i paper scritti da questi IDautDEI
dPAA = amsr.estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff, sIDautDEI)
#ePAAD.estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
lap2 = timer()
print 'completato estraiPapAutAffDEI in {}'.format(lap2-lap1)

##estraggo gli EdgeCollab
dEdgeCollab = amsr.creaEdgeCollab(pfPapAutAff, pfEdgeCollab, dPAA)
# cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
lap3 = timer()
print 'completato creaEdgeCollab in {}'.format(lap3-lap2)

##estraggo gli AutoriCollab
pfAutoriID = celaborati + 'AutoriDEIMacroFull.txt'
pfEdgeCollab = celaborati + 'EdgeCollabMacroFull.txt'
#eac.estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab, dEdgeCollab)
amsr.estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
lap4 = timer()
print 'completato estraiAutoriCollab in {}'.format(lap4-lap3)

##collasso i nodi
amsr.collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
# cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
lap5 = timer()
print 'completato creaEdgeCollab in {}'.format(lap5-lap4)

##preparo per gephi
pfEdgeCollabUnificati = celaborati + 'EdgeCollabUnificatiMacro.txt'
amsr.preparaPerGephi(pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi)
# cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
lap6 = timer()
print 'completato creaEdgeCollab in {}'.format(lap6-lap5)



##########
# ##in pfPersone ho una lista di nomi del dipartimento
# start = timer()
# ##estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
# sIDautDEI = eaID.estraiIDautori(pfPersone, pfAuthorRAW, pfAutoriID)
# #print 'setlen:{} set:{}'.format(len(sIDautDEI), sIDautDEI)
# lap1 = timer()
# print 'completato estraiIDautori in {}'.format(lap1 - start)

# ##estraggo i paper scritti da questi IDautDEI
# dPAA = ePAAD.estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff, sIDautDEI)
# #ePAAD.estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
# lap2 = timer()
# print 'completato estraiPapAutAffDEI in {}'.format(lap2-lap1)

# ##estraggo gli EdgeCollab
# dEdgeCollab = cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab, dPAA)
# # cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
# lap3 = timer()
# print 'completato creaEdgeCollab in {}'.format(lap3-lap2)

# ##estraggo gli AutoriCollab
# pfAutoriID = celaborati + 'AutoriDEIMacroFull.txt'
# pfEdgeCollab = celaborati + 'EdgeCollabMacroFull.txt'
# #eac.estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab, dEdgeCollab)
# eac.estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
# lap4 = timer()
# print 'completato estraiAutoriCollab in {}'.format(lap4-lap3)

# ##collasso i nodi
# cna.collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
# # cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
# lap5 = timer()
# print 'completato creaEdgeCollab in {}'.format(lap5-lap4)

# ##preparo per gephi
# pfEdgeCollabUnificati = celaborati + 'EdgeCollabUnificatiMacro.txt'
# ppg.preparaPerGephi(pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi)
# # cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
# lap6 = timer()
# print 'completato creaEdgeCollab in {}'.format(lap6-lap5)


################

# celaborati = '...\tesi\versione8'
# cfraw = '...\fileraw'

# nomefpersone = 'PersoneDEI.txt'
# pfpersone = celaborati + "\\" + nomefpersone 

# nomefautoriID = 'AutoriDEIampi.txt'
# pfautoriID = celaborati + "\\" + nomefautoriID

# nomefPAAraw = 'PaperAuthorsAffiliation.txt'
# pfPAAraw = nomefPAAraw + "\\" + cfraw

# nomePAA = 'PapAutAffDEI.txt'
# pfPAA = celaborati + '\\' + nomePAA

# nomePadua = 'PadovaPadua.txt'
# cPadua = '...\tesi'
# pfPadua = cPadua + '\\' + nomePadua

# nomePPadovani = 'PaperPadovani.txt'
# pfPPadovani = celaborati + '\\' + nomePPadovani

# moduloEstraiIDautori.estraiIDautori(pfpersone, pfautoriID)
# moduloEstraiPapAutAffDEI.estraiPaperCollab(pfautoriID, pfPAAraw, pfPAA)
# modulo.estraiPaperPadovani(pfPAAraw, pfPadua, pfPPadovani)

################

# # print 'Ora importo'

# # import using_name

# # print 'Ho importato'

# # a = 'macro'
# # print 'macro: {}'.format(using_name.elabora(a))

# # print 'b: {}'.format(using_name.b)
# # using_name.elabora('faicose')
# # print 'b: {}'.format(using_name.b)

# import EstraiPaperModulo
# import CollassaNodiAmpiModulo
# 

# subfolderin = 'C:\Users\Test\Documents\Linguaggi\Prove\proveModuliMacro\subfolderin'
# subfolderout = 'C:\Users\Test\Documents\Linguaggi\Prove\proveModuliMacro\subfolderout'

# finputestrai = 'input200.txt'
# foutputestrai = 'outputEstraiMACRO1.txt'

# EstraiPaperModulo.init( nomefilein = finputestrai,
                        # nomefileout = foutputestrai,
                        # cartellain = subfolderin)

# finputcollassa = foutputestrai
# foutputcollassa = 'outputCollassaMACRO.txt'
# #finputpath = ''++''
# CollassaNodiAmpiModulo.init(nomefilein=finputcollassa,
                            # nomefileout=foutputcollassa)

                            
# start = timer()
# EstraiPaperModulo.estrai()
# lap1 = timer()
# print 'estrai:{}'.format(lap1-start)
# CollassaNodiAmpiModulo.collassa()
# end = timer()

# print 'totale:{}\testrai:{}\tcollassa:{}'.format(end-start, lap1-start, end-lap1)






