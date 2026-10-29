"""Roda o pipeline inteiro: ingestão -> refined -> marts -> painel."""
import dashboard
import ingestao
import marts
import refined

if __name__ == "__main__":
    print("== ingestão")
    ingestao.main()
    print("\n== refined")
    refined.main()
    print("\n== marts")
    marts.main()
    print("\n== painel")
    dashboard.main()
