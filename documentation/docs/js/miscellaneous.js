'use strict';

/* Hide Table of Content items that match one of the following criteria:
* - has the 'no-toc' class
* - has the 'h1' class
* - its heading has a `display: none` style (e.g. when it is inside a tab that is not active)
*/
function hideTocItems() {
    const no_toc_classes = ['no-toc', 'h1']
    let toc_items = document.querySelectorAll('[aria-label="On this page"] .md-nav__item')
    toc_items.forEach(item => {
        let parag_id = item.querySelector('a').href.split('#')[1];
        let parag = document.getElementById(parag_id)
        if (parag && no_toc_classes.some(className => parag.classList.contains(className))) {
            item.style.display = 'none'
        }
    })
}

// Add buttons at the top of each table column (when hovered) to sort it
function sortTables() {
  let tables = document.querySelectorAll("article table:not([class])");
  tables.forEach(table => new Tablesort(table));
}

/*
  Add functionality to tabs 
*/
function tabFunctionality() {
  let activeEl = document.activeElement;
  // If tab is activeElement (for example if a link points to an ID 
  // inside the tab content/button), make that tab active
  if (activeEl?.parentElement.classList.contains("tabLabels")) {
    activeEl.blur();
    openTab(activeEl);
  } else {
    // Otherwise first check if a tab was open and a page reloaded, and open the same tab, 
    // otherwise open the tab that has the .activeTab class, otherwise open the first tab
    document.querySelectorAll(".tabLabels").forEach(tabLabels => {
      let label = tabLabels.getAttribute("label");
      let tabID;
      if (sessionStorage.getItem(`tabs-label=${label}`)) {
        tabID = document.getElementById(tabID) ? sessionStorage.getItem(`tabs-label=${label}`) : tabLabels.firstElementChild.id;
      } else if (tabLabels.querySelector(".activeTab")) {
        tabID = tabLabels.querySelector(".activeTab").id;
      } else {
        tabID = tabLabels.firstElementChild.id;
      }
      openTab(document.getElementById(tabID));
    })
  }
  // Add click event to tab buttons
  let tabButtons = document.querySelectorAll(".tabLabels > button");
  tabButtons.forEach(button=>{
    button.addEventListener('click', (e) => openTab(e.currentTarget));
  })

  // Add click event for links to tab IDs
  document.querySelectorAll('[href^="#"]:not([class^="md"])').forEach(el => {
    let href = el.getAttribute('href');
    let tabEl = document.getElementById(href.slice(1,))
    if (tabEl?.parentElement.classList.contains("tabLabels")) {
      el.addEventListener("click",(e) => openTab(tabEl), false);
    }
  })
  
  function openTab(tab) {
    let label = tab.parentElement.getAttribute('label');
    let index = Array.from(tab.parentElement.children).indexOf(tab)+1;
    // Remove active classes from tabs with matching labels 
    document.querySelectorAll(`.tabLabels[label="${label}"] > .activeTab`).forEach(elem => {
      elem.classList.remove('activeTab');
    });
    // Remove active classes from contents whose none of their associated tabs IDs are activeTabs
    document.querySelectorAll('[tabcontentfor]').forEach(elem => {
      let tabcontentfor = elem.getAttribute('tabcontentfor');
      if (
        ! tabcontentfor.split(' ').some(tabID => {
          return document.getElementById(tabID).classList.contains('activeTab')
        })
      ) {
          elem.classList.remove('activeTab');
      }
    });
    // Add active classes to tab labels
    document.querySelectorAll(`.tabLabels[label=${label}] > :nth-child(${index})`)
      .forEach(button => {button.classList.add('activeTab')});
    // Add active classes to contents whose any associated tabs IDs are activeTabs
    document.querySelectorAll('[tabcontentfor]').forEach(elem => {
      let tabcontentfor = elem.getAttribute('tabcontentfor');
      if (
        tabcontentfor.split(' ').some(tabID => {
          return document.getElementById(tabID).classList.contains('activeTab')
        })
      ) {
        elem.classList.add('activeTab');
      }
    });
    // Add tab ID hash to URL
    history.pushState(null, null, `#${tab.id}`);
    // Save active tab to sessionStorage
    sessionStorage.setItem(`tabs-label=${label}`,`${tab.id}`);
  }
}


/*
  Make links that go to a different website 'external' by adding the
  target="_blank" attribute, and add an external-link icon to them.
*/
function makeLinksExternal() {
  // Links to be opened in a new tab
  document.querySelectorAll("a[href^='http']:not([href^='https://access-hive.org.au'])")
    .forEach(link => {
      link.setAttribute('target','_blank');
    });
  // Add external link icon only to some external links
  document.querySelectorAll("article a[href^='http']:not([href^='https://access-hive.org.au']):not(:is(.vertical-card,.horizontal-card,.text-card))")
    .forEach(link => {
      link.classList.add('external-link');
    });
}


