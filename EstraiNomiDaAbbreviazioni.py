#! python2

#da PersoneDEI.txt ho una lista di nome soprannome cognome
#da cui ricavo n s cognome; nome s cognome; n soprannome cognome;
#devo salvare i riferimenti per risalire da n s cognome alla forma intera
#snippet chiamato all'inizio di CollassaNodiAmpi.py

def trovaNome(abbreviato):
  for entry in dpersone:
    #printType(dpersone[entry])
    if abbreviato in dpersone[entry]:
      #print dpersone[entry]
      return entry
  return "NOTFOUND!"

tot = 0
dpersone = {}
fpersone = open("PersoneDEI.txt")
for line in fpersone:
  line = line.rstrip()
  dpersone.update({line:set()})
  pz = line.split()
  #print(pz, " ", len(pz))
  if len(pz)==2:
    dpersone[line].add(pz[0][0]+" "+pz[1])
    tot += 2
  elif len(pz)==3:
    dpersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2])
    dpersone[line].add(pz[0]   +" "+pz[1][0]+" "+pz[2])
    dpersone[line].add(pz[0][0]+" "+pz[1]   +" "+pz[2])
    tot += 4
  elif len(pz)==4:
    dpersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2][0]+" "+pz[3])
    dpersone[line].add(pz[0]   +" "+pz[1][0]+" "+pz[2][0]+" "+pz[3])
    dpersone[line].add(pz[0][0]+" "+pz[1]   +" "+pz[2][0]+" "+pz[3])
    dpersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2]   +" "+pz[3])
    dpersone[line].add(pz[0]   +" "+pz[1]   +" "+pz[2][0]+" "+pz[3])
    dpersone[line].add(pz[0]   +" "+pz[1][0]+" "+pz[2]   +" "+pz[3])
    dpersone[line].add(pz[0][0]+" "+pz[1]   +" "+pz[2]   +" "+pz[3])
    tot += 8
  elif len(pz)==6:
    dpersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2][0]+" "+pz[3][0]+" "+pz[4][0]+" "+pz[5])
    tot += 2

print "Totale:",tot
print dpersone

print "p villoresi si chiama "+trovaNome("p villoresi")
print "p m ra si chiama "+trovaNome("p m ra")
