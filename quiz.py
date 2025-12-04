def mostra_feedback(messaggio: str) -> None:
    """
    Restituisce il feedback formattato nella maniera desiderata.
    """
    simbol: str = "*"*30
    print(f"""
{simbol}
{messaggio}
{simbol}
""")

def is_risposta_esatta(scelta: str, risposta_esatta: str) -> bool:
    if scelta.upper() == risposta_esatta:
        return True
    else:
        return False


def genera_feedback(is_corretta: bool) -> str:

    if is_corretta == True:
        return "Hai indovinato!"
    else:
        return "Non hai indovinato."

def valida_scelta(scelta: str) -> bool:
    """
    Questa funzione prende un valore di tipo stringa e verifica che la risposta sia una delle opzioni tra A, B, C e D. 
    Se la risposta è una stringa vuota, restituisce false, idem se la risposta non è una di quelle sopra elencate.
    """
    scelta_tmp = scelta.upper()
    if scelta_tmp == "A" or scelta_tmp == "B" or scelta_tmp == "C" or scelta_tmp == "D":
        return True
    else: 
        return False

def mostra_domanda(domanda: str) -> None: 
    """
    Questa funzione restituisce la domanda e le opzioni della riposta. 
    """
    
    print(domanda)

def raccogli_risposta() -> str:
    """
    Questa funzione si occupa solamente di prendere l'input dell'utente. 
    Il controllo di tale valore avverrà attraverso una funzione dedicata.
    """ 
    return input("Inserisci la tua scelta: ")
    

def leggi_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        content = file.read()
        return content

def estrai_index(content: str) -> int: 
    return content.index("£")

def estrai_domanda(content: str, index: int) -> str:
    return content[0:index]

def estrai_risposta(content: str, index: int) -> str:
    return content[index+1:]

def estrai_lista_domande(file_path: str) -> list[str]:
    lista_domande: list[str] = []
    with open(file_path, "r") as f:
        for i in f:
            lista_domande.append(i.strip())
    return lista_domande 

def genera_statistiche(risultato_finale: list[dict[str, str | bool]]) -> dict[str, int]:
    statistica: dict[str, int] = {}

    risposte_esatte: int = 0
    risposte_non_esatte: int = 0

    for i in risultato_finale: 
        if i["risposta_corretta"]:
            risposte_esatte += 1
        else:
            risposte_non_esatte += 1

    statistica["risposte_esatte"] = risposte_esatte
    statistica["risposte_non_esatte"] = risposte_non_esatte
    return statistica

def mostra_progresso(counter_attuale: int, totale_domande: int) -> None:
    """
    Mostra il progresso dell'utente nel quiz.
    """
    percentuale: float = (counter_attuale / totale_domande) * 100
    print(f"\n--- PROGRESSO: {counter_attuale}/{totale_domande} ({percentuale:.1f}%) ---\n")

def mostra_menu_navigazione() -> str:
    """
    Mostra il menu di navigazione e raccoglie l'input dell'utente.
    """
    print("\n--- OPZIONI DI NAVIGAZIONE ---")
    print("[N] Prossima domanda")
    print("[I] Domanda precedente")
    print("[E] Esci dal quiz")
    scelta: str = input("Scegli un'opzione: ").upper()
    return scelta

def gestisci_navigazione(scelta_navigazione: str, counter_attuale: int, totale_domande: int) -> int:
    """
    Gestisce la navigazione tra le domande.
    Ritorna il nuovo valore del counter.
    """
    if scelta_navigazione == "N":
        if counter_attuale < totale_domande - 1:
            counter_attuale += 1
            print("Prossima domanda...")
        else:
            print("Sei già all'ultima domanda!")
    elif scelta_navigazione == "I":
        if counter_attuale > 0:
            counter_attuale -= 1
            print("Domanda precedente...")
        else:
            print("Sei già alla prima domanda!")
    elif scelta_navigazione == "E":
        print("Quiz terminato!")
        return -1  # Segnale per uscire
    else:
        print("Opzione non valida!")
    
    return counter_attuale

def main():
    lista_domande: list[str] = []
    risultato_finale: list[dict[str, str | bool]] = []
    domanda_e_risposta: dict[str, str] = {"domanda" : None, "risposta" : None}
    
    # Leggi tutti e tre i file di domande
    lista_domande = estrai_lista_domande("domande1.txt")
    lista_domande.extend(estrai_lista_domande("domande2.txt"))
    lista_domande.extend(estrai_lista_domande("domande3.txt"))

    counter_domanda_corrente: int = 0
    lista_domande_length: int = len(lista_domande)

    while counter_domanda_corrente < lista_domande_length:
        mostra_progresso(counter_domanda_corrente + 1, lista_domande_length)
        
        content: str = lista_domande[counter_domanda_corrente]
        index: int = estrai_index(content)
        domanda_e_risposta["domanda"] = estrai_domanda(content, index)
        domanda_e_risposta["risposta"] = estrai_risposta(content, index)

        mostra_domanda(domanda_e_risposta["domanda"])

        risposta_utente: str = raccogli_risposta()

        is_risposta_valid: bool = valida_scelta(risposta_utente)

        feedback: str = ""

        if is_risposta_valid:
            risultato: dict[str, str | bool] = {}
            is_risposta_corretta: bool = is_risposta_esatta(risposta_utente, domanda_e_risposta["risposta"])
            feedback = genera_feedback(is_risposta_corretta)
            risultato["domanda"] = lista_domande[counter_domanda_corrente]
            risultato["risposta_corretta"] = is_risposta_corretta
            risultato_finale.append(risultato)
            
            mostra_feedback(feedback)
            
            # Dopo aver risposto, mostra il menu di navigazione
            scelta_navigazione: str = mostra_menu_navigazione()
            counter_domanda_corrente = gestisci_navigazione(scelta_navigazione, counter_domanda_corrente, lista_domande_length)
            
            if counter_domanda_corrente == -1:  # Utente ha scelto di uscire
                break
        else: 
            feedback = "Inserisci solo la risposta tra le opzioni elencate"
            mostra_feedback(feedback)

    # Mostra statistiche finali
    statistiche: dict[str, int] = genera_statistiche(risultato_finale)

    print("\n--- STATISTICHE FINALI ---")
    print(f"Risposte esatte: {statistiche['risposte_esatte']}")
    print(f"Risposte errate: {statistiche['risposte_non_esatte']}")
    print(f"Domande completate: {len(risultato_finale)}/{lista_domande_length}")

# Entry point del nostro programma
main()