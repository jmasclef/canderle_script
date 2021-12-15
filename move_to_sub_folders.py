import os, sys, logging, getopt
from shutil import move as move_file

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
logger=logging.getLogger('LOG')
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger.setLevel(INFO)

if __name__=='__main__':
  argumentList = sys.argv[1:]
  target_folder=None
  if argumentList.__len__()>0:
    try:
      optlist, args = getopt.getopt(argumentList, 'd:')
      _, target_folder=optlist[0]
    except:
      logger.error(" ¯\_(⊙︿⊙)_/¯ arguments non reconnus: utiliser '-d destination' pour exécuter le script dans un autre dossier.")
      quit()

    if not os.path.isdir(target_folder):
      logger.error(f" ¯\_(⊙︿⊙)_/¯ le dossier nommé {target_folder} n'a pas été trouvé.")
      quit()
    else:
      target_folder = os.path.abspath(target_folder) #transforme les chemins relatifs en absolus
      logger.info(f"Exécution du script dans le dossier destination: {target_folder}")
      os.chdir(target_folder)

  if target_folder is None:
    target_folder=os.getcwd()
    logger.info(f"Exécution du script dans le dossier courant: {target_folder}")

  scanned_files=0
  target_files_list=set()
  transfered_files_list=set()
  replaced_files_list=set()
  ignored_files_list=set()
  folders_to_create=set()
  created_folders=set()
  ignored_folders=set()
  existing_folders=set()
  with os.scandir(target_folder) as entries:
    for entry in entries:
      if entry.is_file():
        scanned_files+=1
        if entry.name.split('_').__len__()==3:
          folder_name=entry.name.split('_')[1]
          target_files_list.add((entry.name, folder_name))
          if os.path.isfile(folder_name):
            logger.error(f" ¯\_(⊙︿⊙)_/¯ Le traitement du fichier {entry.name} est impossible, le fichier existant {folder_name} va bloquer la création du dossier !")
            quit()
      elif entry.is_dir():
        existing_folders.add(entry.name)

  folders_to_create=set( [folder for _, folder in target_files_list if folder not in existing_folders])
  previous_created_folders= set( [folder for _, folder in target_files_list if folder in existing_folders])

  logger.info(f"{scanned_files} fichier(s) scanné(s) au total.")
  logger.info("{} fichier(s) à traiter: {}".format(target_files_list.__len__(), ", ".join([ file_name for file_name,_ in target_files_list])))

  if len(folders_to_create)>0:
    logger.info("{0} dossiers à créer: {1}".format(len(folders_to_create),", ".join(folders_to_create)))

  if target_files_list.__len__()==0:
    logger.warning(" ¯\_(⊙︿⊙)_/¯ Aucune opération identifiée, quitter.")
    quit()
  else:
    reponse=input('(P)rocéder ou (Q)uitter ? ')
    if reponse.lower()!="p":
      logger.warning(" ¯\_(⊙︿⊙)_/¯ Opération annulée, quitter.")
      quit()

  for folder_name in folders_to_create:
    is_done=False
    while not is_done:
      try:
        # Il essaie de le créer si réussi is_done passe à True
        os.mkdir(folder_name)
        logger.info(f"Le dossier {folder_name} a été créé")
        created_folders.add(folder_name)
        is_done = True
      except:
        reponse = input(f"(҂◡_◡) Création du dossier {folder_name} impossible: (R)éessayer,(I)gnorer ou (Q)uitter ? ").lower()
        if reponse == "q":
          logger.error(f" ¯\_(⊙︿⊙)_/¯ Création du dossier {folder_name} impossible, quitter a été choisi")
          quit()
        elif reponse == "r":
          is_done = False
        elif reponse == "i":
          logger.warning(f"(҂◡_◡) Création du dossier {folder_name} impossible, ignorer a été choisi !'")
          ignored_folders.add(folder_name)
          is_done = True
        else:
            print("Choix non reconnu => Réessayer")
            is_done = False

  for file_name, folder_name in target_files_list:
    if not os.path.isdir(folder_name):
      logger.error(f"(҂◡_◡) Transfert du fichier {file_name} impossible, le dossier  {folder_name} n\'existe pas !")
      ignored_files_list.add(file_name)
      continue
    elif os.path.isfile(folder_name) :
      logger.error(f"(҂◡_◡) Transfert du fichier {file_name} impossible, un fichier porte le nom du dossier destination {folder_name} !'")
      ignored_files_list.add(file_name)
      continue

    is_done = False
    while not is_done:
      try:
        move_file(file_name,  folder_name) # provoque une exception si le fichier existe déjà
        is_done = True
        transfered_files_list.add(file_name)
      except:
        try:
          move_file(file_name,  os.path.join(folder_name, file_name)) #préciser le nom complet force l'écrasement si existant
          is_done = True
          transfered_files_list.add(file_name)
          replaced_files_list.add(file_name)
          logger.info(f"Le fichier {file_name} a été remplacé. ")
        except:
          reponse = input(f"Transfert du fichier {file_name} impossible: (R)éessayer,(I)gnorer ou (Q)uitter ? ")
          if reponse.lower() == "q":
            logger.error(f" ¯\_(⊙︿⊙)_/¯ Transfert du fichier {file_name} impossible, quitter a été choisi")
            quit()
          elif reponse.lower() == "r":
            is_done = False
          elif reponse.lower() == "i":
            logger.error(f"(҂◡_◡) Transfert du fichier {file_name} impossible, ignorer a été choisi, le fichier {file_name} n\' pas été traité !'")
            ignored_files_list.add(file_name)
            is_done = True
          else:
            print("(҂◡_◡) Choix non reconnu => Réessayer")
            is_done = False

  logger.info(f"{scanned_files} fichier(s) ont été scanné(s).")

  if created_folders.__len__()>0:
    logger.info("{} dossier(s) créé(s): {}.".format(len(created_folders), ", ".join(created_folders)))
  else:
    logger.info("Aucun dossier n'a été créé.")

  if previous_created_folders.__len__()>0:
    logger.info("{} dossier(s) déjà créé(s) précédemment: {}.".format(len(previous_created_folders), ", ".join(previous_created_folders)))

  if ignored_folders.__len__()>0:
    logger.warning("(҂◡_◡) {} dossier(s) ignoré(s): {}.".format(len(ignored_folders), ", ".join(ignored_folders)))
  else:
    if created_folders.__len__()>0:
      logger.info(" ᕙ(⇀‸↼)ᕗ Tous les dossiers nécessaires ont été créés.")

  if transfered_files_list.__len__()>0:

    logger.info("{} fichier(s) transféré(s): {}.".format(len(transfered_files_list), ", ".join(transfered_files_list)))

    if replaced_files_list.__len__()>0:
      logger.info("{} fichier(s) remplacé(s) à destination: {}.".format(len(replaced_files_list), ", ".join(replaced_files_list)))

    if ignored_files_list.__len__()>0:
      logger.warning("(҂◡_◡) {} fichier(s) ignoré(s): {}.".format(len(ignored_files_list), ", ".join(ignored_files_list)))
    else:
      logger.info(" ᕙ(⇀‸↼)ᕗ Tous les fichiers à traiter ont bien été transférés !")


  else:
    logger.info("(҂◡_◡) Aucun fichier n'a été transféré.")



