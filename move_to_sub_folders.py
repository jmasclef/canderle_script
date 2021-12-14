import os
import logging

from shutil import move as move_file
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
logger=logging.getLogger('LOG')
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger.setLevel(INFO)

if __name__=='__main__':
  effectif_scannes=0
  effectif_a_traiter=0
  effectif_tentes=0
  effectif_deplaces=0
  dossiers_crees=0
  dossiers_a_creer=0
  files_list=[]
  folders_to_create=set()
  folders_found=set()
  with os.scandir() as entries:
    for entry in entries:
      if entry.is_file():
        effectif_scannes+=1
        if entry.name.split('_').__len__()==3:
          effectif_a_traiter += 1
          folder_name=entry.name.split('_')[1]
          files_list.append((entry.name, folder_name))
      elif entry.is_dir():
        folders_found.add(entry.name)
  folders_to_create=set( [folder for file, folder in files_list if folder not in folders_found])
  logger.info(f"{effectif_scannes} fichiers scannés au total.")
  logger.info(f"{effectif_a_traiter} fichiers à traiter.")
  if len(folders_to_create)>0:
    logger.info("{0} dossiers à créer: {1}".format(len(folders_to_create),", ".join(folders_to_create)))
  reponse=input('(P)rocéder ou (Q)uitter ?')
  if reponse.lower()=="q":
    logger.info("Opération annulée, quitter.")
    quit()

  for folder_name in folders_to_create:
    is_done=False
    while not is_done:
      try:
        # Il essaie de le créer si réussi is_done passe à True
        os.mkdir(folder_name)
        logger.info(f"Le dossier {folder_name} a été créé")
        is_done = True
        dossiers_crees += 1
      except:
        reponse = input(f"Création du dossier {folder_name} impossible: (R)éessayer,(I)gnorer ou (Q)uitter ?")
        if reponse.lower() == "q":
          logger.error(f"Création du dossier {folder_name} impossible, quitter a été choisi")
          quit()
        elif reponse.lower() == "r":
          is_done = False
        elif reponse.lower() == "i":
          logger.error(
            f"Création du dossier {folder_name} impossible, ignorer a été choisi !'")
          continue
        else:
          print("Choix non reconnu => Réessayer")
          is_done = False

  for file_name, folder_name in files_list:
    is_done = False
    while not is_done:
      try:
        move_file(file_name, folder_name)
        is_done = True
        effectif_deplaces += 1
      except:
        reponse = input(f"Transfert du fichier {file_name} impossible: (R)éessayer,(I)gnorer ou (Q)uitter ?")
        if reponse.lower() == "q":
          logger.error(f"Transfert du fichier {file_name} impossible, quitter a été choisi")
          quit()
        elif reponse.lower() == "r":
          is_done = False
        elif reponse.lower() == "i":
          logger.error(
            f"Transfert du fichier {file_name} impossible, ignorer a été choisi, le fichier {file_name} n\' pas été traité !'")
          continue
        else:
          print("Choix non reconnu => Réessayer")
          is_done = False

  logger.info(f"{effectif_scannes} fichiers ont été scannés.")
  logger.info(f"{dossiers_crees} dossiers ont été créés.")
  logger.info(f"{effectif_tentes} fichiers ont fait l'objet d'une tentative de transfert.")
  logger.info(f"{effectif_deplaces} fichiers ont été déplacés avec succes.")