import cytoscape from 'https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.15.2/cytoscape.esm.min.js';
import Fuse from 'https://cdn.jsdelivr.net/npm/fuse.js@6.4.0/dist/fuse.esm.js';

function graphArea () {
  const div = document.createElement('div');
  div.style.width = '100%';
  div.style.height = '60vh';
  div.style.position = 'relative';
  div.style.top = '0px';
  div.style.left = '0px';
  return div
}

function noteElement (note, currentNote = false) {
  return {
    data: {
      id: note.id,
      title: note.title,
      label: note.id,
      color: 'white',
      bgColor: currentNote ? 'black' : 'gray'
    }
  }
}

function linkElement (type, source, target) {
  console.assert(['backlink', 'direct', 'sequence'].includes(type));
  const id = type.slice(0, 1) + `${source}-${target}`;
  const style = type === 'sequence' ? 'dashed' : 'solid';
  const color = 'black';
  return {
    data: { id, source, target, arrow: 'triangle', style, color }
  }
}

function * neighborElements (query, note) {
  yield noteElement(note, true);

  for (const backlink of note.backlinks()) {
    yield noteElement(backlink.src);
    yield linkElement('backlink', backlink.src.id, note.id);
  }
  for (const link of note.links()) {
    yield noteElement(link.dest);
    yield linkElement('direct', note.id, link.dest.id);
  }
  for (const parent of note.parents()) {
    yield noteElement(parent.note);
    yield linkElement('sequence', parent.note.id, note.id);
  }
  for (const child of note.children()) {
    yield noteElement(child.note);
    yield linkElement('sequence', note.id, child.note.id);
  }
  for (const alias of note.aliases()) {
    for (const ancestor of query.ancestors(alias)) {
      yield noteElement(ancestor.note);
      yield noteElement(query.note(ancestor.childID));
      yield linkElement('sequence', ancestor.note.id, ancestor.childID);
    }
    for (const descendant of query.descendants(alias)) {
      yield noteElement(descendant.note);
      yield noteElement(query.note(descendant.parentID));
      yield linkElement('sequence', descendant.parentID, descendant.note.id);
    }
  }
}

function createCytoscape (container, elements) {
  return cytoscape({
    directed: true,
    multigraph: true,
    container: container,
    elements: elements,
    selectionType: 'additive',
    style: [
      {
        selector: 'node',
        style: {
          label: 'data(label)',
          height: 'label',
          width: 'label',
          padding: '8px',
          shape: 'round-rectangle',
          color: 'data(color)',
          'background-color': 'data(bgColor)',
          'text-halign': 'center',
          'text-valign': 'center',
          'text-wrap': 'wrap',
          'text-max-width': 100
        }
      },
      {
        selector: 'edge',
        style: {
          width: 2,
          'curve-style': 'bezier',
          'line-color': 'data(color)',
          'line-style': 'data(style)'
        }
      },
      {
        selector: 'edge[arrow]',
        style: {
          'target-arrow-color': 'data(color)',
          'target-arrow-shape': 'data(arrow)'
        }
      }
    ]
  })
}

function noteInfoDiv () {
  const div = document.createElement('div');
  div.style.bottom = 0;
  div.style.right = 0;
  div.style.padding = '20px';
  div.style.position = 'fixed';
  div.style.maxWidth = '30em';
  div.style.zIndex = 1;
  return div
}

function hoverHandlers (container) {
  const h3 = document.createElement('h3');
  const a = document.createElement('a');
  h3.appendChild(a);
  const infoDiv = noteInfoDiv();
  infoDiv.appendChild(h3);
  container.appendChild(infoDiv);

  const show = event => {
    const title = event.target.data('title');
    a.textContent = title;
    a.href = '#' + event.target.data('id');
    event.target.data('label', title);
  };
  const hide = event => {
    event.target.data('label', event.target.data('id'));
    a.textContent = '';
  };
  return [show, hide]
}

