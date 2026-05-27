"""
Programa principal — Conversor de Números Romanos.

Fluxo:
    1. Recebe a cadeia (argumento ou input interativo).
    2. Valida com o AFD; em caso de rejeição, exibe mensagem com posição do erro.
    3. Se válida, converte com o parser GLC e exibe o resultado.
    4. Com --comparar, exibe também o resultado da abordagem imperativa.

Uso:
    python src/main.py [ROMANO] [--comparar]
    python src/main.py            # modo interativo
    python src/main.py XIV        # conversão direta
    python src/main.py XIV --comparar
"""

from __future__ import annotations

import argparse
import os
import sys

# Garante que src/ seja encontrado independentemente do diretório de trabalho
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from afd import executar, posicao_erro
from glc_parser import converter as converter_glc
from conversor_tradicional import converter as converter_tradicional


# ---------------------------------------------------------------------------
# Lógica de processamento
# ---------------------------------------------------------------------------

def processar(romano: str, comparar: bool = False) -> None:
    """
    Valida e converte um número romano, imprimindo o resultado no terminal.

    Args:
        romano:   Cadeia a processar (será convertida para maiúsculas).
        comparar: Se True, exibe também o resultado da abordagem imperativa.
    """
    romano = romano.strip().upper()

    if not romano:
        print("Erro: entrada vazia. Forneça um número romano (ex.: XIV).")
        return

    aceito, historico = executar(romano)

    if not aceito:
        pos = posicao_erro(romano, historico)
        print(f"Erro: '{romano}' não é um número romano canônico válido.")
        if pos is not None:
            char = romano[pos]
            marcador = ' ' * pos + '^'
            print(f"       {romano}")
            print(f"       {marcador}")
            print(f"  Caractere problemático: '{char}' na posição {pos}")
        print(f"  Trajetória do AFD: {' → '.join(historico)}")
        return

    resultado = converter_glc(romano)

    if comparar:
        resultado_trad = converter_tradicional(romano)
        print(f"Resultado (GLC parser):  {romano} = {resultado}")
        print(f"Resultado (imperativo):  {romano} = {resultado_trad}")
        if resultado == resultado_trad:
            print("  [OK] Ambas as abordagens concordam.")
        else:
            print("  [DIVERGENCIA] As abordagens retornaram valores diferentes!")
    else:
        print(f"{romano} = {resultado}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog='conversor',
        description='Conversor de números romanos para arábicos (1–3999).',
        epilog=(
            'Exemplos:\n'
            '  python src/main.py XIV\n'
            '  python src/main.py MMMCMXCIX --comparar\n'
            '  python src/main.py          # modo interativo'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        'romano',
        nargs='?',
        metavar='ROMANO',
        help='Número romano a converter (ex.: MCMXCIX). Omita para modo interativo.',
    )
    p.add_argument(
        '--comparar',
        action='store_true',
        help='Exibe também o resultado da abordagem imperativa para comparação.',
    )
    return p


def main() -> None:
    """Ponto de entrada principal."""
    args = _construir_parser().parse_args()

    if args.romano:
        processar(args.romano, comparar=args.comparar)
        return

    # Modo interativo
    print("Conversor de Números Romanos (1–3999)")
    print("Digite um número romano e pressione Enter. 'sair' para encerrar.")
    while True:
        try:
            entrada = input('\n> ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not entrada:
            continue
        if entrada.lower() in ('sair', 'exit', 'quit', 'q'):
            break
        processar(entrada, comparar=args.comparar)


if __name__ == '__main__':
    main()
