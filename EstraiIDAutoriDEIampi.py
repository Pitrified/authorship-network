#! python3

#da PersoneDEI.txt ho una lista di nomi
#in Authors.txt ci sono ID-autori, cerco gli autori
#salvo il AutoriDEIampi

spersone = set()
fpersone = open("PersoneDEI.txt")
for line in fpersone:
  line = line.rstrip()
  spersone.add(line)
  pz = line.split()
  #print(pz, " ", len(pz))
  if len(pz)==2:
    spersone.add(pz[0][0]+" "+pz[1])
  elif len(pz)==3:
    spersone.add(pz[0][0]+" "+pz[1][0]+" "+pz[2])
    spersone.add(pz[0]   +" "+pz[1][0]+" "+pz[2])
    spersone.add(pz[0][0]+" "+pz[1]   +" "+pz[2])
  elif len(pz)==4:
    spersone.add(pz[0][0]+" "+pz[1][0]+" "+pz[2][0]+" "+pz[3])
    spersone.add(pz[0]   +" "+pz[1][0]+" "+pz[2][0]+" "+pz[3])
    spersone.add(pz[0][0]+" "+pz[1]   +" "+pz[2][0]+" "+pz[3])
    spersone.add(pz[0][0]+" "+pz[1][0]+" "+pz[2]   +" "+pz[3])
    spersone.add(pz[0]   +" "+pz[1]   +" "+pz[2][0]+" "+pz[3])
    spersone.add(pz[0]   +" "+pz[1][0]+" "+pz[2]   +" "+pz[3])
    spersone.add(pz[0][0]+" "+pz[1]   +" "+pz[2]   +" "+pz[3])
  elif len(pz)==6:
    spersone.add(pz[0][0]+" "+pz[1][0]+" "+pz[2][0]+" "+pz[3][0]+" "+pz[4][0]+" "+pz[5])

#print(spersone)
#ffampie = open("PersoneDEIampie.txt", "w")
#ffampie.writelines(spersone)

fautori = open("Authors1000.txt", encoding="utf8") 
festratti = open("AutoriDEIampi.txt", "w")

i=0
for line in fautori:
  pz = line.rstrip().split("\t")
  if pz[1] in spersone:
    festratti.write(line)
  i+=1
  if i%1000000==0:
    print(i)