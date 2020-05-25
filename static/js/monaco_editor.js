require.config({ paths: { 'vs': '../static/node_modules/monaco-editor/min/vs' }});
require(['vs/editor/editor.main'], function() {
  window.editor = monaco.editor.create(
      document.getElementById('monaco-editor'),
      {
          value: [
              'function x() {',
              '\tconsole.log("Hello world!");',
              '}'
          ].join('\n'),
          language: 'javascript'
      }
  );
});

class TreeElement {
    constructor(name, isFile = null, text = null) {
        this.name = name;
        this.isFile = isFile;
        if (this.isFile)
            this.text = text;
    }
}

mainFile = new TreeElement(
    'main.java',
    true,
    '// this is the main file'
);
let filesAndFolders = {
    items: [

    ],
};

function createListView(_filesAndFolders) {
    let ul = document.createElement('ul');
    ul.classList.add('root');

    let curr = ul;

    for (let i = 0; i < _filesAndFolders.length; i++) {
        let treeElem = _filesAndFolders[i];

        let li = document.createElement('li');
        li.appendChild(document.createTextNode(treeElem.name));

        if (treeElem.isFile) {
            li.onclick = () => window.editor.setValue(treeElem.text);
            li.classList.add('file-tree-file');
        }
        else {
            li.classList.add('file-tree-folder');
        }

        ul.appendChild(li);
    }
    return ul;
}
document.getElementById('file-tree-view')
    .appendChild(createListView(files));

