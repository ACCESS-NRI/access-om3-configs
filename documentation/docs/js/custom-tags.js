'use strict';

// Create an HTML tag to render the not-supported danger admonition
class NotSupported extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        this.innerHTML = `<details class="not-supported" open="open">
        <summary>NOT directly supported by ACCESS-NRI</summary>
        <p>
        The information below can be useful for the ACCESS community, 
        but is not directly supported by ACCESS-NRI unless stated otherwise.
        </p>
        </details>
        `
    }
}

// Create an HTML tag to render the references
class References extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        let inner = this.innerHTML.split("\n")
        let ul = document.createElement("ul")
        inner.forEach((item) => {
            item = item.trim()
            if (item != "") {
                let li = document.createElement("li")
                item.startsWith('- ') ? li.innerHTML = item.slice(2) : li.innerHTML = item
                ul.appendChild(li)
            }
        })
        this.innerHTML = `<hr>
        <h6>References</h6>
        <div class="references">
            ${ul.outerHTML}
        </div>
        `
    }
}

customElements.define("custom-not-supported", NotSupported)
customElements.define("custom-references", References)