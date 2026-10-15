import subprocess
import sys


def main():
    print("Verifica dei requisiti del workshop\n")
    tutto_ok = sys.version_info >= (3, 10)
    stato = "OK" if tutto_ok else "ERRORE"
    print(f"[{stato}] Python: {sys.version.split()[0]}")
    if not tutto_ok:
        print("  Installa Python 3.10 o successivo e selezionalo come interprete in VS Code.")

    for nome, comando in (("Git", "git"), ("UV", "uv")):
        try:
            risultato = subprocess.run(
                [comando, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
                check=True,
            )
            print(f"[OK] {nome}: {risultato.stdout.strip()}")
        except FileNotFoundError:
            tutto_ok = False
            print(f"[ERRORE] {nome} non trovato. Installalo seguendo il README.")
        except (OSError, subprocess.SubprocessError) as errore:
            tutto_ok = False
            print(f"[ERRORE] {nome}: {errore}")

    if tutto_ok:
        print("\nTutto pronto! Puoi proseguire con il workshop.")
    else:
        print("\nSistema gli errori, chiudi e riapri VS Code e riprova.")
    return 0 if tutto_ok else 1


if __name__ == "__main__":
    sys.exit(main())
