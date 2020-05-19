window.addEventListener("DOMContentLoaded", domReady);

function domReady() {
  (function () {
    const showRouteId = "create-new-show-route";
    const artistControlId = "artist-control";
    const availableTimesId = "available";
    const availableHiddenClassName = "available--hidden";
    const availableBodyId = "available__body";

    if (document.getElementById(showRouteId)) {
      const artistEl = document.getElementById(artistControlId);
      const availableTimeEl = document.getElementById(availableTimesId);
      const availableBodyEl = document.getElementById(availableBodyId);

      const artistId = artistEl.value;

      if (isValidId(artistId)) {
        fetchArtist(artistId);
      }

      artistEl.addEventListener("change", (evt) => {
        availableBodyEl.innerHTML = "";
        const artistId = artistEl.value;

        if (isValidId(artistId)) {
          fetchArtist(artistId);
        }
      });

      function isValidId(artistId) {
        return /^\d$/.test(artistId);
      }

      async function fetchArtist(artistId) {
        const response = await fetch(`/artists/available-times/${artistId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        const { data } = await response.json();
        if (data) {
          availableTimeEl.classList.remove(availableHiddenClassName);

          data.forEach((datum, index) => {
            const trEl = document.createElement("tr");
            availableBodyEl.appendChild(trEl);

            const snEl = document.createElement("td");
            snEl.textContent = index + 1;
            trEl.appendChild(snEl);

            const dayOfWeekEl = document.createElement("td");
            dayOfWeekEl.textContent = datum.day_of_week;
            trEl.appendChild(dayOfWeekEl);

            const fromEl = document.createElement("td");
            fromEl.textContent = datum.from_time;
            trEl.appendChild(fromEl);

            const toEl = document.createElement("td");
            toEl.textContent = datum.to_time || "";
            trEl.appendChild(toEl);
          });
        } else {
          availableTimeEl.classList.add(availableHiddenClassName);
        }
      }
    }
  })();
}