/*
  Add button to toggle terminal-animations for the whole page (next to the page title)
*/
function toggleTerminalAnimations() {
    if (document.querySelector('terminal-window')) {
        const COOKIE_TEXT = 'ACCESS-Hive-Docs-animated-terminal-state';
        const SWITCH_IMG = '/assets/terminal_animation_switch.png';
        const SWITCH_IMG_INACTIVE = '/assets/terminal_animation_switch_inactive.png';
        
        function getState() {
            return localStorage.getItem(COOKIE_TEXT) || 'active';
        }

        function setStateCookie(state) {
            localStorage.setItem(COOKIE_TEXT, state);
        }
        
        function setSwitchIcon(element, state) {
            if (state === 'active') {
                element.classList.add('hidden');
            } else {
                element.classList.remove('hidden');
            }
        }
        
        function applyStateToTerminalWindows(state) {
            let terminalWindows = document.querySelectorAll('terminal-window');
            if (state === 'active') {
                terminalWindows.forEach(t => {
                    t.removeAttribute('static');
                })
            } else {
                terminalWindows.forEach(t => {
                    t.setAttribute('static',"");
                })
            }
        }

        function applyState(container, state) {
            // Change the switch icon and title            
            setSwitchIcon(container.children[1], state);
            setSwitchTooltipText(container.querySelector('.terminal-switch-tooltip'), state);
            // Apply the state to terminal windows
            applyStateToTerminalWindows(state);
        }
        
        function setSwitchTooltipText(element, state) {
            let word = state === 'active' ? 'disable' : 'enable';
            element.innerHTML = `
            Terminal animations are <b>${state}</b>. Click to ${word} them.<br><br>
            In this documentation, the same code is sometimes shown in a <b>code block</b> 
            and also as a <b>terminal animation</b>.<br>
            The <b>code blocks</b> show the commands to be run in a terminal. They can be easily copied
            by clicking on the icon over the right side of the code block.<br>
            The <b>terminal animations</b> are produced using 
            <a href="https://github.com/atteggiani/animated-terminal.js" target="_blank" rel="noopener noreferrer" 
                class="external-link">animated-terminal.js</a>
            and provide examples of the output to expect when the commands are run. 
            Sometimes they might slightly differ from the actual outputs.
            `
        }

        function toggleState(event) {
            const newstate = getState() === 'active' ? 'inactive' : 'active';
            applyState(event.currentTarget, newstate);
            setStateCookie(newstate);
        }

        // Create the Animation switch
        const terminalAnimationsSwitch = document.createElement('img');
        terminalAnimationsSwitch.setAttribute('src',SWITCH_IMG);
        terminalAnimationsSwitch.classList.add('terminal-switch');
        const terminalAnimationsSwitchInactive = document.createElement('img');
        terminalAnimationsSwitchInactive.classList.add('terminal-switch');
        terminalAnimationsSwitchInactive.setAttribute('src',SWITCH_IMG_INACTIVE);
        // Create the Animation Switch tooltip
        const terminalAnimationsTooltip = document.createElement('div');
        terminalAnimationsTooltip.classList.add('terminal-switch-tooltip');
        terminalAnimationsTooltip.addEventListener("mouseenter", (event) => {
            terminalAnimationsTooltip.classList.add('visible');
        });
        terminalAnimationsTooltip.addEventListener("mouseleave", (event) => {
            terminalAnimationsTooltip.classList.remove('visible');
        });
        // Create the Animation Switch Container
        const terminalAnimationsSwitchContainer = document.createElement('div');
        terminalAnimationsSwitchContainer.classList.add('terminal-switch-container');
        terminalAnimationsSwitchContainer.appendChild(terminalAnimationsSwitch);
        terminalAnimationsSwitchContainer.appendChild(terminalAnimationsSwitchInactive);
        terminalAnimationsSwitchContainer.appendChild(terminalAnimationsTooltip);
        terminalAnimationsSwitchContainer.addEventListener('click', toggleState, false);
        let state = getState();
        applyState(terminalAnimationsSwitchContainer, state);
        // Place the Animation switch within the document
        const h1 = document.querySelector('h1');
        h1.parentElement.insertBefore(terminalAnimationsSwitchContainer, h1);
    }
}

/*
  Fit text to div if overflowing (for 'card-text-container' and 'fitText' class)
*/
function fitText() {
  const coeff = 0.9;
  function isOverflowing(el) {
    return el.scrollHeight > el.clientHeight || el.scrollWidth > el.clientWidth;
  }
  function fit(el) {
    el.style.fontSize = null;
    while (isOverflowing(el)) {
      el.style.fontSize = `${parseFloat(getComputedStyle(el).fontSize) * coeff}px`;
    }
  }
  const observer = new ResizeObserver(entries => {
    entries.forEach(entry => fit(entry.target));
  })
  document.querySelectorAll('.card-text-container,.fit-text').forEach(el => {
    observer.observe(el);
  })
}


/*
  Make footnote citations link to article
*/
function makeCitationLinks() {
  let match;
  let href;
  document.querySelectorAll('.footnote [id^="fn:"] > p').forEach(el => {
    if (match = el.innerHTML.match('<a\\s*href="https://doi.org/[\\w\./-]*')) { // Assignment to variable NOT AN ERROR!
      href = match[0].slice(9,);
      el.outerHTML = `<a href="${href}" target="_blank">${el.innerHTML}</a>`;
    } else if (match = el.innerHTML.match('URL: <a href="[\\w\./:-]*')) {
      href = match[0].slice(14,);
      el.outerHTML = `<a href="${href}" target="_blank">${el.innerHTML}</a>`;
    }
  })
}

// Join all functions
function main() {
  tabFunctionality();
  hideTocItems();
  makeLinksExternal();
  fitText();
  toggleTerminalAnimations();
  makeCitationLinks();
  sortTables();
}

// Run all functions
window.onload = () => document$.subscribe(() => main());