function init (query) {
  let container = graphArea();
  let infoContainer = document.createElement('div');
  const hr = document.createElement('hr');

  function resetGraph () {
    hr.remove();
    container.remove();
    infoContainer.remove();

    const id = Number(window.location.hash.slice(1));
    if (!Number.isInteger(id)) return

    const note = query.note(id);
    const elements = [];
    if (note != null) {
      elements.push(...neighborElements(query, note));
    }
    if (elements.length < 2) return

    container = graphArea();
    infoContainer = document.createElement('div');
    document.body.appendChild(hr);
    document.body.appendChild(infoContainer);
    document.body.appendChild(container);

    const cy = createCytoscape(container, elements);
    cy.layout({ name: 'cose' }).run();
    cy.reset();
    cy.center();

    const [show, hide] = hoverHandlers(infoContainer);
    cy.on('select', 'node', show);
    cy.on('unselect', 'node', hide);
  }

  resetGraph();
  window.addEventListener('hashchange', resetGraph);
}

function characterClass (character) {
  const code = character.charCodeAt();
  return code >= 47 && code < 58 ? 'd'
    : code >= 97 && code < 123 ? 'a' : null
}

function isValidAlias (alias) {
  if (alias === null) return true
  if (typeof alias !== 'string') return false
  if (!alias) return false
  if (characterClass(alias.slice(0, 1)) !== 'd') return false
  for (const c of alias) {
    const charClass = characterClass(c);
    if (charClass !== 'd' && charClass !== 'a') {
      return false
    }
  }
  return true
}

function isNumber (string) {
  if (!string) return false
  for (const c of string) {
    if (characterClass(c) !== 'd') return false
  }
  return true
}

function aliasParent (alias) {
  if (!isValidAlias(alias)) return null
  if (alias === null) return null

  const last = characterClass(alias.slice(-1));
  const pattern = last === 'd' ? /^(.*?)[0-9]+$/ : /^(.*?)[a-z]+$/;
  return alias.replace(pattern, '$1') || null
}

function isSequence (prev, next) {
  return aliasParent(next) === prev
}

class Database {
  // Schema
  // {
  //   aliases: {
  //     <alias:str>: { id: <int>, children: [<str>], parent: <str> }
  //   },
  //   notes: [
  //     {
  //       title: <str>,
  //       aliases: [<str>],
  //       links: [{ src: <int>, dest: <int>, annotation: <str> }],
  //       backlinks: [<link>]
  //     }
  //   ]
  // }

  constructor () {
    this.data = { aliases: {}, notes: [] };
  }

  add (record) {
    return record.addTo(this) || record
  }
}

class IntegrityError extends Error {}
class DomainError extends IntegrityError {}
class ReferenceError extends IntegrityError {}

function check (condition, message) {
  if (!condition) throw new DomainError(message)
}

class Note {
  constructor (id, title) {
    check(Number.isInteger(id), 'invalid Note.id');
    check(typeof title === 'string', 'invalid Note.title');
    check(title, 'empty Note.title');

    this.id = id;
    this.title = title;
  }

  addTo (db) {
    // Overwrite existing entry in notes.
    db.data.notes[this.id] = {
      title: this.title,
      aliases: [],
      links: [],
      backlinks: []
    };
  }

  equals (note) {
    return this.id === note.id && this.title === note.title
  }
}

class Alias {
  constructor (id, alias) {
    check(Number.isInteger(id), 'non-integer Alias.id');
    check(typeof alias === 'string', 'non-string Alias.alias');
    check(isValidAlias(alias), 'malformed Alias.alias');
    check(alias, 'empty alias');
    if (isNumber(alias)) {
      check(String(id) === alias, 'invalid Alias.alias');
    }

    this.id = id;
    this.alias = alias;
  }

  addTo (db) {
    // Overwrite existing entry in aliases.
    // Note with ID must exist.
    const note = db.data.notes[this.id];
    if (!note) return new ReferenceError('Alias.id')

    db.data.aliases[this.alias] = {
      id: this.id,
      children: [],
      parent: null
    };
    note.aliases.push(this.alias);
  }
}

class Sequence {
  constructor (prev, next) {
    check(isValidAlias(prev), 'malformed Sequence.prev');
    check(isValidAlias(next), 'malformed Sequence.next');
    check(isSequence(prev, next),
      'Sequence.prev and Sequence.next not in sequence');
    check(prev != null, 'null Sequence.prev');
    check(next != null, 'null Sequence.next');

    this.prev = prev;
    this.next = next;
  }

