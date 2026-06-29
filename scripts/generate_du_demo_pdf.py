#!/usr/bin/env python3
"""Genera PDF demo ≤2 páginas para Document Understanding."""

from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).resolve().parents[1] / "data" / "du_demo_inspection.pdf"


def main() -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, "PC Doctor S.A. - Informe de inspeccion de campo", ln=True)
    pdf.ln(4)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(
        0,
        7,
        "Cliente: DOMINGUEZ GOMEZ JUAN ERNESTO\n"
        "RUC: 1709123456001\n"
        "Tipo: Re-inspeccion residencial post-SOP\n"
        "Observaciones: Hub operativo. Sin placeholders.\n"
        "Fecha informe: 2026-06-28",
    )
    pdf.add_page()
    pdf.multi_cell(
        0,
        7,
        "Checklist:\n"
        "- Hub-first: OK\n"
        "- MongoDB live: OK\n"
        "- Entrega PDF-first: pendiente revision",
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    print(f"OK: {OUT}")


if __name__ == "__main__":
    main()
