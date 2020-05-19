window.addEventListener("DOMContentLoaded", domReady);

function domReady() {
  const firstClassName = "availability--first";
  const removeClassName = "availability__remove";
  const availabilityClassName = "availability";
  const controlClassName = "availability__control";
  const removeHiddenClassName = "availability__remove--hidden";

  (function () {
    const availabilitiesEl = document.getElementById("availabilities");

    const entitiesEl = availabilitiesEl
      .getElementsByClassName("availability-entities")
      .item(0);

    // we will cache this node for always reuse
    const templateEl = availabilitiesEl
      .getElementsByClassName(firstClassName)
      .item(0);

    availabilitiesEl.addEventListener("click", (evt) => {
      const target = evt.target;

      if (target) {
        if (target.classList.contains("availability__add")) {
          const removeElsLen = getAvailabilityEls(entitiesEl).length;

          const availabilityEl = templateEl.cloneNode(true);
          availabilityEl.classList.remove(firstClassName);

          [].forEach.call(
            availabilityEl.getElementsByClassName(controlClassName),
            (el) => {
              setFormAttrs(el, removeElsLen);
            }
          );

          entitiesEl.appendChild(availabilityEl);
          toggleRemoveUiVisibility(entitiesEl);
          return;
        }

        if (target.classList.contains(removeClassName)) {
          const el = target.closest(`.${availabilityClassName}`);
          el.remove();
          toggleRemoveUiVisibility(entitiesEl);
          return;
        }
      }
    });
  })();

  function setFormAttrs(el, index) {
    el.name = el.name.replace(/\d/, index);
    el.id = el.id.replace(/\d/, index);
  }

  function getAvailabilityEls(entitiesEl) {
    return entitiesEl.getElementsByClassName(availabilityClassName);
  }

  function onToggleUiVisibility(availabilityEl, classListProp, index) {
    availabilityEl
      .getElementsByClassName(removeClassName)
      .item(0)
      .classList[classListProp](removeHiddenClassName);

    [].forEach.call(
      availabilityEl.getElementsByClassName(controlClassName),
      (el) => {
        setFormAttrs(el, index);
      }
    );
  }

  function toggleRemoveUiVisibility(entitiesEl) {
    const availabilityEls = getAvailabilityEls(entitiesEl);

    if (availabilityEls.length === 1) {
      const availabilityEl = availabilityEls.item(0);
      onToggleUiVisibility(availabilityEl, "add", 0);
    } else {
      [].forEach.call(availabilityEls, (el, index) => {
        onToggleUiVisibility(el, "remove", index);
      });
    }
  }
}