  addTo (db) {
    let prev = db.data.aliases[this.prev];
    const next = db.data.aliases[this.next];

    if (!next) return
    if (!prev) {
      try {
        if (!db.add(new Alias(Number(this.prev), this.prev))) {
          return null
        }
        prev = db.data.aliases[this.prev];
      } catch (e) {
        return null
      }
    }

    const prevNote = db.data.notes[prev.id];
    const nextNote = db.data.notes[next.id];
    if (!prevNote || !nextNote) return

    next.parent = this.prev;
    prev.children.push(this.next);
  }
}

class Link {
  constructor (src, dest, annotation) {
    check(src instanceof Note, 'invalid src Note');
    check(dest instanceof Note, 'invalid dest Note');
    check(typeof annotation === 'string', 'non-string Link.annotation');

    this.src = src;
    this.dest = dest;
    this.annotation = annotation;
  }

  addTo (db) {
    const src = db.data.notes[this.src.id];
    const dest = db.data.notes[this.dest.id];
    if (!src) return new ReferenceError('Link.src')
    if (!dest) return new ReferenceError('Link.dest')

    // Existing entries get overwritten.
    const link = {
      src: this.src,
      dest: this.dest,
      annotation: this.annotation
    };
    src.links.push(link);
    dest.backlinks.push(link);
  }
}

class Query {
  constructor (db) {
    this.db = db;
  }

  note (id) {
    const record = this.db.data.notes[id];
    if (!record) return null

    const note = new Note(id, record.title);

    note.links = () => this.links(note);
    note.backlinks = () => this.backlinks(note);

    note.aliases = function * () {
      yield * record.aliases;
    };

    const self = this;
    note.parents = function * () {
      for (const alias of record.aliases) {
        const parent = self.parent(alias);
        if (parent) {
          yield parent;
        }
      }
    };

    note.children = function * () {
      for (const alias of record.aliases) {
        yield * self.children(alias);
      }
    };
    return note
  }

  * links (note) {
    const src = this.db.data.notes[note.id];
    if (src && src.links) {
      yield * src.links;
    }
  }

  * backlinks (note) {
    const dest = this.db.data.notes[note.id];
    if (dest && dest.backlinks) {
      yield * dest.backlinks;
    }
  }

  parent (alias) {
    const record = this.db.data.aliases[alias];
    if (!record || !record.parent) return null
    const parentRecord = this.db.data.aliases[record.parent];
    if (!parentRecord || parentRecord.id == null) return null
    return {
      note: this.note(parentRecord.id),
      alias: record.parent
    }
  }

  * children (alias) {
    const record = this.db.data.aliases[alias];
    if (record) {
      const children = record.children || [];
      for (const childAlias of children) {
        const childRecord = this.db.data.aliases[childAlias];
        if (!childRecord) continue
        const childID = childRecord.id;
        const child = this.note(childID);
        if (child) {
          yield {
            note: child,
            alias: childAlias,
            parentID: record.id,
            parentAlias: alias
          };
        }
      }
    }
  }

  * ancestors (alias) {
    const record = this.db.data.aliases[alias];
    if (record) {
      const parentRecord = this.db.data.aliases[record.parent];
      if (parentRecord) {
        const parent = this.note(parentRecord.id);
        if (parent) {
          yield {
            note: parent,
            alias: record.parent,
            childID: record.id, // of between alias and ancestor
            childAlias: alias
          };
        }
        yield * this.ancestors(record.parent);
      }
    }
  }

  * descendants (alias) {
    const record = this.db.data.aliases[alias];
    if (record) {
      for (const child of this.children(alias)) {
        yield child;
        yield * this.descendants(child.alias);
      }
    }
  }
}

var Model = /*#__PURE__*/Object.freeze({
  __proto__: null,
  Alias: Alias,
  aliasParent: aliasParent,
  Database: Database,
  DomainError: DomainError,
  isNumber: isNumber,
  isSequence: isSequence,
  Link: Link,
  Note: Note,
  Query: Query,
  ReferenceError: ReferenceError,
  Sequence: Sequence
});

function createFuse () {
  const options = {
    includeMatches: true,
    ignoreLocation: true,
    keys: ['textContent'],
    threshold: 0.45
  };
  const nodes = document.body.querySelectorAll('section.level1');
  const sections = Array.prototype.filter.call(nodes, function (node) {
    return Number.isInteger(Number(node.id))
  });
  return new Fuse(sections, options)
}

