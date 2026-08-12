// web/components/lluvias.ts
import * as d3 from 'd3';

export interface RegistroLluvia {
  estacion: string;
  mm: number;
}

export function renderLluviaIndicator(containerId: string, data: RegistroLluvia[]): void {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = "";

  const totalMM = data.reduce((acc, curr) => acc + curr.mm, 0);

  // Crear tarjeta visual vectorizada con D3
  const svg = d3.create("svg")
    .attr("width", 420)
    .attr("height", 100)
    .attr("viewBox", [0, 0, 420, 100]);

  svg.append("rect")
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("fill", "#0d6efd")
    .attr("rx", 10);

  svg.append("text")
    .attr("x", "50%")
    .attr("y", "50%")
    .attr("dominant-baseline", "middle")
    .attr("text-anchor", "middle")
    .attr("fill", "#ffffff")
    .attr("font-family", "system-ui, sans-serif")
    .attr("font-size", "15px")
    .attr("font-weight", "bold")
    .text(`D3 + TS Active | Registros: ${data.length} | Acumulado: ${totalMM} mm`);

  container.appendChild(svg.node() as Node);
}