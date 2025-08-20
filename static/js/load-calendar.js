/**
 * Charge un tableau depuis une URL JSON et l'affiche dans un conteneur spécifié.
 * @param {string} jsonUrl - URL du fichier JSON contenant les données du tableau.
 * @param {string} containerId - ID du conteneur HTML où le tableau sera inséré.
 */
function loadCalendar(jsonUrl, containerId) {
  // Fonction pour créer le tableau avec Bootstrap
  function createTable(data) {
      const container = document.getElementById(containerId);
    if (!container) {
      console.error(`Le conteneur avec l'ID "${containerId}" n'existe pas.`);
      return;
    }

    const table = document.createElement("table");
    table.className = "table table-hover";

    // Ajouter les en-têtes
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    data.headers.forEach(header => {
      const th = document.createElement("th");
      th.textContent = header;
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Ajouter les lignes
    const tbody = document.createElement("tbody");
    data.rows.forEach(row => {
      const tr = document.createElement("tr");
      row.forEach(cell => {
        const td = document.createElement("td");
        td.textContent = cell;
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    container.appendChild(table);}

  // Charger les données via AJAX
  fetch(jsonUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error("Erreur lors du chargement des données");
      }
      return response.json();
    })
    .then(data => {
      createTable(data);
    })
    .catch(error => {
      console.error("Erreur :", error);
      const container = document.getElementById(containerId);
      if (container) {
        container.innerHTML =
          '<div class="alert alert-danger">Impossible de charger les données.</div>';
      }
    });
}