function displayResults (results, container) {
  // Display results in container.
  const div = container;
  div.textContent = '';
  for (const result of results) {
    const p = document.createElement('p');
    const h3 = document.createElement('h3');
    h3.innerHTML = `<a href="#${result.item.id}">${result.item.title}</a>`;
    p.appendChild(h3);

    let count = 3;
    for (const child of result.item.children) {
      const clone = child.cloneNode(true);
      if (count-- <= 0) break
      if (clone.tagName === 'H1' && clone.title === result.item.title) {
        continue
      }
      p.appendChild(clone);
    }

    div.appendChild(p);
    div.appendChild(document.createElement('hr'));
  }
}

function searchBar (fuse, container) {
  // Container will contain search results.
  const input = document.createElement('input');
  input.type = 'text';
  input.placeholder = 'Search notes...';
  input.classList.add('search-bar');
  input.style.width = '100%';
  input.style.background = 'transparent';
  input.style.border = 'none';
  input.style.borderBottomStyle = 'solid';
  input.style.borderWidth = 'thin';

  input.addEventListener('change', function () {
    window.location.hash = '#search';
    const results = fuse.search(input.value);
    displayResults(results, container);
  });
  return input
}

function searchResults () {
  const div = document.createElement('div');
  div.classList.add('search-results');
  return div
}

function searchPage (container) {
  // Container will contain search results.
  const page = document.createElement('section');
  page.id = 'search';
  page.title = 'Search';
  page.classList.add('level1');
  page.appendChild(container);
  return page
}

function searchSpan () {
  const span = document.createElement('span');
  span.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M23.809 21.646l-6.205-6.205c1.167-1.605 1.857-3.579 1.857-5.711 0-5.365-4.365-9.73-9.731-9.73-5.365 0-9.73 4.365-9.73 9.73 0 5.366 4.365 9.73 9.73 9.73 2.034 0 3.923-.627 5.487-1.698l6.238 6.238 2.354-2.354zm-20.955-11.916c0-3.792 3.085-6.877 6.877-6.877s6.877 3.085 6.877 6.877-3.085 6.877-6.877 6.877c-3.793 0-6.877-3.085-6.877-6.877z"/></svg>';
  span.firstChild.style.height = '1em';
  return span
}

function searchForm (container) {
  // Container will contain search results.
  const button = searchSpan();
  const input = searchBar(createFuse(), container);
  input.style.display = 'none';

  button.addEventListener('click', function () {
    button.style.display = 'none';
    input.style.display = '';
    input.focus();
  });

  input.addEventListener('focusout', function () {
    button.style.display = '';
    input.style.display = 'none';
  });

  const div = document.createElement('div');
  div.appendChild(button);
  div.appendChild(input);
  return div
}

function init$1 () {
  const container = searchResults();
  document.body.appendChild(searchPage(container));
  document.body.insertBefore(searchForm(container), document.body.firstChild);
}

function getSectionFromHash (hash) {
  const id = hash.substring(1);
  if (!id) { return null }
  const elem = document.getElementById(id);
  if (elem) {
    return elem.closest('section.level1')
  }
}

function sectionChanger () {
  let _previousHash = window.location.hash;
  return function () {
    const oldSection = getSectionFromHash(_previousHash);
    if (oldSection) {
      oldSection.style.display = 'none';
    }
    _previousHash = window.location.hash;
    const newSection = getSectionFromHash(_previousHash);
    if (newSection) {
      newSection.style.display = '';
      document.title = newSection.title || 'Slipbox';
    } else {
      window.location.hash = '#0';
    }
    window.scrollTo(0, 0);
  }
}

function notFoundSection () {
  const section = document.createElement('section');
  section.id = '0';
  section.classList.add('level1');
  section.style.display = 'none';
  const h1 = document.createElement('h1');
  h1.innerText = 'Note not found';
  section.appendChild(h1);
  return section
}

function init$2 () {
  document.body.appendChild(notFoundSection());
  const changeSection = sectionChanger();
  changeSection();
  window.addEventListener('hashchange', changeSection);
}

window.query = new Query(new Database());

window.Model = Model;

window.initSlipbox = function () {
  const title = document.getElementById('title-block-header');
  if (title) { title.remove(); }
  init$1();
  init$2();
  init(window.query);
};
